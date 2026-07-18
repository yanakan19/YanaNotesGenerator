"""Plain data records describing what the scanner finds on disk."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class NoteFile:
    path: Path

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def suffix(self) -> str:
        return self.path.suffix.lower().lstrip(".")


@dataclass
class Week:
    number: int
    label: str
    path: Path
    generated: list[NoteFile] = field(default_factory=list)  # *_Notes.pdf/.tex/.md
    raw: list[NoteFile] = field(default_factory=list)  # uploaded source material

    @property
    def has_content(self) -> bool:
        return bool(self.generated or self.raw)


@dataclass
class Module:
    code: str
    name: str
    path: Path
    weeks: list[Week] = field(default_factory=list)
