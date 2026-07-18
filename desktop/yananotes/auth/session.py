"""Secure, cross session storage of the signed in user's tokens.

Tokens go in the OS keychain via ``keyring`` when available (Windows
Credential Manager, macOS Keychain, Secret Service on Linux). If keyring is
missing the app still works; it just will not remember the login between
runs.
"""
from __future__ import annotations

from dataclasses import dataclass

from ..config import APP_NAME, settings

_ACCESS = "access_token"
_REFRESH = "refresh_token"

try:
    import keyring

    _HAVE_KEYRING = True
except Exception:  # pragma: no cover
    keyring = None  # type: ignore
    _HAVE_KEYRING = False


@dataclass
class StoredSession:
    email: str
    access_token: str
    refresh_token: str


def save(email: str, access_token: str, refresh_token: str) -> None:
    settings.set_last_email(email)
    if _HAVE_KEYRING:
        keyring.set_password(APP_NAME, f"{email}:{_ACCESS}", access_token)
        keyring.set_password(APP_NAME, f"{email}:{_REFRESH}", refresh_token)


def load() -> StoredSession | None:
    email = settings.last_email()
    if not email or not _HAVE_KEYRING:
        return None
    access = keyring.get_password(APP_NAME, f"{email}:{_ACCESS}")
    refresh = keyring.get_password(APP_NAME, f"{email}:{_REFRESH}")
    if not access or not refresh:
        return None
    return StoredSession(email=email, access_token=access, refresh_token=refresh)


def clear() -> None:
    email = settings.last_email()
    if email and _HAVE_KEYRING:
        for key in (_ACCESS, _REFRESH):
            try:
                keyring.delete_password(APP_NAME, f"{email}:{key}")
            except Exception:
                pass
    settings.set_last_email("")
