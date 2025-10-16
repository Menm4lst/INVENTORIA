"""
Dashboard Avanzado para EXPANSION DE DOMINIO - INVENTORIA
Sistema completo de métricas y estadísticas con tema oscuro elegante.
"""

import os
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import sqlite3

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QProgressBar, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QLinearGradient, QPixmap, QIcon

class MetricCard(QFrame):
    """Tarjeta elegante para mostrar métricas individuales."""
    
    clicked = pyqtSignal()
    
    def __init__(self, title: str, value: str, subtitle: str = "", icon: str = "📊", color: str = "#4a9eff"):
        super().__init__()
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.icon = icon
        self.color = color
        self.setup_ui()
        self.setup_animation()
    
    def setup_ui(self):
        """Configura la interfaz de la tarjeta."""
        self.setFixedSize(280, 120)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(5)
        
        # Header con ícono y título
        header_layout = QHBoxLayout()
        
        # Ícono
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet(f"""
            font-size: 24px;
            color: {self.color};
            background: transparent;
        """)
        header_layout.addWidget(icon_label)
        
        # Título
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            font-size: 12px;
            font-weight: 600;
            color: #b0b0b0;
            background: transparent;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Valor principal
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"""
            font-size: 28px;
            font-weight: bold;
            color: {self.color};
            background: transparent;
        """)
        layout.addWidget(self.value_label)
        
        # Subtítulo
        if self.subtitle:
            subtitle_label = QLabel(self.subtitle)
            subtitle_label.setStyleSheet("""
                font-size: 10px;
                color: #808080;
                background: transparent;
            """)
            layout.addWidget(subtitle_label)
        
        # Estilo de la tarjeta
        self.setStyleSheet(f"""
            MetricCard {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2a2a2a, stop:1 #1f1f1f);
                border: 1px solid #3a3a3a;
                border-radius: 12px;
            }}
            MetricCard:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3a3a3a, stop:1 #2f2f2f);
                border: 1px solid {self.color};
            }}
        """)
        
        # Sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 3)
        self.setGraphicsEffect(shadow)
    
    def setup_animation(self):
        """Configura animación de hover."""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def enterEvent(self, event):
        """Animación al pasar el mouse."""
        current = self.geometry()
        new_rect = QRect(current.x(), current.y() - 2, current.width(), current.height())
        self.animation.setStartValue(current)
        self.animation.setEndValue(new_rect)
        self.animation.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        """Animación al salir el mouse."""
        current = self.geometry()
        new_rect = QRect(current.x(), current.y() + 2, current.width(), current.height())
        self.animation.setStartValue(current)
        self.animation.setEndValue(new_rect)
        self.animation.start()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """Emite señal al hacer clic."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
    
    def update_value(self, new_value: str, new_subtitle: str = ""):
        """Actualiza el valor mostrado en la tarjeta."""
        self.value_label.setText(new_value)
        if new_subtitle:
            self.subtitle = new_subtitle


class ChartWidget(QWidget):
    """Widget para mostrar gráficos personalizados."""
    
    def __init__(self, chart_type: str = "bar", data: Dict[str, int] = None):
        super().__init__()
        self.chart_type = chart_type
        self.data = data or {}
        # Tamaño mayor para gráfico circular para acomodar la leyenda
        if chart_type == "pie":
            self.setMinimumSize(400, 250)
        else:
            self.setMinimumSize(300, 200)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del gráfico."""
        self.setStyleSheet("""
            ChartWidget {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
            }
        """)
    
    def paintEvent(self, event):
        """Dibuja el gráfico personalizado."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Fondo
        painter.fillRect(self.rect(), QColor(42, 42, 42))
        
        if not self.data:
            # Mensaje de sin datos
            painter.setPen(QPen(QColor(160, 160, 160)))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Sin datos disponibles")
            return
        
        if self.chart_type == "bar":
            self.draw_bar_chart(painter)
        elif self.chart_type == "pie":
            self.draw_pie_chart(painter)
    
    def draw_bar_chart(self, painter: QPainter):
        """Dibuja un gráfico de barras."""
        if not self.data:
            return
            
        margin = 40
        chart_width = self.width() - 2 * margin
        chart_height = self.height() - 2 * margin
        
        max_value = max(self.data.values()) if self.data.values() else 1
        bar_width = chart_width // len(self.data) - 10
        colors = ["#4a9eff", "#28a745", "#ffc107", "#dc3545", "#17a2b8", "#6f42c1"]
        
        x = margin
        for i, (label, value) in enumerate(self.data.items()):
            # Altura de la barra
            bar_height = (value / max_value) * chart_height if max_value > 0 else 0
            
            # Color de la barra
            color = QColor(colors[i % len(colors)])
            
            # Gradiente para la barra
            gradient = QLinearGradient(0, 0, 0, bar_height)
            gradient.setColorAt(0, color.lighter(120))
            gradient.setColorAt(1, color)
            
            # Dibujar barra
            painter.setBrush(QBrush(gradient))
            painter.setPen(QPen(color, 2))
            bar_rect = QRect(x, self.height() - margin - int(bar_height), bar_width, int(bar_height))
            painter.drawRoundedRect(bar_rect, 4, 4)
            
            # Etiqueta
            painter.setPen(QPen(QColor(224, 224, 224)))
            painter.drawText(x, self.height() - 5, bar_width, 20, 
                           Qt.AlignmentFlag.AlignCenter, label[:8])
            
            # Valor
            painter.drawText(x, self.height() - margin - int(bar_height) - 20, bar_width, 20,
                           Qt.AlignmentFlag.AlignCenter, str(value))
            
            x += bar_width + 10
    
    def draw_pie_chart(self, painter: QPainter):
        """Dibuja un gráfico circular con leyenda."""
        if not self.data:
            return
        
        # Dibujar título del gráfico
        painter.setPen(QPen(QColor(255, 255, 255)))
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        painter.setFont(title_font)
        painter.drawText(10, 20, "Distribución por Estado")
            
        # Ajustar posición para dejar espacio a la leyenda y título
        center_x = self.width() // 2 - 60
        center_y = self.height() // 2 + 10  # Un poco más abajo por el título
        radius = min(center_x, center_y) - 70
        
        total = sum(self.data.values())
        if total == 0:
            return
            
        # Colores específicos para cada estado
        color_map = {
            'Aprobadas': '#28a745',    # Verde
            'Pendientes': '#ffc107',   # Amarillo
            'Rechazadas': '#dc3545'    # Rojo
        }
        
        start_angle = 0
        legend_y = 30
        
        for i, (label, value) in enumerate(self.data.items()):
            # Calcular ángulo
            span_angle = (value / total) * 360 * 16  # PyQt usa 1/16 de grado
            
            # Color específico para cada estado
            color_hex = color_map.get(label, "#4a9eff")
            color = QColor(color_hex)
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color.darker(110), 2))
            
            # Dibujar sector
            painter.drawPie(center_x - radius, center_y - radius, 
                          radius * 2, radius * 2, int(start_angle), int(span_angle))
            
            # Dibujar leyenda en el lado derecho
            legend_x = center_x + radius + 20
            
            # Cuadrito de color
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(color, 1))
            painter.drawRoundedRect(legend_x, legend_y + i * 25, 12, 12, 2, 2)
            
            # Texto de la leyenda con íconos
            painter.setPen(QPen(QColor(224, 224, 224)))
            font = QFont()
            font.setPointSize(10)
            painter.setFont(font)
            
            # Íconos para cada estado
            icon_map = {
                'Aprobadas': '✅',
                'Pendientes': '⏳',
                'Rechazadas': '❌'
            }
            
            icon = icon_map.get(label, '📊')
            percentage = (value / total * 100) if total > 0 else 0
            legend_text = f"{icon} {label}: {value} ({percentage:.1f}%)"
            painter.drawText(legend_x + 20, legend_y + i * 25 + 10, legend_text)
            
            start_angle += span_angle
    
    def update_data(self, new_data: Dict[str, int]):
        """Actualiza los datos del gráfico."""
        self.data = new_data
        self.update()


class DashboardWidget(QWidget):
    """Widget principal del dashboard con todas las métricas."""
    
    def __init__(self, db_path: str = "homologaciones.db"):
        super().__init__()
        self.db_path = db_path
        self.metrics_cards = {}
        self.charts = {}
        self.setup_ui()
        self.setup_timer()
        self.load_data()
    
    def setup_ui(self):
        """Configura la interfaz principal del dashboard."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Título del dashboard
        title_layout = QHBoxLayout()
        title = QLabel("📊 Dashboard - EXPANSION DE DOMINIO - INVENTORIA")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4a9eff;
            background: transparent;
            padding: 10px;
        """)
        title_layout.addWidget(title)
        
        # Botón de actualizar
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.clicked.connect(self.load_data)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5aafff;
            }
        """)
        title_layout.addWidget(refresh_btn)
        title_layout.addStretch()
        
        main_layout.addLayout(title_layout)
        
        # Scroll area para todo el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(20)
        
        # Grid de tarjetas de métricas
        self.setup_metrics_cards(scroll_layout)
        
        # Sección de gráficos
        self.setup_charts_section(scroll_layout)
        
        # Información adicional
        self.setup_info_section(scroll_layout)
        
        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)
        
        # Estilo del widget principal
        self.setStyleSheet("""
            DashboardWidget {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
        """)
    
    def setup_metrics_cards(self, layout: QVBoxLayout):
        """Configura las tarjetas de métricas principales."""
        # Título de sección
        section_title = QLabel("📈 Métricas Principales")
        section_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #e0e0e0;
            background: transparent;
            margin-bottom: 10px;
        """)
        layout.addWidget(section_title)
        
        # Grid de tarjetas
        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)
        
        # Crear tarjetas
        self.metrics_cards['total'] = MetricCard("Total Homologaciones", "0", "Todas las aplicaciones", "📱", "#4a9eff")
        self.metrics_cards['approved'] = MetricCard("Aprobadas", "0", "Listas para producción", "✅", "#28a745")
        self.metrics_cards['pending'] = MetricCard("Pendientes", "0", "En proceso de revisión", "⏳", "#ffc107")
        self.metrics_cards['rejected'] = MetricCard("Rechazadas", "0", "Requieren corrección", "❌", "#dc3545")
        self.metrics_cards['this_month'] = MetricCard("Este Mes", "0", "Homologaciones nuevas", "📅", "#17a2b8")
        self.metrics_cards['avg_time'] = MetricCard("Tiempo Promedio", "0 días", "Duración del proceso", "⏰", "#6f42c1")
        self.metrics_cards['apps_percent'] = MetricCard("APPS%", "0", "Aplicaciones APPS%", "🔧", "#ff6b6b")
        self.metrics_cards['aesa'] = MetricCard("AESA", "0", "Aplicaciones AESA", "✈️", "#4ecdc4")
        
        # Posicionar tarjetas en grid (ahora con 8 tarjetas, 3 columnas)
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]
        for i, (card_key, card) in enumerate(self.metrics_cards.items()):
            row, col = positions[i] if i < len(positions) else (i // 3, i % 3)
            cards_layout.addWidget(card, row, col)
            
            # Conectar eventos
            card.clicked.connect(lambda key=card_key: self.on_card_clicked(key))
        
        layout.addLayout(cards_layout)
    
    def setup_charts_section(self, layout: QVBoxLayout):
        """Configura la sección de gráficos."""
        # Título de sección
        section_title = QLabel("📊 Análisis Visual")
        section_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #e0e0e0;
            background: transparent;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        layout.addWidget(section_title)
        
        # Layout horizontal para gráficos
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Gráfico de barras - Homologaciones por mes
        bar_frame = QFrame()
        bar_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        bar_layout = QVBoxLayout(bar_frame)
        
        bar_title = QLabel("Homologaciones por Mes")
        bar_title.setStyleSheet("font-weight: bold; color: #e0e0e0; font-size: 14px;")
        bar_layout.addWidget(bar_title)
        
        self.charts['monthly'] = ChartWidget("bar")
        bar_layout.addWidget(self.charts['monthly'])
        
        # Gráfico circular - Estados
        pie_frame = QFrame()
        pie_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        pie_layout = QVBoxLayout(pie_frame)
        
        pie_title = QLabel("Distribución por Estado")
        pie_title.setStyleSheet("font-weight: bold; color: #e0e0e0; font-size: 14px;")
        pie_layout.addWidget(pie_title)
        
        self.charts['status'] = ChartWidget("pie")
        pie_layout.addWidget(self.charts['status'])
        
        charts_layout.addWidget(bar_frame)
        charts_layout.addWidget(pie_frame)
        layout.addLayout(charts_layout)
    
    def setup_info_section(self, layout: QVBoxLayout):
        """Configura la sección de información adicional."""
        # Título de sección
        section_title = QLabel("ℹ️ Información del Sistema")
        section_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #e0e0e0;
            background: transparent;
            margin-top: 20px;
            margin-bottom: 10px;
        """)
        layout.addWidget(section_title)
        
        # Frame de información
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border: 1px solid #3a3a3a;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        
        # Información del sistema
        self.system_info = QLabel()
        self.system_info.setStyleSheet("""
            color: #b0b0b0;
            font-size: 12px;
            line-height: 1.4;
        """)
        info_layout.addWidget(self.system_info)
        
        layout.addWidget(info_frame)
    
    def setup_timer(self):
        """Configura timer para actualización automática."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(30000)  # Actualizar cada 30 segundos
    
    def load_data(self):
        """Carga todos los datos del dashboard."""
        try:
            # Obtener métricas de la base de datos
            metrics = self.get_database_metrics()
            
            # Actualizar tarjetas
            self.update_metric_cards(metrics)
            
            # Actualizar gráficos
            self.update_charts(metrics)
            
            # Actualizar información del sistema
            self.update_system_info()
            
        except Exception as e:
            print(f"Error cargando datos del dashboard: {e}")
    
    def get_database_metrics(self) -> Dict[str, Any]:
        """Obtiene métricas de la base de datos."""
        metrics = {
            'total': 0,
            'approved': 0,
            'pending': 0,
            'rejected': 0,
            'this_month': 0,
            'apps_percent': 0,
            'aesa': 0,
            'avg_time': 0,
            'monthly_data': {},
            'status_data': {}
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de homologaciones
            cursor.execute("SELECT COUNT(*) FROM homologations")
            metrics['total'] = cursor.fetchone()[0]
            
            # Contadores por estado usando el campo status
            cursor.execute("SELECT COUNT(*) FROM homologations WHERE status = 'Aprobada'")
            approved_count = cursor.fetchone()[0]
            metrics['approved'] = approved_count
            
            cursor.execute("SELECT COUNT(*) FROM homologations WHERE status = 'Pendiente'")
            pending_count = cursor.fetchone()[0]
            metrics['pending'] = pending_count
            
            cursor.execute("SELECT COUNT(*) FROM homologations WHERE status = 'Rechazada'")
            rejected_count = cursor.fetchone()[0]
            metrics['rejected'] = rejected_count
            
            # APPS% - buscar en repository_location, real_name o logical_name
            cursor.execute("""
                SELECT COUNT(*) FROM homologations 
                WHERE repository_location = 'APPS$' 
                OR UPPER(real_name) LIKE '%APPS%' 
                OR UPPER(logical_name) LIKE '%APPS%'
            """)
            apps_count = cursor.fetchone()[0]
            metrics['apps_percent'] = apps_count
            
            # AESA - buscar en repository_location, real_name o logical_name
            cursor.execute("""
                SELECT COUNT(*) FROM homologations 
                WHERE repository_location = 'AESA' 
                OR UPPER(real_name) LIKE '%AESA%' 
                OR UPPER(logical_name) LIKE '%AESA%'
            """)
            aesa_count = cursor.fetchone()[0]
            metrics['aesa'] = aesa_count
            
            # Este mes
            first_day = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            cursor.execute("SELECT COUNT(*) FROM homologations WHERE created_at >= ?", (first_day,))
            result = cursor.fetchone()
            metrics['this_month'] = result[0] if result else 0
            
            # Datos mensuales para gráfico
            cursor.execute("""
                SELECT strftime('%Y-%m', created_at) as month, COUNT(*) 
                FROM homologations 
                WHERE created_at >= date('now', '-6 months')
                GROUP BY month 
                ORDER BY month
            """)
            monthly_results = cursor.fetchall()
            
            for month, count in monthly_results:
                if month:
                    month_name = datetime.strptime(month + '-01', '%Y-%m-%d').strftime('%b %Y')
                    metrics['monthly_data'][month_name] = count
            
            # Datos de estado para gráfico circular
            metrics['status_data'] = {
                'Aprobadas': metrics['approved'],
                'Pendientes': metrics['pending'], 
                'Rechazadas': metrics['rejected']
            }
            
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Error de base de datos: {e}")
        except Exception as e:
            print(f"Error obteniendo métricas: {e}")
            
        return metrics
    
    def update_metric_cards(self, metrics: Dict[str, Any]):
        """Actualiza las tarjetas de métricas."""
        try:
            self.metrics_cards['total'].update_value(str(metrics.get('total', 0)))
            self.metrics_cards['approved'].update_value(str(metrics.get('approved', 0)))
            self.metrics_cards['pending'].update_value(str(metrics.get('pending', 0)))
            self.metrics_cards['rejected'].update_value(str(metrics.get('rejected', 0)))
            self.metrics_cards['this_month'].update_value(str(metrics.get('this_month', 0)))
            self.metrics_cards['apps_percent'].update_value(str(metrics.get('apps_percent', 0)))
            self.metrics_cards['aesa'].update_value(str(metrics.get('aesa', 0)))
            
            # Tiempo promedio (simplificado)
            avg_days = metrics.get('avg_time', 0)
            self.metrics_cards['avg_time'].update_value(f"{avg_days} días")
        except Exception as e:
            print(f"Error actualizando tarjetas de métricas: {e}")
    
    def update_charts(self, metrics: Dict[str, Any]):
        """Actualiza los gráficos."""
        # Gráfico mensual
        if metrics['monthly_data']:
            self.charts['monthly'].update_data(metrics['monthly_data'])
        
        # Gráfico de estados
        if metrics['status_data']:
            # Solo mostrar estados con datos
            filtered_status = {k: v for k, v in metrics['status_data'].items() if v > 0}
            self.charts['status'].update_data(filtered_status)
    
    def update_system_info(self):
        """Actualiza la información del sistema."""
        try:
            db_size = os.path.getsize(self.db_path) / 1024  # KB
            last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            info_text = f"""
            📁 Base de datos: {db_size:.1f} KB
            🕐 Última actualización: {last_update}
            💾 Archivo: {os.path.basename(self.db_path)}
            🔄 Actualización automática: Cada 30 segundos
            """
            
            self.system_info.setText(info_text.strip())
            
        except Exception as e:
            self.system_info.setText(f"Error obteniendo información: {e}")
    
    def on_card_clicked(self, card_key: str):
        """Maneja clics en las tarjetas de métricas."""
        print(f"Tarjeta clickeada: {card_key}")
        # Aquí se puede agregar funcionalidad específica por tarjeta
        # Por ejemplo, abrir filtros, mostrar detalles, etc.


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # Aplicar tema oscuro global
    app.setStyleSheet("""
        QWidget {
            background-color: #1a1a1a;
            color: #e0e0e0;
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    """)
    
    dashboard = DashboardWidget()
    dashboard.show()
    
    sys.exit(app.exec())