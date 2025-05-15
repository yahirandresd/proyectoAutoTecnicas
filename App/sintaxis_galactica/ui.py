from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class SintaxisWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sintaxis Galáctica")
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Aquí puedes agregar la interfaz para Sintaxis Galáctica
        label = QLabel("Interfaz de Sintaxis Galáctica", self)
        layout.addWidget(label)

        self.setLayout(layout)
