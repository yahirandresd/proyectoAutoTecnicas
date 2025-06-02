import sys
import os
from PyQt6.QtWidgets import QApplication
from ui import UniversoWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana_mision = UniversoWidget()
    ventana_mision.show()
    sys.exit(app.exec())
