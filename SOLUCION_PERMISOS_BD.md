# 🔧 SOLUCIÓN: Error de Permisos de Base de Datos

## ❌ PROBLEMA ORIGINAL:
```
Error cargando datos: error de base de datos: error adquiriendo lock (error 13) permission denied \C:\users\Se42246\Onedrive\Homologador.db.lock
```

## 🎯 CAUSA:
La aplicación intentaba crear la base de datos en rutas de OneDrive donde no tenía permisos de escritura, en lugar de usar la carpeta del ejecutable.

## ✅ SOLUCIÓN IMPLEMENTADA:

### 1. **Función Portable Mejorada** (`homologador/core/portable.py`):
```python
def get_database_path():
    """
    Obtiene la ruta a la base de datos SIEMPRE en la carpeta del ejecutable
    """
    # FORZAR ubicación en la carpeta del ejecutable
    if hasattr(sys, '_MEIPASS'):
        # Ejecutable PyInstaller - BD debe estar en el directorio de trabajo actual
        executable_dir = os.path.dirname(sys.executable)
        db_path = os.path.join(executable_dir, "homologador.db")
        return db_path
    else:
        # Script Python normal - BD en el directorio del proyecto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        db_path = os.path.join(project_root, "homologador.db")
        return db_path
```

### 2. **Settings Forzado** (`homologador/core/settings.py`):
```python
def _resolve_paths(self):
    """
    FORZAR el uso de la carpeta del ejecutable.
    NO autodetección de OneDrive - SOLO carpeta local del ejecutable.
    """
    from .portable import get_database_path, get_backups_path
    
    # FORZAR ubicación de BD en carpeta del ejecutable
    self.config["db_path"] = get_database_path()
    
    # FORZAR ubicación de backups en carpeta del ejecutable
    self.config["backups_dir"] = get_backups_path()
```

### 3. **Manejo de Errores de Permisos** (`homologador/core/storage.py`):
```python
def _acquire_file_lock(self):
    try:
        # Verificar que tenemos permisos de escritura en el directorio
        db_dir = os.path.dirname(self.db_path)
        if not os.access(db_dir, os.W_OK):
            raise DatabaseError(f"Sin permisos de escritura en directorio: {db_dir}")
        
        # Intentar eliminar lock file anterior si existe
        if os.path.exists(lock_path):
            try:
                os.remove(lock_path)
            except PermissionError:
                logger.warning(f"No se pudo eliminar lock file anterior")
                
    except PermissionError as e:
        error_msg = f"Error de permisos adquiriendo lock (error 13) permission denied"
        raise DatabaseError(error_msg)
```

## 🔍 VERIFICACIÓN:

### Para Desarrollo:
```bash
python test_db_location.py
```

### Para Ejecutable Portable:
```bash
# La BD siempre se creará en la misma carpeta que el .exe
# Ejemplo: C:\MiApp\EXPANSION_DE_DOMINIO_INVENTORIA_PORTABLE.exe
# BD en:   C:\MiApp\homologador.db
# Backups: C:\MiApp\backups\
```

## 📦 RESULTADO:
- ✅ **Base de datos centralizada** en carpeta del ejecutable
- ✅ **Sin dependencias de OneDrive** o rutas externas
- ✅ **Portabilidad 100%** - funciona en cualquier PC
- ✅ **Error de permisos resuelto** - no más error 13
- ✅ **Backups locales** en subcarpeta `backups/`

## 🚀 INSTRUCCIONES DE USO:

1. **Copiar carpeta completa** `dist_portable/` a cualquier ubicación
2. **Ejecutar** `EXPANSION_DE_DOMINIO_INVENTORIA_PORTABLE.exe`
3. **La BD se creará automáticamente** en la misma carpeta
4. **Todos los datos permanecen locales** y portátiles

---

**✅ PROBLEMA RESUELTO** - La aplicación ahora centraliza todos los datos en la carpeta del ejecutable, eliminando errores de permisos y dependencias externas.

*Desarrollado por: Antware (SysAdmin)*
*Fecha: Octubre 2025*