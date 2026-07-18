"""Supabase backed authentication, email 2FA, and license gating.

The flow, all through Supabase's own primitives:

1. :meth:`AuthService.request_code` calls ``sign_in_with_otp`` which emails a
   six digit code (the email template must expose ``{{ .Token }}``; see
   ``supabase/schema.sql`` and the README).
2. :meth:`AuthService.verify_code` verifies that code and establishes a
   session. On first sight of an email a ``licenses`` row is upserted with
   status ``pending``.
3. :meth:`AuthService.license_status` reads that row. The app only unlocks
   when an admin has flipped the row to ``approved`` in Supabase, giving you
   manual approval of every licence.

All methods raise on failure with a readable message; callers run them on a
worker via :mod:`yananotes.async_task`.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..config import deployment


class LicenseStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REVOKED = "revoked"
    UNKNOWN = "unknown"


@dataclass
class AuthSession:
    email: str
    access_token: str
    refresh_token: str


class AuthError(RuntimeError):
    """Any auth failure, carrying a message safe to show the user."""


class AuthService:
    """Thin wrapper over supabase-py, lazily created so imports stay cheap."""

    def __init__(self) -> None:
        self._client = None

    def reset(self) -> None:
        """Drop the cached client so a changed connection takes effect."""
        self._client = None

    # -- client lifecycle -------------------------------------------------
    def _get_client(self):
        if self._client is not None:
            return self._client
        if not deployment.configured:
            raise AuthError(
                "Supabase is not configured. Add SUPABASE_URL and "
                "SUPABASE_ANON_KEY to your .env file (see the README)."
            )
        try:
            from supabase import create_client
        except ImportError as exc:  # pragma: no cover
            raise AuthError(
                "The 'supabase' package is not installed. Run "
                "'pip install -r requirements.txt'."
            ) from exc
        self._client = create_client(
            deployment.supabase_url, deployment.supabase_anon_key
        )
        return self._client

    # -- step 1: send the 6 digit code ------------------------------------
    def request_code(self, email: str) -> None:
        client = self._get_client()
        email = email.strip().lower()
        if "@" not in email:
            raise AuthError("Please enter a valid email address.")
        try:
            client.auth.sign_in_with_otp(
                {"email": email, "options": {"should_create_user": True}}
            )
        except Exception as exc:  # network / rate limit / etc.
            raise AuthError(f"Could not send the code: {exc}") from exc

    # -- step 2: verify the code, open a session --------------------------
    def verify_code(self, email: str, code: str) -> AuthSession:
        client = self._get_client()
        email = email.strip().lower()
        code = code.strip()
        try:
            res = client.auth.verify_otp(
                {"email": email, "token": code, "type": "email"}
            )
        except Exception as exc:
            raise AuthError("That code was not accepted. Try again.") from exc
        session = getattr(res, "session", None)
        if session is None:
            raise AuthError("That code was not accepted. Try again.")
        # Record a pending licence request on first login. If the row already
        # exists this is a no-op thanks to the unique email constraint.
        self._ensure_license_row(email)
        return AuthSession(
            email=email,
            access_token=session.access_token,
            refresh_token=session.refresh_token,
        )

    def _ensure_license_row(self, email: str) -> None:
        client = self._get_client()
        try:
            existing = (
                client.table("licenses").select("email").eq("email", email).execute()
            )
            if not existing.data:
                client.table("licenses").insert(
                    {"email": email, "status": LicenseStatus.PENDING.value}
                ).execute()
        except Exception:
            # Never block login on the bookkeeping insert; license_status()
            # will report UNKNOWN and the UI handles that gracefully.
            pass

    # -- step 3: has an admin approved this licence? ----------------------
    def license_status(self, email: str) -> LicenseStatus:
        client = self._get_client()
        email = email.strip().lower()
        try:
            res = (
                client.table("licenses")
                .select("status")
                .eq("email", email)
                .limit(1)
                .execute()
            )
        except Exception as exc:
            raise AuthError(f"Could not check your licence: {exc}") from exc
        if not res.data:
            return LicenseStatus.PENDING
        raw = str(res.data[0].get("status", "")).lower()
        try:
            return LicenseStatus(raw)
        except ValueError:
            return LicenseStatus.UNKNOWN

    # -- restore / end a session -----------------------------------------
    def restore(self, access_token: str, refresh_token: str) -> bool:
        client = self._get_client()
        try:
            client.auth.set_session(access_token, refresh_token)
            return True
        except Exception:
            return False

    def sign_out(self) -> None:
        if self._client is None:
            return
        try:
            self._client.auth.sign_out()
        except Exception:
            pass
