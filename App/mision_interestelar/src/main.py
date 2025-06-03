import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QDesktopWidget
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QFont, QPalette, QColor, QMovie
from ui import UniversoWidget

class VentanaInicial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Misión Interestelar")
        
        # Obtener el tamaño de la pantalla
        screen = QDesktopWidget().screenGeometry()
        # Establecer el tamaño de la ventana al 80% del tamaño de la pantalla
        window_width = int(screen.width() * 0.8)
        window_height = int(screen.height() * 0.8)
        self.resize(window_width, window_height)

        # Centrar ventana en pantalla
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        # Configurar el fondo animado
        self.background_label = QLabel(self)
        self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_base = os.path.dirname(os.path.dirname(__file__))
        gif_path = os.path.join(ruta_base, "assets", "galaxy.gif")
        self.movie = QMovie(gif_path)
        
        # Configurar el GIF para que se ajuste proporcionalmente
        self.movie.setCacheMode(QMovie.CacheMode.CacheAll)
        self.background_label.setMovie(self.movie)
        self.movie.start()
        
        # Ajustar el tamaño y posición del label de fondo
        self.background_label.setGeometry(0, 0, window_width, window_height)
        self.background_label.setScaledContents(True)
        self.background_label.lower()

        # Establecer el estilo del widget principal para el fondo negro
        self.setStyleSheet("background-color: black;")

        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        # Título
        titulo = QLabel("MISIÓN INTERESTELAR")
        titulo.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        titulo.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 0.3);
                padding: 20px;
                border-radius: 15px;
                border: 2px solid rgba(255, 255, 255, 0.2);
            }
        """)
        layout.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botón "Misión Interestelar"
        boton_mision = QPushButton("Ir a Misión Interestelar", self)
        boton_mision.clicked.connect(self.ir_mision)
        boton_mision.setFixedSize(300, 80)
        boton_mision.setStyleSheet("""
            QPushButton {
                background-color: #225c2c;
                color: #fff;
                font-size: 18px;
                font-weight: 900;
                border: 2px solid #0d2c13;
                border-radius: 15px;
                padding: 20px 30px;
                margin: 10px;
                text-shadow: 1px 1px 4px #000;
            }
            QPushButton:hover {
                background-color: #2e7d32;
                border: 2px solid #1b5e20;
            }
            QPushButton:pressed {
                background-color: #1b4020;
                border: 2px solid #0d2c13;
            }
        """)
        layout.addWidget(boton_mision, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botón "Salir"
        boton_salir = QPushButton("Salir", self)
        boton_salir.clicked.connect(QApplication.instance().quit)
        boton_salir.setFixedSize(300, 80)
        boton_salir.setStyleSheet("""
            QPushButton {
                background-color: #b71c1c;
                color: #fff;
                font-size: 18px;
                font-weight: 900;
                border: 2px solid #7f0000;
                border-radius: 15px;
                padding: 20px 30px;
                margin: 10px;
                text-shadow: 1px 1px 4px #000;
            }
            QPushButton:hover {
                background-color: #d32f2f;
                border: 2px solid #b71c1c;
            }
            QPushButton:pressed {
                background-color: #7f0000;
                border: 2px solid #7f0000;
            }
        """)
        layout.addWidget(boton_salir, alignment=Qt.AlignmentFlag.AlignCenter)

        # Añadir espacio al final
        layout.addStretch()

        # Establecer el layout principal en la ventana
        self.setLayout(layout)

    def ir_mision(self):
        try:
            self.ventana_mision = UniversoWidget()
            self.ventana_mision.show()
            self.close()
            print("Misión Interestelar abierta correctamente.")
        except Exception as e:
            print(f"Error al abrir Misión Interestelar: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_inicial = VentanaInicial()
    ventana_inicial.show()
    sys.exit(app.exec())
