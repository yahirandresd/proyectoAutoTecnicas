import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QMovie
from ui import UniversoWidget
from universo import Universo


class VentanaInicial(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Misión Interestelar")
        self.resize(1024, 768)

        # Centrar ventana en pantalla
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        # Fondo animado con GIF
        self.background_label = QLabel(self)
        gif_path = os.path.join(os.path.dirname(__file__), '../assets/galaxy.gif')
        self.movie = QMovie(gif_path)
        self.background_label.setMovie(self.movie)
        self.background_label.setGeometry(0, 0, 1024, 768)
        self.background_label.setScaledContents(True)
        self.movie.start()
        self.background_label.lower()  # Asegura que el fondo esté detrás

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
        boton_mision = QPushButton("Misión Interestelar", self)
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

        # Botón "Sintaxis Galáctica"
        boton_sintaxis = QPushButton("patrulla sintactica", self)
        boton_sintaxis.clicked.connect(self.ir_sintaxis)
        boton_sintaxis.setFixedSize(300, 80)
        boton_sintaxis.setStyleSheet("""
            QPushButton {
                background-color: #0d47a1;
                color: #fff;
                font-size: 18px;
                font-weight: 900;
                border: 2px solid #002171;
                border-radius: 15px;
                padding: 20px 30px;
                margin: 10px;
                text-shadow: 1px 1px 4px #000;
            }
            QPushButton:hover {
                background-color: #1976d2;
                border: 2px solid #0d47a1;
            }
            QPushButton:pressed {
                background-color: #08306b;
                border: 2px solid #002171;
            }
        """)
        layout.addWidget(boton_sintaxis, alignment=Qt.AlignmentFlag.AlignCenter)

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

    def ir_sintaxis(self):
        try:
            from App.patrulla_sintactica.ui.main_window import MainWindow
            self.ventana_sintaxis = MainWindow()
            self.ventana_sintaxis.show()
            self.close()
            print("Sintaxis Galáctica abierta correctamente.")
        except Exception as e:
            print(f"Error al abrir Sintaxis Galáctica: {e}")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.background_label.setGeometry(0, 0, self.width(), self.height())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_inicial = VentanaInicial()
    ventana_inicial.show()
    sys.exit(app.exec())
