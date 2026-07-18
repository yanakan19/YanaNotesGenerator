"""The application shell: wires the auth flow, the sidebar navigation, and the
library / viewer / settings pages together, running all network and disk work
off the UI thread."""
from __future__ import annotations

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from ..async_task import run_async
from ..auth import AuthError, AuthService, LicenseStatus, session as session_store
from ..config import AUTH_ENABLED, settings
from ..library import NoteFile
from ..theme import ThemeManager, ThemeMode
from .pages import (
    LibraryPage,
    LoginPage,
    OtpPage,
    PendingApprovalPage,
    SettingsPage,
    ViewerPage,
)
from .widgets import Button, PageStack, Toast, heading


class MainWindow(QMainWindow):
    def __init__(self, theme: ThemeManager):
        super().__init__()
        self._theme = theme
        self._auth = AuthService()
        self._email = ""

        self.setWindowTitle("YanaNotes")
        self.resize(1120, 760)
        self.setMinimumSize(880, 600)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)

        self._stack = PageStack()
        outer.addWidget(self._stack)

        self._toast = Toast(root)

        self._build_auth_pages()
        self._build_shell()

        self._stack.add(self._login)
        self._stack.add(self._otp)
        self._stack.add(self._pending)
        self._stack.add(self._shell)

        if AUTH_ENABLED:
            self._try_restore()
        else:
            self._enter_local_mode()

    # -- construction -----------------------------------------------------
    def _build_auth_pages(self) -> None:
        self._login = LoginPage()
        self._otp = OtpPage()
        self._pending = PendingApprovalPage()

        self._login.submitted.connect(self._send_code)
        self._otp.verify.connect(self._verify_code)
        self._otp.resend.connect(lambda: self._send_code(self._email))
        self._otp.back_btn.clicked.connect(lambda: self._stack.show_page(self._login))
        self._pending.recheck.connect(self._check_license)
        self._pending.logout.connect(self._logout)

    def _build_shell(self) -> None:
        self._shell = QWidget()
        layout = QHBoxLayout(self._shell)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Sidebar.
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(16, 22, 16, 22)
        sb.setSpacing(6)
        brand = heading("YanaNotes", "h2")
        brand.setProperty("role", "accent")
        sb.addWidget(brand)
        sb.addSpacing(18)

        self._nav_library = self._nav_button("Library")
        self._nav_settings = self._nav_button("Settings")
        sb.addWidget(self._nav_library)
        sb.addWidget(self._nav_settings)
        sb.addStretch(1)
        layout.addWidget(sidebar)

        # Content.
        self._content = PageStack()
        self._library = LibraryPage()
        self._viewer = ViewerPage()
        self._settings = SettingsPage()
        self._content.add(self._library)
        self._content.add(self._viewer)
        self._content.add(self._settings)
        layout.addWidget(self._content, 1)

        self._nav_library.clicked.connect(self._go_library)
        self._nav_settings.clicked.connect(self._go_settings)

        self._library.open_note.connect(self._open_note)
        self._library.reveal_note.connect(self._reveal_note)
        self._viewer.back.connect(self._go_library)
        self._viewer.open_external.connect(self._reveal_note)

        self._settings.theme_changed.connect(self._on_theme_changed)
        self._settings.repository_changed.connect(self._library.reload)
        self._settings.connection_changed.connect(self._auth.reset)
        self._settings.logout.connect(self._logout)
        self._settings.toast.connect(self._toast.show_message)

        self._set_active_nav(self._nav_library)

    def _nav_button(self, text: str) -> Button:
        btn = Button(text, role="nav")
        return btn

    def _set_active_nav(self, active: Button) -> None:
        for btn in (self._nav_library, self._nav_settings):
            btn.setProperty("active", "true" if btn is active else "false")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # -- navigation -------------------------------------------------------
    def _go_library(self) -> None:
        self._content.show_page(self._library)
        self._set_active_nav(self._nav_library)

    def _go_settings(self) -> None:
        self._settings.set_account(self._email)
        self._content.show_page(self._settings)
        self._set_active_nav(self._nav_settings)

    def _open_note(self, note: NoteFile) -> None:
        self._viewer.show_note(note)
        self._content.show_page(self._viewer)

    def _reveal_note(self, note: NoteFile) -> None:
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(note.path)))

    # -- auth flow --------------------------------------------------------
    def _enter_local_mode(self) -> None:
        """AUTH_ENABLED is off: skip login entirely, run fully locally."""
        self._email = ""
        self._settings.set_account("")
        self._library.reload()
        self._go_library()
        self._stack.show_page(self._shell)

    def _try_restore(self) -> None:
        stored = session_store.load()
        if stored is None:
            self._login.prefill(settings.last_email())
            self._stack.show_page(self._login)
            return
        self._email = stored.email

        def restore():
            ok = self._auth.restore(stored.access_token, stored.refresh_token)
            if not ok:
                raise AuthError("Session expired.")
            return self._auth.license_status(stored.email)

        run_async(
            restore,
            on_ok=self._on_license_result,
            on_error=lambda _msg: self._stack.show_page(self._login),
        )

    def _send_code(self, email: str) -> None:
        self._email = email
        self._login.set_busy(True)
        self._login.set_hint("")

        run_async(
            lambda: self._auth.request_code(email),
            on_ok=lambda _r: self._on_code_sent(),
            on_error=self._on_login_error,
        )

    def _on_code_sent(self) -> None:
        self._login.set_busy(False)
        self._otp.reset()
        self._otp.set_email(self._email)
        settings.set_last_email(self._email)
        self._stack.show_page(self._otp)

    def _on_login_error(self, msg: str) -> None:
        self._login.set_busy(False)
        self._login.set_hint(msg)

    def _verify_code(self, code: str) -> None:
        self._otp.set_busy(True)
        self._otp.set_hint("")

        def verify():
            sess = self._auth.verify_code(self._email, code)
            session_store.save(sess.email, sess.access_token, sess.refresh_token)
            return self._auth.license_status(sess.email)

        run_async(
            verify,
            on_ok=self._on_license_result,
            on_error=self._on_otp_error,
        )

    def _on_otp_error(self, msg: str) -> None:
        self._otp.set_busy(False)
        self._otp.set_hint(msg)

    def _check_license(self) -> None:
        self._pending.set_hint("Checking...")
        run_async(
            lambda: self._auth.license_status(self._email),
            on_ok=self._on_license_result,
            on_error=lambda msg: self._pending.set_hint(msg),
        )

    def _on_license_result(self, status: LicenseStatus) -> None:
        self._otp.set_busy(False)
        if status == LicenseStatus.APPROVED:
            self._enter_app()
        elif status == LicenseStatus.REVOKED:
            self._pending.set_hint("This licence has been revoked.")
            self._stack.show_page(self._pending)
        else:
            self._pending.set_hint("")
            self._stack.show_page(self._pending)

    def _enter_app(self) -> None:
        self._settings.set_account(self._email)
        self._library.reload()
        self._go_library()
        self._stack.show_page(self._shell)

    def _logout(self) -> None:
        if not AUTH_ENABLED:
            self._toast.show_message("Login is disabled in this build.")
            return
        run_async(self._auth.sign_out, on_ok=lambda _r: None, on_error=lambda _m: None)
        session_store.clear()
        self._email = ""
        self._login.prefill("")
        self._stack.show_page(self._login)
        self._toast.show_message("Signed out.")

    # -- theme ------------------------------------------------------------
    def _on_theme_changed(self, mode: str) -> None:
        try:
            self._theme.set_mode(ThemeMode(mode))
        except ValueError:
            self._theme.set_mode(ThemeMode.DARK)

    # -- events -----------------------------------------------------------
    def resizeEvent(self, event) -> None:  # keep the toast anchored
        super().resizeEvent(event)
        if self._toast.isVisible():
            self._toast.move(
                max((self.width() - self._toast.width()) // 2, 12),
                self.height() - self._toast.height() - 40,
            )
