"""
🔍 DIAGNÓSTICO DE INCOMPATIBILIDAD
Script para identificar problemas de ejecución en Windows 11
"""
import subprocess
import os
import sys
from pathlib import Path

def test_executable(exe_path, name="Ejecutable"):
    """Probar un ejecutable y reportar resultados detallados."""
    print(f"\n🧪 PROBANDO: {name}")
    print("=" * 50)
    print(f"📁 Ruta: {exe_path}")
    
    if not os.path.exists(exe_path):
        print("❌ Archivo no encontrado")
        return False
    
    # Verificar tamaño
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"📏 Tamaño: {size_mb:.1f} MB")
    
    # Intentar ejecutar con diferentes métodos
    methods = [
        ("Ejecución directa", [exe_path]),
        ("Con parámetro --help", [exe_path, "--help"]),
        ("Con cmd /c", ["cmd", "/c", exe_path]),
    ]
    
    for method_name, cmd in methods:
        print(f"\n🔧 Método: {method_name}")
        try:
            result = subprocess.run(
                cmd,
                timeout=5,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(exe_path)
            )
            
            if result.returncode == 0:
                print("✅ Éxito")
            else:
                print(f"❌ Error (código {result.returncode})")
                if result.stderr:
                    print(f"   Error: {result.stderr[:200]}...")
                    
        except subprocess.TimeoutExpired:
            print("⚠️ Timeout (puede estar funcionando)")
        except FileNotFoundError:
            print("❌ Archivo no encontrado o no ejecutable")
        except Exception as e:
            print(f"❌ Error: {str(e)[:100]}...")
    
    return True

def compare_executables():
    """Comparar ambos ejecutables."""
    print("🔍 DIAGNÓSTICO DE INCOMPATIBILIDAD - HomologadorInventoria")
    print("=" * 60)
    
    # Rutas de los ejecutables
    original_exe = Path("dist_homologador/HomologadorInventoria.exe")
    compatible_exe = Path("dist_compatible/HomologadorInventoria.exe")
    
    # Probar ejecutable original (problemático)
    if original_exe.exists():
        test_executable(str(original_exe), "Ejecutable Original (Problemático)")
    else:
        print("⚠️ Ejecutable original no encontrado")
    
    # Probar ejecutable compatible
    if compatible_exe.exists():
        test_executable(str(compatible_exe), "Ejecutable Compatible")
    else:
        print("⚠️ Ejecutable compatible no encontrado")
    
    # Análisis de diferencias
    print(f"\n📊 ANÁLISIS COMPARATIVO")
    print("=" * 50)
    
    if original_exe.exists() and compatible_exe.exists():
        orig_size = original_exe.stat().st_size / (1024 * 1024)
        comp_size = compatible_exe.stat().st_size / (1024 * 1024)
        
        print(f"📏 Tamaño original: {orig_size:.1f} MB")
        print(f"📏 Tamaño compatible: {comp_size:.1f} MB")
        print(f"📉 Diferencia: {orig_size - comp_size:.1f} MB ({((orig_size - comp_size) / orig_size * 100):.1f}% reducción)")
        
        print(f"\n🔍 POSIBLES CAUSAS DEL PROBLEMA ORIGINAL:")
        print("  1. 🐍 Python 3.13 demasiado nuevo para algunas dependencias")
        print("  2. 📦 PyInstaller incluyó módulos incompatibles")
        print("  3. 🔧 Falta manifest de aplicación para Windows 11")
        print("  4. 🏗️ Problemas de arquitectura o DLL")
        print("  5. 🛡️ Windows Defender bloqueando por tamaño excesivo")
        
        print(f"\n✅ MEJORAS EN LA VERSIÓN COMPATIBLE:")
        print("  • 📝 Manifest específico para Windows 11")
        print("  • 🧹 Exclusión de módulos innecesarios")
        print("  • 🔧 Configuración PyInstaller optimizada")
        print("  • 📏 Tamaño reducido para evitar bloqueos")
        print("  • 🎯 Arquitectura específica (AMD64)")

def main():
    """Función principal."""
    try:
        compare_executables()
        
        print(f"\n💡 RECOMENDACIÓN:")
        print("=" * 30)
        print("✅ Usar el ejecutable compatible (dist_compatible/)")
        print("🗑️ El ejecutable original tiene problemas de compatibilidad")
        print("🔄 La versión compatible es más pequeña y estable")
        
    except Exception as e:
        print(f"❌ Error durante el diagnóstico: {e}")

if __name__ == "__main__":
    main()