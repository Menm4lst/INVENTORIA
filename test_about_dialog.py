#!/usr/bin/env python3
"""
Test script para verificar el diálogo "Acerca de" con la información de Antware
"""

import sys
import os

# Añadir el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

class TestAboutDialog(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Test: Acerca de Dialog")
        self.setGeometry(100, 100, 300, 200)
        
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Botón para mostrar diálogo "Acerca de"
        about_btn = QPushButton("🌟 Mostrar Acerca de...")
        about_btn.clicked.connect(self.show_about)
        layout.addWidget(about_btn)
        
        # Información
        info_btn = QPushButton("ℹ️ Información del desarrollador")
        info_btn.clicked.connect(self.show_dev_info)
        layout.addWidget(info_btn)
        
    def show_about(self):
        """Muestra información sobre la aplicación - misma función que en main_window.py"""
        QMessageBox.about(
            self, 
            "Acerca de EXPANSION DE DOMINIO - INVENTORIA",
            "🌟 EXPANSION DE DOMINIO - INVENTORIA v1.0.0\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "👨‍💻 Desarrollado por: Antware\n"
            "🔧 Rol: SysAdmin\n"
            "📧 Sistema: Homologación y Gestión de Aplicaciones\n\n"
            "🚀 Características principales:\n"
            "• Sistema de estados: Pendiente, Aprobado, Rechazado\n"
            "• Dashboard avanzado con métricas en tiempo real\n"
            "• Exportación profesional a CSV/Excel con UTF-8\n"
            "• Notificaciones interactivas y configurables\n"
            "• Backup automático y gestión de usuarios\n"
            "• Tema oscuro/claro adaptativos\n\n"
            "🛡️ © 2024-2025 - Sistema de Inventario Empresarial\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "💡 'La eficiencia es hacer las cosas bien, \n"
            "    la efectividad es hacer las cosas correctas.'"
        )
        
    def show_dev_info(self):
        """Información adicional del desarrollador"""
        QMessageBox.information(
            self,
            "👨‍💻 Información del Desarrollador",
            "🌟 ANTWARE - SYSTEM ADMINISTRATOR\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "🔧 Especialidades:\n"
            "• Administración de Sistemas\n"
            "• Desarrollo de Aplicaciones PyQt6\n"
            "• Gestión de Bases de Datos SQLite\n"
            "• Automatización y Scripts\n"
            "• Sistemas de Backup y Seguridad\n\n"
            "💻 Tecnologías utilizadas:\n"
            "• Python 3.11+\n"
            "• PyQt6 (Interface Gráfica)\n"
            "• SQLite (Base de Datos)\n"
            "• Pandas (Exportación de Datos)\n"
            "• Logging & Error Handling\n\n"
            "🎯 Proyecto: Sistema de inventario y\n"
            "homologación de aplicaciones empresariales"
        )

def main():
    app = QApplication(sys.argv)
    
    # Aplicar tema oscuro básico
    app.setStyle('Fusion')
    
    window = TestAboutDialog()
    window.show()
    
    print("🚀 Test del diálogo 'Acerca de' iniciado")
    print("📝 Haz clic en los botones para ver la información de Antware")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()