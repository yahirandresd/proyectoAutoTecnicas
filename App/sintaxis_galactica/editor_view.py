"""
Vista del editor de código para el módulo Sintaxis Galáctica.
"""

import re
from tkinter.filedialog import FileDialog
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QMessageBox
)
from PyQt5.QtGui import QTextCursor, QColor, QSyntaxHighlighter, QTextCharFormat
from PyQt5.QtCore import Qt

from App.constants import (
    COLOR_BACKGROUND, COLOR_TEXT, COLOR_ACCENT,
    COLOR_ERROR, COLOR_SUCCESS, TEXT_LOAD_CODE,
    TEXT_VALIDATE_CODE, TEXT_CLEAR, TEXT_CODE_VALID,
    TEXT_CODE_INVALID
)
from App.sintaxis_galactica.lexer import Lexer, TokenType
from App.sintaxis_galactica.automaton import Automaton

class SyntaxHighlighter(QSyntaxHighlighter):
    """Resaltador de sintaxis para el editor de código."""
    
    def __init__(self, parent=None):
        super(SyntaxHighlighter, self).__init__(parent)
        self.highlighting_rules = []
        self._init_rules()
    
    def _init_rules(self):
        """Inicializa las reglas de resaltado."""
        # Palabras reservadas
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#88C0D0"))
        keywords = [
            "iniciar", "finalizar", "número", "para", "hasta",
            "hacer", "fin", "mostrar"
        ]
        for word in keywords:
            pattern = f"\\b{word}\\b"
            self.highlighting_rules.append((pattern, keyword_format))
        
        # Números
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B48EAD"))
        self.highlighting_rules.append(("\\b\\d+\\b", number_format))
        
        # Cadenas
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#A3BE8C"))
        self.highlighting_rules.append(('"[^"]*"', string_format))
        
        # Operadores
        operator_format = QTextCharFormat()
        operator_format.setForeground(QColor("#EBCB8B"))
        operators = [":=", ";", ",", "\\(", "\\)"]
        for op in operators:
            self.highlighting_rules.append((op, operator_format))
    
    def highlightBlock(self, text):
        """Aplica el resaltado de sintaxis al bloque de texto."""
        for pattern, format in self.highlighting_rules:
            for match in re.finditer(pattern, text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, format)

class EditorView(QWidget):
    """Vista del editor de código."""
    
    def __init__(self, parent=None):
        super(EditorView, self).__init__(parent)
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa la interfaz de usuario."""
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Editor de código
        self.editor = QTextEdit()
        self.editor.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLOR_BACKGROUND};
                color: {COLOR_TEXT};
                font-family: 'Consolas', monospace;
                font-size: 14px;
                padding: 10px;
            }}
        """)
        self.highlighter = SyntaxHighlighter(self.editor.document())
        layout.addWidget(self.editor)
        
        # Panel de controles
        control_layout = QHBoxLayout()
        
        # Botón para cargar código
        self.load_button = QPushButton(TEXT_LOAD_CODE)
        self.load_button.clicked.connect(self._on_load_code)
        control_layout.addWidget(self.load_button)
        
        # Botón para validar código
        self.validate_button = QPushButton(TEXT_VALIDATE_CODE)
        self.validate_button.clicked.connect(self._on_validate_code)
        control_layout.addWidget(self.validate_button)
        
        # Botón para limpiar
        self.clear_button = QPushButton(TEXT_CLEAR)
        self.clear_button.clicked.connect(self._on_clear)
        control_layout.addWidget(self.clear_button)
        
        layout.addLayout(control_layout)
        
        # Etiqueta de resultado
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        layout.addWidget(self.result_label)
    
    def set_code(self, code: str):
        """
        Establece el código en el editor.
        
        Args:
            code: Código a establecer
        """
        self.editor.setPlainText(code)
    
    def get_code(self) -> str:
        """
        Obtiene el código del editor.
        
        Returns:
            str: Código actual
        """
        return self.editor.toPlainText()
    
    def _on_load_code(self):
        """Maneja el evento de cargar código."""
        file_path, _ = FileDialog.getOpenFileName(
            self, "Cargar archivo de código", "", "Archivos de texto (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    code = file.read()
                self.set_code(code)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar el archivo: {str(e)}")
    
    def _on_validate_code(self):
        """Maneja el evento de validar código."""
        code = self.get_code()
        
        try:
            # Validar con el analizador léxico
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            
            # Validar con el autómata
            automaton = Automaton()
            valid = True
            
            for token in tokens:
                if token.type == TokenType.EOF:
                    break
                    
                for char in token.value:
                    if not automaton.process_char(char):
                        valid = False
                        break
                
                if not valid:
                    break
            
            if valid and automaton.is_accepting():
                self.result_label.setText(TEXT_CODE_VALID)
                self.result_label.setStyleSheet(f"color: {COLOR_SUCCESS}; font-weight: bold;")
            else:
                self.result_label.setText(TEXT_CODE_INVALID)
                self.result_label.setStyleSheet(f"color: {COLOR_ERROR}; font-weight: bold;")
                
        except Exception as e:
            self.result_label.setText(f"Error: {str(e)}")
            self.result_label.setStyleSheet(f"color: {COLOR_ERROR}; font-weight: bold;")
    
    def _on_clear(self):
        """Maneja el evento de limpiar el editor."""
        self.editor.clear()
        self.result_label.setText("")