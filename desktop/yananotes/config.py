"""Application configuration and persisted user settings.

Two distinct concerns live here:

* **Deployment config** (Supabase URL/key) comes from the environment or a
  ``.env`` file next to the app. The anon key is designed to be shipped in a
  client; row level security on the Supabase side is what protects data.
* **User settings** (theme, repository location) are stored per user with
  :class:`QSettings`, so they survive restarts and live in the OS specific
  config location.
"""
from __future__ import annotations

import os
from pathlib import Path

from PySide6.QtCore import QSettings

APP_NAME = "YanaNotes"
APP_ORG = "Yanakan"

try:  # Optional: load a .env if python-dotenv is installed.
    from dotenv import load_dotenv

    for candidate in (
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent / ".env",
    ):
        if candidate.exists():
            load_dotenv(candidate)
            break
except Exception:  # pragma: no cover - dotenv is optional
    pass


class Deployment:
    """Read only deployment values sourced from the environment."""

    @property
    def supabase_url(self) -> str:
        return os.environ.get("SUPABASE_URL", "").strip()

    @property
    def supabase_anon_key(self) -> str:
        return os.environ.get("SUPABASE_ANON_KEY", "").strip()

    @property
    def configured(self) -> bool:
        return bool(self.supabase_url and self.supabase_anon_key)


class Settings:
    """Typed wrapper over QSettings for the values the UI cares about."""

    def __init__(self) -> None:
        self._s = QSettings(APP_ORG, APP_NAME)

    # -- Appearance -------------------------------------------------------
    def theme_mode(self) -> str:
        return str(self._s.value("appearance/theme", "dark"))

    def set_theme_mode(self, mode: str) -> None:
        self._s.setValue("appearance/theme", mode)

    # -- Repository -------------------------------------------------------
    def repository(self) -> str:
        return str(self._s.value("library/repository", ""))

    def set_repository(self, path: str) -> None:
        self._s.setValue("library/repository", path)

    # -- Integrations -----------------------------------------------------
    def gdrive_enabled(self) -> bool:
        return self._s.value("integrations/gdrive", False, type=bool)

    def set_gdrive_enabled(self, enabled: bool) -> None:
        self._s.setValue("integrations/gdrive", enabled)

    # -- Session hint (non secret) ----------------------------------------
    def last_email(self) -> str:
        return str(self._s.value("session/email", ""))

    def set_last_email(self, email: str) -> None:
        self._s.setValue("session/email", email)


deployment = Deployment()
settings = Settings()
