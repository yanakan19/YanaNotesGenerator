"""Small reusable widgets shared across pages.

Everything visual routes through here so the neon look stays consistent and
pages read declaratively.
"""
from __future__ import annotations

from PySide6.QtCore import (
    QAbstractAnimation,
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    QTimer,
    Signal,
)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..theme.animations import cross_fade


def heading(text: str, level: str = "h1") -> QLabel:
    label = QLabel(text)
    label.setProperty("role", level)
    return label


def muted(text: str) -> QLabel:
    label = QLabel(text)
    label.setProperty("role", "muted")
    label.setWordWrap(True)
    return label


class Button(QPushButton):
    def __init__(self, text: str, role: str = "primary", parent: QWidget | None = None):
        super().__init__(text, parent)
        self.setProperty("role", role)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class Card(QFrame):
    def __init__(self, role: str = "card", parent: QWidget | None = None):
        super().__init__(parent)
        self.setProperty("role", role)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(22, 22, 22, 22)
        self._layout.setSpacing(14)

    def body(self) -> QVBoxLayout:
        return self._layout


class PageStack(QWidget):
    """A stack that cross fades between pages for smooth navigation."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._pages: list[QWidget] = []
        self._current: QWidget | None = None

    def add(self, page: QWidget) -> None:
        page.setParent(self)
        page.hide()
        self._layout.addWidget(page)
        self._pages.append(page)
        if self._current is None:
            self._current = page
            page.show()

    def show_page(self, page: QWidget) -> None:
        if page is self._current:
            return
        old = self._current
        page.show()
        page.raise_()
        cross_fade(old, page)
        if old is not None:
            QTimer.singleShot(220, old.hide)
        self._current = page

    @property
    def current(self) -> QWidget | None:
        return self._current


class Toast(QFrame):
    """A transient message that fades in at the bottom of its parent."""

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName("toast")
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        self._label = QLabel("")
        self._label.setWordWrap(True)
        layout.addWidget(self._label)
        self.hide()
        self._anim: QPropertyAnimation | None = None

    def show_message(self, text: str, msecs: int = 2600) -> None:
        self._label.setText(text)
        self.adjustSize()
        parent = self.parentWidget()
        if parent is not None:
            x = (parent.width() - self.width()) // 2
            y = parent.height() - self.height() - 28
            self.move(max(x, 12), max(y, 12))
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        self.show()
        self.raise_()
        anim = QPropertyAnimation(effect, b"opacity", self)
        anim.setDuration(180)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        self._anim = anim
        QTimer.singleShot(msecs, self.hide)


class OtpInput(QLineEdit):
    """Six digit code entry that emits when full."""

    completed = Signal(str)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setProperty("role", "otp")
        self.setMaxLength(6)
        self.setPlaceholderText("------")
        self.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.textChanged.connect(self._on_changed)

    def _on_changed(self, text: str) -> None:
        digits = "".join(ch for ch in text if ch.isdigit())
        if digits != text:
            self.setText(digits)
            return
        if len(digits) == 6:
            self.completed.emit(digits)
