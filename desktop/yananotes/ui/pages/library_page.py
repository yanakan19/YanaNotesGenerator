"""Browse the repository: modules and weeks on the left, that week's notes
split into Generated and Raw on the right."""
from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QTreeView,
    QVBoxLayout,
    QWidget,
)

from ...library import Module, NoteFile, Week, scan
from ..widgets import Button, Card, heading, muted

_ROLE_KIND = Qt.ItemDataRole.UserRole + 1
_ROLE_REF = Qt.ItemDataRole.UserRole + 2


class LibraryPage(QWidget):
    open_note = Signal(object)  # NoteFile
    reveal_note = Signal(object)  # NoteFile (open externally)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self._modules: list[Module] = []

        root = QHBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(18)

        # Left: module / week tree.
        left = QVBoxLayout()
        left.setSpacing(10)
        header_row = QHBoxLayout()
        header_row.addWidget(heading("Library", "h2"))
        header_row.addStretch(1)
        self.refresh_btn = Button("Refresh", role="ghost")
        header_row.addWidget(self.refresh_btn)
        left.addLayout(header_row)

        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree.setMinimumWidth(300)
        self.tree.setMaximumWidth(380)
        left.addWidget(self.tree, 1)
        root.addLayout(left)

        # Right: detail panel for the selected week.
        self.detail = QScrollArea()
        self.detail.setWidgetResizable(True)
        self.detail.setFrameShape(QScrollArea.Shape.NoFrame)
        self._detail_host = QWidget()
        self._detail_layout = QVBoxLayout(self._detail_host)
        self._detail_layout.setContentsMargins(4, 4, 4, 4)
        self._detail_layout.setSpacing(16)
        self._detail_layout.addStretch(1)
        self.detail.setWidget(self._detail_host)
        root.addWidget(self.detail, 1)

        self.refresh_btn.clicked.connect(self.reload)
        self.tree.clicked.connect(self._on_tree_click)

        self._show_placeholder("Select a week to see its notes.")

    # -- data -------------------------------------------------------------
    def reload(self) -> None:
        from ...config import settings

        repo = settings.repository()
        if not repo:
            self._modules = []
            self._populate_tree()
            self._show_placeholder(
                "No repository set. Open Settings to choose where your notes "
                "live on this PC."
            )
            return
        self._modules = scan(repo)
        self._populate_tree()
        if not self._modules:
            self._show_placeholder(
                "No modules found in this repository yet. Generated notes will "
                "appear here automatically."
            )
        else:
            self._show_placeholder("Select a week to see its notes.")

    def _populate_tree(self) -> None:
        model = QStandardItemModel()
        for module in self._modules:
            m_item = QStandardItem(f"{module.code}  ·  {module.name}")
            m_item.setData("module", _ROLE_KIND)
            m_item.setEditable(False)
            for week in module.weeks:
                w_item = QStandardItem(week.label)
                w_item.setData("week", _ROLE_KIND)
                w_item.setData(week, _ROLE_REF)
                w_item.setEditable(False)
                m_item.appendRow(w_item)
            model.appendRow(m_item)
        self.tree.setModel(model)
        self.tree.expandAll()

    # -- interaction ------------------------------------------------------
    def _on_tree_click(self, index) -> None:
        kind = index.data(_ROLE_KIND)
        if kind == "week":
            week = index.data(_ROLE_REF)
            if isinstance(week, Week):
                self._show_week(week)

    def _clear_detail(self) -> None:
        while self._detail_layout.count():
            item = self._detail_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def _show_placeholder(self, text: str) -> None:
        self._clear_detail()
        self._detail_layout.addStretch(1)
        lbl = muted(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._detail_layout.addWidget(lbl)
        self._detail_layout.addStretch(1)

    def _show_week(self, week: Week) -> None:
        self._clear_detail()
        self._detail_layout.addWidget(heading(week.label, "h1"))

        self._detail_layout.addWidget(
            self._section("Generated notes", week.generated,
                          "Compiled study notes produced by the pipeline.")
        )
        self._detail_layout.addWidget(
            self._section("Raw notes", week.raw,
                          "Your original uploaded source material.")
        )
        self._detail_layout.addStretch(1)

    def _section(self, title: str, files: list[NoteFile], subtitle: str) -> Card:
        card = Card()
        body = card.body()
        body.addWidget(heading(title, "h2"))
        body.addWidget(muted(subtitle))
        if not files:
            body.addWidget(muted("Nothing here yet."))
            return card
        for note in files:
            body.addWidget(self._file_row(note))
        return card

    def _file_row(self, note: NoteFile) -> QWidget:
        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        badge = QLabel(note.suffix.upper())
        badge.setProperty("role", "accent")
        badge.setFixedWidth(46)
        layout.addWidget(badge)

        name = QLabel(note.name)
        name.setToolTip(str(note.path))
        layout.addWidget(name, 1)

        viewable = note.suffix in {"pdf", "md", "txt"}
        if viewable:
            open_btn = Button("Open", role="ghost")
            open_btn.clicked.connect(lambda _=False, n=note: self.open_note.emit(n))
            layout.addWidget(open_btn)

        ext_btn = Button("Reveal", role="ghost")
        ext_btn.clicked.connect(lambda _=False, n=note: self.reveal_note.emit(n))
        layout.addWidget(ext_btn)
        return row
