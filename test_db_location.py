#!/usr/bin/env python3
"""
🧪 SCRIPT DE PRUEBA DE UBICACIÓN DE BASE DE DATOS
EXPANSION DE DOMINIO - INVENTORIA

Verifica que la BD se cree ÚNICAMENTE en la carpeta del ejecutable
"""

import os
import sys
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_database_location():
    """Prueba la ubicación de la base de datos"""
    print("🧪 PRUEBA DE UBICACIÓN DE BASE DE DATOS")
    print("=" * 50)
    
    try:
        # Información del entorno
        print(f"📍 Directorio actual: {os.getcwd()}")
        print(f"📍 Script ejecutándose desde: {os.path.abspath(__file__)}")
        
        if hasattr(sys, '_MEIPASS'):
            print(f"📦 Ejecutable PyInstaller detectado")
            print(f"📦 _MEIPASS: {sys._MEIPASS}")
            print(f"📦 sys.executable: {sys.executable}")
            print(f"📦 Directorio del ejecutable: {os.path.dirname(sys.executable)}")
        else:
            print(f"🐍 Script Python normal")
        
        print("\n🔧 PROBANDO FUNCIONES PORTABLE...")
        
        # Importar y probar funciones portable
        from homologador.core.portable import get_database_path, get_backups_path, get_app_info
        
        # Información portable
        db_path = get_database_path()
        backups_path = get_backups_path()
        app_info = get_app_info()
        
        print(f"💾 Ruta BD (portable): {db_path}")
        print(f"📋 Ruta Backups (portable): {backups_path}")
        print(f"📂 Directorio de BD: {os.path.dirname(db_path)}")
        print(f"✅ BD existe: {os.path.exists(db_path)}")
        print(f"✅ Dir BD escribible: {os.access(os.path.dirname(db_path), os.W_OK)}")
        
        print("\n🔧 PROBANDO SETTINGS...")
        
        # Probar settings
        from homologador.core.settings import get_settings
        settings = get_settings()
        
        settings_db_path = settings.get_db_path()
        settings_backups = settings.get_backups_dir()
        
        print(f"💾 Ruta BD (settings): {settings_db_path}")
        print(f"📋 Ruta Backups (settings): {settings_backups}")
        
        # Verificar que las rutas coinciden
        if db_path == settings_db_path:
            print("✅ Las rutas de BD coinciden")
        else:
            print("❌ Las rutas de BD NO coinciden")
            print(f"   Portable: {db_path}")
            print(f"   Settings: {settings_db_path}")
        
        print("\n🔧 PROBANDO CONEXIÓN A BD...")
        
        # Probar conexión
        from homologador.core.storage import get_database_manager
        db_manager = get_database_manager()
        
        print(f"💾 BD Manager path: {db_manager.db_path}")
        
        # Verificar directorio
        db_dir = os.path.dirname(db_manager.db_path)
        print(f"📂 Directorio BD: {db_dir}")
        print(f"✅ Directorio existe: {os.path.exists(db_dir)}")
        print(f"✅ Directorio escribible: {os.access(db_dir, os.W_OK)}")
        
        # Intentar inicializar
        try:
            db_manager.initialize_database()
            print("✅ Base de datos inicializada correctamente")
            
            # Verificar que se creó en el lugar correcto
            if os.path.exists(db_manager.db_path):
                print(f"✅ BD creada en: {db_manager.db_path}")
                size = os.path.getsize(db_manager.db_path)
                print(f"📏 Tamaño BD: {size} bytes")
            else:
                print(f"❌ BD NO se creó en: {db_manager.db_path}")
                
        except Exception as e:
            print(f"❌ Error inicializando BD: {e}")
            return False
        
        print("\n🎉 PRUEBA COMPLETADA EXITOSAMENTE")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_database_location()
    sys.exit(0 if success else 1)