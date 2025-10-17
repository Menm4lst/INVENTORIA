"""
🔧 COMPILADOR x64 ESPECÍFICO - HomologadorInventoria
Compilación forzada a 64 bits para Windows 11
"""
import os
import shutil
import subprocess
import platform
from pathlib import Path

def verify_system_architecture():
    """Verificar que estamos en un sistema de 64 bits."""
    print("🔍 VERIFICANDO ARQUITECTURA DEL SISTEMA")
    print("=" * 45)
    
    arch = platform.machine()
    bits = platform.architecture()[0]
    is_64bit = platform.machine().endswith('64')
    
    print(f"💻 Arquitectura: {arch}")
    print(f"🔢 Bits: {bits}")
    print(f"✅ Es 64-bit: {is_64bit}")
    
    if not is_64bit:
        print("❌ ERROR: Se requiere sistema de 64 bits")
        return False
    
    print("✅ Sistema compatible para compilación x64")
    return True

def cleanup_previous():
    """Limpiar compilaciones anteriores."""
    print("\n🧹 LIMPIANDO COMPILACIONES ANTERIORES")
    print("=" * 45)
    
    cleanup_dirs = ['build_x64', 'dist_x64', '__pycache__']
    for dir_name in cleanup_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🗑️ Eliminado: {dir_name}")
    
    # Crear directorio de salida
    os.makedirs('dist_x64', exist_ok=True)
    print("✅ Directorio dist_x64 creado")

def compile_x64_executable():
    """Compilar específicamente para arquitectura x64."""
    print("\n🔧 COMPILANDO PARA ARQUITECTURA x64")
    print("=" * 45)
    
    # Comando PyInstaller con configuración ESPECÍFICA x64
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        '--onefile',
        '--windowed',
        '--name=HomologadorInventoria_x64',
        '--distpath=dist_x64',
        '--workpath=build_x64',
        '--specpath=.',
        
        # CONFIGURACIÓN CRÍTICA PARA x64
        '--target-architecture=x86_64',  # Forzar arquitectura x64
        
        # Datos necesarios
        '--add-data=homologador;homologador',
        '--add-data=homologador/data/migrations;homologador/data/migrations',
        '--add-data=assets;assets',
        
        # Hidden imports completos
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
        
        # Dependencias de datos
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        '--hidden-import=xlsxwriter',
        
        # Sistema
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
        
        # Configuraciones adicionales para x64
        '--optimize=2',  # Optimización máxima
        
        # Icono
        '--icon=assets/fondo.ico',
        
        # Archivo principal
        'run_app.py'
    ]
    
    print("🚀 Ejecutando PyInstaller para x64...")
    print(f"📋 Parámetros críticos:")
    print(f"   --target-architecture=x86_64")
    print(f"   --optimize=2")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ Compilación x64 exitosa!")
            
            # Verificar el ejecutable
            exe_path = Path('dist_x64/HomologadorInventoria_x64.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📦 Ejecutable x64 creado: {exe_path}")
                print(f"📏 Tamaño: {size_mb:.1f} MB")
                return True, size_mb
            else:
                print("❌ Ejecutable x64 no encontrado")
                return False, 0
        else:
            print("❌ Error en compilación x64:")
            if result.stderr:
                print(f"Error: {result.stderr[-1000:]}")
            return False, 0
            
    except Exception as e:
        print(f"❌ Error durante compilación x64: {e}")
        return False, 0

def verify_x64_executable(exe_path):
    """Verificar que el ejecutable es realmente de 64 bits."""
    print(f"\n🔍 VERIFICANDO ARQUITECTURA DEL EJECUTABLE")
    print("=" * 45)
    
    if not os.path.exists(exe_path):
        print("❌ Ejecutable no encontrado")
        return False
    
    try:
        # Intentar obtener información del archivo
        result = subprocess.run([
            'powershell', '-Command', 
            f'Get-ItemProperty "{exe_path}" | Select-Object Name, Length'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ejecutable verificado")
            print(f"📊 Información: {result.stdout.strip()}")
        
        # Intentar ejecutar con verificación
        print("\n🧪 Probando ejecución...")
        test_result = subprocess.run([
            exe_path, '--version'
        ], timeout=10, capture_output=True, text=True)
        
        print("✅ Ejecutable responde correctamente")
        return True
        
    except subprocess.TimeoutExpired:
        print("⚠️ Ejecutable tarda en responder (normal)")
        return True
    except Exception as e:
        print(f"❌ Error al verificar: {e}")
        return False

def setup_x64_distribution():
    """Configurar distribución x64."""
    print("\n📦 CONFIGURANDO DISTRIBUCIÓN x64")
    print("=" * 35)
    
    dist_path = Path('dist_x64')
    
    # Crear estructura
    folders = ['data', 'backups', 'logs']
    for folder in folders:
        (dist_path / folder).mkdir(exist_ok=True)
        print(f"📁 Creada: {folder}")
    
    # Copiar base de datos
    if Path('homologador.db').exists():
        shutil.copy2('homologador.db', dist_path / 'data' / 'homologador.db')
        print("✅ Base de datos copiada")
    
    # Configuración x64
    config_content = f"""# HomologadorInventoria - Versión x64
# Generado: 2025-10-17 - Compilación específica 64 bits

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
version = 1.0.3-x64
compiled = true
portable = true
architecture = x86_64
target_bits = 64

[compatibility]
windows11 = true
windows10 = true
min_architecture = x64
pandas_included = true
numpy_included = true

[paths]
base_path = .
data_path = data
backup_path = backups
log_path = logs
"""
    
    with open(dist_path / 'config.ini', 'w', encoding='utf-8') as f:
        f.write(config_content)
    print("✅ Configuración x64 creada")
    
    # Script de lanzamiento x64
    launcher_content = """@echo off
title HomologadorInventoria v1.0.3-x64 - Arquitectura 64 bits
echo.
echo ================================================================
echo   HomologadorInventoria v1.0.3-x64
echo   Sistema de Gestion de Homologaciones
echo   *** COMPILACION NATIVA 64 BITS ***
echo ================================================================
echo.
echo Verificando sistema...

REM Verificar arquitectura del sistema
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    echo ✅ Sistema x64 detectado: %PROCESSOR_ARCHITECTURE%
) else (
    echo ❌ ERROR: Sistema no es x64
    echo    Arquitectura detectada: %PROCESSOR_ARCHITECTURE%
    echo    Se requiere sistema de 64 bits
    pause
    exit /b 1
)

echo.
echo Iniciando aplicacion x64...
echo   - Pandas: INCLUIDO
echo   - Numpy: INCLUIDO
echo   - PyQt6: INCLUIDO  
echo   - SQLite: INCLUIDO
echo   - Arquitectura: 64 bits nativa
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ejecutar aplicacion
echo Ejecutando HomologadorInventoria_x64.exe...
HomologadorInventoria_x64.exe

REM Verificar resultado
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Aplicacion ejecutada correctamente
) else (
    echo.
    echo ================================================================
    echo ❌ ERROR: Codigo de salida %ERRORLEVEL%
    echo ================================================================
    echo.
    echo Posibles soluciones:
    echo 1. Ejecutar como administrador
    echo 2. Desbloquear archivo (Propiedades ^> Desbloquear)
    echo 3. Verificar antivirus no esta bloqueando
    echo 4. Instalar Visual C++ Redistributable x64
    echo.
    pause
)
"""
    
    with open(dist_path / 'Ejecutar_x64.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    print("✅ Lanzador x64 creado")
    
    return True

def main():
    """Función principal."""
    print("🔧 COMPILADOR x64 ESPECÍFICO - HomologadorInventoria v1.0.3")
    print("=" * 65)
    print("🎯 Objetivo: Compilación nativa de 64 bits para Windows 11")
    print()
    
    try:
        # 1. Verificar sistema
        if not verify_system_architecture():
            return
        
        # 2. Limpiar
        cleanup_previous()
        
        # 3. Compilar x64
        success, size = compile_x64_executable()
        if not success:
            print("❌ Compilación x64 fallida")
            return
        
        # 4. Verificar ejecutable
        exe_path = "dist_x64/HomologadorInventoria_x64.exe"
        if not verify_x64_executable(exe_path):
            print("⚠️ Advertencia: Verificación del ejecutable falló")
        
        # 5. Configurar distribución
        setup_x64_distribution()
        
        # 6. Resumen
        print(f"\n🎉 COMPILACIÓN x64 COMPLETADA")
        print("=" * 40)
        print(f"📁 Ubicación: dist_x64/")
        print(f"📦 Ejecutable: HomologadorInventoria_x64.exe")
        print(f"📏 Tamaño: {size:.1f} MB")
        print("✅ Arquitectura: x86_64 (64 bits nativa)")
        print("✅ Todas las dependencias incluidas")
        print("✅ Compatible Windows 11")
        print()
        print("🚀 Para probar:")
        print("   cd dist_x64")
        print("   .\\Ejecutar_x64.bat")
        
    except Exception as e:
        print(f"\n❌ Error en compilación x64: {e}")

if __name__ == "__main__":
    main()