"""View a single note in app: PDFs via QtPdf when available, markdown and
text rendered inline. Anything else defers to the system application."""
from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QStackedWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ...library import NoteFile
from ..widgets import Button, heading, muted

# QtPdf ships with PySide6 >= 6.4 but is a separate module; degrade gracefully.
try:
    from PySide6.QtPdf import QPdfDocument
    from PySide6.QtPdfWidgets import QPdfView

    _HAVE_PDF = True
except Exception:  # pragma: no cover
    _HAVE_PDF = False


class ViewerPage(QWidget):
    back = Signal()
    open_external = Signal(object)  # NoteFile

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._note: NoteFile | None = None
        self._pdf_doc = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 24)
        root.setSpacing(14)

        bar = QHBoxLayout()
        self.back_btn = Button("Back to library", role="ghost")
        bar.addWidget(self.back_btn)
        self._title = heading("", "h2")
        bar.addWidget(self._title, 1)
        self.external_btn = Button("Open externally", role="ghost")
        bar.addWidget(self.external_btn)
        root.addLayout(bar)

        self._stack = QStackedWidget()
        root.addWidget(self._stack, 1)

        # Markdown / text view.
        self._text = QTextBrowser()
        self._text.setOpenExternalLinks(True)
        self._stack.addWidget(self._text)

        # PDF view (or a fallback notice).
        if _HAVE_PDF:
            self._pdf_view = QPdfView()
            self._pdf_view.setPageMode(QPdfView.PageMode.MultiPage)
            self._stack.addWidget(self._pdf_view)
        else:
            self._pdf_fallback = QWidget()
            fb = QVBoxLayout(self._pdf_fallback)
            fb.addStretch(1)
            fb.addWidget(muted(
                "Inline PDF preview is unavailable in this build. Use "
                "'Open externally' to view the PDF."),
            )
            fb.addStretch(1)
            self._stack.addWidget(self._pdf_fallback)

        self.back_btn.clicked.connect(self.back.emit)
        self.external_btn.clicked.connect(self._emit_external)

    def _emit_external(self) -> None:
        if self._note is not None:
            self.open_external.emit(self._note)

    def show_note(self, note: NoteFile) -> None:
        self._note = note
        self._title.setText(note.name)
        suffix = note.suffix
        if suffix in {"md", "txt"}:
            self._render_text(note.path, markdown=(suffix == "md"))
        elif suffix == "pdf":
            self._render_pdf(note.path)
        else:  # Unsupported inline; nudge to external.
            self._text.setPlainText("This file type opens in your system app.")
            self._stack.setCurrentWidget(self._text)

    def _render_text(self, path: Path, markdown: bool) -> None:
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            self._text.setPlainText(f"Could not open file:\n{exc}")
        else:
            if markdown:
                self._text.setMarkdown(content)
            else:
                self._text.setPlainText(content)
        self._stack.setCurrentWidget(self._text)

    def _render_pdf(self, path: Path) -> None:
        if not _HAVE_PDF:
            self._stack.setCurrentWidget(self._pdf_fallback)
            return
        self._pdf_doc = QPdfDocument(self)
        self._pdf_doc.load(str(path))
        self._pdf_view.setDocument(self._pdf_doc)
        self._stack.setCurrentWidget(self._pdf_view)
