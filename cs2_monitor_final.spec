# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(SPEC))
sys.path.insert(0, current_dir)

block_cipher = None

a = Analysis(
    ['floating_ping_monitor.py'],
    pathex=[current_dir],
    binaries=[],
    datas=[
        ('icons', 'icons'),  # Include icons folder
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CS2-Ping-Monitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # CRITICAL: No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icons/icon.ico',
    windows_no_console=True,  # Additional Windows-specific setting
)

# Create version info
app = BUNDLE(
    exe,
    name='CS2-Ping-Monitor.exe',
    version='1.0.0',
    description='CS2 Ping Monitor - Official Servers',
    author='Alaeddine bereche',
    copyright='© 2025',
    icon='icons/icon.ico',
    bundle_identifier=None,
)
