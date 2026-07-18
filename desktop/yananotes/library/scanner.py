"""Walk a repository folder and build the module / week / notes tree.

The layout mirrors what the YanaNotesGenerator pipeline writes:

    <REPO>/
      <MODULE>/
        module.md                      (optional; gives the full module name)
        Week 01/
          sources/                     -> raw notes (uploaded material)
          MODULE_Week01_Notes.pdf      -> generated notes
          MODULE_Week01_Notes.tex
          MODULE_Week01_Notes.md
          extraction/ figures/ ...     (pipeline internals, ignored)

Anything named ``*_Notes.*`` at a week root is a generated note; the contents
of ``sources/`` (plus any loose upload in the week folder) are raw notes.
"""
from __future__ import annotations

import re
from pathlib import Path

from .models import Module, NoteFile, Week

_WEEK_RE = re.compile(r"week[\s_]*0*(\d+)", re.IGNORECASE)
_GENERATED_RE = re.compile(r"_notes\.", re.IGNORECASE)
# Only real deliverables count as generated notes; skip LaTeX build artifacts
# (.aux/.log/.out/.toc/.synctex.gz/.fls/.fdb_latexmk) that also match *_Notes.*.
_GENERATED_SUFFIXES = {".pdf", ".tex", ".md", ".docx", ".html"}
_RAW_SUFFIXES = {".pdf", ".pptx", ".ppt", ".docx", ".doc", ".md", ".txt", ".png", ".jpg"}
_INTERNAL_DIRS = {"extraction", "figures", "pages-cache", "sources"}


def _module_display_name(module_dir: Path) -> str:
    """Prefer the full name from module.md, else fall back to the folder."""
    md = module_dir / "module.md"
    if md.exists():
        try:
            for line in md.read_text(encoding="utf-8", errors="ignore").splitlines():
                low = line.lower()
                if "full module name" in low and ":" in line:
                    value = line.split(":", 1)[1].strip().strip("*").strip()
                    if value:
                        return value
        except Exception:
            pass
    return module_dir.name


def _scan_week(week_dir: Path) -> Week | None:
    match = _WEEK_RE.search(week_dir.name)
    if not match:
        return None
    number = int(match.group(1))

    generated: list[NoteFile] = []
    raw: list[NoteFile] = []

    # Generated notes and any loose uploads sitting at the week root.
    for item in sorted(week_dir.iterdir()):
        if item.is_dir():
            continue
        suffix = item.suffix.lower()
        if _GENERATED_RE.search(item.name) and suffix in _GENERATED_SUFFIXES:
            generated.append(NoteFile(item))
        elif _GENERATED_RE.search(item.name):
            continue  # LaTeX build artifact for a notes file; skip it.
        elif suffix in _RAW_SUFFIXES:
            raw.append(NoteFile(item))

    # Raw uploads live under sources/.
    sources = week_dir / "sources"
    if sources.is_dir():
        for item in sorted(sources.iterdir()):
            if item.is_file() and item.suffix.lower() in _RAW_SUFFIXES:
                raw.append(NoteFile(item))

    week = Week(number=number, label=f"Week {number:02d}", path=week_dir,
                generated=generated, raw=raw)
    return week if week.has_content else None


def _looks_like_module(candidate: Path) -> bool:
    if (candidate / "module.md").exists():
        return True
    return any(_WEEK_RE.search(child.name) for child in candidate.iterdir()
               if child.is_dir())


def scan(repository: str | Path) -> list[Module]:
    """Return the sorted list of modules found under ``repository``."""
    root = Path(repository).expanduser()
    if not root.is_dir():
        return []

    modules: list[Module] = []
    for module_dir in sorted(root.iterdir()):
        if not module_dir.is_dir() or module_dir.name.startswith("."):
            continue
        if module_dir.name in _INTERNAL_DIRS:
            continue
        try:
            if not _looks_like_module(module_dir):
                continue
        except PermissionError:
            continue

        weeks: list[Week] = []
        for child in sorted(module_dir.iterdir()):
            if child.is_dir():
                week = _scan_week(child)
                if week:
                    weeks.append(week)
        weeks.sort(key=lambda w: w.number)
        modules.append(
            Module(
                code=module_dir.name,
                name=_module_display_name(module_dir),
                path=module_dir,
                weeks=weeks,
            )
        )
    return modules
