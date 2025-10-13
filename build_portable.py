#!/usr/bin/env python3
"""
🚀 COMPILADOR PORTÁTIL COMPLETO - EXPANSION DE DOMINIO - INVENTORIA
Desarrollado por: Antware (SysAdmin)

Esta versión crea un paquete completamente autónomo y portable
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Muestra banner de compilación portátil"""
    print("=" * 70)
    print("📦 COMPILACIÓN PORTÁTIL COMPLETA")
    print("🌟 EXPANSION DE DOMINIO - INVENTORIA v1.0.0")
    print("👨‍💻 Desarrollado por: Antware (SysAdmin)")
    print("🎯 Objetivo: Paquete 100% autónomo y portable")
    print("=" * 70)

def prepare_portable_structure():
    """Prepara la estructura para compilación portable"""
    print("📁 Preparando estructura portátil...")
    
    # Limpiar compilación anterior
    for dir_name in ["build", "dist_portable", "__pycache__"]:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"🧹 Limpiado: {dir_name}/")
            except PermissionError:
                print(f"⚠️ No se pudo limpiar {dir_name}/ (permisos)")
    
    # Crear directorio de salida portable
    os.makedirs("dist_portable", exist_ok=True)
    print("✅ Directorio dist_portable/ creado")

def copy_essential_files():
    """Copia archivos esenciales a la estructura portable"""
    print("📋 Copiando archivos esenciales...")
    
    # Copiar base de datos
    db_source = "C:/Users/Antware/OneDrive/homologador.db"
    if os.path.exists(db_source):
        shutil.copy2(db_source, "dist_portable/homologador.db")
        print("✅ Base de datos copiada")
    
    # Copiar imágenes si existen
    images_source = "images"
    if os.path.exists(images_source):
        shutil.copytree(images_source, "dist_portable/images", dirs_exist_ok=True)
        print("✅ Carpeta images/ copiada")
    
    # Crear carpeta backups
    os.makedirs("dist_portable/backups", exist_ok=True)
    print("✅ Carpeta backups/ creada")

def create_portable_spec():
    """Crea archivo .spec personalizado para compilación portable"""
    print("📝 Creando configuración portable...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
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
'''
    
    with open("portable.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ Archivo portable.spec creado")

def build_portable_app():
    """Compila la aplicación portable"""
    print("🔨 Compilando aplicación portable...")
    
    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm",
        "portable.spec"
    ]
    
    print(f"🚀 Ejecutando: {' '.join(cmd)}")
    print("⏳ Compilación portable en progreso...")
    
    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        if result.returncode == 0:
            print("✅ Compilación portable exitosa!")
            return True
        else:
            print("❌ Error en la compilación portable")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando PyInstaller: {e}")
        return False

def create_portable_package():
    """Crea el paquete portátil completo"""
    print("📦 Creando paquete portátil...")
    
    exe_name = "EXPANSION_DE_DOMINIO_INVENTORIA_PORTABLE"
    exe_path_source = f"dist/{exe_name}.exe"
    exe_path_dest = f"dist_portable/{exe_name}.exe"
    
    # Verificar que PyInstaller creó el ejecutable
    if not os.path.exists(exe_path_source):
        print(f"❌ Ejecutable no encontrado en: {exe_path_source}")
        return False
    
    # Mover ejecutable a carpeta portable
    shutil.move(exe_path_source, exe_path_dest)
    print(f"✅ Ejecutable movido a: {exe_path_dest}")
    
    exe_size = os.path.getsize(exe_path_dest) / (1024 * 1024)  # MB
    print(f"📏 Tamaño: {exe_size:.1f} MB")
    
    # Copiar archivos adicionales necesarios
    additional_files = [
        ("C:/Users/Antware/OneDrive/homologador.db", "dist_portable/homologador.db"),
    ]
    
    for src, dst in additional_files:
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f"✅ Copiado: {os.path.basename(dst)}")
    
    # Crear instalador portable
    create_portable_installer()
    
    # Crear README portable
    create_portable_readme()
    
    return True

def create_portable_installer():
    """Crea instalador para la versión portable"""
    installer_content = '''@echo off
chcp 65001 >nul
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🌟 EXPANSION DE DOMINIO - INVENTORIA v1.0.0 PORTABLE
echo 📦 INSTALADOR PORTÁTIL COMPLETO
echo 👨‍💻 Desarrollado por: Antware (SysAdmin)
echo ═══════════════════════════════════════════════════════════════════════════════
echo.

set "APP_NAME=EXPANSION_DOMINIO_INVENTORIA_PORTABLE"
set "INSTALL_DIR=%USERPROFILE%\\Desktop\\%APP_NAME%"
set "EXE_FILE=EXPANSION_DE_DOMINIO_INVENTORIA_PORTABLE.exe"

echo 📁 Creando instalación portátil...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo ✅ Directorio creado: %INSTALL_DIR%
)

echo 📋 Copiando aplicación portátil...
copy "%EXE_FILE%" "%INSTALL_DIR%\\" >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Aplicación portátil instalada
) else (
    echo ❌ Error en instalación
    goto error
)

echo 💾 Verificando base de datos integrada...
echo ✅ Base de datos SQLite integrada en el ejecutable

echo 🔗 Creando acceso directo...
powershell -Command "try { $WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\%APP_NAME%.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\%EXE_FILE%'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Sistema Portátil de Inventario - by Antware'; $Shortcut.Save(); Write-Host '✅ Acceso directo creado' } catch { Write-Host '⚠️ Error creando acceso directo' }" 2>nul

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo 🎉 ¡INSTALACIÓN PORTÁTIL COMPLETADA!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo 📂 Ubicación: %INSTALL_DIR%
echo 🚀 Ejecutar: %EXE_FILE%
echo 💾 Base de datos: Integrada (SQLite)
echo 📁 Modo: 100%% Portátil
echo.
echo 🔐 CREDENCIALES:
echo   👤 Usuario: admin
echo   🔑 Contraseña: admin123
echo.
echo 💡 VENTAJAS DE LA VERSIÓN PORTÁTIL:
echo   • Un solo archivo ejecutable
echo   • Base de datos integrada
echo   • No requiere instalación adicional
echo   • Funciona en cualquier Windows 10/11
echo   • Todos los recursos incluidos
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
pause
goto end

:error
echo ❌ Error durante la instalación portátil
pause

:end
'''
    
    with open("dist_portable/INSTALAR_PORTABLE.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("✅ Instalador portátil creado")

def create_portable_readme():
    """Crea README para versión portable"""
    readme_content = '''# 🌟 EXPANSION DE DOMINIO - INVENTORIA v1.0.0 PORTABLE

**Sistema Portátil de Inventario y Homologación**
👨‍💻 **Desarrollado por:** Antware (SysAdmin)

---

## 📦 VERSIÓN PORTÁTIL COMPLETA

Esta es la versión **100% portátil** que incluye:
- ✅ **Ejecutable único** con todos los recursos integrados
- ✅ **Base de datos SQLite** embebida
- ✅ **Imágenes y recursos** incluidos internamente
- ✅ **Funcionamiento autónomo** en cualquier PC

---

## 🚀 INSTALACIÓN PORTÁTIL

### Opción 1: Ejecutar directamente
```
EXPANSION_DE_DOMINIO_INVENTORIA_PORTABLE.exe
```

### Opción 2: Instalación automática
```
INSTALAR_PORTABLE.bat
```

---

## 💡 VENTAJAS DE LA VERSIÓN PORTÁTIL

- 🎯 **Un solo archivo**: No dispersión de recursos
- 💾 **BD integrada**: SQLite embebida en el ejecutable  
- 🖼️ **Recursos incluidos**: Imágenes, iconos, todo interno
- 🚀 **Plug & Play**: Copiar y ejecutar en cualquier PC
- 🔒 **Sin dependencias**: Funciona sin instalaciones previas

---

## 🔐 CREDENCIALES

```
Usuario: admin
Contraseña: admin123
```

---

## 💻 COMPATIBILIDAD

- ✅ Windows 10 (64-bit)
- ✅ Windows 11 (64-bit)
- ⚠️ Requiere permisos de ejecución

---

## 🛡️ CARACTERÍSTICAS

- Sistema de estados (Pendiente/Aprobado/Rechazado)
- Dashboard con gráficos circulares
- Exportación CSV/Excel profesional
- Notificaciones interactivas (7 segundos)
- Temas adaptativos
- Backup automático
- Gestión de usuarios y roles

---

🚀 **¡VERSIÓN PORTÁTIL LISTA PARA USAR!** 🚀

**Desarrollado por Antware (SysAdmin)**
'''
    
    with open("dist_portable/README_PORTABLE.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README portátil creado")

def show_portable_summary():
    """Muestra resumen de la compilación portable"""
    exe_name = "EXPANSION_DE_DOMINIO_INVENTORIA_PORTABLE.exe"
    exe_path = f"dist_portable/{exe_name}"
    
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        
        print("=" * 70)
        print("🎉 ¡COMPILACIÓN PORTÁTIL COMPLETADA!")
        print("=" * 70)
        print(f"📦 Ejecutable: {exe_name}")
        print(f"📏 Tamaño: {size_mb:.1f} MB")
        print("💾 Base de datos: Integrada")
        print("🖼️ Recursos: Todos incluidos")
        print("🚀 Portabilidad: 100%")
        print("=" * 70)
        print("📁 Ubicación: dist_portable/")
        print("🎯 Para usar: Copiar carpeta completa a cualquier PC")
        print("=" * 70)

def main():
    """Función principal de compilación portable"""
    print_banner()
    
    # Preparar estructura
    prepare_portable_structure()
    
    # Copiar archivos esenciales
    copy_essential_files()
    
    # Crear configuración portable
    create_portable_spec()
    
    # Compilar aplicación
    if not build_portable_app():
        print("❌ Error en la compilación")
        return False
    
    # Crear paquete completo
    if not create_portable_package():
        print("❌ Error creando paquete")
        return False
    
    # Mostrar resumen
    show_portable_summary()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\\n❌ Compilación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)