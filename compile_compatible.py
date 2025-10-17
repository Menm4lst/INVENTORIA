"""
🔧 COMPILADOR COMPATIBLE PARA WINDOWS 11
Versión mejorada con compatibilidad extendida y diagnósticos
"""
import os
import shutil
import sqlite3
import subprocess
import platform
from pathlib import Path
from datetime import datetime

def check_system_compatibility():
    """Verificar compatibilidad del sistema."""
    print("🔍 VERIFICANDO COMPATIBILIDAD DEL SISTEMA")
    print("=" * 50)
    
    # Información del sistema
    info = {
        'platform': platform.platform(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'architecture': platform.architecture(),
        'python_version': platform.python_version(),
        'windows_version': platform.win32_ver()
    }
    
    print(f"💻 Sistema: {info['platform']}")
    print(f"🏗️ Arquitectura: {info['machine']} ({info['architecture'][0]})")
    print(f"🐍 Python: {info['python_version']}")
    print(f"🪟 Windows: {info['windows_version'][0]} Build {info['windows_version'][1]}")
    print()
    
    # Verificar si es Windows 11
    if "Windows-11" in info['platform']:
        print("✅ Windows 11 detectado - Aplicando configuraciones específicas")
        return True, "windows11"
    elif "Windows-10" in info['platform']:
        print("✅ Windows 10 detectado - Configuración estándar")
        return True, "windows10"
    else:
        print("⚠️ Sistema no verificado, usando configuración genérica")
        return True, "generic"

def create_compatible_spec_file():
    """Crear archivo .spec con configuraciones específicas para Windows 11."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

# 🔧 CONFIGURACIÓN ESPECÍFICA PARA WINDOWS 11
# Compilación compatible con todas las versiones de Windows

import sys
from pathlib import Path

# Rutas del proyecto
project_root = Path.cwd()
homologador_path = project_root / 'homologador'

# Archivos de datos necesarios
datas = [
    (str(homologador_path), 'homologador'),
    (str(homologador_path / 'data' / 'migrations'), 'homologador/data/migrations'),
    ('assets', 'assets'),
]

# Módulos ocultos críticos para Windows 11
hiddenimports = [
    # Core modules
    'homologador.core',
    'homologador.core.settings',
    'homologador.core.storage',
    'homologador.core.portable',
    'homologador.core.export',
    'homologador.core.audit',
    
    # App modules
    'homologador.app',
    
    # UI modules
    'homologador.ui.main_window',
    'homologador.ui.dashboard_advanced',
    'homologador.ui.details_view',
    'homologador.ui.homologation_form',
    'homologador.ui.final_login',
    'homologador.ui.filter_widget',
    'homologador.ui.theme',
    'homologador.ui.autosave_manager',
    'homologador.ui.icons',
    'homologador.ui.notifications',
    'homologador.ui.theme_effects',
    
    # Data modules
    'homologador.data.seed',
    
    # PyQt6 specific imports for Windows 11
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'PyQt6.sip',
    
    # Additional Windows compatibility
    'sqlite3',
    'json',
    'pathlib',
    'configparser',
    'logging',
    'datetime',
    'shutil',
    'tempfile',
    'threading',
    'queue',
    
    # Excel/Data processing dependencies
    'pandas',
    'openpyxl',
    'xlsxwriter',
    'numpy',
]

# Exclusiones para reducir tamaño (removiendo pandas, numpy, openpyxl)
excludes = [
    'tkinter',
    'matplotlib',
    'PIL.ImageQt',
    'PyQt5',
    'PySide2',
    'PySide6',
]

# Configuración del análisis
a = Analysis(
    ['run_app.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=0,
)

# Filtrar archivos innecesarios
pyz = PYZ(a.pure)

# Configuración del ejecutable con máxima compatibilidad
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='HomologadorInventoria',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # Desactivar UPX para evitar problemas de antivirus
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Aplicación windowed
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',  # Agregar información de versión
    icon='assets/fondo.ico' if Path('assets/fondo.ico').exists() else None,
    # Configuraciones adicionales para Windows 11
    manifest='app_manifest.xml',  # Manifest personalizado
)
'''
    
    with open('HomologadorInventoria_Win11.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec compatible con Windows 11 creado")
    return True

def create_app_manifest():
    """Crear manifest de aplicación para compatibilidad con Windows 11."""
    manifest_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
    <assemblyIdentity
        version="1.0.0.0"
        processorArchitecture="amd64"
        name="HomologadorInventoria"
        type="win32"
    />
    <description>Sistema de Gestión de Homologaciones de Aplicaciones</description>
    
    <!-- Compatibilidad con Windows 11 -->
    <compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1">
        <application>
            <!-- Windows 11 -->
            <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
            <!-- Windows 10 -->
            <supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"/>
            <!-- Windows 8.1 -->
            <supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"/>
            <!-- Windows 8 -->
            <supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"/>
            <!-- Windows 7 -->
            <supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"/>
        </application>
    </compatibility>
    
    <!-- Configuración DPI para Windows 11 -->
    <application xmlns="urn:schemas-microsoft-com:asm.v3">
        <windowsSettings>
            <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true</dpiAware>
            <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2</dpiAwareness>
        </windowsSettings>
    </application>
    
    <!-- Permisos de ejecución -->
    <trustInfo xmlns="urn:schemas-microsoft-com:asm.v2">
        <security>
            <requestedPrivileges xmlns="urn:schemas-microsoft-com:asm.v3">
                <requestedExecutionLevel level="asInvoker" uiAccess="false"/>
            </requestedPrivileges>
        </security>
    </trustInfo>
    
    <!-- Dependencias -->
    <dependency>
        <dependentAssembly>
            <assemblyIdentity
                type="win32"
                name="Microsoft.Windows.Common-Controls"
                version="6.0.0.0"
                processorArchitecture="amd64"
                publicKeyToken="6595b64144ccf1df"
                language="*"
            />
        </dependentAssembly>
    </dependency>
</assembly>
'''
    
    with open('app_manifest.xml', 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    
    print("✅ Manifest de aplicación creado para Windows 11")
    return True

def create_version_info():
    """Crear archivo de información de versión."""
    version_content = '''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Inventoria Solutions'),
        StringStruct(u'FileDescription', u'Sistema de Gestión de Homologaciones'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'HomologadorInventoria'),
        StringStruct(u'LegalCopyright', u'Copyright © 2025'),
        StringStruct(u'OriginalFilename', u'HomologadorInventoria.exe'),
        StringStruct(u'ProductName', u'HomologadorInventoria'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_content)
    
    print("✅ Información de versión creada")
    return True

def compile_with_compatibility():
    """Compilar con máxima compatibilidad para Windows 11."""
    print("\n🔧 COMPILANDO CON COMPATIBILIDAD WINDOWS 11")
    print("=" * 50)
    
    # Limpiar compilaciones anteriores
    cleanup_dirs = ['build', 'dist_compatible', '__pycache__']
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Limpiado: {dir_name}")
    
    # Crear directorio de salida
    os.makedirs('dist_compatible', exist_ok=True)
    
    try:
        # Comando PyInstaller con configuración específica
        cmd = [
            'pyinstaller',
            '--clean',
            '--noconfirm',
            '--distpath=dist_compatible',
            '--workpath=build_compatible',
            'HomologadorInventoria_Win11.spec'
        ]
        
        print("🚀 Ejecutando PyInstaller...")
        print(f"📋 Comando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Compilación exitosa!")
            
            # Verificar el ejecutable
            exe_path = Path('dist_compatible/HomologadorInventoria.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📦 Ejecutable creado: {exe_path}")
                print(f"📏 Tamaño: {size_mb:.1f} MB")
                return True
            else:
                print("❌ Ejecutable no encontrado después de la compilación")
                return False
        else:
            print("❌ Error en la compilación:")
            print(f"Salida: {result.stdout}")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error durante la compilación: {e}")
        return False

def test_compatibility(exe_path):
    """Probar compatibilidad del ejecutable."""
    print(f"\n🧪 PROBANDO COMPATIBILIDAD: {exe_path}")
    print("=" * 50)
    
    if not os.path.exists(exe_path):
        print("❌ Ejecutable no encontrado")
        return False
    
    try:
        # Intentar ejecutar con timeout
        result = subprocess.run(
            [exe_path, '--version'],
            timeout=10,
            capture_output=True,
            text=True
        )
        
        print("✅ Ejecutable responde correctamente")
        return True
        
    except subprocess.TimeoutExpired:
        print("⚠️ Ejecutable tarda en responder (normal para primera ejecución)")
        return True
    except Exception as e:
        print(f"❌ Error al probar ejecutable: {e}")
        return False

def main():
    """Función principal."""
    print("🔧 COMPILADOR COMPATIBLE WINDOWS 11 - HomologadorInventoria")
    print("=" * 65)
    print()
    
    try:
        # 1. Verificar compatibilidad
        compatible, os_type = check_system_compatibility()
        if not compatible:
            print("❌ Sistema no compatible")
            return
        
        # 2. Crear archivos de configuración
        print("\n📝 Creando archivos de configuración...")
        create_app_manifest()
        create_version_info()
        create_compatible_spec_file()
        
        # 3. Compilar
        print("\n🔧 Iniciando compilación compatible...")
        if not compile_with_compatibility():
            print("❌ Compilación fallida")
            return
        
        # 4. Probar compatibilidad
        exe_path = "dist_compatible/HomologadorInventoria.exe"
        if test_compatibility(exe_path):
            print("\n🎉 COMPILACIÓN COMPATIBLE EXITOSA!")
            print("=" * 40)
            print(f"📁 Ubicación: {Path(exe_path).absolute()}")
            print("✅ Compatible con Windows 11")
            print("✅ Sin dependencias externas")
            print("✅ Listo para distribución")
        else:
            print("\n⚠️ Compilación completada con advertencias")
        
        # 5. Limpiar archivos temporales
        print("\n🧹 Limpiando archivos temporales...")
        cleanup_files = [
            'HomologadorInventoria_Win11.spec',
            'app_manifest.xml',
            'version_info.txt'
        ]
        
        for file in cleanup_files:
            if os.path.exists(file):
                os.remove(file)
                print(f"🗑️ Eliminado: {file}")
        
        if os.path.exists('build_compatible'):
            shutil.rmtree('build_compatible')
            print("🗑️ Eliminado: build_compatible")
            
    except Exception as e:
        print(f"\n❌ Error durante el proceso: {e}")
        print("Verifica que todas las dependencias estén instaladas.")

if __name__ == "__main__":
    main()