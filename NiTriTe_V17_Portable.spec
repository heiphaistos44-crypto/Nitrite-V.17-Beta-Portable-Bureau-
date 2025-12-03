# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['psutil', 'requests', 'wmi', 'win32com', 'win32com.client', 'pythoncom']
hiddenimports += collect_submodules('win32com')
hiddenimports += collect_submodules('wmi')
hiddenimports += collect_submodules('pythoncom')


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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
