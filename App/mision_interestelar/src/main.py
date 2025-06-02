import sys
import os
import json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDesktopWidget
from App.patrulla_sintactica import UniversoWidget
from App.sintaxis_galactica.ui import SintaxisWidget  # Asegúrate de tener este archivo para Sintaxis Galáctica
from universo import Universo
from PyQt5.QtCore import Qt


class VentanaInicial(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Seleccionar Módulo")
        self.setFixedSize(1280, 720)  # Tamaño fijo de la ventana

        # Centrar la ventana en la pantalla
        screen = QDesktopWidget().screenGeometry()  # Obtiene las dimensiones de la pantalla
        x = (screen.width() - self.width()) // 2  # Calcula la posición en X
        y = (screen.height() - self.height()) // 2  # Calcula la posición en Y
        self.move(x, y)  # Mueve la ventana al centro

        # Layout
        layout = QVBoxLayout()

        # Botón para "Misión Interestelar"
        boton_mision = QPushButton("Ir a Misión Interestelar", self)
        boton_mision.clicked.connect(self.ir_mision)
        # Aplicar estilo CSS a los botones
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
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s;
                max-width: 300px;  /* Limita el tamaño del botón */
                text-align: center;
                min-width: 150px;  /* Ajusta el tamaño mínimo del botón */
            }
            QPushButton:hover {
                background-color: #45a049;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #388e3c;
                transform: scale(1);
            }
        """)
        layout.addWidget(boton_mision, alignment=Qt.AlignCenter)

        # Botón para "Sintaxis Galáctica"
        boton_sintaxis = QPushButton("Ir a Sintaxis Galáctica", self)
        boton_sintaxis.clicked.connect(self.ir_sintaxis)
        # Aplicar estilo CSS a los botones
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
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s;
                max-width: 300px;  /* Limita el tamaño del botón */
                text-align: center;
                min-width: 150px;  /* Ajusta el tamaño mínimo del botón */
            }
            QPushButton:hover {
                background-color: #1976D2;
                transform: scale(1.05);
            }
            QPushButton:pressed {
                background-color: #1565C0;
                transform: scale(1);
            }
        """)
        layout.addWidget(boton_sintaxis, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    import os

    def ir_mision(self):
        try:
            ruta = os.path.join(os.path.dirname(__file__), '..', 'data', 'universo.json')
            universo = Universo(ruta)
            self.ventana_mision = UniversoWidget(universo)  # ← Aquí está el cambio
            self.ventana_mision.show()
            self.close()
            print("Misión Interestelar abierta correctamente.")
        except Exception as e:
            print(f"Error al abrir Misión Interestelar: {e}")

    def ir_sintaxis(self):
        # Iniciar la interfaz de "Sintaxis Galáctica"
        ventana_sintaxis = SintaxisWidget()  # Asegúrate de tener esta clase en la ruta correcta
        ventana_sintaxis.show()
        self.close()  # Cierra la ventana inicial

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_inicial = VentanaInicial()
    ventana_inicial.show()
    sys.exit(app.exec_())
