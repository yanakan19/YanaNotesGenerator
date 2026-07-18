"""Application bootstrap: create the QApplication, apply the theme, and show
the main window."""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from .config import APP_NAME, APP_ORG, deployment, settings
from .theme import ThemeManager, ThemeMode
from .ui import MainWindow


def _resolve_startup_mode() -> ThemeMode:
    try:
        return ThemeMode(settings.theme_mode())
    except ValueError:
        return ThemeMode.DARK


def _app_icon() -> QIcon:
    icon_path = Path(__file__).resolve().parent / "resources" / "icons" / "app.png"
    return QIcon(str(icon_path)) if icon_path.exists() else QIcon()


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_ORG)
    app.setWindowIcon(_app_icon())

    theme = ThemeManager(app, _resolve_startup_mode())
    theme.apply()

    # First run: if there is no Supabase connection yet, ask for one before
    # showing the app so login can actually work.
    if not deployment.configured:
        from .ui.pages import ConnectionDialog

        ConnectionDialog().exec()

    window = MainWindow(theme)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
