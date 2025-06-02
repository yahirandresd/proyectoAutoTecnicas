import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy, QSpacerItem, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Automatización")
        self.setMinimumSize(1000, 700)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a1a;
            }
        """)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal centrado
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(40)

        # Título
        titulo = QLabel("SISTEMA DE AUTOMATIZACIÓN")
        titulo.setFont(QFont("Arial", 32, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            QLabel {
                color: #00ffff;
                padding: 20px;
                background-color: rgba(10, 10, 26, 0.7);
                border-radius: 15px;
                border: 2px solid #00ffff;
                text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff;
            }
        """)
        main_layout.addWidget(titulo)

        # Estilo común para botones azules
        estilo_boton_azul = """
            QPushButton {
                background-color: #0066cc;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                border: 2px solid #00aaff;
                padding: 12px;
                text-shadow: 0 0 5px #00aaff;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #0088ff;
                border: 2px solid #00ffff;
                text-shadow: 0 0 10px #00ffff;
            }
            QPushButton:pressed {
                background-color: #0044aa;
                border: 2px solid #00aaff;
            }
        """

        # Botones
        btn_mision = QPushButton("MISIÓN INTERESTELAR")
        btn_patrulla = QPushButton("PATRULLA SINTÁCTICA")
        btn_salir = QPushButton("SALIR")

        for btn in [btn_mision, btn_patrulla]:
            btn.setStyleSheet(estilo_boton_azul)

        btn_salir.setStyleSheet("""
            QPushButton {
                background-color: #cc0000;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                border: 2px solid #ff3333;
                padding: 12px;
                text-shadow: 0 0 5px #ff3333;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #ff0000;
                border: 2px solid #ff6666;
                text-shadow: 0 0 10px #ff6666;
            }
            QPushButton:pressed {
                background-color: #990000;
                border: 2px solid #ff3333;
            }
        """)

        btn_mision.clicked.connect(self.abrir_mision_interestelar)
        btn_patrulla.clicked.connect(self.abrir_patrulla_sintactica)
        btn_salir.clicked.connect(self.close)

        # Widget contenedor para los botones
        contenedor_botones = QWidget()
        contenedor_botones.setMaximumWidth(400)  # Limita el ancho
        contenedor_botones_layout = QVBoxLayout(contenedor_botones)
        contenedor_botones_layout.setSpacing(20)

        for btn in [btn_mision, btn_patrulla, btn_salir]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            contenedor_botones_layout.addWidget(btn)

        # Layout para centrar el contenedor de botones horizontalmente
        centrar_horizontal = QHBoxLayout()
        centrar_horizontal.addStretch()
        centrar_horizontal.addWidget(contenedor_botones)
        centrar_horizontal.addStretch()

        main_layout.addLayout(centrar_horizontal)
        self.center()

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def abrir_mision_interestelar(self):
        try:
            ruta_mision = os.path.join(os.path.dirname(__file__), 'App', 'mision_interestelar', 'src', 'main.py')
            subprocess.Popen([sys.executable, ruta_mision])
            self.close()
        except Exception as e:
            print(f"Error al abrir Misión Interestelar: {e}")

    def abrir_patrulla_sintactica(self):
        try:
            ruta_patrulla = os.path.join(os.path.dirname(__file__), 'App', 'patrulla_sintactica', 'main.py')
            subprocess.Popen([sys.executable, ruta_patrulla])
            self.close()
        except Exception as e:
            print(f"Error al abrir Patrulla Sintáctica: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ventana = VentanaPrincipal()
    ventana.showMaximized()
    ventana.show()
    sys.exit(app.exec_())
