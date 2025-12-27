# Fighting_Game_Simple.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_all

# Автоматический сбор данных
datas, binaries, hiddenimports = collect_all('src')

# Добавляем дополнительные данные
additional_datas = [
    ('Sprites', 'Sprites'),
    ('Sounds', 'Sounds'),
    ('locales', 'locales'),
    ('game_settings.json', '.'),
    ('game_save.json', '.'),
]

datas.extend(additional_datas)

# Добавляем дополнительные скрытые импорты
hiddenimports.extend([
    'pygame',
    'json',
    'os',
    'sys',
])

a = Analysis(
    ['main.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Fighting_Game',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='Sprites/arts/logo.ico' if os.path.exists('Sprites/arts/logo.ico') else None,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='Fighting_Game'
)