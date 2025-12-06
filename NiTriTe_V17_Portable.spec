# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules, collect_all

# Imports cachés critiques pour NiTriTe V17
hiddenimports = [
    # Système et monitoring
    'psutil', 'requests', 'wmi', 'win32com', 'win32com.client', 'pythoncom',
    # Interface graphique
    'customtkinter', 'tkinter', 'tkinter.ttk', 'tkinter.font',
    # Images
    'PIL', 'PIL.Image', 'PIL.ImageTk', 'PIL._tkinter_finder',
    # Modules v14_mvp
    'v14_mvp', 'v14_mvp.design_system', 'v14_mvp.components',
    'v14_mvp.navigation', 'v14_mvp.pages_simple', 'v14_mvp.pages_optimized',
    'v14_mvp.pages_full', 'v14_mvp.pages_settings',
    'v14_mvp.page_master_install', 'v14_mvp.page_portables',
    'v14_mvp.page_terminal', 'v14_mvp.splash_loader', 'v14_mvp.installer',
]
hiddenimports += collect_submodules('win32com')
hiddenimports += collect_submodules('wmi')
hiddenimports += collect_submodules('pythoncom')
hiddenimports += collect_submodules('customtkinter')


a = Analysis(
    ['src\\v14_mvp\\main_app.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('assets', 'assets'), ('src', 'src')],
    hiddenimports=hiddenimports,
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
    a.binaries,
    a.datas,
    [],
    name='NiTriTe_V17_Portable',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Application GUI, pas de console
    disable_windowed_traceback=False,
    icon='assets/logo.ico' if os.path.exists('assets/logo.ico') else None,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
