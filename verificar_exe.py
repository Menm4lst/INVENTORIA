"""
Verificar la arquitectura del ejecutable generado
"""
import struct
import os

def check_exe_architecture(exe_path):
    """Verifica si un .exe es de 32 o 64 bits"""
    if not os.path.exists(exe_path):
        print(f"❌ Archivo no encontrado: {exe_path}")
        return None
    
    try:
        with open(exe_path, 'rb') as f:
            # Leer DOS header
            dos_header = f.read(64)
            if dos_header[:2] != b'MZ':
                print("❌ No es un ejecutable válido")
                return None
            
            # Obtener offset del PE header
            pe_offset = struct.unpack('<I', dos_header[60:64])[0]
            f.seek(pe_offset)
            
            # Leer PE signature
            pe_sig = f.read(4)
            if pe_sig != b'PE\0\0':
                print("❌ No es un ejecutable PE válido")
                return None
            
            # Leer machine type del COFF header
            machine = struct.unpack('<H', f.read(2))[0]
            
            if machine == 0x014c:
                return "32-bit (x86)"
            elif machine == 0x8664:
                return "64-bit (x64)"
            elif machine == 0xaa64:
                return "64-bit (ARM64)"
            else:
                return f"Desconocida (0x{machine:04x})"
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return None

# Verificar el ejecutable
exe_path = r"dist_simple\HomologadorInventoria.exe"
print("=" * 60)
print("VERIFICACIÓN DE ARQUITECTURA")
print("=" * 60)
print(f"Archivo: {exe_path}")

if os.path.exists(exe_path):
    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"Tamaño: {size_mb:.2f} MB")
    
    arch = check_exe_architecture(exe_path)
    if arch:
        print(f"Arquitectura: {arch}")
        if "64-bit" in arch:
            print("\n✅ ¡PERFECTO! El ejecutable es de 64 bits")
            print("\n📌 INSTRUCCIONES:")
            print("1. Navega a la carpeta: dist_simple")
            print("2. Haz doble clic en: HomologadorInventoria.exe")
            print("3. Si Windows SmartScreen aparece, haz clic en 'Más información' → 'Ejecutar de todos modos'")
        else:
            print("\n⚠️ ADVERTENCIA: El ejecutable NO es de 64 bits")
else:
    print("❌ El archivo no existe")
