"""
🔐 MÓDULO DE FIRMADO DIGITAL
Integración para firmar automáticamente el ejecutable durante la compilación
"""
import subprocess
import os
from pathlib import Path

def sign_executable_with_commercial_cert(exe_path, cert_path, cert_password, timestamp_url="http://timestamp.sectigo.com"):
    """
    Firmar ejecutable con certificado comercial usando signtool.exe
    
    Args:
        exe_path: Ruta al ejecutable
        cert_path: Ruta al archivo .p12/.pfx del certificado
        cert_password: Contraseña del certificado
        timestamp_url: URL del servidor de timestamp
    """
    try:
        # Buscar signtool.exe (incluido con Windows SDK)
        signtool_paths = [
            r"C:\Program Files (x86)\Windows Kits\10\bin\x64\signtool.exe",
            r"C:\Program Files (x86)\Windows Kits\10\bin\x86\signtool.exe",
            r"C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\signtool.exe"
        ]
        
        signtool = None
        for path in signtool_paths:
            if os.path.exists(path):
                signtool = path
                break
        
        if not signtool:
            print("❌ Error: signtool.exe no encontrado. Instala Windows SDK.")
            return False
        
        # Comando de firmado
        cmd = [
            signtool,
            "sign",
            "/f", cert_path,
            "/p", cert_password,
            "/t", timestamp_url,
            "/v",
            exe_path
        ]
        
        print(f"🔐 Firmando {exe_path}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ejecutable firmado exitosamente!")
            return True
        else:
            print(f"❌ Error al firmar: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error en el proceso de firmado: {e}")
        return False

def sign_executable_self_signed(exe_path, cert_name="HomologadorInventoria"):
    """
    Firmar ejecutable con certificado autofirmado usando PowerShell
    """
    try:
        ps_script = f'''
        $cert = Get-ChildItem -Path "Cert:\\CurrentUser\\My" | Where-Object {{$_.Subject -like "*{cert_name}*"}}
        if ($cert) {{
            Set-AuthenticodeSignature -FilePath "{exe_path}" -Certificate $cert[0] -TimestampServer "http://timestamp.sectigo.com"
            Write-Output "SUCCESS"
        }} else {{
            Write-Output "CERT_NOT_FOUND"
        }}
        '''
        
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True
        )
        
        if "SUCCESS" in result.stdout:
            print("✅ Ejecutable firmado con certificado autofirmado!")
            return True
        elif "CERT_NOT_FOUND" in result.stdout:
            print("⚠️ Certificado no encontrado. Ejecuta sign_software.ps1 primero.")
            return False
        else:
            print(f"❌ Error al firmar: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error en firmado autofirmado: {e}")
        return False

def integrate_signing_to_compilation():
    """
    Ejemplo de integración en compile_app.py
    """
    example_code = '''
# Agregar al final de compile_app.py, después de la compilación exitosa:

def sign_compiled_executable(dist_path):
    """Firmar el ejecutable compilado."""
    exe_path = dist_path / "HomologadorInventoria.exe"
    
    if not exe_path.exists():
        print("❌ Ejecutable no encontrado para firmar")
        return False
    
    # Opción 1: Certificado comercial (si tienes uno)
    cert_path = "certificados/mi_certificado.p12"  # Ruta a tu certificado
    cert_password = "tu_contraseña"  # Contraseña del certificado
    
    if os.path.exists(cert_path):
        return sign_executable_with_commercial_cert(
            str(exe_path), cert_path, cert_password
        )
    else:
        # Opción 2: Certificado autofirmado
        print("📝 Usando certificado autofirmado...")
        return sign_executable_self_signed(str(exe_path))

# Luego en la función main(), después de la compilación:
if compile_application():
    print("\\n🔐 Firmando ejecutable...")
    if sign_compiled_executable(dist_path):
        print("✅ Ejecutable firmado y listo para distribución")
    else:
        print("⚠️ Advertencia: Ejecutable no firmado")
'''
    
    return example_code

if __name__ == "__main__":
    print("🔐 MÓDULO DE FIRMADO DIGITAL")
    print("=" * 40)
    print()
    print("Funciones disponibles:")
    print("1. sign_executable_with_commercial_cert() - Certificado comercial")  
    print("2. sign_executable_self_signed() - Certificado autofirmado")
    print("3. integrate_signing_to_compilation() - Integración con compilación")
    print()
    print("Para usar, importa las funciones en tu script de compilación.")