# -*- mode: python ; coding: utf-8 -*-
"""
Configuración PyInstaller para EXPANSION DE DOMINIO - INVENTORIA
Versión portátil completa - by Antware (SysAdmin)
"""

import os
from pathlib import Path

# Configuración básica
app_name = 'EXPANSION_DE_DOMINIO_INVENTORIA_PORTABLE'
main_script = 'run_app.py'
icon_file = 'images/fondo.png' if os.path.exists('images/fondo.png') else None

# Archivos de datos a incluir
added_files = [
    ('homologador', 'homologador'),
    ('images', 'images'),
    ('dist_portable/homologador.db', '.'),  # BD en raíz del ejecutable
    ('dist_portable/images', 'images'),     # Imágenes accesibles
]

# Datos binarios adicionales
binaries = []

# Módulos ocultos necesarios
hidden_imports = [
    'PyQt6',
    'PyQt6.QtCore',
    'PyQt6.QtWidgets', 
    'PyQt6.QtGui',
    'sqlite3',
    'pandas',
    'openpyxl',
    'argon2',
    'PIL',
    'PIL.Image',
    'homologador',
    'homologador.core',
    'homologador.data', 
    'homologador.ui'
]

# Análisis del script principal
a = Analysis(
    [main_script],
    pathex=['.'],
    binaries=binaries,
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'numpy.distutils',
        'scipy', 
        'IPython',
        'jupyter',
        'notebook',
        'test',
        'unittest'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Recolección de archivos
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Creación del ejecutable portable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
    distpath='dist_portable',  # Salida en carpeta portable
    workpath='build_portable',
)
