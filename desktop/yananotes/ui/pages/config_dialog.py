"""First run (and later editable) Supabase connection dialog.

Lets an end user paste their Supabase project URL and anon key without ever
editing a file. Values are saved via :meth:`config.Deployment.save` into a
per user ``connection.json``.
"""
from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from ...config import deployment
from ..widgets import Button, heading, muted


class ConnectionDialog(QDialog):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Connect to Supabase")
        self.setObjectName("root")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(26, 26, 26, 22)
        layout.setSpacing(12)
        layout.addWidget(heading("Connect to Supabase", "h2"))
        layout.addWidget(muted(
            "Paste your project URL and anon (public) key from Supabase, "
            "Project Settings, API. The anon key is safe to store on this "
            "device; row level security protects your data."
        ))

        self.url = QLineEdit()
        self.url.setPlaceholderText("https://your-project-ref.supabase.co")
        self.url.setText(deployment.supabase_url)
        layout.addWidget(self.url)

        self.key = QLineEdit()
        self.key.setPlaceholderText("anon public key")
        self.key.setText(deployment.supabase_anon_key)
        self.key.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.key)

        self.hint = muted("")
        layout.addWidget(self.hint)

        row = QHBoxLayout()
        row.addStretch(1)
        self.later = Button("Later", role="ghost")
        self.save = Button("Save and connect")
        row.addWidget(self.later)
        row.addWidget(self.save)
        layout.addLayout(row)

        self.later.clicked.connect(self.reject)
        self.save.clicked.connect(self._save)

    def _save(self) -> None:
        url = self.url.text().strip()
        key = self.key.text().strip()
        if not url.startswith("http") or "supabase" not in url:
            self.hint.setText("That does not look like a Supabase URL.")
            return
        if len(key) < 20:
            self.hint.setText("That anon key looks too short.")
            return
        deployment.save(url, key)
        self.accept()
