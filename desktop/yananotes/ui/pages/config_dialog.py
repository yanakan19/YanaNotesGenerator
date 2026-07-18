"""First run (and later editable) Supabase connection dialog.

Lets an end user paste their Supabase project URL and publishable (anon) key
without ever editing a file. Values are saved via
:meth:`config.Deployment.save` into a per user ``connection.json``.

Validation here is deliberately strict about SHAPE (not reachability, which
we can't check without a network round trip) because the most common real
world mistake is pasting the wrong string entirely: the dashboard page URL
instead of the project API URL, or a leftover placeholder. Catching that
early avoids a cryptic OS level DNS error surfacing during sign in.
"""
from __future__ import annotations

import re

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLineEdit,
    QVBoxLayout,
    QWidget,
)

from ...config import deployment
from ..widgets import Button, heading, muted

# A Supabase project URL is exactly https://<project-ref>.supabase.co (or a
# custom domain) with no path. The dashboard URL (supabase.com/dashboard/...)
# is the single most common paste mistake, so it gets its own message.
_VALID_HOST_RE = re.compile(
    r"^https://[a-z0-9][a-z0-9\-]*\.supabase\.co/?$", re.IGNORECASE
)
_PLACEHOLDER_MARKERS = ("your-project-ref", "your_project_ref", "xxxxxxxxxxxx")


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
            "Paste your project URL and publishable (anon) key from "
            "Supabase, Project Settings -> API. This key is safe to store "
            "on this device; row level security protects your data. Never "
            "paste a secret key here."
        ))

        self.url = QLineEdit()
        self.url.setPlaceholderText("https://abcdxyz.supabase.co")
        self.url.setText(deployment.supabase_url)
        layout.addWidget(self.url)

        self.key = QLineEdit()
        self.key.setPlaceholderText("sb_publishable_... (or the legacy anon key)")
        self.key.setText(deployment.supabase_anon_key)
        self.key.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.key)

        self.hint = muted("")
        self.hint.setProperty("role", "danger")
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
        url = self.url.text().strip().rstrip("/")
        key = self.key.text().strip()

        error = self._validate(url, key)
        if error:
            self.hint.setText(error)
            return
        deployment.save(url, key)
        self.accept()

    @staticmethod
    def _validate(url: str, key: str) -> str | None:
        if not url or not key:
            return "Enter both the project URL and the key."
        low = url.lower()
        if any(marker in low for marker in _PLACEHOLDER_MARKERS):
            return "That's still the placeholder text, paste your real project URL."
        if "/dashboard" in low or "supabase.com" in low:
            return (
                "That's the dashboard page link. Use the Project URL from "
                "Project Settings -> API instead (https://xxxx.supabase.co)."
            )
        if not _VALID_HOST_RE.match(url):
            return (
                "URL should look like https://your-project-ref.supabase.co "
                "with nothing else after it."
            )
        if key.startswith("sb_secret_"):
            return "That's a secret key. Use the publishable key instead, never the secret one."
        if len(key) < 20:
            return "That key looks too short."
        return None
