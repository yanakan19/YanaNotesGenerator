"""Settings: appearance, repository location (with the migration popup),
Google Drive sync, and sign out."""
from __future__ import annotations

import shutil
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from ...config import settings
from ...integrations import gdrive
from ...theme import ThemeMode
from ..widgets import Button, Card, heading, muted


class RepositoryChangeDialog(QDialog):
    """Ask what to do with existing files when the location changes.

    Returns one of: ``duplicate``, ``disconnect``, ``fresh``, ``delete``.
    """

    def __init__(self, old_path: str, new_path: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Change repository location")
        self.setObjectName("root")
        self.setMinimumWidth(460)
        self.choice = "fresh"

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 22)
        layout.setSpacing(14)
        layout.addWidget(heading("Change repository", "h2"))
        layout.addWidget(muted(
            f"Moving from:\n{old_path or '(none)'}\n\nTo:\n{new_path}\n\n"
            "What would you like to do with your existing notes?"
        ))

        self._group = QButtonGroup(self)
        options = [
            ("duplicate", "Duplicate", "Copy existing notes into the new location."),
            ("disconnect", "Remove link only",
             "Point at the new location but leave the old files untouched."),
            ("fresh", "Start brand new",
             "Use the new location as an empty, fresh library."),
            ("delete", "Remove previous files",
             "Permanently delete everything at the old location."),
        ]
        for value, title, desc in options:
            rb = QRadioButton(f"{title}  —  {desc}")
            rb.setProperty("_value", value)
            if value == "fresh":
                rb.setChecked(True)
            self._group.addButton(rb)
            layout.addWidget(rb)

        row = QHBoxLayout()
        row.addStretch(1)
        cancel = Button("Cancel", role="ghost")
        confirm = Button("Apply")
        row.addWidget(cancel)
        row.addWidget(confirm)
        layout.addLayout(row)

        cancel.clicked.connect(self.reject)
        confirm.clicked.connect(self._confirm)

        # No old files -> only "fresh" makes sense; hide the rest.
        if not old_path or not Path(old_path).exists():
            for btn in self._group.buttons():
                if btn.property("_value") != "fresh":
                    btn.setEnabled(False)

    def _confirm(self) -> None:
        checked = self._group.checkedButton()
        if checked is not None:
            self.choice = checked.property("_value")
        self.accept()


class SettingsPage(QWidget):
    theme_changed = Signal(str)  # ThemeMode value
    repository_changed = Signal()
    logout = Signal()
    toast = Signal(str)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 24, 28, 24)
        root.setSpacing(18)
        root.addWidget(heading("Settings"))

        root.addWidget(self._appearance_card())
        root.addWidget(self._repository_card())
        root.addWidget(self._integrations_card())
        root.addWidget(self._account_card())
        root.addStretch(1)

        self._sync_from_settings()

    # -- appearance -------------------------------------------------------
    def _appearance_card(self) -> Card:
        card = Card()
        body = card.body()
        body.addWidget(heading("Appearance", "h2"))
        body.addWidget(muted("Choose how YanaNotes looks. System follows your "
                             "operating system."))
        row = QHBoxLayout()
        row.addWidget(QLabel("Theme"))
        row.addStretch(1)
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Light", ThemeMode.LIGHT.value)
        self.theme_combo.addItem("System", ThemeMode.SYSTEM.value)
        self.theme_combo.addItem("Dark", ThemeMode.DARK.value)
        self.theme_combo.currentIndexChanged.connect(self._on_theme)
        row.addWidget(self.theme_combo)
        body.addLayout(row)
        return card

    def _on_theme(self) -> None:
        mode = self.theme_combo.currentData()
        settings.set_theme_mode(mode)
        self.theme_changed.emit(mode)

    # -- repository -------------------------------------------------------
    def _repository_card(self) -> Card:
        card = Card()
        body = card.body()
        body.addWidget(heading("Repository", "h2"))
        body.addWidget(muted("Where your module notes live on this PC."))
        row = QHBoxLayout()
        self.repo_label = QLabel("")
        self.repo_label.setWordWrap(True)
        row.addWidget(self.repo_label, 1)
        change = Button("Change...", role="ghost")
        change.clicked.connect(self._change_repository)
        row.addWidget(change)
        body.addLayout(row)
        return card

    def _change_repository(self) -> None:
        new_path = QFileDialog.getExistingDirectory(
            self, "Choose repository folder", settings.repository() or ""
        )
        if not new_path:
            return
        old_path = settings.repository()
        if Path(new_path) == Path(old_path or ""):
            return
        dialog = RepositoryChangeDialog(old_path, new_path, self)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        try:
            self._apply_repository_change(old_path, new_path, dialog.choice)
        except Exception as exc:
            self.toast.emit(f"Could not update repository: {exc}")
            return
        settings.set_repository(new_path)
        self._sync_from_settings()
        self.repository_changed.emit()
        self.toast.emit("Repository updated.")

    def _apply_repository_change(self, old: str, new: str, choice: str) -> None:
        new_dir = Path(new)
        new_dir.mkdir(parents=True, exist_ok=True)
        old_dir = Path(old) if old else None

        if choice == "duplicate" and old_dir and old_dir.exists():
            for item in old_dir.iterdir():
                dest = new_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest)
        elif choice == "delete" and old_dir and old_dir.exists():
            for item in old_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
        # "disconnect" and "fresh" need no file operations.

    # -- integrations -----------------------------------------------------
    def _integrations_card(self) -> Card:
        card = Card()
        body = card.body()
        body.addWidget(heading("Phone access (Google Drive)", "h2"))
        st = gdrive.status()
        body.addWidget(muted(gdrive.guidance()))
        self.gdrive_btn = Button(
            "Enable Drive sync" if not settings.gdrive_enabled() else "Disable Drive sync",
            role="ghost",
        )
        self.gdrive_btn.setEnabled(st.available or settings.gdrive_enabled())
        self.gdrive_btn.clicked.connect(self._toggle_gdrive)
        body.addWidget(self.gdrive_btn)
        if not st.available:
            body.addWidget(muted(st.detail))
        return card

    def _toggle_gdrive(self) -> None:
        new_state = not settings.gdrive_enabled()
        settings.set_gdrive_enabled(new_state)
        self.gdrive_btn.setText(
            "Disable Drive sync" if new_state else "Enable Drive sync"
        )
        self.toast.emit("Drive sync " + ("enabled." if new_state else "disabled."))

    # -- account ----------------------------------------------------------
    def _account_card(self) -> Card:
        card = Card()
        body = card.body()
        body.addWidget(heading("Account", "h2"))
        self.account_label = muted("")
        body.addWidget(self.account_label)
        logout_btn = Button("Sign out", role="danger")
        logout_btn.clicked.connect(self.logout.emit)
        body.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        return card

    # -- helpers ----------------------------------------------------------
    def set_account(self, email: str) -> None:
        self.account_label.setText(f"Signed in as {email}")

    def _sync_from_settings(self) -> None:
        idx = self.theme_combo.findData(settings.theme_mode())
        if idx >= 0:
            self.theme_combo.blockSignals(True)
            self.theme_combo.setCurrentIndex(idx)
            self.theme_combo.blockSignals(False)
        repo = settings.repository()
        self.repo_label.setText(repo if repo else "No repository set.")
