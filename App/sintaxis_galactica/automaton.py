"""
Implementación del autómata finito determinista para el lenguaje Neutrino.
"""

from enum import Enum
from typing import Dict, Set, List, Optional

class State(Enum):
    """Estados del autómata."""
    INITIAL = 0
    IDENTIFIER = 1
    NUMBER = 2
    STRING = 3
    ASSIGNMENT = 4
    SEMICOLON = 5
    COMMA = 6
    PARENTHESIS = 7
    ERROR = 8
    FINAL = 9

class Automaton:
    """Autómata finito determinista para validar la sintaxis del lenguaje Neutrino."""
    
    def __init__(self):
        """Inicializa el autómata."""
        self.current_state = State.INITIAL
        self.transitions = self._build_transition_table()
        self.accepting_states = {State.IDENTIFIER, State.NUMBER, State.STRING, 
                               State.ASSIGNMENT, State.SEMICOLON, State.COMMA, 
                               State.PARENTHESIS, State.FINAL}
    
    def _build_transition_table(self) -> Dict[State, Dict[str, State]]:
        """Construye la tabla de transiciones del autómata."""
        transitions = {
            State.INITIAL: {
                'letter': State.IDENTIFIER,
                'digit': State.NUMBER,
                '"': State.STRING,
                ':': State.ASSIGNMENT,
                ';': State.SEMICOLON,
                ',': State.COMMA,
                '(': State.PARENTHESIS,
                ')': State.PARENTHESIS,
                'space': State.INITIAL,
                'other': State.ERROR
            },
            State.IDENTIFIER: {
                'letter': State.IDENTIFIER,
                'digit': State.IDENTIFIER,
                '_': State.IDENTIFIER,
                'other': State.FINAL
            },
            State.NUMBER: {
                'digit': State.NUMBER,
                'other': State.FINAL
            },
            State.STRING: {
                'any': State.STRING,
                '"': State.FINAL
            },
            State.ASSIGNMENT: {
                '=': State.FINAL,
                'other': State.ERROR
            },
            State.SEMICOLON: {
                'any': State.FINAL
            },
            State.COMMA: {
                'any': State.FINAL
            },
            State.PARENTHESIS: {
                'any': State.FINAL
            },
            State.ERROR: {
                'any': State.ERROR
            },
            State.FINAL: {
                'any': State.INITIAL
            }
        }
        return transitions
    
    def _get_char_type(self, char: str) -> str:
        """Determina el tipo de carácter para la transición."""
        if char.isalpha():
            return 'letter'
        elif char.isdigit():
            return 'digit'
        elif char == '_':
            return '_'
        elif char == '"':
            return '"'
        elif char == ':':
            return ':'
        elif char == '=':
            return '='
        elif char == ';':
            return ';'
        elif char == ',':
            return ','
        elif char in '()':
            return char
        elif char.isspace():
            return 'space'
        else:
            return 'other'
    
    def process_char(self, char: str) -> bool:
        """
        Procesa un carácter y actualiza el estado del autómata.
        
        Args:
            char: Carácter a procesar
            
        Returns:
            bool: True si el carácter es válido, False en caso contrario
        """
        char_type = self._get_char_type(char)
        
        if self.current_state == State.STRING and char != '"':
            return True
        
        if char_type in self.transitions[self.current_state]:
            self.current_state = self.transitions[self.current_state][char_type]
        else:
            self.current_state = State.ERROR
        
        return self.current_state != State.ERROR
    
    def is_accepting(self) -> bool:
        """
        Verifica si el estado actual es de aceptación.
        
        Returns:
            bool: True si el estado es de aceptación, False en caso contrario
        """
        return self.current_state in self.accepting_states
    
    def reset(self) -> None:
        """Reinicia el autómata a su estado inicial."""
        self.current_state = State.INITIAL