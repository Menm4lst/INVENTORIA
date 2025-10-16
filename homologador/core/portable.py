#!/usr/bin/env python3
"""
UTILIDADES PARA APLICACIÓN PORTÁTIL
EXPANSION DE DOMINIO - INVENTORIA v1.0.0
Desarrollado por: Antware (SysAdmin)

Funciones helper para manejo de rutas portátiles
"""

import os
import sys
from pathlib import Path

def get_resource_path(relative_path):
    """
    Obtiene la ruta absoluta a un recurso, compatible con PyInstaller
    
    Args:
        relative_path (str): Ruta relativa al recurso
        
    Returns:
        str: Ruta absoluta al recurso
    """
    try:
        # Si está ejecutándose como ejecutable PyInstaller
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            # Si está ejecutándose como script Python
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
    except Exception:
        # Fallback: usar ruta relativa
        return relative_path

def get_database_path():
    """
    Obtiene la ruta a la base de datos SIEMPRE en la carpeta del ejecutable
    
    Returns:
        str: Ruta a la base de datos EN LA CARPETA DEL EJECUTABLE
    """
    # FORZAR ubicación en la carpeta del ejecutable
    if hasattr(sys, '_MEIPASS'):
        # Ejecutable PyInstaller - BD debe estar en data/homologador.db
        executable_dir = os.path.dirname(sys.executable)
        db_path = os.path.join(executable_dir, "data", "homologador.db")
        print(f"[PORTABLE] Ejecutable detectado, BD en: {db_path}")
        return db_path
    else:
        # Script Python normal - BD en el directorio del proyecto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        db_path = os.path.join(project_root, "homologador.db")
        print(f"[DESARROLLO] Script Python, BD en: {db_path}")
        return db_path

def get_images_path():
    """
    Obtiene la ruta a la carpeta de imágenes
    
    Returns:
        str: Ruta a la carpeta de imágenes
    """
    return get_resource_path("images")

def get_backups_path():
    """
    Obtiene la ruta a la carpeta de backups
    
    Returns:
        str: Ruta a la carpeta de backups
    """
    # La carpeta de backups debe estar en el directorio de trabajo
    backups_dir = os.path.join(os.getcwd(), "backups")
    
    # Crear si no existe
    os.makedirs(backups_dir, exist_ok=True)
    
    return backups_dir

def ensure_portable_structure():
    """
    Asegura que la estructura de directorios portable existe
    """
    dirs_to_create = [
        get_backups_path()
    ]
    
    for directory in dirs_to_create:
        try:
            os.makedirs(directory, exist_ok=True)
        except PermissionError:
            # Si no se puede crear, usar temp
            import tempfile
            return tempfile.gettempdir()
    
    return True

def get_app_info():
    """
    Retorna información de la aplicación para debugging
    
    Returns:
        dict: Información de la aplicación
    """
    info = {
        "is_frozen": hasattr(sys, '_MEIPASS'),
        "executable_path": sys.executable,
        "working_directory": os.getcwd(),
        "database_path": get_database_path(),
        "images_path": get_images_path(),
        "backups_path": get_backups_path()
    }
    
    if hasattr(sys, '_MEIPASS'):
        info["meipass"] = sys._MEIPASS
    
    return info

def print_portable_debug():
    """
    Imprime información de debug para la aplicación portable
    """
    info = get_app_info()
    
    print("INFORMACIÓN DE APLICACIÓN PORTÁTIL:")
    print(f"   📦 Ejecutable congelado: {'Sí' if info['is_frozen'] else 'No'}")
    print(f"   🚀 Ejecutable: {info['executable_path']}")
    print(f"   📁 Directorio de trabajo: {info['working_directory']}")
    print(f"   Base de datos: {info['database_path']}")
    print(f"   🖼️ Imágenes: {info['images_path']}")
    print(f"   📋 Backups: {info['backups_path']}")
    
    if 'meipass' in info:
        print(f"   📦 MEIPASS: {info['meipass']}")
    
    # Verificar existencia de archivos críticos
    critical_files = [
        ("Base de datos", info['database_path']),
        ("Carpeta imágenes", info['images_path']),
        ("Carpeta backups", info['backups_path'])
    ]
    
    print("   🔍 Verificación de archivos:")
    for name, path in critical_files:
        exists = os.path.exists(path)
        status = "✅" if exists else "❌"
        print(f"      {status} {name}: {path}")

if __name__ == "__main__":
    # Test de las funciones
    print_portable_debug()