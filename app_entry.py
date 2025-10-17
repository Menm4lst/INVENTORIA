#!/usr/bin/env python3
"""
Punto de entrada ULTRA SIMPLE - Sin complejidad innecesaria
Compatible con modo --windowed (sin consola)
"""

if __name__ == "__main__":
    import sys
    import os
    
    # Configurar encoding para Windows SOLO si hay consola
    if sys.platform == "win32":
        # En modo --windowed, stdout/stderr pueden ser None
        if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
            import codecs
            sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        if sys.stderr is not None and hasattr(sys.stderr, 'buffer'):
            import codecs
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
        # Si algo falla y hay consola disponible, mostrar error
        if sys.stderr is not None:
            import traceback
            print(f"Error: {e}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
        sys.exit(1)
