"""
Tema simple y robusto para asegurar visibilidad de elementos.
"""

def get_simple_dark_stylesheet():
    """Retorna un stylesheet simple pero efectivo para tema oscuro."""
    return """
    /* ===== CONFIGURACIÓN GLOBAL ===== */
    QWidget {
        background-color: #2b2b2b;
        color: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 10pt;
    }
    
    /* ===== VENTANAS ===== */
    QMainWindow, QDialog, QWidget#LoginWindow {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    
    /* ===== LABELS ===== */
    QLabel {
        color: #ffffff;
        background-color: transparent;
        padding: 2px;
    }
    
    /* ===== INPUTS ===== */
    QLineEdit {
        background-color: #404040;
        color: #ffffff;
        border: 2px solid #555555;
        border-radius: 4px;
        padding: 8px;
        min-height: 20px;
    }
    
    QLineEdit:focus {
        border-color: #0078d4;
        background-color: #484848;
    }
    
    /* ===== BOTONES ===== */
    QPushButton {
        background-color: #0078d4;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        padding: 10px 20px;
        font-weight: bold;
        min-width: 100px;
        min-height: 30px;
    }
    
    QPushButton:hover {
        background-color: #106ebe;
    }
    
    QPushButton:pressed {
        background-color: #005a9e;
    }
    
    QPushButton:disabled {
        background-color: #555555;
        color: #888888;
    }
    
    /* ===== BOTONES SECUNDARIOS ===== */
    QPushButton[class="secondary"] {
        background-color: #6c757d;
        color: #ffffff;
    }
    
    QPushButton[class="secondary"]:hover {
        background-color: #545b62;
    }
    
    /* ===== FRAMES ===== */
    QFrame {
        background-color: transparent;
        border: none;
    }
    
    /* ===== FORMULARIOS ===== */
    QFormLayout {
        spacing: 10px;
    }
    
    /* ===== TÍTULOS ===== */
    QLabel#title {
        font-size: 18pt;
        font-weight: bold;
        color: #ffffff;
        margin: 10px 0px;
    }
    
    QLabel#subtitle {
        font-size: 12pt;
        color: #cccccc;
        margin: 5px 0px;
    }
    
    /* ===== MENSAJES DE ESTADO ===== */
    QLabel#status {
        padding: 8px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QLabel#status[class="error"] {
        background-color: #d13438;
        color: #ffffff;
    }
    
    QLabel#status[class="success"] {
        background-color: #107c10;
        color: #ffffff;
    }
    
    QLabel#status[class="info"] {
        background-color: #0078d4;
        color: #ffffff;
    }
    """

def apply_simple_theme(widget):
    """Aplica el tema simple a un widget."""
    widget.setStyleSheet(get_simple_dark_stylesheet())
    widget.setAutoFillBackground(True)