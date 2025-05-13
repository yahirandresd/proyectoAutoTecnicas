"""
Analizador léxico para el lenguaje Neutrino.
"""

from enum import Enum
from typing import List, Tuple, Optional

class TokenType(Enum):
    """Tipos de tokens en el lenguaje Neutrino."""
    INICIAR = "iniciar"
    FINALIZAR = "finalizar"
    NUMERO = "número"
    IDENTIFICADOR = "identificador"
    ASIGNACION = ":="
    PARA = "para"
    HASTA = "hasta"
    HACER = "hacer"
    FIN = "fin"
    MOSTRAR = "mostrar"
    PUNTO_COMA = ";"
    COMA = ","
    PARENTESIS_IZQ = "("
    PARENTESIS_DER = ")"
    CADENA = "cadena"
    EOF = "EOF"

class Token:
    """Representa un token en el código fuente."""
    
    def __init__(self, type: TokenType, value: str, line: int, column: int):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __str__(self) -> str:
        return f"Token({self.type}, '{self.value}', línea={self.line}, columna={self.column})"

class Lexer:
    """Analizador léxico para el lenguaje Neutrino."""
    
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[0] if source else None
    
    def advance(self) -> None:
        """Avanza al siguiente carácter en el código fuente."""
        self.position += 1
        self.column += 1
        
        if self.position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.position]
            
            if self.current_char == '\n':
                self.line += 1
                self.column = 1
    
    def skip_whitespace(self) -> None:
        """Salta los espacios en blanco y saltos de línea."""
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self) -> None:
        """Salta los comentarios de una línea."""
        while self.current_char and self.current_char != '\n':
            self.advance()
    
    def read_identifier(self) -> str:
        """Lee un identificador o palabra reservada."""
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return result
    
    def read_number(self) -> str:
        """Lee un número."""
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return result
    
    def read_string(self) -> str:
        """Lee una cadena de texto."""
        result = ''
        self.advance()  # Salta la comilla inicial
        
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        
        if self.current_char == '"':
            self.advance()  # Salta la comilla final
        else:
            raise SyntaxError(f"Error en línea {self.line}, columna {self.column}: Cadena sin cerrar")
        
        return result
    
    def get_next_token(self) -> Token:
        """Obtiene el siguiente token del código fuente."""
        while self.current_char:
            # Salta espacios en blanco
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Salta comentarios
            if self.current_char == '#':
                self.skip_comment()
                continue
            
            # Identificadores y palabras reservadas
            if self.current_char.isalpha():
                identifier = self.read_identifier()
                token_type = TokenType.IDENTIFICADOR
                
                # Verifica si es una palabra reservada
                for type in TokenType:
                    if type.value == identifier:
                        token_type = type
                        break
                
                return Token(token_type, identifier, self.line, self.column - len(identifier))
            
            # Números
            if self.current_char.isdigit():
                number = self.read_number()
                return Token(TokenType.NUMERO, number, self.line, self.column - len(number))
            
            # Cadenas
            if self.current_char == '"':
                string = self.read_string()
                return Token(TokenType.CADENA, string, self.line, self.column - len(string) - 2)
            
            # Operadores y delimitadores
            if self.current_char == ':':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.ASIGNACION, ":=", self.line, self.column - 2)
                raise SyntaxError(f"Error en línea {self.line}, columna {self.column}: ':' inválido")
            
            if self.current_char == ';':
                self.advance()
                return Token(TokenType.PUNTO_COMA, ";", self.line, self.column - 1)
            
            if self.current_char == ',':
                self.advance()
                return Token(TokenType.COMA, ",", self.line, self.column - 1)
            
            if self.current_char == '(':
                self.advance()
                return Token(TokenType.PARENTESIS_IZQ, "(", self.line, self.column - 1)
            
            if self.current_char == ')':
                self.advance()
                return Token(TokenType.PARENTESIS_DER, ")", self.line, self.column - 1)
            
            raise SyntaxError(f"Error en línea {self.line}, columna {self.column}: Carácter inválido '{self.current_char}'")
        
        return Token(TokenType.EOF, "", self.line, self.column)
    
    def tokenize(self) -> List[Token]:
        """Tokeniza todo el código fuente."""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens