"""
🔧 COMPILADOR FINAL CON TODAS LAS DEPENDENCIAS
Versión corregida incluyendo pandas y numpy para Windows 11
"""
import os
import shutil
import subprocess
from pathlib import Path

def cleanup_and_prepare():
    """Limpiar y preparar para compilación."""
    print("🧹 Limpiando compilaciones anteriores...")
    
    cleanup_dirs = ['build_final', 'dist_final', '__pycache__']
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ Eliminado: {dir_name}")
    
    # Crear directorio de salida
    os.makedirs('dist_final', exist_ok=True)
    print("✅ Directorio de salida creado: dist_final")

def compile_with_all_dependencies():
    """Compilar con todas las dependencias necesarias."""
    print("\n🔧 RECOMPILANDO CON DEPENDENCIAS COMPLETAS")
    print("=" * 50)
    
    # Comando PyInstaller con TODAS las dependencias
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--name=HomologadorInventoria',
        '--distpath=dist_final',
        '--workpath=build_final',
        '--specpath=.',
        
        # Agregar TODOS los datos necesarios
        '--add-data=homologador;homologador',
        '--add-data=homologador/data/migrations;homologador/data/migrations',
        '--add-data=assets;assets',
        
        # Hidden imports COMPLETOS - incluir PANDAS y NUMPY
        '--hidden-import=homologador.core',
        '--hidden-import=homologador.core.settings',
        '--hidden-import=homologador.core.storage',
        '--hidden-import=homologador.core.portable',
        '--hidden-import=homologador.core.export',
        '--hidden-import=homologador.core.audit',
        '--hidden-import=homologador.app',
        '--hidden-import=homologador.ui.main_window',
        '--hidden-import=homologador.ui.dashboard_advanced',
        '--hidden-import=homologador.ui.details_view',
        '--hidden-import=homologador.ui.homologation_form',
        '--hidden-import=homologador.ui.final_login',
        '--hidden-import=homologador.ui.filter_widget',
        '--hidden-import=homologador.ui.theme',
        '--hidden-import=homologador.ui.autosave_manager',
        '--hidden-import=homologador.ui.icons',
        '--hidden-import=homologador.ui.notifications',
        '--hidden-import=homologador.ui.theme_effects',
        '--hidden-import=homologador.data.seed',
        
        # PyQt6 específico
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.sip',
        
        # PANDAS Y NUMPY - CRÍTICOS PARA EXPORTACIÓN
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        '--hidden-import=xlsxwriter',
        
        # Dependencias adicionales
        '--hidden-import=sqlite3',
        '--hidden-import=json',
        '--hidden-import=pathlib',
        '--hidden-import=configparser',
        '--hidden-import=logging',
        '--hidden-import=datetime',
        '--hidden-import=shutil',
        '--hidden-import=tempfile',
        '--hidden-import=threading',
        '--hidden-import=queue',
        
        # Configuraciones específicas para Windows 11
        '--target-arch=x86_64',
        
        # Icono
        '--icon=assets/fondo.ico',
        
        # Archivo principal
        'run_app.py'
    ]
    
    print("🚀 Ejecutando PyInstaller con dependencias completas...")
    print(f"📋 Comando: {' '.join(cmd[:8])}... (+{len(cmd)-8} parámetros más)")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Compilación exitosa!")
            
            # Verificar el ejecutable
            exe_path = Path('dist_final/HomologadorInventoria.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📦 Ejecutable creado: {exe_path}")
                print(f"📏 Tamaño: {size_mb:.1f} MB")
                return True, size_mb
            else:
                print("❌ Ejecutable no encontrado después de la compilación")
                return False, 0
        else:
            print("❌ Error en la compilación:")
            if result.stdout:
                print(f"Salida: {result.stdout[-500:]}")
            if result.stderr:
                print(f"Error: {result.stderr[-500:]}")
            return False, 0
            
    except Exception as e:
        print(f"❌ Error durante la compilación: {e}")
        return False, 0

def setup_final_distribution():
    """Configurar la distribución final con todos los archivos."""
    print("\n📦 CONFIGURANDO DISTRIBUCIÓN FINAL")
    print("=" * 40)
    
    dist_path = Path('dist_final')
    
    # Crear estructura de carpetas
    folders = ['data', 'backups', 'logs']
    for folder in folders:
        (dist_path / folder).mkdir(exist_ok=True)
        print(f"📁 Creada carpeta: {folder}")
    
    # Copiar base de datos
    if Path('homologador.db').exists():
        shutil.copy2('homologador.db', dist_path / 'data' / 'homologador.db')
        print("✅ Base de datos copiada")
    
    # Crear configuración final
    config_content = f"""# Configuración HomologadorInventoria - Versión Final Windows 11
# Generado: 2025-10-17 con todas las dependencias

[database]
path = data/homologador.db
backup_path = backups/
auto_backup = true

[logging]
level = INFO
file = logs/homologador.log
max_size = 10MB
backup_count = 5

[application]
name = HomologadorInventoria
version = 1.0.2-final
compiled = true
portable = true
windows11_compatible = true
pandas_included = true
numpy_included = true

[paths]
base_path = .
data_path = data
backup_path = backups
log_path = logs

[features]
export_excel = true
dashboard_advanced = true
copy_clipboard = true
all_dependencies = true
"""
    
    with open(dist_path / 'config.ini', 'w', encoding='utf-8') as f:
        f.write(config_content)
    print("✅ Configuración final creada")
    
    # Crear script de lanzamiento final
    launcher_content = """@echo off
title HomologadorInventoria v1.0.2-final - Windows 11 Compatible
echo.
echo ========================================================
echo   HomologadorInventoria v1.0.2-final
echo   Sistema de Gestion de Homologaciones
echo   *** TODAS LAS DEPENDENCIAS INCLUIDAS ***
echo ========================================================
echo.
echo Iniciando aplicacion final...
echo   - Pandas: INCLUIDO
echo   - Numpy: INCLUIDO  
echo   - PyQt6: INCLUIDO
echo   - SQLite: INCLUIDO
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar Windows
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo Sistema detectado: Windows %VERSION%

REM Ejecutar la aplicacion
echo.
echo Ejecutando HomologadorInventoria...
HomologadorInventoria.exe

REM Verificar resultado
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Aplicacion cerrada correctamente.
) else (
    echo.
    echo ============================================
    echo ERROR: Codigo de salida %ERRORLEVEL%
    echo ============================================
    echo.
    echo Si persisten problemas:
    echo 1. Ejecutar como administrador
    echo 2. Desbloquear archivo (Propiedades)
    echo 3. Verificar antivirus
    echo.
    pause
)
"""
    
    with open(dist_path / 'Ejecutar_Final.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    print("✅ Script de lanzamiento final creado")
    
    return True

def main():
    """Función principal de recompilación."""
    print("🔧 RECOMPILADOR FINAL - HomologadorInventoria v1.0.2")
    print("=" * 60)
    print("🎯 Objetivo: Incluir TODAS las dependencias (pandas, numpy, etc.)")
    print()
    
    try:
        # 1. Limpiar y preparar
        cleanup_and_prepare()
        
        # 2. Compilar con todas las dependencias
        success, size = compile_with_all_dependencies()
        if not success:
            print("❌ Compilación fallida")
            return
        
        # 3. Configurar distribución
        setup_final_distribution()
        
        # 4. Resumen final
        print(f"\n🎉 RECOMPILACIÓN COMPLETADA")
        print("=" * 40)
        print(f"📁 Ubicación: dist_final/")
        print(f"📏 Tamaño ejecutable: {size:.1f} MB")
        print("✅ Pandas incluido")
        print("✅ Numpy incluido")
        print("✅ Todas las dependencias incluidas")
        print("✅ Compatible Windows 11")
        print()
        print("🚀 Para probar:")
        print("   cd dist_final")
        print("   .\\Ejecutar_Final.bat")
        
    except Exception as e:
        print(f"\n❌ Error durante la recompilación: {e}")

if __name__ == "__main__":
    main()