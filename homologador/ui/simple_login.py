"""
Login window completamente funcional y simple para debugging.
"""

import sys
import logging
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from data.seed import get_auth_service, AuthenticationError

logger = logging.getLogger(__name__)

class SimpleLoginWindow(QWidget):
    """Ventana de login simple y funcional."""
    
    login_successful = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.auth_service = get_auth_service()
        self.setup_ui()
        self.apply_inline_styles()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        self.setWindowTitle("Homologador de Aplicaciones - Login")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowCloseButtonHint)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Título
        title = QLabel("Homologador de Aplicaciones")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff !important; background-color: transparent !important; font-size: 18pt !important;")
        main_layout.addWidget(title)
        
        # Subtítulo
        subtitle = QLabel("Sistema de Gestión de Homologaciones")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet("color: #cccccc !important; background-color: transparent !important; font-size: 12pt !important;")
        main_layout.addWidget(subtitle)
        
        # Formulario
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #404040 !important; border: 2px solid #ffffff !important; border-radius: 10px !important; padding: 20px !important;")
        form_layout = QFormLayout(form_frame)
        form_layout.setSpacing(15)
        
        # Usuario
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Nombre de usuario")
        self.username_edit.setText("admin")  # Pre-llenar
        self.username_edit.setStyleSheet("background-color: #606060 !important; color: #ffffff !important; border: 3px solid #ffffff !important; padding: 10px !important; font-size: 14pt !important;")
        form_layout.addRow("Usuario:", self.username_edit)
        
        # Contraseña
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setPlaceholderText("Contraseña")
        self.password_edit.setText("admin123")  # Pre-llenar
        self.password_edit.setStyleSheet("background-color: #606060 !important; color: #ffffff !important; border: 3px solid #ffffff !important; padding: 10px !important; font-size: 14pt !important;")
        self.password_edit.returnPressed.connect(self.handle_login)
        form_layout.addRow("Contraseña:", self.password_edit)
        
        main_layout.addWidget(form_frame)
        
        # Botones
        button_layout = QHBoxLayout()
        
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setDefault(True)
        self.login_button.setStyleSheet("background-color: #0078d4 !important; color: #ffffff !important; border: 2px solid #ffffff !important; padding: 12px 25px !important; font-size: 14pt !important; font-weight: bold !important;")
        button_layout.addWidget(self.login_button)
        
        exit_button = QPushButton("Salir")
        exit_button.clicked.connect(self.close)
        exit_button.setStyleSheet("background-color: #d13438 !important; color: #ffffff !important; border: 2px solid #ffffff !important; padding: 12px 25px !important; font-size: 14pt !important; font-weight: bold !important;")
        button_layout.addWidget(exit_button)
        
        main_layout.addLayout(button_layout)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #ffffff !important; background-color: transparent !important; font-size: 12pt !important; font-weight: bold !important; padding: 10px !important;")
        main_layout.addWidget(self.status_label)
    
    def apply_inline_styles(self):
        """Aplica estilos directamente con setStyleSheet."""
        # Estilo para toda la ventana - FORZANDO VISIBILIDAD
        self.setStyleSheet("""
            SimpleLoginWindow {
                background-color: #404040 !important;
                color: #ffffff !important;
            }
            
            QWidget {
                background-color: #404040 !important;
                color: #ffffff !important;
                font-family: Arial, sans-serif !important;
                font-size: 12pt !important;
            }
            
            QLabel {
                color: #ffffff !important;
                background-color: transparent !important;
                font-size: 12pt !important;
                padding: 5px !important;
            }
            
            QLineEdit {
                background-color: #606060 !important;
                color: #ffffff !important;
                border: 3px solid #ffffff !important;
                border-radius: 5px !important;
                padding: 10px !important;
                font-size: 14pt !important;
                min-height: 30px !important;
            }
            
            QLineEdit:focus {
                border-color: #00ff00 !important;
                background-color: #707070 !important;
            }
            
            QPushButton {
                background-color: #0078d4 !important;
                color: #ffffff !important;
                border: 2px solid #ffffff !important;
                border-radius: 5px !important;
                padding: 12px 25px !important;
                font-size: 14pt !important;
                font-weight: bold !important;
                min-width: 120px !important;
                min-height: 40px !important;
            }
            
            QPushButton:hover {
                background-color: #106ebe !important;
                border-color: #00ff00 !important;
            }
            
            QPushButton:pressed {
                background-color: #005a9e !important;
            }
            
            QPushButton:disabled {
                background-color: #555555 !important;
                color: #cccccc !important;
            }
            
            QFormLayout QLabel {
                color: #ffffff !important;
                font-weight: bold !important;
                font-size: 13pt !important;
            }
        """)
        
        # Aplicar colores adicionales directamente a widgets específicos
        self.setAutoFillBackground(True)
        palette = self.palette()
        from PyQt6.QtGui import QColor
        palette.setColor(self.backgroundRole(), QColor("#404040"))
        self.setPalette(palette)
    
    def handle_login(self):
        """Maneja el proceso de login."""
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        if not username:
            self.show_status("Ingrese su nombre de usuario", is_error=True)
            return
        
        if not password:
            self.show_status("Ingrese su contraseña", is_error=True)
            return
        
        self.login_button.setEnabled(False)
        self.login_button.setText("Autenticando...")
        
        try:
            user_info = self.auth_service.authenticate(username, password)
            self.show_status("Autenticación exitosa", is_error=False)
            logger.info(f"Login exitoso para: {user_info['username']}")
            self.login_successful.emit(user_info)
        except AuthenticationError as e:
            self.show_status(str(e), is_error=True)
            self.reset_login_state()
        except Exception as e:
            logger.error(f"Error inesperado en login: {e}")
            self.show_status("Error interno del sistema", is_error=True)
            self.reset_login_state()
    
    def show_status(self, message: str, is_error: bool = False):
        """Muestra mensaje de estado."""
        self.status_label.setText(message)
        if is_error:
            self.status_label.setStyleSheet("color: #ff6b6b; font-weight: bold;")
        else:
            self.status_label.setStyleSheet("color: #51cf66; font-weight: bold;")
    
    def reset_login_state(self):
        """Resetea el estado del botón de login."""
        self.login_button.setEnabled(True)
        self.login_button.setText("Iniciar Sesión")