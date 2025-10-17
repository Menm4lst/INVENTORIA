"""
Compilación ULTRA SIMPLE - Un solo archivo ejecutable de 64 bits
Sin complicaciones, sin carpetas adicionales, solo el ejecutable
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("COMPILACIÓN ULTRA SIMPLE - UN SOLO ARCHIVO X64")
    print("=" * 60)
    
    # Verificar Python
    import struct
    bits = struct.calcsize('P') * 8
    print(f"\n✓ Python: {bits} bits")
    
    if bits != 64:
        print("❌ ERROR: Necesitas Python de 64 bits!")
        print("Descarga Python 64-bit de: https://www.python.org/downloads/")
        return
    
    # Limpiar
    print("\n🧹 Limpiando compilaciones anteriores...")
    dirs_to_clean = ['dist_simple', 'build_simple']
    for d in dirs_to_clean:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"   Eliminado: {d}")
    
    # Configuración SIMPLE
    print("\n📦 Configurando PyInstaller...")
    
    cmd = [
        'pyinstaller',
        '--name=HomologadorInventoria',
        '--onefile',  # UN SOLO ARCHIVO
        '--windowed',  # Sin consola
        '--icon=assets/icon.ico' if os.path.exists('assets/icon.ico') else '',
        '--clean',
        '--noconfirm',
        '--distpath=dist_simple',
        '--workpath=build_simple',
        '--specpath=.',
        # Datos necesarios
        '--add-data=homologador;homologador',
        '--add-data=assets;assets' if os.path.exists('assets') else '',
        # Imports ocultos
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        '--hidden-import=sqlite3',
        # Entry point
        'run_app.py'
    ]
    
    # Filtrar argumentos vacíos
    cmd = [c for c in cmd if c]
    
    print("\n🔨 Compilando aplicación...")
    print(f"Comando: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        # Verificar resultado
        exe_path = Path('dist_simple/HomologadorInventoria.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print("\n" + "=" * 60)
            print("✅ COMPILACIÓN EXITOSA!")
            print("=" * 60)
            print(f"📦 Ejecutable: {exe_path}")
            print(f"📏 Tamaño: {size_mb:.2f} MB")
            print("\n🎉 Ahora ejecuta el archivo desde:")
            print(f"   {exe_path.absolute()}")
            print("\n💡 Es un archivo ÚNICO, no necesita carpetas adicionales")
        else:
            print("\n❌ Error: No se generó el ejecutable")
            if result.stderr:
                print("Errores:", result.stderr)
                
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error en compilación:")
        print(e.stderr)
        return
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return

if __name__ == "__main__":
    main()
