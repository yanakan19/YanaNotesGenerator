"""Logic tests for the parts of the app that don't need a display:
the library scanner, the connection config, and the repository migration."""
from __future__ import annotations

from pathlib import Path

import pytest


# ----------------------------------------------------------------- scanner
def _make_week(root: Path, module: str, week: str) -> Path:
    wk = root / module / week
    (wk / "sources").mkdir(parents=True)
    return wk


def test_scanner_splits_generated_and_raw(tmp_path: Path):
    from yananotes.library import scan

    (tmp_path / "ES3C2").mkdir()
    (tmp_path / "ES3C2" / "module.md").write_text(
        "- **Full module name:** Advanced Mechanical Engineering Design\n"
    )
    wk = _make_week(tmp_path, "ES3C2", "Week 01")
    # Generated deliverables.
    (wk / "ES3C2_Week01_Notes.pdf").write_text("pdf")
    (wk / "ES3C2_Week01_Notes.tex").write_text("tex")
    (wk / "ES3C2_Week01_Notes.md").write_text("# notes")
    # LaTeX build artifacts that also match *_Notes.* must be ignored.
    (wk / "ES3C2_Week01_Notes.aux").write_text("aux")
    (wk / "ES3C2_Week01_Notes.log").write_text("log")
    # Raw upload under sources/.
    (wk / "sources" / "ES3C2_Week1_Lecture.pdf").write_text("raw")

    modules = scan(tmp_path)
    assert [m.code for m in modules] == ["ES3C2"]
    module = modules[0]
    assert module.name == "Advanced Mechanical Engineering Design"
    assert len(module.weeks) == 1
    week = module.weeks[0]
    gen = {f.name for f in week.generated}
    raw = {f.name for f in week.raw}
    assert gen == {
        "ES3C2_Week01_Notes.pdf",
        "ES3C2_Week01_Notes.tex",
        "ES3C2_Week01_Notes.md",
    }
    assert "ES3C2_Week01_Notes.aux" not in gen
    assert "ES3C2_Week01_Notes.log" not in gen
    assert raw == {"ES3C2_Week1_Lecture.pdf"}


def test_scanner_week_numbering_and_sort(tmp_path: Path):
    from yananotes.library import scan

    for wk_name in ("Week 10", "Week 02", "Week 1"):
        wk = _make_week(tmp_path, "ES386", wk_name)
        (wk / f"ES386_{wk_name.replace(' ', '')}_Notes.pdf").write_text("x")
    modules = scan(tmp_path)
    numbers = [w.number for w in modules[0].weeks]
    assert numbers == [1, 2, 10]  # sorted numerically, not lexically


def test_scanner_ignores_non_module_dirs(tmp_path: Path):
    from yananotes.library import scan

    (tmp_path / "random").mkdir()
    (tmp_path / "random" / "notes.txt").write_text("hi")
    assert scan(tmp_path) == []


def test_scanner_missing_repo_returns_empty():
    from yananotes.library import scan

    assert scan("/nonexistent/path/xyz") == []


# ------------------------------------------------------------ connection cfg
def test_deployment_file_roundtrip(qapp, tmp_path, monkeypatch):
    import yananotes.config as cfg

    target = tmp_path / "connection.json"
    monkeypatch.setattr(cfg, "_runtime_config_path", lambda: target)
    dep = cfg.Deployment()
    assert not dep.configured
    dep.save("https://abc.supabase.co", "a" * 40)
    assert dep.configured
    # A fresh instance reads the persisted file.
    dep2 = cfg.Deployment()
    assert dep2.supabase_url == "https://abc.supabase.co"
    assert dep2.supabase_anon_key == "a" * 40


def test_env_overrides_file(qapp, tmp_path, monkeypatch):
    import yananotes.config as cfg

    target = tmp_path / "connection.json"
    monkeypatch.setattr(cfg, "_runtime_config_path", lambda: target)
    dep = cfg.Deployment()
    dep.save("https://file.supabase.co", "f" * 40)
    monkeypatch.setenv("SUPABASE_URL", "https://env.supabase.co")
    assert dep.supabase_url == "https://env.supabase.co"  # env wins


# ------------------------------------------------------- repository migration
def test_repository_duplicate_and_delete(qapp, tmp_path):
    from yananotes.ui.pages.settings_page import SettingsPage

    old = tmp_path / "old"
    (old / "ES3C2" / "Week 01").mkdir(parents=True)
    (old / "ES3C2" / "Week 01" / "note.md").write_text("hello")
    new = tmp_path / "new"

    page = SettingsPage()

    # Duplicate copies the tree into the new location.
    page._apply_repository_change(str(old), str(new), "duplicate")
    assert (new / "ES3C2" / "Week 01" / "note.md").read_text() == "hello"
    assert (old / "ES3C2" / "Week 01" / "note.md").exists()  # original intact

    # Delete removes everything at the old location.
    page._apply_repository_change(str(old), str(new), "delete")
    assert not any(old.iterdir())


def test_repository_fresh_is_noop_on_old(qapp, tmp_path):
    from yananotes.ui.pages.settings_page import SettingsPage

    old = tmp_path / "old"
    old.mkdir()
    (old / "keep.txt").write_text("keep")
    new = tmp_path / "new"
    page = SettingsPage()
    page._apply_repository_change(str(old), str(new), "fresh")
    assert (old / "keep.txt").exists()  # untouched
    assert new.exists()


# ------------------------------------------------------------------- theme
def test_theme_qss_builds_for_all_modes(qapp):
    from yananotes.theme import ThemeMode, build_qss, resolve

    for mode in ThemeMode:
        qss = build_qss(resolve(mode))
        assert "QPushButton" in qss and "background" in qss
