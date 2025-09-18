"""
Sistema de notificaciones para el Homologador de Aplicaciones.
Proporciona una interfaz para mostrar mensajes de estado, éxito, error y advertencias.
"""

import logging
from enum import Enum
from typing import Optional, Callable

from PyQt6.QtWidgets import (
    QFrame, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, 
    QGraphicsOpacityEffect, QApplication, QWidget
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QEasingCurve, QSize, pyqtProperty
from PyQt6.QtGui import QColor, QPainter, QPainterPath, QFont, QPen

logger = logging.getLogger(__name__)

class NotificationType(Enum):
    """Tipos de notificaciones con sus colores y estilos."""
    INFO = ("#0078d4", "🔹")      # Azul (información)
    SUCCESS = ("#107c10", "✓")   # Verde (éxito)
    WARNING = ("#ff8c00", "⚠️")   # Naranja (advertencia)
    ERROR = ("#d13438", "❌")      # Rojo (error)

class NotificationWidget(QFrame):
    """Widget para mostrar notificaciones con animaciones."""
    
    def __init__(
        self, 
        parent: QWidget, 
        message: str, 
        type: NotificationType = NotificationType.INFO, 
        duration: int = 3000,
        on_dismiss: Optional[Callable] = None
    ):
        """
        Inicializa un widget de notificación.
        
        Args:
            parent: Widget padre
            message: Mensaje a mostrar
            type: Tipo de notificación
            duration: Duración en milisegundos (0 para no cerrarse automáticamente)
            on_dismiss: Función a llamar cuando se cierra la notificación
        """
        super().__init__(parent)
        self.message = message
        self.type = type
        self.duration = duration
        self.on_dismiss = on_dismiss
        self.opacity_effect = None
        self.fade_animation = None
        self.slide_animation = None
        self._opacity = 0.0
        
        self.setup_ui()
        self.setup_animations()
        
        # Iniciar la animación de entrada
        self.show_notification()
    
    def setup_ui(self):
        """Configura la interfaz de usuario del widget."""
        # Configurar el frame
        self.setFixedHeight(60)
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        
        # Establecer layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        
        # Ícono según tipo
        icon_label = QLabel(self.type.value[1])
        icon_label.setStyleSheet(f"color: {self.type.value[0]}; font-size: 18px;")
        layout.addWidget(icon_label)
        
        # Mensaje
        message_label = QLabel(self.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("color: white; font-size: 12px;")
        layout.addWidget(message_label, 1)  # Estira horizontalmente
        
        # Botón cerrar
        close_button = QPushButton("×")
        close_button.setFixedSize(24, 24)
        close_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #cccccc;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            }
            QPushButton:hover {
                color: white;
            }
            QPushButton:pressed {
                color: #999999;
            }
        """)
        close_button.clicked.connect(self.dismiss)
        layout.addWidget(close_button)
        
        # Estilo del widget según tipo
        self.setStyleSheet(f"""
            NotificationWidget {{
                background-color: #333333;
                border-left: 4px solid {self.type.value[0]};
                border-radius: 4px;
                color: white;
            }}
        """)
        
        # Efecto de sombra
        self.setGraphicsEffect(None)  # Eliminar cualquier efecto previo
        
        # Efecto de opacidad
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.opacity = 0.0  # Inicialmente invisible
        self.setGraphicsEffect(self.opacity_effect)
    
    def setup_animations(self):
        """Configura las animaciones del widget."""
        # Auto-cierre si duration > 0
        if self.duration > 0:
            QTimer.singleShot(self.duration, self.dismiss)
    
    def show_notification(self):
        """Muestra la notificación con animación."""
        # Calcular posición
        parent_rect = self.parent().rect()
        self_size = QSize(parent_rect.width() // 3, 60)
        self.setFixedSize(self_size)
        
        # Posicionar en la parte superior derecha
        target_x = parent_rect.width() - self_size.width() - 20
        target_y = 20
        
        # Posición inicial fuera de la vista
        self.move(parent_rect.width(), target_y)
        self.show()
        
        # Animar la opacidad
        self.fade_animation = QPropertyAnimation(self, b"opacity")
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Animar el deslizamiento
        self.slide_animation = QPropertyAnimation(self, b"pos")
        self.slide_animation.setDuration(300)
        self.slide_animation.setStartValue(QPoint(parent_rect.width(), target_y))
        self.slide_animation.setEndValue(QPoint(target_x, target_y))
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Iniciar animaciones
        self.fade_animation.start()
        self.slide_animation.start()
    
    def dismiss(self):
        """Cierra la notificación con animación."""
        # Detener animaciones existentes
        if self.fade_animation and self.fade_animation.state() == QPropertyAnimation.State.Running:
            self.fade_animation.stop()
        if self.slide_animation and self.slide_animation.state() == QPropertyAnimation.State.Running:
            self.slide_animation.stop()
        
        # Animar la salida
        fade_out = QPropertyAnimation(self, b"opacity")
        fade_out.setDuration(200)
        fade_out.setStartValue(self.opacity)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.OutCubic)
        fade_out.finished.connect(self._on_fade_out_finished)
        fade_out.start()
        
        # Deslizar hacia afuera
        parent_rect = self.parent().rect()
        slide_out = QPropertyAnimation(self, b"pos")
        slide_out.setDuration(200)
        slide_out.setStartValue(self.pos())
        slide_out.setEndValue(QPoint(parent_rect.width(), self.pos().y()))
        slide_out.setEasingCurve(QEasingCurve.Type.OutCubic)
        slide_out.start()
    
    def _on_fade_out_finished(self):
        """Maneja el fin de la animación de salida."""
        # Eliminar widget
        self.hide()
        self.deleteLater()
        
        # Llamar a callback si existe
        if self.on_dismiss:
            self.on_dismiss()
    
    # Propiedades para animaciones
    def _get_opacity(self):
        return self._opacity
    
    def _set_opacity(self, value):
        self._opacity = value
        if self.opacity_effect:
            self.opacity_effect.setOpacity(value)
    
    opacity = pyqtProperty(float, _get_opacity, _set_opacity)

class NotificationManager:
    """Gestiona la creación y seguimiento de notificaciones."""
    
    _active_notifications = []
    
    @classmethod
    def show_notification(
        cls, 
        parent: QWidget, 
        message: str, 
        type: NotificationType = NotificationType.INFO, 
        duration: int = 3000
    ) -> NotificationWidget:
        """
        Muestra una nueva notificación.
        
        Args:
            parent: Widget padre donde mostrar la notificación
            message: Mensaje a mostrar
            type: Tipo de notificación
            duration: Duración en milisegundos
            
        Returns:
            El widget de notificación creado
        """
        # Crear notificación
        notification = NotificationWidget(
            parent, 
            message, 
            type, 
            duration,
            on_dismiss=lambda: cls._remove_notification(notification)
        )
        
        # Agregar al seguimiento
        cls._active_notifications.append(notification)
        
        # Limitar notificaciones activas
        cls._manage_notification_limits()
        
        return notification
    
    @classmethod
    def _remove_notification(cls, notification: NotificationWidget):
        """Elimina una notificación del seguimiento."""
        if notification in cls._active_notifications:
            cls._active_notifications.remove(notification)
    
    @classmethod
    def _manage_notification_limits(cls):
        """Gestiona el límite de notificaciones activas."""
        max_notifications = 3
        
        # Si hay demasiadas notificaciones, cerrar las más antiguas
        while len(cls._active_notifications) > max_notifications:
            oldest = cls._active_notifications[0]
            oldest.dismiss()  # Esto llamará a _remove_notification indirectamente
    
    @classmethod
    def clear_all(cls):
        """Cierra todas las notificaciones activas."""
        # Crear una copia para evitar problemas al modificar durante la iteración
        notifications = cls._active_notifications.copy()
        for notification in notifications:
            notification.dismiss()

# Funciones de conveniencia
def show_info(parent: QWidget, message: str, duration: int = 3000):
    """Muestra una notificación de información."""
    return NotificationManager.show_notification(parent, message, NotificationType.INFO, duration)

def show_success(parent: QWidget, message: str, duration: int = 3000):
    """Muestra una notificación de éxito."""
    return NotificationManager.show_notification(parent, message, NotificationType.SUCCESS, duration)

def show_warning(parent: QWidget, message: str, duration: int = 4000):
    """Muestra una notificación de advertencia."""
    return NotificationManager.show_notification(parent, message, NotificationType.WARNING, duration)

def show_error(parent: QWidget, message: str, duration: int = 5000):
    """Muestra una notificación de error."""
    return NotificationManager.show_notification(parent, message, NotificationType.ERROR, duration)