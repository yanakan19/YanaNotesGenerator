"""Application bootstrap: create the QApplication, apply the theme, and show
the main window."""
from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from .config import APP_NAME, APP_ORG, settings
from .theme import ThemeManager, ThemeMode
from .ui import MainWindow


def _resolve_startup_mode() -> ThemeMode:
    try:
        return ThemeMode(settings.theme_mode())
    except ValueError:
        return ThemeMode.DARK


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName(APP_ORG)

    theme = ThemeManager(app, _resolve_startup_mode())
    theme.apply()

    window = MainWindow(theme)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
