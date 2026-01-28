# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all
from PyInstaller.utils.hooks import copy_metadata

datas = [('models', 'models')]
binaries = []
hiddenimports = ['mediapipe', 'mediapipe.tasks', 'mediapipe.tasks.python', 'mediapipe.tasks.python.vision', 'cv2', 'numpy', 'PySide6', 'PySide6.QtCore', 'PySide6.QtWidgets', 'PySide6.QtGui', 'gui.main_window', 'gui.regular_mode_view', 'gui.pomodoro_mode_view', 'model.regular_mode_model', 'model.pomodoro_mode_model', 'controller.regular_mode_controller', 'controller.pomodoro_mode_controller', 'controller.facial_imaging_controller', 'utils.notification']
datas += copy_metadata('mediapipe')
datas += copy_metadata('opencv-contrib-python')
tmp_ret = collect_all('mediapipe')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('PySide6')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('cv2')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['src/main.py'],
    pathex=['src'],
    binaries=binaries,
    datas=datas,
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
    [],
    exclude_binaries=True,
    name='FocusPomodoro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FocusPomodoro',
)
app = BUNDLE(
    coll,
    name='FocusPomodoro.app',
    icon=None,
    bundle_identifier='com.focus.pomodoro',
)
