"""
Script para compilar la aplicación HomologadorInventoria
Centraliza todos los archivos necesarios en una carpeta de distribución.
"""
import os
import shutil
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime

def create_distribution_folder():
    """Crear carpeta de distribución limpia."""
    dist_path = Path("dist_homologador")
    
    # Limpiar carpeta si existe
    if dist_path.exists():
        shutil.rmtree(dist_path)
    
    # Crear estructura de carpetas
    dist_path.mkdir()
    (dist_path / "data").mkdir()
    (dist_path / "backups").mkdir()
    (dist_path / "logs").mkdir()
    
    return dist_path

def prepare_database(dist_path):
    """Preparar base de datos para distribución."""
    source_db = Path("homologador.db")
    target_db = dist_path / "data" / "homologador.db"
    
    if source_db.exists():
        # Copiar base de datos existente
        shutil.copy2(source_db, target_db)
        print(f"✓ Base de datos copiada a: {target_db}")
    else:
        # Crear base de datos nueva
        print("Creando nueva base de datos...")
        conn = sqlite3.connect(target_db)
        
        # Ejecutar schema
        schema_file = Path("homologador/data/schema.sql")
        if schema_file.exists():
            with open(schema_file, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        
        # Ejecutar migraciones
        migrations_dir = Path("homologador/data/migrations")
        if migrations_dir.exists():
            for migration_file in migrations_dir.glob("*.sql"):
                try:
                    with open(migration_file, 'r', encoding='utf-8') as f:
                        conn.executescript(f.read())
                    print(f"✓ Migración aplicada: {migration_file.name}")
                except Exception as e:
                    print(f"⚠ Error en migración {migration_file.name}: {e}")
        
        conn.close()
        print(f"✓ Nueva base de datos creada en: {target_db}")

def copy_essential_files(dist_path):
    """Copiar archivos esenciales para la distribución."""
    essential_files = [
        "README.md",
        "requirements.txt",
        "LICENSE",
    ]
    
    for file_name in essential_files:
        source_file = Path(file_name)
        if source_file.exists():
            shutil.copy2(source_file, dist_path / file_name)
            print(f"✓ Archivo copiado: {file_name}")

def create_config_file(dist_path):
    """Crear archivo de configuración para la distribución."""
    config_content = f"""# Configuración de HomologadorInventoria - Versión Compilada
# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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
version = 1.0.0
compiled = true
portable = true

[paths]
base_path = .
data_path = data
backup_path = backups
log_path = logs
"""
    
    config_file = dist_path / "config.ini"
    with open(config_file, 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    print(f"✓ Archivo de configuración creado: {config_file}")

def compile_application():
    """Compilar la aplicación usando PyInstaller."""
    print("Compilando aplicación...")
    
    # Comando PyInstaller con configuración específica
    cmd = [
        "pyinstaller",
        "--clean",
        "--noconfirm", 
        "--onefile",
        "--windowed",
        "--name=HomologadorInventoria",
        "--distpath=dist_homologador",
        "--workpath=build_temp",
        "--specpath=.",
        # Agregar explícitamente los paths (corregidos)
        "--add-data=homologador;homologador",
        "--add-data=homologador/data/migrations;homologador/data/migrations",
        # Hidden imports críticos (corregidos)
        "--hidden-import=homologador.core",
        "--hidden-import=homologador.core.settings",
        "--hidden-import=homologador.core.storage", 
        "--hidden-import=homologador.core.portable",
        "--hidden-import=homologador.core.export",
        "--hidden-import=homologador.core.audit",
        "--hidden-import=homologador.app",
        "--hidden-import=homologador.ui.main_window",
        "--hidden-import=homologador.ui.dashboard_advanced",
        "--hidden-import=homologador.ui.details_view", 
        "--hidden-import=homologador.ui.homologation_form",
        "--hidden-import=homologador.ui.final_login",
        "--hidden-import=homologador.ui.filter_widget",
        "--hidden-import=homologador.ui.theme",
        "--hidden-import=homologador.ui.autosave_manager",
        "--hidden-import=homologador.data.seed",
        "run_app.py"
    ]
    
    # Agregar icono si existe
    icon_path = Path("assets/icon.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
        print(f"✓ Usando icono: {icon_path}")
    else:
        print("⚠ No se encontró icono, usando icono por defecto")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✓ Compilación exitosa")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error en compilación: {e}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def create_launcher_script(dist_path):
    """Crear script de lanzamiento."""
    launcher_content = """@echo off
title HomologadorInventoria - Sistema de Gestión
echo.
echo ======================================
echo   HomologadorInventoria v1.0.0
echo   Sistema de Gestión de Homologaciones
echo ======================================
echo.
echo Iniciando aplicación...
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Ejecutar la aplicación
HomologadorInventoria.exe

REM Pausa si hay error
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error al ejecutar la aplicación. Código: %ERRORLEVEL%
    pause
)
"""
    
    launcher_file = dist_path / "Ejecutar_Homologador.bat"
    with open(launcher_file, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"✓ Script de lanzamiento creado: {launcher_file}")

def create_readme_dist(dist_path):
    """Crear README para la distribución."""
    readme_content = """# HomologadorInventoria - Versión Compilada

## Descripción
Sistema de Gestión de Homologaciones de Aplicaciones
Versión compilada y portable - No requiere instalación de Python.

## Estructura de Archivos
```
HomologadorInventoria/
├── HomologadorInventoria.exe    # Ejecutable principal
├── Ejecutar_Homologador.bat     # Script de lanzamiento
├── config.ini                   # Configuración de la aplicación
├── README_DISTRIBUCION.md       # Este archivo
├── data/
│   └── homologador.db           # Base de datos SQLite
├── backups/                     # Respaldos automáticos
└── logs/                        # Archivos de log
```

## Instrucciones de Uso

### Opción 1: Ejecución Directa
Doble clic en `HomologadorInventoria.exe`

### Opción 2: Script de Lanzamiento
Doble clic en `Ejecutar_Homologador.bat`

## Características
- ✅ Aplicación completamente portable
- ✅ Base de datos SQLite integrada
- ✅ Respaldos automáticos
- ✅ Sistema de logging
- ✅ Tema oscuro completo
- ✅ Dashboard con métricas avanzadas
- ✅ Gestión completa de estados

## Credenciales por Defecto
- **Usuario**: admin
- **Contraseña**: admin123

## Soporte Técnico
Para soporte o reportar problemas, contacte al administrador del sistema.

---
Generado el: """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
"""
    
    readme_file = dist_path / "README_DISTRIBUCION.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✓ README de distribución creado: {readme_file}")

def main():
    """Función principal del script de compilación."""
    print("=" * 60)
    print("   COMPILADOR HomologadorInventoria v1.0.0")
    print("=" * 60)
    print()
    
    try:
        # 1. Crear carpeta de distribución
        print("1. Creando estructura de distribución...")
        dist_path = create_distribution_folder()
        
        # 2. Preparar base de datos
        print("\n2. Preparando base de datos...")
        prepare_database(dist_path)
        
        # 3. Copiar archivos esenciales
        print("\n3. Copiando archivos esenciales...")
        copy_essential_files(dist_path)
        
        # 4. Crear configuración
        print("\n4. Creando configuración...")
        create_config_file(dist_path)
        
        # 5. Compilar aplicación
        print("\n5. Compilando aplicación...")
        if not compile_application():
            print("✗ Error en compilación. Abortando.")
            return
        
        # 6. Crear scripts auxiliares
        print("\n6. Creando scripts auxiliares...")
        create_launcher_script(dist_path)
        create_readme_dist(dist_path)
        
        # 7. Limpiar archivos temporales
        print("\n7. Limpiando archivos temporales...")
        temp_dirs = ["build_temp", "__pycache__"]
        for temp_dir in temp_dirs:
            temp_path = Path(temp_dir)
            if temp_path.exists():
                shutil.rmtree(temp_path)
                print(f"✓ Eliminado: {temp_dir}")
        
        print(f"\n{'='*60}")
        print("🎉 COMPILACIÓN COMPLETADA EXITOSAMENTE")
        print(f"{'='*60}")
        print(f"📁 Carpeta de distribución: {dist_path.absolute()}")
        print(f"🚀 Ejecutable: {dist_path / 'HomologadorInventoria.exe'}")
        print(f"📋 Tamaño aprox: {get_folder_size(dist_path):.1f} MB")
        print()
        print("✅ La aplicación está lista para distribuir")
        print("✅ Todos los archivos están centralizados")
        print("✅ No requiere instalación adicional")
        
    except Exception as e:
        print(f"\n✗ Error durante la compilación: {e}")
        print("Verifique los logs para más detalles.")

def get_folder_size(folder_path):
    """Calcular el tamaño de una carpeta en MB."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size / (1024 * 1024)  # Convertir a MB

if __name__ == "__main__":
    main()