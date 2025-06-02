from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout,
      QMessageBox, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem)
from PyQt6.QtCore import Qt, QTimer
import os
from universo import Universo  # Asegúrate de que esta importación es correcta
from algoritmo import Algoritmo
from nave import Nave
import json

from PyQt6.QtGui import QPixmap

class UniversoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.universo = None
        self.setWindowTitle("Universo de Algoritmos - Misión Interestelar")
        self.setStyleSheet("background-color: #0e0e1a; color: white;")
        # Layout principal
        main_layout = QVBoxLayout(self)
        # Escena y vista gráfica para animar la nave
        self.escena = QGraphicsScene()
        self.vista = QGraphicsView(self.escena)
        main_layout.addWidget(self.vista)

        self.tam_celda = 25  # tamaño de cada celda para el dibujo
        # Configurar tamaño
        self.resize(1920, 1080)

        # Centrar ventana en la pantalla
        self.center_on_screen()


        # Layout para botón de carga (parte superior)
        cargar_layout = QHBoxLayout()
        self.btn_cargar = QPushButton("Cargar archivo JSON")
        self.btn_cargar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.btn_cargar.clicked.connect(self.abrir_explorador)
        cargar_layout.addStretch()
        cargar_layout.addWidget(self.btn_cargar)
        cargar_layout.addStretch()
        main_layout.addLayout(cargar_layout)

        # Layout para la matriz (centro)
        self.layout_matriz = QGridLayout()
        self.layout_matriz.setContentsMargins(10, 10, 10, 10)
        self.layout_matriz.setSpacing(3)

        # Mensaje "¡Universo Vacío!" en el centro
        self.label_vacio = QLabel("¡Universo Vacío!")
        self.label_vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_vacio.setStyleSheet("font-size: 24px; font-weight: bold; color: white; margin: 50px;")

        # Contenedor para matriz o mensaje
        matriz_container = QVBoxLayout()
        matriz_container.addWidget(self.label_vacio)
        matriz_container.addLayout(self.layout_matriz)
        main_layout.addLayout(matriz_container)

        # Layout para controles (parte inferior)
        controls_layout = QVBoxLayout()

        # Botón para iniciar recorrido
        self.iniciar_btn = QPushButton("Iniciar Recorrido")
        self.iniciar_btn.clicked.connect(self.iniciar_recorrido)
        self.iniciar_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
        self.iniciar_btn.setEnabled(False)  # Deshabilitado hasta que se cargue un universo
        controls_layout.addWidget(self.iniciar_btn)

        # Leyenda
        self.layout_leyenda = QVBoxLayout()
        self.leyenda = QLabel("Leyenda:")
        self.leyenda.setStyleSheet("font-size: 14px; color: white;")
        self.layout_leyenda.addWidget(self.leyenda)

        self.layout_leyenda.addWidget(QLabel("⭐ Estrella gigante"))
        self.layout_leyenda.addWidget(QLabel("🕳️ Agujero negro"))
        self.layout_leyenda.addWidget(QLabel("🌌 Agujero gusano"))
        self.layout_leyenda.addWidget(QLabel("🔑 Portal"))

        controls_layout.addLayout(self.layout_leyenda)
        main_layout.addLayout(controls_layout)

    def center_on_screen(self):
        """Centra la ventana en la pantalla."""
        # Obtener el rectángulo de la pantalla
        screen_geometry = self.screen().geometry()

        # Calcular el centro
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2

        # Mover la ventana al centro
        self.move(center_x, center_y)

    def abrir_explorador(self):
        # Abrir diálogo de selección de archivos
        ruta_archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo JSON",
            "",
            "Archivos JSON (*.json)"
        )

        if ruta_archivo:
            self.cargar_universo(ruta_archivo)

    def cargar_universo(self, ruta):
        try:
            # Cargar el universo con la ruta seleccionada
            self.universo = Universo(ruta)
                    # ✅ Crear la nave con su energía inicial
            self.nave = Nave(self.universo)

        # ✅ Pasar universo y nave al algoritmo
            self.algoritmo = Algoritmo(self.universo, self.nave)

           # Si tu algoritmo necesita usar la escena para animar
            self.algoritmo.configurar_grafica(self.escena, self.vista)

            # Ocultar el mensaje de universo vacío
            self.label_vacio.hide()

            # Habilitar el botón de iniciar recorrido
            self.iniciar_btn.setEnabled(True)

            # Cambiar el texto del botón cargar
            self.btn_cargar.setText("Cargar otro archivo")

            # Crear la matriz
            self.crear_matriz()

            print(f"Universo cargado desde: {ruta}")
        except Exception as e:
            print(f"Error al cargar el universo: {e}")
            self.label_vacio.setText(f"Error al cargar el archivo: {e}")
            self.label_vacio.show()

    def crear_matriz(self):
        # Limpiar matriz existente
        while self.layout_matriz.count():
            item = self.layout_matriz.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Crear nueva matriz
        for i in range(self.universo.filas):
            for j in range(self.universo.columnas):
                numero = self.universo.matrizInicial[i][j]
                simbolo = self.obtener_simbolo(i, j)
                contenido = f"{numero} {simbolo}" if simbolo else str(numero)
                celda = QLabel(contenido)
                celda.setFixedSize(25, 25)
                celda.setAlignment(Qt.AlignmentFlag.AlignCenter)
                celda.setStyleSheet(self.obtener_estilo_celda(i, j))
                self.layout_matriz.addWidget(celda, i, j)

    def obtener_simbolo(self, i, j):
        pos = [i, j]
        if pos == self.universo.origen:
            return "O"
        if pos == self.universo.destino:
            return "D"
        if pos in self.universo.agujerosNegros:
            return "🕳️"
        if pos in self.universo.estrellasGigantes:
            return "⭐"
        for gusano in self.universo.agujerosGusano:
            if pos == gusano['entrada'] or pos == gusano['salida']:
                return "🌌"
        for portal in self.universo.portales:
            if pos == portal['entrada'] or pos == portal['salida']:
                return "🔑"
        return ""

    def obtener_estilo_celda(self, i, j):
        pos = [i, j]
        if pos == self.universo.origen:
            return "background-color: green; border: 1px solid white;"
        if pos == self.universo.destino:
            return "background-color: red; border: 1px solid white;"
        if pos in self.universo.agujerosNegros:
            return "background-color: black; border: 1px solid white;"
        if pos in self.universo.estrellasGigantes:
            return "background-color: yellow; border: 1px solid white;"
        for gusano in self.universo.agujerosGusano:
            if pos == gusano['entrada'] or pos == gusano['salida']:
                return "background-color: blue; border: 1px solid white;"
        for portal in self.universo.portales:
            if pos == portal['entrada'] or pos == portal['salida']:
                return "background-color: orange; border: 1px solid white;"
        return "background-color: #1c1c2e; border: 1px solid gray;"
    
    def iniciar_recorrido(self):
     x = self.universo.origen[0]
     y = self.universo.origen[1]
     camino = []

    # Llamamos a backtracking sin pasar la energía ni el universo
     exito, camino = self.algoritmo.backtracking(x, y, camino, set())
     if exito:
        self.algoritmo.animar_camino(camino)
     else:
        QMessageBox.information(self, "Sin solución", "No existe una ruta válida desde el origen al destino.")
    def animar_camino(self, camino):
     self.paso = 0
     self.camino = camino
     self.timer = QTimer()
     self.timer.timeout.connect(self.mostrar_paso)
     self.timer.start(500)  # medio segundo por paso

    def mostrar_paso(self):
     if self.paso >= len(self.camino):
        self.timer.stop()
        return

     x, y = self.camino[self.paso]
     self.dibujar_nave_en(x, y)  # método tuyo que pinta la nave
     self.paso += 1

    def dibujar_nave_en(self, x, y):
     if hasattr(self, 'nave_actual') and self.nave_actual:
        self.escena.removeItem(self.nave_actual)

     item = QGraphicsPixmapItem(QPixmap("/assets/astronave.png").scaled(self.tam_celda, self.tam_celda))
     item.setPos(y * self.tam_celda, x * self.tam_celda)
     self.escena.addItem(item)
     self.nave_actual = item
