"""The pre-library flow: email login, 6 digit code, and awaiting approval."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from ..widgets import Button, Card, OtpInput, heading, muted


class _Centered(QWidget):
    """Shared layout: a single card centred on the page."""

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(40, 40, 40, 40)
        outer.addStretch(1)
        row = QHBoxLayout()
        row.addStretch(1)
        self.card = Card()
        self.card.setMinimumWidth(420)
        self.card.setMaximumWidth(480)
        row.addWidget(self.card)
        row.addStretch(1)
        outer.addLayout(row)
        outer.addStretch(1)


class LoginPage(_Centered):
    """Collect an email and request a one time code."""

    submitted = Signal(str)  # email

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        body = self.card.body()
        body.addWidget(heading("YanaNotes"))
        body.addWidget(muted("Sign in with your email. We'll send a six digit "
                             "code to confirm it's you."))

        self.email = QLineEdit()
        self.email.setPlaceholderText("you@example.com")
        self.email.setClearButtonEnabled(True)
        body.addWidget(self.email)

        self.button = Button("Send code")
        body.addWidget(self.button)

        self.hint = muted("")
        self.hint.setProperty("role", "muted")
        body.addWidget(self.hint)

        self.button.clicked.connect(self._submit)
        self.email.returnPressed.connect(self._submit)

    def _submit(self) -> None:
        email = self.email.text().strip()
        if "@" not in email:
            self.set_hint("Enter a valid email address.")
            return
        self.submitted.emit(email)

    def set_busy(self, busy: bool) -> None:
        self.button.setDisabled(busy)
        self.button.setText("Sending..." if busy else "Send code")

    def set_hint(self, text: str) -> None:
        self.hint.setText(text)

    def prefill(self, email: str) -> None:
        if email:
            self.email.setText(email)


class OtpPage(_Centered):
    """Verify the six digit code sent to the user's inbox."""

    verify = Signal(str)  # code
    resend = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        body = self.card.body()
        body.addWidget(heading("Check your email", "h2"))
        self._subtitle = muted("Enter the six digit code we just sent you.")
        body.addWidget(self._subtitle)

        self.code = OtpInput()
        body.addWidget(self.code)

        self.button = Button("Verify")
        body.addWidget(self.button)

        row = QHBoxLayout()
        self.resend_btn = Button("Resend code", role="ghost")
        self.back_btn = Button("Use another email", role="ghost")
        row.addWidget(self.resend_btn)
        row.addWidget(self.back_btn)
        body.addLayout(row)

        self.hint = muted("")
        body.addWidget(self.hint)

        self.button.clicked.connect(self._verify)
        self.code.completed.connect(lambda _: self._verify())
        self.resend_btn.clicked.connect(self.resend.emit)

    def _verify(self) -> None:
        code = self.code.text().strip()
        if len(code) != 6:
            self.set_hint("The code is six digits.")
            return
        self.verify.emit(code)

    def set_email(self, email: str) -> None:
        self._subtitle.setText(f"Enter the six digit code we sent to {email}.")

    def set_busy(self, busy: bool) -> None:
        self.button.setDisabled(busy)
        self.button.setText("Verifying..." if busy else "Verify")

    def set_hint(self, text: str) -> None:
        self.hint.setText(text)

    def reset(self) -> None:
        self.code.clear()
        self.hint.setText("")


class PendingApprovalPage(_Centered):
    """Shown when the licence exists but has not been approved yet."""

    recheck = Signal()
    logout = Signal()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        body = self.card.body()
        body.addWidget(heading("Awaiting approval", "h2"))
        body.addWidget(muted(
            "Your account is verified. A licence request has been sent for "
            "manual approval. You'll get access as soon as it's approved."
        ))
        self.button = Button("Check again")
        body.addWidget(self.button)
        self.logout_btn = Button("Sign out", role="ghost")
        body.addWidget(self.logout_btn)
        self.hint = muted("")
        body.addWidget(self.hint)

        self.button.clicked.connect(self.recheck.emit)
        self.logout_btn.clicked.connect(self.logout.emit)

    def set_hint(self, text: str) -> None:
        self.hint.setText(text)
