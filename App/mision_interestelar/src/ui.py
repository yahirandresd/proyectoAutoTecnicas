from PyQt6.QtWidgets import (QWidget, QGridLayout, QLabel, QVBoxLayout, QPushButton, QFileDialog, QHBoxLayout,
      QMessageBox, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QTimer, QSize
import os
from universo import Universo
from algoritmo import Algoritmo
from nave import Nave
import json
from PyQt6.QtGui import QPixmap, QFont, QPalette, QColor

class UniversoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.universo = None
        self.setWindowTitle("Universo de Algoritmos - Misión Interestelar")
        self.setStyleSheet("""
            QWidget {
                background-color: #0e0e1a;
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 8px 15px;
                border-radius: 5px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Panel superior
        top_panel = QHBoxLayout()
        
        # Botones del panel superior
        self.btn_cargar = QPushButton("Cargar JSON")
        self.btn_cargar.clicked.connect(self.abrir_explorador)
        
        self.btn_iniciar = QPushButton("Iniciar Recorrido")
        self.btn_iniciar.clicked.connect(self.iniciar_recorrido)
        self.btn_iniciar.setEnabled(False)
        
        self.btn_reiniciar = QPushButton("Reiniciar")
        self.btn_reiniciar.clicked.connect(self.reiniciar_simulacion)
        self.btn_reiniciar.setEnabled(False)
        
        # Información de energía
        self.energia_label = QLabel("Energía: N/A")
        self.energia_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 0.7);
                padding: 10px;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        # Añadir widgets al panel superior
        top_panel.addWidget(self.btn_cargar)
        top_panel.addWidget(self.btn_iniciar)
        top_panel.addWidget(self.btn_reiniciar)
        top_panel.addStretch()
        top_panel.addWidget(self.energia_label)
        
        main_layout.addLayout(top_panel)

        # Panel central con vista del universo y leyenda
        central_panel = QHBoxLayout()
        
        # Contenedor para la matriz
        matriz_container = QVBoxLayout()
        
        # Escena y vista gráfica
        self.escena = QGraphicsScene()
        self.vista = QGraphicsView(self.escena)
        self.vista.setMinimumSize(800, 600)
        self.vista.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.vista.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        matriz_container.addWidget(self.vista)
        
        # Mensaje "¡Universo Vacío!"
        self.label_vacio = QLabel("¡Universo Vacío!")
        self.label_vacio.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_vacio.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin: 50px;
        """)
        matriz_container.addWidget(self.label_vacio)
        
        central_panel.addLayout(matriz_container, stretch=4)

        # Panel de leyenda y estadísticas
        info_panel = QVBoxLayout()
        
        # Leyenda
        leyenda_frame = QFrame()
        leyenda_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        leyenda_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        leyenda_layout = QVBoxLayout(leyenda_frame)
        
        leyenda_titulo = QLabel("Leyenda")
        leyenda_titulo.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        leyenda_layout.addWidget(leyenda_titulo)
        
        leyendas = [
            ("O", "Origen", "#4CAF50"),
            ("D", "Destino", "#f44336"),
            ("⭐", "Estrella Gigante", "#FFD700"),
            ("🕳️", "Agujero Negro", "#000000"),
            ("🌌", "Agujero Gusano", "#0000FF"),
            ("⚡", "Zona Recarga", "#00FFFF")
        ]
        
        for simbolo, texto, color in leyendas:
            item_layout = QHBoxLayout()
            simbolo_label = QLabel(simbolo)
            simbolo_label.setStyleSheet(f"font-size: 16px; color: {color}; font-weight: bold;")
            texto_label = QLabel(texto)
            item_layout.addWidget(simbolo_label)
            item_layout.addWidget(texto_label)
            item_layout.addStretch()
            leyenda_layout.addLayout(item_layout)
        
        info_panel.addWidget(leyenda_frame)
        
        # Log de eventos
        self.log_text = QLabel("Log de eventos:")
        self.log_text.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 5px;
            font-family: monospace;
            min-height: 200px;
        """)
        self.log_text.setWordWrap(True)
        
        # Scroll area para el log
        scroll = QScrollArea()
        scroll.setWidget(self.log_text)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        info_panel.addWidget(scroll)
        info_panel.addStretch()
        
        central_panel.addLayout(info_panel, stretch=1)
        main_layout.addLayout(central_panel)

        self.tam_celda = 25
        self.resize(1200, 800)
        self.center_on_screen()

    def center_on_screen(self):
        screen_geometry = self.screen().geometry()
        center_x = (screen_geometry.width() - self.width()) // 2
        center_y = (screen_geometry.height() - self.height()) // 2
        self.move(center_x, center_y)

    def abrir_explorador(self):
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
            self.universo = Universo(ruta)
            self.nave = Nave(self.universo)
            self.algoritmo = Algoritmo(self.universo, self.nave)
            self.algoritmo.configurar_grafica(self.escena, self.vista)

            self.label_vacio.hide()
            self.btn_iniciar.setEnabled(True)
            self.btn_reiniciar.setEnabled(True)
            self.btn_cargar.setText("Cargar otro JSON")
            self.energia_label.setText(f"Energía: {self.nave.energia}")
            
            self.actualizar_log("Universo cargado correctamente")
            self.actualizar_log(f"Energía inicial: {self.nave.energia}")
            print(f"Universo cargado desde: {ruta}")
            
        except Exception as e:
            print(f"Error al cargar el universo: {e}")
            self.label_vacio.setText(f"Error al cargar el archivo: {e}")
            self.label_vacio.show()
            self.actualizar_log(f"Error: {str(e)}")

    def iniciar_recorrido(self):
        self.btn_iniciar.setEnabled(False)
        self.btn_cargar.setEnabled(False)
        x = self.universo.origen[0]
        y = self.universo.origen[1]

        self.actualizar_log("Iniciando búsqueda de camino...")
        self.actualizar_log(f"Energía inicial: {self.nave.energia}")
        self.actualizar_log("Origen: " + str(self.universo.origen))
        self.actualizar_log("Destino: " + str(self.universo.destino))
        
        exito, camino = self.algoritmo.iniciar_busqueda(x, y)
        
        if exito:
            self.actualizar_log(f"¡Camino encontrado! Longitud: {len(camino)} pasos")
            self.actualizar_log(f"Energía final: {self.nave.energia}")
            
            # Mostrar el log detallado del camino
            log_detallado = self.algoritmo.obtener_log_camino()
            self.actualizar_log("\nRegistro detallado del camino:")
            for linea in log_detallado.split('\n')[1:]:  # Saltamos la primera línea que es el título
                self.actualizar_log(linea)
            
            self.algoritmo.animar_camino(camino)
        else:
            QMessageBox.warning(self, "Sin solución", 
                "No se encontró una ruta válida desde el origen al destino.\n" +
                "Esto puede deberse a:\n" +
                "- Insuficiente energía para completar el recorrido\n" +
                "- Obstáculos bloqueando todas las rutas posibles\n" +
                "- Complejidad excesiva del mapa\n\n" +
                "Sugerencias:\n" +
                "- Verifica la distribución de zonas de recarga\n" +
                "- Asegúrate de que los agujeros negros pueden ser destruidos\n" +
                "- Considera aumentar la energía inicial")
            self.actualizar_log("No se encontró un camino válido")
            self.btn_iniciar.setEnabled(True)
            self.btn_cargar.setEnabled(True)

    def reiniciar_simulacion(self):
        if self.universo:
            self.nave.reiniciar()
            self.algoritmo = Algoritmo(self.universo, self.nave)
            self.algoritmo.configurar_grafica(self.escena, self.vista)
            self.energia_label.setText(f"Energía: {self.nave.energia}")
            self.btn_iniciar.setEnabled(True)
            self.btn_cargar.setEnabled(True)
            self.actualizar_log("Simulación reiniciada")

    def actualizar_log(self, mensaje):
        texto_actual = self.log_text.text()
        if texto_actual == "Log de eventos:":
            nuevo_texto = f"Log de eventos:\n• {mensaje}"
        else:
            nuevo_texto = f"{texto_actual}\n• {mensaje}"
        self.log_text.setText(nuevo_texto)
        
    def closeEvent(self, event):
        # Limpiar recursos antes de cerrar
        if hasattr(self, 'algoritmo') and self.algoritmo.timer:
            self.algoritmo.timer.stop()
        event.accept()
