#!/usr/bin/env python3
"""
Prueba de ventana extremadamente simple para diagnóstico.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLabel, QMessageBox
)

class SimpleTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configuración básica
        self.setWindowTitle("Prueba de Ventana")
        self.setGeometry(100, 100, 400, 300)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Etiqueta
        label = QLabel("¿Puedes ver esta ventana?", self)
        label.setStyleSheet("font-size: 16pt; color: black; background-color: white;")
        layout.addWidget(label)
        
        # Botón
        button = QPushButton("Haz clic aquí", self)
        button.setStyleSheet("font-size: 14pt; background-color: white; color: black;")
        button.clicked.connect(self.show_message)
        layout.addWidget(button)
        
    def show_message(self):
        QMessageBox.information(self, "Prueba", "El botón funciona correctamente!")

def main():
    app = QApplication(sys.argv)
    
    # Forzar estilo
    app.setStyle('Fusion')
    
    # Forzar stylesheet básico
    app.setStyleSheet("QMainWindow {background-color: white;}")
    
    # Mostrar mensaje previo
    QMessageBox.information(None, "Prueba", "¿Puedes ver este mensaje? A continuación se mostrará la ventana.")
    
    # Crear y mostrar ventana
    window = SimpleTestWindow()
    window.show()
    
    # Mostrar mensaje posterior
    QMessageBox.information(None, "Prueba", "¿La ventana está visible ahora?")
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()