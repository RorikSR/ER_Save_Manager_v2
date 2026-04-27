# -*- mode: python ; coding: utf-8 -*-

datas = [
    ("data/assets", "data/assets"),
    ("data/items", "data/items"),
    ("data/background.png", "data"),
    ("data/changelog.txt", "data"),
    ("data/config.example.json", "data"),
    ("data/copy-readme.txt", "data"),
    ("data/icon.ico", "data"),
    ("data/readme.txt", "data"),
    ("data/upd.ico", "data"),
]
from PyInstaller.utils.hooks import collect_data_files

datas += collect_data_files("customtkinter")


a = Analysis(
    ["app_nexus.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        "PIL._tkinter_finder",
        "customtkinter",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="ER_Save_Manager_v2_Nexus",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="data/icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="ER_Save_Manager_v2_Nexus",
)
