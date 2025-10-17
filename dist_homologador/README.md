# 🌟 EXPANSION DE DOMINIO - INVENTORIA

**Sistema Profesional de Gestión e Inventario de Aplicaciones**

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green.svg)](https://pypi.org/project/PyQt6/)
[![SQLite](https://img.shields.io/badge/SQLite-Database-orange.svg)](https://sqlite.org)

---

## 📖 DESCRIPCIÓN

**EXPANSION DE DOMINIO - INVENTORIA** es una aplicación de escritorio profesional desarrollada en **Python** con **PyQt6** que permite gestionar inventarios de aplicaciones con sistema de homologaciones, estados de aprobación, dashboard interactivo y exportación profesional de datos.

### ✨ CARACTERÍSTICAS PRINCIPALES

- 🎛️ **Dashboard Interactivo** con gráficos circulares y métricas
- 📊 **Sistema de Estados** (Pendiente/Aprobado/Rechazado)
- 📋 **Gestión Completa** de aplicaciones y homologaciones
- 📤 **Exportación Profesional** (CSV/Excel) con encoding UTF-8
- 🔔 **Sistema de Notificaciones** interactivas (7 segundos, cerrables)
- 🎨 **Temas Adaptativos** (Claro/Oscuro automático)
- 💾 **Base de Datos SQLite** portable y eficiente
- 🔐 **Sistema de Usuarios** con roles diferenciados
- 📦 **Versión Portátil** 100% autocontenida

---

## 🚀 INSTALACIÓN Y USO

### Opción 1: Ejecutable Portátil (Recomendado)

```bash
# Descargar y extraer
1. Descargar carpeta dist_portable/
2. Ejecutar: EXPANSION_DE_DOMINIO_INVENTORIA_PORTABLE.exe
3. ¡Listo! No requiere instalación de Python
```

### Opción 2: Desde Código Fuente

```bash
# Clonar repositorio
git clone https://github.com/Menm4lst/INVENTORIA.git
cd INVENTORIA

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python run_app.py
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
📂 INVENTORIA/
├── 📂 homologador/           # Código fuente principal
│   ├── 📂 core/              # Lógica de negocio
│   ├── 📂 data/              # Base de datos y esquemas
│   └── 📂 ui/                # Interfaz de usuario
├── 📂 dist_portable/         # Versión portátil completa
├── 📂 images/                # Recursos multimedia
├── 📄 run_app.py             # Script de ejecución
├── 📄 requirements.txt       # Dependencias Python
└── 📄 README.md              # Documentación
```

---

## 🛠️ TECNOLOGÍAS

| Componente | Tecnología | Versión |
|------------|------------|---------|
| **Lenguaje** | Python | 3.13+ |
| **GUI** | PyQt6 | Latest |
| **Base de Datos** | SQLite | 3.x |
| **Gráficos** | matplotlib | Latest |
| **Exportación** | pandas, openpyxl | Latest |
| **Compilación** | PyInstaller | 6.14.2 |

---

## 👨‍💻 AUTOR

**Antware** - *SysAdmin y Desarrollador*
- GitHub: [@Menm4lst](https://github.com/Menm4lst)
- Proyecto: [INVENTORIA](https://github.com/Menm4lst/INVENTORIA)
