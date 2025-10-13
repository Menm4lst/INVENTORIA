"""
Script para analizar y limpiar el repositorio del Homologador.
Identifica archivos innecesarios y los elimina para optimizar el proyecto.
"""

import os
import shutil
from pathlib import Path

def analyze_repository():
    """Analiza el repositorio actual y categoriza los archivos."""
    
    base_dir = Path("c:/Users/Antware/OneDrive/Desktop/PROYECTOS DEV/APP HOMOLOGACIONES")
    
    # 📁 ARCHIVOS PRINCIPALES (MANTENER)
    essential_files = {
        # Core de la aplicación
        "homologador/app.py": "✅ Entrada principal de la aplicación",
        "homologador/__init__.py": "✅ Módulo Python",
        
        # UI Principal
        "homologador/ui/__init__.py": "✅ Módulo UI",
        "homologador/ui/main_window.py": "✅ Ventana principal con dashboard",
        "homologador/ui/final_login.py": "✅ Ventana de login actual",
        "homologador/ui/details_view.py": "✅ Vista de detalles (corregida)",
        "homologador/ui/homologation_form.py": "✅ Formulario de homologaciones",
        "homologador/ui/theme.py": "✅ Sistema de tema oscuro",
        "homologador/ui/notifications.py": "✅ Sistema de notificaciones",
        "homologador/ui/dashboard_advanced.py": "✅ Dashboard avanzado integrado",
        "homologador/ui/icons.py": "✅ Manejo de iconos",
        
        # Core del sistema
        "homologador/core/__init__.py": "✅ Módulo core",
        "homologador/core/storage.py": "✅ Manejo de base de datos",
        "homologador/core/settings.py": "✅ Configuraciones",
        "homologador/core/export.py": "✅ Exportación de datos",
        "homologador/core/audit.py": "✅ Sistema de auditoría",
        "homologador/core/optimization.py": "✅ Optimizaciones",
        
        # Data
        "homologador/data/__init__.py": "✅ Módulo data",
        "homologador/data/seed.py": "✅ Datos iniciales y autenticación",
        "homologador/data/schema.sql": "✅ Esquema de base de datos",
        
        # Configuración
        "requirements.txt": "✅ Dependencias del proyecto",
        "README.md": "✅ Documentación"
    }
    
    # 🗑️ ARCHIVOS PARA ELIMINAR
    files_to_delete = {
        # Cache y archivos temporales
        "__pycache__/": "❌ Cache de Python",
        "homologador/__pycache__/": "❌ Cache",
        "homologador/ui/__pycache__/": "❌ Cache",
        "homologador/core/__pycache__/": "❌ Cache",
        "homologador/data/__pycache__/": "❌ Cache",
        "tests/__pycache__/": "❌ Cache de tests",
        "tests/unit/__pycache__/": "❌ Cache de tests",
        
        # Builds y distribuciones
        "build/": "❌ Archivos de build de PyInstaller",
        "dist/": "❌ Ejecutables compilados",
        "scripts/": "❌ Scripts de build obsoletos",
        
        # Paquetes y deployment obsoletos
        "Paquete_Homologador_Autocontenido/": "❌ Paquete obsoleto",
        "Paquete_Homologador_OneDrive/": "❌ Paquete obsoleto",
        "deployment/": "❌ Deployment obsoleto",
        
        # Tests (muchos obsoletos)
        "tests/": "❌ Tests obsoletos y fragmentados",
        
        # Archivos de UI obsoletos/duplicados
        "homologador/ui/login_window.py": "❌ Login obsoleto (usamos final_login.py)",
        "homologador/ui/simple_login.py": "❌ Login simple obsoleto",
        "homologador/ui/ultra_simple_login.py": "❌ Login ultra simple obsoleto", 
        "homologador/ui/white_black_login.py": "❌ Login de prueba obsoleto",
        "homologador/ui/simple_theme.py": "❌ Tema simple obsoleto",
        "homologador/ui/theme_effects.py": "❌ Efectos de tema no usados",
        "homologador/ui/main_window_temp.py": "❌ Ventana temporal obsoleta",
        "homologador/ui/homologation_form_fix.py": "❌ Fix obsoleto",
        "homologador/ui/autosave_manager.py": "❌ Autosave no implementado",
        
        # Archivos de prueba y temporales
        "simple_test_window.py": "❌ Ventana de prueba",
        "homologador/test_simple.py": "❌ Test simple obsoleto",
        "homologador/test_funcionalidades.py": "❌ Test funcionalidades obsoleto",
        "aplicar_tema_oscuro_global.py": "❌ Script temporal (ya aplicado)",
        
        # Logs
        "homologador.log": "❌ Log temporal",
        "homologador/homologador.log": "❌ Log temporal",
        "coverage.xml": "❌ Reporte de cobertura",
        
        # Duplicados
        "homologador/requirements.txt": "❌ Duplicado (tenemos el principal)",
        "homologador/README.md": "❌ Duplicado (tenemos el principal)",
        "homologador/config.json": "❌ Config no usado"
    }
    
    return essential_files, files_to_delete

def clean_repository():
    """Elimina archivos innecesarios del repositorio."""
    
    base_dir = Path("c:/Users/Antware/OneDrive/Desktop/PROYECTOS DEV/APP HOMOLOGACIONES")
    essential_files, files_to_delete = analyze_repository()
    
    print("🧹 LIMPIEZA DEL REPOSITORIO HOMOLOGADOR")
    print("=" * 50)
    
    deleted_count = 0
    total_size_saved = 0
    
    for file_path, reason in files_to_delete.items():
        full_path = base_dir / file_path
        
        try:
            if full_path.exists():
                if full_path.is_dir():
                    # Calcular tamaño del directorio
                    size = sum(f.stat().st_size for f in full_path.rglob('*') if f.is_file())
                    shutil.rmtree(full_path)
                    print(f"📁 Eliminado directorio: {file_path} ({size//1024}KB) - {reason}")
                else:
                    size = full_path.stat().st_size
                    full_path.unlink()
                    print(f"📄 Eliminado archivo: {file_path} ({size//1024}KB) - {reason}")
                
                deleted_count += 1
                total_size_saved += size
                
        except Exception as e:
            print(f"❌ Error eliminando {file_path}: {e}")
    
    print(f"\n✅ LIMPIEZA COMPLETADA")
    print(f"📊 Archivos/carpetas eliminados: {deleted_count}")
    print(f"💾 Espacio liberado: {total_size_saved//1024//1024}MB")
    
    # Mostrar archivos esenciales que se mantuvieron
    print(f"\n📋 ARCHIVOS PRINCIPALES MANTENIDOS:")
    for file_path, description in essential_files.items():
        full_path = base_dir / file_path
        if full_path.exists():
            print(f"   {description}: {file_path}")
        else:
            print(f"   ⚠️ FALTA: {file_path}")

if __name__ == "__main__":
    clean_repository()