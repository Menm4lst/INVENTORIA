#!/usr/bin/env python3
"""
Punto de entrada principal para EXPANSION DE DOMINIO - INVENTORIA
Este script asegura que los imports relativos funcionen correctamente
"""

import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path para imports absolutos
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Ahora podemos importar correctamente
if __name__ == "__main__":
    # Importar y ejecutar la aplicación
    from homologador.app import main
    main()