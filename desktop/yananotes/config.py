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

import json
import os
from pathlib import Path

from PySide6.QtCore import QSettings, QStandardPaths

APP_NAME = "YanaNotes"
APP_ORG = "Yanakan"


def _config_dir() -> Path:
    base = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppConfigLocation
    )
    path = Path(base) if base else Path.home() / ".config" / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def _runtime_config_path() -> Path:
    return _config_dir() / "connection.json"

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
    """Supabase connection values.

    Resolution order: environment / ``.env`` first (good for developers and
    for a bundled build), then a per user ``connection.json`` written by the
    in app first run dialog (so end users never hand edit files).
    """

    def __init__(self) -> None:
        self._cache: dict[str, str] | None = None

    def _file_values(self) -> dict[str, str]:
        if self._cache is not None:
            return self._cache
        path = _runtime_config_path()
        if path.exists():
            try:
                self._cache = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                self._cache = {}
        else:
            self._cache = {}
        return self._cache

    @property
    def supabase_url(self) -> str:
        env = os.environ.get("SUPABASE_URL", "").strip()
        return env or self._file_values().get("supabase_url", "").strip()

    @property
    def supabase_anon_key(self) -> str:
        env = os.environ.get("SUPABASE_ANON_KEY", "").strip()
        return env or self._file_values().get("supabase_anon_key", "").strip()

    @property
    def configured(self) -> bool:
        return bool(self.supabase_url and self.supabase_anon_key)

    def save(self, url: str, anon_key: str) -> None:
        """Persist a connection entered in the app and refresh the cache."""
        data = {"supabase_url": url.strip(), "supabase_anon_key": anon_key.strip()}
        _runtime_config_path().write_text(json.dumps(data, indent=2), encoding="utf-8")
        self._cache = data


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
