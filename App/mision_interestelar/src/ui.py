from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class UniversoWidget(QWidget):
    def __init__(self, universo):
        super().__init__()
        self.universo = universo
        self.setWindowTitle("Universo de Algoritmos - Misión Interestelar")
        self.setStyleSheet("background-color: #0e0e1a; color: white;")

        # Crear el layout principal
        main_layout = QVBoxLayout(self)

        # Crear el layout para la matriz
        self.layout_matriz = QGridLayout()
        self.layout_matriz.setContentsMargins(10, 10, 10, 10)
        self.layout_matriz.setSpacing(5)

        # Crear el layout para los controles (leyenda y botones)
        controls_layout = QVBoxLayout()
        self.layout_leyenda = QVBoxLayout()

        # Leyenda
        self.leyenda = QLabel("Leyenda:")
        self.leyenda.setStyleSheet("font-size: 14px; color: white;")
        self.layout_leyenda.addWidget(self.leyenda)

        self.leyenda_estrellasGigantes = QLabel("⭐ Estrella gigante")
        self.layout_leyenda.addWidget(self.leyenda_estrellasGigantes)

        self.leyenda_agujeros_negros = QLabel("🕳️ Agujero negro")
        self.layout_leyenda.addWidget(self.leyenda_agujeros_negros)

        self.leyenda_agujeros_gusano = QLabel("🌌 Agujero gusano")
        self.layout_leyenda.addWidget(self.leyenda_agujeros_gusano)

        self.leyenda_portales = QLabel("🔑 Portal")
        self.layout_leyenda.addWidget(self.leyenda_portales)

        # Botón para iniciar el recorrido
        self.iniciar_btn = QPushButton("Iniciar Recorrido")
        self.iniciar_btn.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px;")
        controls_layout.addWidget(self.iniciar_btn)

        # Agregar la matriz y los controles al layout principal
        main_layout.addLayout(self.layout_matriz)
        main_layout.addLayout(controls_layout)

        # Agregar la leyenda
        controls_layout.addLayout(self.layout_leyenda)

        self.crear_matriz()

    def crear_matriz(self):
        for i in range(self.universo.filas):
            for j in range(self.universo.columnas):
                numero = self.universo.matrizInicial[i][j]
                simbolo = self.obtener_simbolo(i, j)

                contenido = f"{numero} {simbolo}" if simbolo else str(numero)
                print(
                    f"Creando celda: ({i}, {j}) - Contenido: {contenido}")  # Para ver el contenido que se está añadiendo

                celda = QLabel(contenido)
                celda.setFixedSize(60, 60)  # Tamaño de la celda
                celda.setAlignment(Qt.AlignCenter)
                celda.setStyleSheet(self.obtener_estilo_celda(i, j))
                self.layout_matriz.addWidget(celda, i, j)

    def obtener_simbolo(self, i, j):
        # Verificar si es el origen
        if [i, j] == self.universo.origen:
            return "O"  # Origen
        # Verificar si es el destino
        if [i, j] == self.universo.destino:
            return "D"  # Destino
        # Agujeros negros
        if [i, j] in self.universo.agujerosNegros:
            return "🕳️"
        # estrellasGigantes gigantes
        if [i, j] in self.universo.estrellasGigantes:
            return "⭐"
        # Agujeros gusano
        if any([i, j] == entrada for entrada, _ in self.universo.agujerosGusano):
            return "🌌"
        # Portales
        if any([i, j] == desde for desde, _ in self.universo.portales):
            return "🔑"
        return ""  # Si no tiene símbolo

    def obtener_estilo_celda(self, i, j):
        if (i, j) == self.universo.origen:
            return "background-color: green; border: 1px solid white;"
        if (i, j) == self.universo.destino:
            return "background-color: red; border: 1px solid white;"
        if (i, j) in self.universo.agujerosNegros:
            return "background-color: black; border: 1px solid white;"
        if (i, j) in self.universo.estrellasGigantes:
            return "background-color: yellow; border: 1px solid white;"  # Estilo para estrella
        if any((i, j) == entrada for entrada, _ in self.universo.agujerosGusano):
            return "background-color: blue; border: 1px solid white;"  # Estilo para agujero gusano
        if any((i, j) == desde for desde, _ in self.universo.portales):
            return "background-color: orange; border: 1px solid white;"  # Estilo para portal
        return "background-color: #1c1c2e; border: 1px solid gray;"  # Fondo de celdas vacías
