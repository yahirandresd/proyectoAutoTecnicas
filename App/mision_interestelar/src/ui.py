from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class UniversoWidget(QWidget):
    def __init__(self, universo):
        super().__init__()
        self.universo = universo
        self.setWindowTitle("Universo de Algoritmos - Misión Interestelar")
        self.setStyleSheet("background-color: #0e0e1a; color: white;")

        main_layout = QVBoxLayout(self)

        self.layout_matriz = QGridLayout()
        self.layout_matriz.setContentsMargins(10, 10, 10, 10)
        self.layout_matriz.setSpacing(3)

        controls_layout = QVBoxLayout()
        self.layout_leyenda = QVBoxLayout()

        self.leyenda = QLabel("Leyenda:")
        self.leyenda.setStyleSheet("font-size: 14px; color: white;")
        self.layout_leyenda.addWidget(self.leyenda)

        self.layout_leyenda.addWidget(QLabel("⭐ Estrella gigante"))
        self.layout_leyenda.addWidget(QLabel("🕳️ Agujero negro"))
        self.layout_leyenda.addWidget(QLabel("🌌 Agujero gusano"))
        self.layout_leyenda.addWidget(QLabel("🔑 Portal"))

        self.iniciar_btn = QPushButton("Iniciar Recorrido")
        self.iniciar_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
        controls_layout.addWidget(self.iniciar_btn)

        main_layout.addLayout(self.layout_matriz)
        main_layout.addLayout(controls_layout)
        controls_layout.addLayout(self.layout_leyenda)

        self.crear_matriz()

    def crear_matriz(self):
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
