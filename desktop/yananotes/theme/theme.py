"""Central theme system: colour tokens, light/dark/system resolution, and QSS.

A single source of truth for the whole app's look. Pages never hard code a
colour; they read tokens from the active :class:`Palette` or rely on the
generated stylesheet. Switching theme restyles every widget on the fly.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QGuiApplication, QPalette, QColor


class ThemeMode(str, Enum):
    """User facing appearance choice."""

    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


@dataclass(frozen=True)
class Palette:
    """A resolved set of colours. Dark is the flagship look."""

    name: str
    # Backgrounds, from deepest to most raised.
    bg: str
    surface: str
    elevated: str
    # Text.
    text: str
    text_muted: str
    # The neon accent and its softer companions.
    accent: str
    accent_soft: str
    accent_glow: str
    # Lines and states.
    border: str
    danger: str
    success: str
    warning: str


# The flagship: near black base with a clean white cyan neon accent.
DARK = Palette(
    name="dark",
    bg="#0B0B0D",
    surface="#141518",
    elevated="#1C1D22",
    text="#F5F7FA",
    text_muted="#8A8F98",
    accent="#5CE6FF",
    accent_soft="#2BB7D6",
    accent_glow="rgba(92, 230, 255, 0.35)",
    border="#26282E",
    danger="#FF5C7A",
    success="#4DE1A0",
    warning="#FFC34D",
)

# Light theme keeps the same cyan identity but darkened enough for contrast.
LIGHT = Palette(
    name="light",
    bg="#F4F6F8",
    surface="#FFFFFF",
    elevated="#FFFFFF",
    text="#0B0B0D",
    text_muted="#5A616B",
    accent="#0BA6C9",
    accent_soft="#59C7DD",
    accent_glow="rgba(11, 166, 201, 0.20)",
    border="#E1E5EA",
    danger="#D63A5A",
    success="#1F9E6E",
    warning="#C7860B",
)


def _system_prefers_dark() -> bool:
    """Best effort read of the OS colour scheme via the Qt palette."""
    app = QGuiApplication.instance()
    if app is None:
        return True
    window = app.palette().color(QPalette.ColorRole.Window)
    # Luminance below the midpoint means a dark desktop theme.
    luminance = 0.299 * window.red() + 0.587 * window.green() + 0.114 * window.blue()
    return luminance < 128


def resolve(mode: ThemeMode) -> Palette:
    """Turn a user choice (incl. SYSTEM) into a concrete palette."""
    if mode == ThemeMode.LIGHT:
        return LIGHT
    if mode == ThemeMode.DARK:
        return DARK
    return DARK if _system_prefers_dark() else LIGHT


def build_qss(p: Palette) -> str:
    """Generate the application wide stylesheet for a palette."""
    return f"""
    * {{
        font-family: "Segoe UI", "Inter", "SF Pro Display", sans-serif;
        color: {p.text};
        outline: none;
    }}
    QWidget#root, QMainWindow, QDialog {{
        background-color: {p.bg};
    }}
    QLabel {{ background: transparent; }}
    QLabel[role="h1"] {{ font-size: 26px; font-weight: 700; }}
    QLabel[role="h2"] {{ font-size: 19px; font-weight: 600; }}
    QLabel[role="muted"] {{ color: {p.text_muted}; font-size: 13px; }}
    QLabel[role="accent"] {{ color: {p.accent}; font-weight: 600; }}

    /* Cards and surfaces */
    QFrame[role="card"] {{
        background-color: {p.surface};
        border: 1px solid {p.border};
        border-radius: 16px;
    }}
    QFrame[role="elevated"] {{
        background-color: {p.elevated};
        border: 1px solid {p.border};
        border-radius: 12px;
    }}

    /* Sidebar */
    QFrame#sidebar {{
        background-color: {p.surface};
        border: none;
        border-right: 1px solid {p.border};
    }}
    QPushButton[role="nav"] {{
        background: transparent;
        border: none;
        border-radius: 10px;
        padding: 11px 14px;
        text-align: left;
        font-size: 14px;
        color: {p.text_muted};
    }}
    QPushButton[role="nav"]:hover {{
        background-color: {p.elevated};
        color: {p.text};
    }}
    QPushButton[role="nav"][active="true"] {{
        background-color: {p.elevated};
        color: {p.accent};
        font-weight: 600;
    }}

    /* Primary neon button */
    QPushButton[role="primary"] {{
        background-color: {p.accent};
        color: #04141A;
        border: none;
        border-radius: 11px;
        padding: 11px 20px;
        font-size: 14px;
        font-weight: 700;
    }}
    QPushButton[role="primary"]:hover {{ background-color: {p.accent_soft}; }}
    QPushButton[role="primary"]:disabled {{
        background-color: {p.border};
        color: {p.text_muted};
    }}

    /* Ghost / secondary button */
    QPushButton[role="ghost"] {{
        background: transparent;
        border: 1px solid {p.border};
        border-radius: 11px;
        padding: 10px 18px;
        font-size: 14px;
        color: {p.text};
    }}
    QPushButton[role="ghost"]:hover {{ border-color: {p.accent}; color: {p.accent}; }}

    QPushButton[role="danger"] {{
        background: transparent;
        border: 1px solid {p.danger};
        border-radius: 11px;
        padding: 10px 18px;
        color: {p.danger};
        font-weight: 600;
    }}
    QPushButton[role="danger"]:hover {{ background-color: {p.danger}; color: #FFFFFF; }}

    /* Inputs */
    QLineEdit {{
        background-color: {p.elevated};
        border: 1px solid {p.border};
        border-radius: 11px;
        padding: 12px 14px;
        font-size: 15px;
        selection-background-color: {p.accent};
        selection-color: #04141A;
    }}
    QLineEdit:focus {{ border: 1px solid {p.accent}; }}
    QLineEdit[role="otp"] {{
        font-size: 26px;
        font-weight: 700;
        letter-spacing: 10px;
        qproperty-alignment: AlignCenter;
        padding: 14px;
    }}

    /* Combos */
    QComboBox {{
        background-color: {p.elevated};
        border: 1px solid {p.border};
        border-radius: 10px;
        padding: 9px 12px;
        min-width: 140px;
    }}
    QComboBox:focus, QComboBox:hover {{ border: 1px solid {p.accent}; }}
    QComboBox QAbstractItemView {{
        background-color: {p.elevated};
        border: 1px solid {p.border};
        selection-background-color: {p.accent};
        selection-color: #04141A;
        border-radius: 8px;
        padding: 4px;
    }}

    /* Trees / lists */
    QTreeView, QListView {{
        background-color: {p.surface};
        border: 1px solid {p.border};
        border-radius: 14px;
        padding: 6px;
        font-size: 14px;
    }}
    QTreeView::item, QListView::item {{
        padding: 8px 6px;
        border-radius: 8px;
    }}
    QTreeView::item:hover, QListView::item:hover {{ background-color: {p.elevated}; }}
    QTreeView::item:selected, QListView::item:selected {{
        background-color: {p.accent};
        color: #04141A;
    }}

    /* Text viewer */
    QTextBrowser {{
        background-color: {p.surface};
        border: 1px solid {p.border};
        border-radius: 14px;
        padding: 22px;
        font-size: 15px;
    }}

    /* Plain scroll areas (library detail) stay on the base background */
    QScrollArea {{ background: transparent; border: none; }}
    QScrollArea > QWidget > QWidget {{ background: transparent; }}

    /* Scrollbars */
    QScrollBar:vertical {{ background: transparent; width: 10px; margin: 4px; }}
    QScrollBar::handle:vertical {{
        background: {p.border}; border-radius: 5px; min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {p.accent_soft}; }}
    QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}
    QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 4px; }}
    QScrollBar::handle:horizontal {{
        background: {p.border}; border-radius: 5px; min-width: 30px;
    }}

    /* Toast */
    QFrame#toast {{
        background-color: {p.elevated};
        border: 1px solid {p.accent};
        border-radius: 12px;
    }}

    QToolTip {{
        background-color: {p.elevated};
        color: {p.text};
        border: 1px solid {p.accent};
        border-radius: 6px;
        padding: 6px 8px;
    }}
    """


class ThemeManager(QObject):
    """Holds the active palette and re-applies QSS when the mode changes."""

    changed = Signal(object)  # emits the new Palette

    def __init__(self, app: QGuiApplication, mode: ThemeMode = ThemeMode.DARK) -> None:
        super().__init__()
        self._app = app
        self._mode = mode
        self._palette = resolve(mode)

    @property
    def palette(self) -> Palette:
        return self._palette

    @property
    def mode(self) -> ThemeMode:
        return self._mode

    def apply(self) -> None:
        self._palette = resolve(self._mode)
        self._apply_qpalette(self._palette)
        self._app.setStyleSheet(build_qss(self._palette))
        self.changed.emit(self._palette)

    def _apply_qpalette(self, p: Palette) -> None:
        """Set base palette roles so default widget backgrounds (e.g. a
        QScrollArea viewport) match the theme instead of painting white."""
        qp = QPalette()
        bg = QColor(p.bg)
        surface = QColor(p.surface)
        text = QColor(p.text)
        accent = QColor(p.accent)
        qp.setColor(QPalette.ColorRole.Window, bg)
        qp.setColor(QPalette.ColorRole.Base, bg)
        qp.setColor(QPalette.ColorRole.AlternateBase, surface)
        qp.setColor(QPalette.ColorRole.WindowText, text)
        qp.setColor(QPalette.ColorRole.Text, text)
        qp.setColor(QPalette.ColorRole.Button, surface)
        qp.setColor(QPalette.ColorRole.ButtonText, text)
        qp.setColor(QPalette.ColorRole.Highlight, accent)
        qp.setColor(QPalette.ColorRole.HighlightedText, QColor("#04141A"))
        qp.setColor(QPalette.ColorRole.ToolTipBase, QColor(p.elevated))
        qp.setColor(QPalette.ColorRole.ToolTipText, text)
        self._app.setPalette(qp)

    def set_mode(self, mode: ThemeMode) -> None:
        self._mode = mode
        self.apply()
