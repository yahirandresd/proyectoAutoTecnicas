import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QSizePolicy, QHBoxLayout,
    QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QTimer
from PyQt5.QtGui import QMovie, QColor


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mejor proyecto de la vida")
        self.setMinimumSize(1000, 700)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0a1a;
            }
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.animaciones = []  # para guardar animaciones y evitar que se destruyan

        # Layout principal
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(50, 20, 50, 50)  # Reducir el margen superior
        self.main_layout.setSpacing(20)  # Reducir el espacio entre elementos

        # Fondo animado
        fondo_label = QLabel(self)
        fondo_label.setGeometry(0, 0, 1920, 1080)
        fondo_label.setScaledContents(True)
        ruta_base = os.path.join(os.path.dirname(__file__), "App", "mision_interestelar", "assets")

        fondo_movie = QMovie(os.path.join(ruta_base, "space_background.gif"))
        fondo_label.setMovie(fondo_movie)
        fondo_movie.start()
        fondo_label.lower()

        # GIF decorativo
        gif_label = QLabel()
        gif_movie = QMovie(os.path.join(ruta_base, "kyle.gif"))
        
        # Configurar el GIF de Kyle
        gif_label.setMinimumSize(400, 300)  # Tamaño mínimo para asegurar visibilidad
        gif_label.setScaledContents(True)  # Permitir escalado del contenido
        gif_movie.setCacheMode(QMovie.CacheAll)  # Mejorar rendimiento
        gif_label.setMovie(gif_movie)
        gif_movie.start()
        
        # Contenedor para mantener la proporción del GIF
        gif_container = QWidget()
        gif_container_layout = QHBoxLayout(gif_container)
        gif_container_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes del contenedor
        gif_container_layout.addStretch()
        gif_container_layout.addWidget(gif_label)
        gif_container_layout.addStretch()
        
        # Asegurar que el GIF no se estire demasiado
        gif_label.setMaximumSize(600, 450)  # Limitar tamaño máximo
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.main_layout.addWidget(gif_container)

        # Crear botones
        self.btn_mision = QPushButton("MISIÓN INTERESTELAR")
        self.btn_patrulla = QPushButton("PATRULLA SINTÁCTICA")
        self.btn_salir = QPushButton("SALIR")

        self.botones = [self.btn_mision, self.btn_patrulla, self.btn_salir]

        self.btn_mision.setStyleSheet(self.estilo_boton_azul())
        self.btn_patrulla.setStyleSheet(self.estilo_boton_azul())
        self.btn_salir.setStyleSheet(self.estilo_boton_rojo())

        for btn in self.botones:
            self.agregar_sombra(btn)

        self.btn_mision.clicked.connect(self.abrir_mision_interestelar)
        self.btn_patrulla.clicked.connect(self.abrir_patrulla_sintactica)
        self.btn_salir.clicked.connect(self.close)

        contenedor_botones = QWidget()
        contenedor_botones.setMaximumWidth(400)
        contenedor_botones.setMinimumWidth(400)  # Asegurar un ancho fijo
        self.layout_botones = QVBoxLayout(contenedor_botones)
        self.layout_botones.setSpacing(15)
        self.layout_botones.setContentsMargins(0, 0, 0, 0)
        self.layout_botones.setAlignment(Qt.AlignCenter)  # Centrar los botones verticalmente

        for btn in self.botones:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.layout_botones.addWidget(btn)

        centrar_horizontal = QHBoxLayout()
        centrar_horizontal.setContentsMargins(0, 0, 0, 0)
        centrar_horizontal.setAlignment(Qt.AlignCenter)  # Centrar el contenedor horizontalmente
        centrar_horizontal.addWidget(contenedor_botones)

        self.main_layout.addLayout(centrar_horizontal)
        self.main_layout.addStretch()

        self.center()

        # Espera a que la ventana esté completamente mostrada antes de animar
        QTimer.singleShot(200, self.animar_botones)

    def estilo_boton_azul(self):
        return """
            QPushButton {
                background-color: #0066cc;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                border: 2px solid #00aaff;
                padding: 12px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #0088ff;
                border: 2px solid #00ffff;
            }
            QPushButton:pressed {
                background-color: #0044aa;
                border: 2px solid #00aaff;
            }
        """

    def estilo_boton_rojo(self):
        return """
            QPushButton {
                background-color: #cc0000;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 15px;
                border: 2px solid #ff3333;
                padding: 12px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #ff0000;
                border: 2px solid #ff6666;
            }
            QPushButton:pressed {
                background-color: #990000;
                border: 2px solid #ff3333;
            }
        """

    def agregar_sombra(self, boton):
        sombra = QGraphicsDropShadowEffect()
        sombra.setBlurRadius(25)
        sombra.setColor(QColor("#00ffff"))
        sombra.setOffset(0, 0)
        boton.setGraphicsEffect(sombra)

    def center(self):
        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def animar_botones(self):
        for i, btn in enumerate(self.botones):
            geo = btn.geometry()
            anim = QPropertyAnimation(btn, b"geometry")
            anim.setDuration(800)
            anim.setStartValue(QRect(geo.x(), geo.y() + 150, geo.width(), geo.height()))
            anim.setEndValue(geo)
            anim.setEasingCurve(QEasingCurve.OutBounce)
            anim.start()
            self.animaciones.append(anim)

    def abrir_mision_interestelar(self):
        try:
            ruta_mision = os.path.join(os.path.dirname(__file__), 'App', 'mision_interestelar', 'src', 'ui.py')
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
