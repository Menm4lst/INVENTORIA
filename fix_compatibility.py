"""
FIX COMPLETO DE COMPATIBILIDAD
Este script corrige todos los problemas encontrados para Windows 11
"""

import os
import shutil
from pathlib import Path

def fix_app_py():
    """Elimina los mensajes de diagnóstico problemáticos de app.py"""
    print("🔧 Corrigiendo homologador/app.py...")
    
    app_path = Path("homologador/app.py")
    content = app_path.read_text(encoding='utf-8')
    
    # Eliminar los mensajes de diagnóstico que causan problemas
    content = content.replace(
        '            # Mostrar mensaje de diagnóstico\n            QMessageBox.information(None, "Diagnóstico", "¿Puedes ver este mensaje? Vamos a mostrar el login.")\n            \n',
        '            # Mensaje de diagnóstico removido para compatibilidad\n            \n'
    )
    
    content = content.replace(
        '            # Otro mensaje para verificar que se mostró\n            QMessageBox.information(None, "Diagnóstico", "El login debería estar visible ahora.")\n            \n',
        '            # Mensaje de diagnóstico removido para compatibilidad\n            \n'
    )
    
    app_path.write_text(content, encoding='utf-8')
    print("✅ app.py corregido")

def create_minimal_entry_point():
    """Crea un punto de entrada ULTRA MINIMALISTA sin complejidad"""
    print("🔧 Creando punto de entrada minimalista...")
    
    content = '''#!/usr/bin/env python3
"""
Punto de entrada ULTRA SIMPLE - Sin complejidad innecesaria
"""

if __name__ == "__main__":
    import sys
    import os
    
    # Configurar encoding para Windows
    if sys.platform == "win32":
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    
    # Asegurar que el directorio actual esté en el path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Importar y ejecutar
    try:
        from homologador.app import main
        main()
    except Exception as e:
        # Si algo falla, mostrar en consola (solo en modo debug)
        import traceback
        print(f"Error: {e}")
        print(traceback.format_exc())
        sys.exit(1)
'''
    
    entry_path = Path("app_entry.py")
    entry_path.write_text(content, encoding='utf-8')
    print(f"✅ Punto de entrada creado: {entry_path}")
    return entry_path

def main():
    print("=" * 60)
    print("FIX COMPLETO DE COMPATIBILIDAD PARA WINDOWS 11")
    print("=" * 60)
    print()
    
    # Paso 1: Corregir app.py
    fix_app_py()
    print()
    
    # Paso 2: Crear punto de entrada minimalista
    entry_file = create_minimal_entry_point()
    print()
    
    print("=" * 60)
    print("✅ CORRECCIONES COMPLETADAS")
    print("=" * 60)
    print()
    print("Archivo de entrada creado:", entry_file)
    print("Ahora ejecuta: python compile_ultra_compatible.py")
    print()

if __name__ == "__main__":
    main()
