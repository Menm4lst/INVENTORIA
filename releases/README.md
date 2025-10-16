# 📦 Releases - HomologadorInventoria

## Estructura de Releases

Cada versión de la aplicación compilada se encuentra en su carpeta correspondiente:

```
releases/
├── v1.0.0/                              # Versión 1.0.0 (Actual)
│   ├── HomologadorInventoria.exe        # 🚀 Ejecutable principal (67.8 MB)
│   ├── Ejecutar_Homologador.bat         # 🔧 Script de lanzamiento
│   ├── config.ini                       # ⚙️ Configuración de aplicación
│   ├── README_DISTRIBUCION.md          # 📖 Guía de usuario
│   ├── data/
│   │   └── homologador.db              # 🗄️ Base de datos SQLite
│   ├── backups/                        # 💾 Carpeta para respaldos automáticos
│   └── logs/                           # 📋 Carpeta para archivos de log
└── README.md                           # 📄 Este archivo
```

## 🚀 Versión v1.0.0 - Características

### ✅ Funcionalidades Principales
- Sistema completo de gestión de homologaciones
- Dashboard avanzado con métricas en tiempo real
- Gestión de estados: Pendiente, Aprobada, Rechazada, En Proceso
- Sistema de autenticación con roles de usuario
- Exportación de datos a Excel
- Respaldos automáticos de base de datos
- Tema oscuro completo

### 🔧 Características Técnicas
- **Aplicación**: PyQt6 Desktop Application
- **Base de Datos**: SQLite embebida
- **Tamaño**: 67.8 MB (portable)
- **Plataforma**: Windows 10/11
- **Dependencias**: Ninguna (completamente autocontenida)

### 🎯 Persistencia de Estados
- ✅ CREATE: Guarda estado correctamente
- ✅ UPDATE: Actualiza estados sin conflictos
- ✅ READ: Muestra estados en todas las vistas
- ✅ Dashboard: Conteo preciso por estado

### 🎨 Interfaz de Usuario
- Icono personalizado (fondo.png)
- Tema oscuro completo
- Notificaciones del sistema
- Filtros avanzados
- Vista detallada de registros

## 📥 Instalación y Uso

### Opción 1: Ejecución Directa
```cmd
# Navegar a la carpeta v1.0.0 y ejecutar:
HomologadorInventoria.exe
```

### Opción 2: Script de Lanzamiento
```cmd
# Doble clic en:
Ejecutar_Homologador.bat
```

## 🔐 Credenciales por Defecto
- **Usuario**: admin
- **Contraseña**: admin123

## 📋 Historial de Versiones

### v1.0.0 (16 Octubre 2025)
- ✅ Sistema de compilación PyInstaller completamente funcional
- ✅ Persistencia de estados corregida completamente
- ✅ Icono personalizado implementado
- ✅ Base de datos centralizada en carpeta data/
- ✅ Aplicación completamente portable
- ✅ Eliminación de emojis para compatibilidad Windows
- ✅ Rutas relativas para ejecución portable

## 🛠️ Desarrollo

Para desarrolladores que quieran modificar la aplicación:

```bash
# Clonar repositorio
git clone https://github.com/Menm4lst/INVENTORIA.git

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar en modo desarrollo
python run_app.py

# Compilar nueva versión
python compile_app.py
```

## 📞 Soporte

Para reportar problemas o solicitar nuevas características:
- Repositorio: https://github.com/Menm4lst/INVENTORIA
- Issues: https://github.com/Menm4lst/INVENTORIA/issues

---
**HomologadorInventoria v1.0.0**  
*Sistema de Gestión de Homologaciones de Aplicaciones*  
*Desarrollado con PyQt6 y SQLite*