from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton, 
                           QLabel, QFileDialog, QWidget, QHBoxLayout,
                           QStyle, QStyleFactory)
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import Qt
from afd_validator import ValidadorNeutrino
from code_editor import CodeEditor
import sys

class ValidadorNeutrinoGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.validador = ValidadorNeutrino()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Validador Neutrino - AFD")
        self.setMinimumSize(1000, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
            }
            QPushButton {
                background-color: #0D47A1;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QLabel {
                color: #D4D4D4;
                font-size: 14px;
            }
        """)

        # Layout principal
        main_layout = QVBoxLayout()
        
        # Barra de herramientas
        toolbar = QHBoxLayout()
        
        self.cargar_btn = QPushButton("📂 Cargar")
        self.cargar_btn.clicked.connect(self.cargar_archivo)
        
        self.validar_btn = QPushButton("✓ Validar")
        self.validar_btn.clicked.connect(self.validar)
        
        toolbar.addWidget(self.cargar_btn)
        toolbar.addWidget(self.validar_btn)
        toolbar.addStretch()
        
        # Editor de código personalizado
        self.text_area = CodeEditor()
        self.text_area.setPlaceholderText("// Escribe o carga tu código Neutrino aquí...")
        
        # Área de resultados
        self.resultado_label = QLabel("Estado: Esperando código para validar...")
        self.resultado_label.setWordWrap(True)
        self.resultado_label.setStyleSheet("""
            QLabel {
                background-color: #1E1E1E;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #3C3C3C;
            }
        """)

        # Agregar widgets al layout principal
        main_layout.addLayout(toolbar)
        main_layout.addWidget(self.text_area)
        main_layout.addWidget(self.resultado_label)

        # Widget contenedor
        contenedor = QWidget()
        contenedor.setLayout(main_layout)
        self.setCentralWidget(contenedor)

    def cargar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Abrir archivo", "", "Archivos de texto (*.txt)")
        if archivo:
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    self.text_area.setPlainText(contenido)
            except Exception as e:
                self.resultado_label.setText(f"❌ Error al cargar el archivo: {str(e)}")
                self.resultado_label.setStyleSheet("color: #ff5252;")

    def validar(self):
        codigo = self.text_area.toPlainText()
        errores = self.validador.validar_codigo(codigo)
        
        if errores:
            resultado = "❌ Se encontraron los siguientes errores:\n\n"
            for error in errores:
                resultado += f"• {error}\n"
            self.resultado_label.setStyleSheet("""
                QLabel {
                    background-color: #421616;
                    color: #ff5252;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
        else:
            resultado = "✅ El código es válido."
            self.resultado_label.setStyleSheet("""
                QLabel {
                    background-color: #1b4d1b;
                    color: #4caf50;
                    padding: 10px;
                    border-radius: 5px;
                }
            """)
        
        self.resultado_label.setText(resultado)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    ventana = ValidadorNeutrinoGUI()
    ventana.show()
    sys.exit(app.exec())
