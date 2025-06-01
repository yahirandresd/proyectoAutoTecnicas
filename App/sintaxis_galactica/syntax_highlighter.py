from PyQt6.QtCore import Qt
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont

class NeutrinoHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Definir formatos de colores
        self.formats = {
            'keyword': self.create_format("#C586C0"),  # Morado para palabras clave
            'types': self.create_format("#569CD6"),    # Azul para tipos
            'operators': self.create_format("#D4D4D4"), # Blanco para operadores
            'strings': self.create_format("#CE9178"),   # Naranja para cadenas
            'numbers': self.create_format("#B5CEA8"),   # Verde claro para números
            'comments': self.create_format("#6A9955")   # Verde para comentarios
        }

        # Palabras clave del lenguaje Neutrino
        self.keywords = ['iniciar', 'finalizar', 'si', 'entonces', 'sino', 
                        'fin', 'mientras', 'hacer', 'para', 'hasta']
        self.types = ['número', 'cadena', 'booleano']
        self.operators = [':=', '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=',
                         'y', 'o', 'no']

    def create_format(self, color, style=''):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if 'bold' in style:
            fmt.setFontWeight(QFont.Weight.Bold)
        if 'italic' in style:
            fmt.setFontItalic(True)
        return fmt

    def highlightBlock(self, text):
        # Resaltar palabras clave
        for word in self.keywords:
            index = text.find(word)
            while index >= 0:
                length = len(word)
                self.setFormat(index, length, self.formats['keyword'])
                index = text.find(word, index + length)

        # Resaltar tipos
        for word in self.types:
            index = text.find(word)
            while index >= 0:
                length = len(word)
                self.setFormat(index, length, self.formats['types'])
                index = text.find(word, index + length)

        # Resaltar operadores
        for op in self.operators:
            index = text.find(op)
            while index >= 0:
                length = len(op)
                self.setFormat(index, length, self.formats['operators'])
                index = text.find(op, index + length)

        # Resaltar cadenas
        quote_index = text.find('"')
        while quote_index >= 0:
            end_quote = text.find('"', quote_index + 1)
            if end_quote == -1:
                break
            length = end_quote - quote_index + 1
            self.setFormat(quote_index, length, self.formats['strings'])
            quote_index = text.find('"', end_quote + 1)

        # Resaltar números
        import re
        for match in re.finditer(r'\b\d+\b', text):
            self.setFormat(match.start(), match.end() - match.start(), 
                          self.formats['numbers'])