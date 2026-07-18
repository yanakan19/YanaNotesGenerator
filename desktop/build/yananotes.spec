# PyInstaller spec for YanaNotes.
# Build a one-folder app:  pyinstaller build/yananotes.spec
# The resulting dist/YanaNotes/ folder is what the Inno Setup installer packs.
# -*- mode: python ; coding: utf-8 -*-
from pathlib import Path

block_cipher = None
project_root = Path(SPECPATH).parent

a = Analysis(
    [str(project_root / "run.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=[],
    hiddenimports=[
        "yananotes",
        "keyring.backends.Windows",
        "keyring.backends.macOS",
        "keyring.backends.SecretService",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="YanaNotes",
    console=False,
    icon=str(project_root / "yananotes" / "resources" / "icons" / "app.ico")
    if (project_root / "yananotes" / "resources" / "icons" / "app.ico").exists()
    else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="YanaNotes",
)
