# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['logView_v1.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\py_project\\virtualEnv\\v_name\\Lib\\site-packages\\tkinterdnd2', 'tkinterdnd2/')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='logView_v1',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['logo-32.ico'],
)
