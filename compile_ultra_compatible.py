"""
Compilación ULTRA COMPATIBLE - Eliminando TODOS los problemas
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("COMPILACIÓN ULTRA COMPATIBLE - WINDOWS 11 x64")
    print("=" * 60)
    
    # Verificar Python
    import struct
    bits = struct.calcsize('P') * 8
    print(f"\n✓ Python: {bits} bits")
    
    if bits != 64:
        print("❌ ERROR: Necesitas Python de 64 bits!")
        return
    
    # Limpiar
    print("\n🧹 Limpiando compilaciones anteriores...")
    dirs_to_clean = ['dist_ultra', 'build_ultra']
    for d in dirs_to_clean:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"   Eliminado: {d}")
    
    # Configuración ULTRA COMPATIBLE
    print("\n📦 Configurando PyInstaller...")
    
    cmd = [
        'pyinstaller',
        '--name=HomologadorInventoria',
        '--onefile',  # UN SOLO ARCHIVO
        '--windowed',  # Sin consola - MODO VENTANA
        '--noupx',  # No usar UPX (puede causar problemas)
        '--clean',
        '--noconfirm',
        '--distpath=dist_ultra',
        '--workpath=build_ultra',
        '--specpath=.',
        
        # Añadir icono si existe
        '--icon=assets/icon.ico' if os.path.exists('assets/icon.ico') else '',
        
        # Datos necesarios
        '--add-data=homologador;homologador',
        '--add-data=assets;assets' if os.path.exists('assets') else '',
        
        # Imports ocultos - TODOS los necesarios
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtSvg',
        '--hidden-import=pandas',
        '--hidden-import=numpy',
        '--hidden-import=openpyxl',
        '--hidden-import=sqlite3',
        '--hidden-import=json',
        '--hidden-import=datetime',
        '--hidden-import=pathlib',
        
        # Entry point - PUNTO DE ENTRADA SIMPLIFICADO
        'app_entry.py'
    ]
    
    # Filtrar argumentos vacíos
    cmd = [c for c in cmd if c]
    
    print("\n🔨 Compilando aplicación...")
    print(f"Comando: {' '.join(cmd)}\n")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        
        # Verificar resultado
        exe_path = Path('dist_ultra/HomologadorInventoria.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print("\n" + "=" * 60)
            print("✅ COMPILACIÓN ULTRA COMPATIBLE EXITOSA!")
            print("=" * 60)
            print(f"📦 Ejecutable: {exe_path}")
            print(f"📏 Tamaño: {size_mb:.2f} MB")
            print("\n🎯 INSTRUCCIONES:")
            print("1. Navega a la carpeta: dist_ultra")
            print("2. Ejecuta: HomologadorInventoria.exe")
            print("3. Si Windows SmartScreen aparece:")
            print("   - Haz clic en 'Más información'")
            print("   - Luego en 'Ejecutar de todos modos'")
            print("\n💡 Este ejecutable tiene TODAS las correcciones:")
            print("   ✓ Sin mensajes de diagnóstico bloqueantes")
            print("   ✓ Encoding correcto para Windows")
            print("   ✓ Imports simplificados")
            print("   ✓ Compatibilidad x64 nativa")
            print("   ✓ Sin UPX (mayor compatibilidad)")
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
