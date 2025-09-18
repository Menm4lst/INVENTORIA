"""
Ventana de login ultra-simple para resolución de problemas de renderizado.
Usa solo componentes básicos y fuentes seguras.
"""

import sys
import logging
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

from data.seed import get_auth_service, AuthenticationError

logger = logging.getLogger(__name__)

class UltraSimpleLoginWindow(QWidget):
    """Ventana de login extremadamente básica para asegurar compatibilidad."""
    
    login_successful = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.auth_service = get_auth_service()
        self.setup_ui()
        self.set_basic_styles()
    
    def setup_ui(self):
        """Configura la interfaz más básica posible."""
        self.setWindowTitle("Login")
        self.resize(400, 300)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("HOMOLOGADOR")
        title.setFont(QFont("Arial", 14))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Form layout para usuario y contraseña
        form = QFormLayout()
        form.setSpacing(10)
        
        self.user_edit = QLineEdit()
        self.user_edit.setText("admin")
        self.pass_edit = QLineEdit()
        self.pass_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_edit.setText("admin123")
        self.pass_edit.returnPressed.connect(self.handle_login)
        
        form.addRow("Usuario:", self.user_edit)
        form.addRow("Contraseña:", self.pass_edit)
        layout.addLayout(form)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.login_btn = QPushButton("Login")
        self.login_btn.clicked.connect(self.handle_login)
        button_layout.addWidget(self.login_btn)
        
        exit_btn = QPushButton("Salir")
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)
        
        layout.addLayout(button_layout)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
    
    def set_basic_styles(self):
        """Aplica estilos básicos sin usar stylesheets complejos."""
        # Usar solo colores directos
        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(0, 0, 0))
        self.setPalette(palette)
        
        # Aplicar la misma paleta a widgets importantes
        self.user_edit.setPalette(palette)
        self.pass_edit.setPalette(palette)
        
        # Colores de botones directos
        login_palette = QPalette()
        login_palette.setColor(QPalette.ColorRole.Button, QColor(0, 0, 200))
        login_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        self.login_btn.setPalette(login_palette)
        
        # No usar stylesheets complejos
        self.setStyleSheet("")
    
    def handle_login(self):
        """Maneja el proceso de login."""
        username = self.user_edit.text().strip()
        password = self.pass_edit.text()
        
        if not username:
            self.status_label.setText("Ingrese usuario")
            return
        
        if not password:
            self.status_label.setText("Ingrese contraseña")
            return
        
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Procesando...")
        
        try:
            user_info = self.auth_service.authenticate(username, password)
            self.status_label.setText("Éxito")
            self.login_successful.emit(user_info)
        except AuthenticationError as e:
            self.status_label.setText(f"Error: {str(e)}")
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Login")
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            self.status_label.setText("Error interno")
            self.login_btn.setEnabled(True)
            self.login_btn.setText("Login")