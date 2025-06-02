import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDesktopWidget# Asegúrate de tener este archivo para Sintaxis Galáctica
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize

from PyQt6.QtWidgets import QApplication
from ui import UniversoWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_mision = UniversoWidget()
    ventana_mision.show()
    sys.exit(app.exec())
