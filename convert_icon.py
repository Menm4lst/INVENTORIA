"""
Script para convertir la imagen fondo.png a icono .ico
"""
from PIL import Image
import os

def convert_png_to_ico():
    """Convertir fondo.png a icon.ico"""
    try:
        # Cargar la imagen PNG
        png_path = "images/fondo.png"
        ico_path = "assets/icon.ico"
        
        if not os.path.exists(png_path):
            print(f"✗ No se encontró la imagen: {png_path}")
            return False
        
        # Crear directorio assets si no existe
        os.makedirs("assets", exist_ok=True)
        
        # Abrir la imagen
        img = Image.open(png_path)
        
        # Convertir a RGBA si no lo está
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Redimensionar a tamaños estándar de icono
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        icons = []
        
        for size in sizes:
            resized = img.resize(size, Image.Resampling.LANCZOS)
            icons.append(resized)
        
        # Guardar como ICO
        icons[0].save(ico_path, format='ICO', sizes=[(icon.width, icon.height) for icon in icons])
        
        print(f"✓ Icono creado exitosamente: {ico_path}")
        print(f"  Tamaños incluidos: {[f'{s[0]}x{s[1]}' for s in sizes]}")
        return True
        
    except ImportError:
        print("✗ Error: Pillow no está instalado. Instalando...")
        os.system("pip install Pillow")
        return convert_png_to_ico()
    except Exception as e:
        print(f"✗ Error al convertir imagen: {e}")
        return False

if __name__ == "__main__":
    print("Convirtiendo fondo.png a icono...")
    convert_png_to_ico()