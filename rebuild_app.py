#!/usr/bin/env python3
"""
🚀 SCRIPT DE RECOMPILACIÓN CORREGIDO - EXPANSION DE DOMINIO - INVENTORIA
Desarrollado por: Antware (SysAdmin)

Este script recompila la aplicación con imports corregidos
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_banner():
    """Muestra banner de recompilación"""
    print("=" * 60)
    print("🔧 RECOMPILACIÓN CORREGIDA - EXPANSION DE DOMINIO - INVENTORIA")
    print("📦 CORRECCIÓN DE IMPORTS PARA PYINSTALLER")
    print("👨‍💻 Desarrollado por: Antware (SysAdmin)")
    print("=" * 60)

def clean_previous_build():
    """Limpia compilaciones anteriores"""
    print("🧹 Limpiando compilaciones anteriores...")
    
    # Limpiar builds anteriores
    build_dirs = ["build", "dist", "__pycache__"]
    for dir_name in build_dirs:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ Limpiado: {dir_name}/")
            except PermissionError:
                print(f"⚠️ No se pudo limpiar {dir_name}/ (permisos)")
    
    # Eliminar archivos .spec anteriores
    for spec_file in Path('.').glob('*.spec'):
        try:
            spec_file.unlink()
            print(f"🗑️ Eliminado: {spec_file}")
        except:
            pass

def test_imports():
    """Prueba que todos los imports funcionen"""
    print("🔍 Probando imports corregidos...")
    
    try:
        # Test de import principal
        sys.path.insert(0, os.getcwd())
        
        # Importar módulos críticos
        from homologador.core.settings import get_settings
        from homologador.core.storage import get_database_manager
        from homologador.ui.main_window import MainWindow
        
        print("✅ Imports principales: OK")
        return True
        
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        return False

def build_application():
    """Compila la aplicación con configuración corregida"""
    print("🔨 Compilando con imports corregidos...")
    
    # Configuración de PyInstaller corregida
    app_name = "EXPANSION_DE_DOMINIO_INVENTORIA"
    icon_path = "images/fondo.png"
    main_script = "homologador/app.py"
    
    # Comando de PyInstaller optimizado
    cmd = [
        "pyinstaller",
        "--onefile",                    # Un solo archivo ejecutable
        "--windowed",                   # Sin consola (GUI)
        "--name", app_name,             # Nombre del ejecutable
        "--distpath", "dist",           # Directorio de salida
        "--workpath", "build",          # Directorio de trabajo
        "--clean",                      # Limpiar cache
        "--noconfirm",                  # No pedir confirmación
        "--icon", icon_path,            # Icono de la aplicación
    ]
    
    # Incluir paquetes completos (método más seguro)
    cmd.extend([
        "--collect-all", "homologador",
        "--collect-data", "homologador",
        "--recursive-copy-metadata", "PyQt6"
    ])
    
    # Ocultar imports críticos
    critical_imports = [
        "PyQt6",
        "PyQt6.QtCore", 
        "PyQt6.QtWidgets",
        "PyQt6.QtGui",
        "sqlite3",
        "pandas",
        "openpyxl",
        "argon2",
        "homologador",
        "homologador.core",
        "homologador.data", 
        "homologador.ui"
    ]
    
    for imp in critical_imports:
        cmd.extend(["--hidden-import", imp])
    
    # Excluir módulos innecesarios
    exclude_modules = [
        "tkinter",
        "matplotlib",
        "numpy.distutils",
        "scipy", 
        "IPython",
        "jupyter",
        "notebook",
        "test"
    ]
    
    for exc in exclude_modules:
        cmd.extend(["--exclude-module", exc])
    
    # Archivo principal
    cmd.append(main_script)
    
    print(f"🚀 Comando: pyinstaller [opciones] {main_script}")
    print("⏳ Esto puede tomar varios minutos...")
    
    try:
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, capture_output=False, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Recompilación exitosa!")
            return True
        else:
            print("❌ Error en la recompilación")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando PyInstaller: {e}")
        return False

def verify_build():
    """Verifica que el ejecutable se creó correctamente"""
    print("📋 Verificando compilación...")
    
    app_name = "EXPANSION_DE_DOMINIO_INVENTORIA"
    exe_path = f"dist/{app_name}.exe"
    
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"✅ Ejecutable creado: {exe_path}")
        print(f"📏 Tamaño: {size_mb:.1f} MB")
        return True
    else:
        print(f"❌ Ejecutable no encontrado: {exe_path}")
        return False

def main():
    """Función principal de recompilación"""
    print_banner()
    
    # Limpiar compilación anterior
    clean_previous_build()
    
    # Probar imports
    if not test_imports():
        print("❌ Error en imports - revise las correcciones")
        return False
    
    # Compilar aplicación
    if not build_application():
        print("❌ Error en la compilación")
        return False
    
    # Verificar build
    if not verify_build():
        print("❌ Error verificando el build")
        return False
    
    print("=" * 60)
    print("🎉 ¡RECOMPILACIÓN COMPLETADA EXITOSAMENTE!")
    print("📦 Archivos generados en: dist/")
    print("🚀 Ejecutable: dist/EXPANSION_DE_DOMINIO_INVENTORIA.exe")
    print("👨‍💻 Desarrollado por: Antware (SysAdmin)")
    print("✅ Imports corregidos para PyInstaller")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Recompilación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)