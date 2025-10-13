#!/usr/bin/env python3
"""
🚀 SCRIPT DE COMPILACIÓN - EXPANSION DE DOMINIO - INVENTORIA
Desarrollado por: Antware (SysAdmin)

Este script compila la aplicación usando PyInstaller con configuración optimizada
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Muestra banner de compilación"""
    print("=" * 60)
    print("🌟 EXPANSION DE DOMINIO - INVENTORIA v1.0.0")
    print("📦 COMPILADOR DE APLICACIÓN")
    print("👨‍💻 Desarrollado por: Antware (SysAdmin)")
    print("=" * 60)

def check_dependencies():
    """Verifica que PyInstaller esté instalado"""
    print("🔍 Verificando dependencias...")
    
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller no encontrado")
        print("📥 Instalando PyInstaller...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller instalado exitosamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error instalando PyInstaller")
            return False

def prepare_build_environment():
    """Prepara el entorno de compilación"""
    print("🛠️ Preparando entorno de compilación...")
    
    # Limpiar builds anteriores
    build_dirs = ["build", "dist", "__pycache__"]
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Limpiado: {dir_name}/")
    
    # Crear directorio de distribución
    os.makedirs("dist", exist_ok=True)
    print("📁 Directorio dist/ creado")

def build_application():
    """Compila la aplicación con PyInstaller"""
    print("🔨 Compilando aplicación...")
    
    # Configuración de PyInstaller
    app_name = "EXPANSION_DE_DOMINIO_INVENTORIA"
    icon_path = "images/fondo.png"
    main_script = "homologador/app.py"
    
    # Verificar archivos necesarios
    if not os.path.exists(main_script):
        print(f"❌ Archivo principal no encontrado: {main_script}")
        return False
        
    if not os.path.exists(icon_path):
        print(f"⚠️ Icono no encontrado: {icon_path} (continuando sin icono)")
        icon_path = None
    else:
        print(f"🎨 Usando icono: {icon_path}")
    
    # Comando de PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin consola (GUI)
        "--name", app_name,             # Nombre del ejecutable
        "--distpath", "dist",           # Directorio de salida
        "--workpath", "build",          # Directorio de trabajo
        "--clean",                      # Limpiar cache
        "--noconfirm",                  # No pedir confirmación
    ]
    
    # Añadir icono si existe
    if icon_path:
        cmd.extend(["--icon", icon_path])
    
    # Incluir directorios de datos
    cmd.extend([
        "--add-data", "homologador;homologador",
        "--add-data", "images;images"
    ])
    
    # Ocultar imports opcionales
    cmd.extend([
        "--hidden-import", "PyQt6",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "sqlite3",
        "--hidden-import", "pandas",
        "--hidden-import", "openpyxl"
    ])
    
    # Archivo principal
    cmd.append(main_script)
    
    print(f"🚀 Ejecutando: {' '.join(cmd)}")
    print("⏳ Esto puede tomar varios minutos...")
    
    try:
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Compilación exitosa!")
            return True
        else:
            print("❌ Error en la compilación:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando PyInstaller: {e}")
        return False

def post_build_tasks():
    """Tareas después de la compilación"""
    print("📋 Ejecutando tareas post-compilación...")
    
    # Verificar que el ejecutable se creó
    app_name = "EXPANSION_DE_DOMINIO_INVENTORIA"
    exe_path = f"dist/{app_name}.exe"
    
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"✅ Ejecutable creado: {exe_path}")
        print(f"📏 Tamaño: {size_mb:.1f} MB")
        
        # Crear script de instalación
        create_installer_script(exe_path)
        
        return True
    else:
        print(f"❌ Ejecutable no encontrado: {exe_path}")
        return False

def create_installer_script(exe_path):
    """Crea script de instalación simple"""
    installer_content = f'''@echo off
echo.
echo ===================================================
echo 🌟 EXPANSION DE DOMINIO - INVENTORIA v1.0.0
echo 📦 INSTALADOR AUTOMATICO
echo 👨‍💻 Desarrollado por: Antware (SysAdmin)
echo ===================================================
echo.

set "APP_NAME=EXPANSION_DE_DOMINIO_INVENTORIA"
set "INSTALL_DIR=%USERPROFILE%\\Desktop\\%APP_NAME%"

echo 📁 Creando directorio de instalación...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo 📋 Copiando ejecutable...
copy "{os.path.basename(exe_path)}" "%INSTALL_DIR%\\" >nul

echo 🔗 Creando acceso directo en Desktop...
powershell -Command "$WshShell = New-Object -ComObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\%APP_NAME%.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\{os.path.basename(exe_path)}'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Sistema de Inventario y Homologación - by Antware'; $Shortcut.Save()"

echo.
echo ✅ Instalación completada exitosamente!
echo 🚀 Ejecutable disponible en: %INSTALL_DIR%
echo 🔗 Acceso directo creado en Desktop
echo.
echo Presiona cualquier tecla para continuar...
pause >nul
'''
    
    installer_path = "dist/INSTALAR.bat"
    with open(installer_path, "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print(f"📦 Instalador creado: {installer_path}")

def main():
    """Función principal de compilación"""
    print_banner()
    
    # Verificar entorno
    if not check_dependencies():
        print("❌ No se pudo instalar PyInstaller")
        return False
    
    # Preparar entorno
    prepare_build_environment()
    
    # Compilar aplicación
    if not build_application():
        print("❌ Error en la compilación")
        return False
    
    # Tareas post-compilación
    if not post_build_tasks():
        print("❌ Error en tareas post-compilación")
        return False
    
    print("=" * 60)
    print("🎉 ¡COMPILACIÓN COMPLETADA EXITOSAMENTE!")
    print("📦 Archivos generados en: dist/")
    print("🚀 Ejecutable: dist/EXPANSION_DE_DOMINIO_INVENTORIA.exe")
    print("📋 Instalador: dist/INSTALAR.bat")
    print("👨‍💻 Desarrollado por: Antware (SysAdmin)")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Compilación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)