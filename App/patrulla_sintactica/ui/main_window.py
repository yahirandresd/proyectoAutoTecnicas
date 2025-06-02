from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, 
                           QLabel, QTabWidget, QFrame, QHBoxLayout, QFileDialog,
                           QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from validators.credit_card_validator import validate_matricula, crear_afd_matricula
from validators.curp_validator import validate_curp, crear_afd_curp

class ModernButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)

class ValidatorWidget(QWidget):
    def __init__(self, title, validate_func, afd_creator):
        super().__init__()
        self.validate_func = validate_func
        self.afd_creator = afd_creator

        # Contenedor principal con sombra
        main_container = QFrame()
        main_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
        """)
        main_container.setObjectName("mainContainer")
        main_container.setStyleSheet("""
            #mainContainer {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Título con estilo moderno
        self.title_label = QLabel(f"<h2 style='color: #1976D2; margin-bottom: 10px;'>{title}</h2>")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1976D2;")
        
        # Botón para cargar archivo
        self.load_file_btn = ModernButton("Cargar Archivo")
        self.load_file_btn.clicked.connect(self.load_file)
        
        # Área de resultados
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setStyleSheet("""
            QTextEdit {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                color: #333;
            }
        """)
        self.result_text.setMinimumHeight(400)

        layout.addWidget(self.title_label)
        layout.addWidget(self.load_file_btn)
        layout.addWidget(self.result_text)
        layout.addStretch()

        main_container.setLayout(layout)
        
        # Layout principal del widget
        main_layout = QVBoxLayout()
        main_layout.addWidget(main_container)
        self.setLayout(main_layout)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Archivos de texto (*.txt);;Todos los archivos (*.*)"
        )
        
        if file_name:
            try:
                # Crear el AFD correspondiente
                afd = self.afd_creator()
                
                # Validar todas las cadenas
                resultados = afd.validar_archivo(file_name)
                
                # Mostrar resultados
                self.result_text.clear()
                for resultado in resultados:
                    self.result_text.append(f"\nLínea {resultado['linea']}: {resultado['cadena']}")
                    if resultado['es_valida']:
                        self.result_text.append("✅ VÁLIDO")
                    else:
                        self.result_text.append(f"❌ INVÁLIDO")
                        self.result_text.append(f"  Error en posición {resultado['posicion_error']}: {resultado['razon_error']}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al procesar el archivo: {str(e)}")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Validador Profesional AFD")
        self.resize(800, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: none;
                background-color: #f5f5f5;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #666;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #1976D2;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background-color: #f0f0f0;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título principal
        title = QLabel("Validador Profesional AFD")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #1976D2;
                margin-bottom: 20px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: none;
            }
        """)

        # Agregar pestañas con validadores
        self.tabs.addTab(
            ValidatorWidget("Validador de Matrícula", validate_matricula, crear_afd_matricula),
            "Matrícula Universitaria"
        )
        self.tabs.addTab(
            ValidatorWidget("Validador de CURP", validate_curp, crear_afd_curp),
            "CURP"
        )

        layout.addWidget(title)
        layout.addWidget(self.tabs)
        self.setLayout(layout)
