import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt6.QtCore import Qt
from ui import UniversoWidget
from universo import Universo


class VentanaInicial(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Seleccionar Módulo")
        self.setFixedSize(1920, 1080)

        # Centrar ventana en pantalla usando QScreen (PyQt6)
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

        # Layout principal
        layout = QVBoxLayout()

        # Botón "Misión Interestelar"
        boton_mision = QPushButton("Ir a Misión Interestelar", self)
        boton_mision.clicked.connect(self.ir_mision)
        boton_mision.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: 2px solid #388E3C;
                border-radius: 8px;
                padding: 12px 20px;
                margin: 10px;
                max-width: 300px;
                min-width: 150px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        layout.addWidget(boton_mision, alignment=Qt.AlignmentFlag.AlignCenter)

        # Botón "Sintaxis Galáctica"
        boton_sintaxis = QPushButton("Ir a Sintaxis Galáctica", self)
        boton_sintaxis.clicked.connect(self.ir_sintaxis)
        boton_sintaxis.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border: 2px solid #1976D2;
                border-radius: 8px;
                padding: 12px 20px;
                margin: 10px;
                max-width: 300px;
                min-width: 150px;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        layout.addWidget(boton_sintaxis, alignment=Qt.AlignmentFlag.AlignCenter)

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
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_inicial = VentanaInicial()
    ventana_inicial.show()
    sys.exit(app.exec())
