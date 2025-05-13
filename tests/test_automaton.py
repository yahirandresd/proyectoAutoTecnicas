"""
Pruebas unitarias para el autómata finito determinista.
"""

import pytest
from App.sintaxis_galactica.automaton import Automaton, State

def test_automaton_initial_state():
    """Prueba el estado inicial del autómata."""
    automaton = Automaton()
    assert automaton.current_state == State.INITIAL
    assert automaton.is_accepting() == False

def test_automaton_identifier():
    """Prueba el reconocimiento de identificadores."""
    automaton = Automaton()
    
    # Procesar "variable"
    assert automaton.process_char('v') == True
    assert automaton.process_char('a') == True
    assert automaton.process_char('r') == True
    assert automaton.process_char('i') == True
    assert automaton.process_char('a') == True
    assert automaton.process_char('b') == True
    assert automaton.process_char('l') == True
    assert automaton.process_char('e') == True
    assert automaton.is_accepting() == True

def test_automaton_number():
    """Prueba el reconocimiento de números."""
    automaton = Automaton()
    
    # Procesar "123"
    assert automaton.process_char('1') == True
    assert automaton.process_char('2') == True
    assert automaton.process_char('3') == True
    assert automaton.is_accepting() == True

def test_automaton_string():
    """Prueba el reconocimiento de cadenas."""
    automaton = Automaton()
    
    # Procesar '"Hola mundo"'
    assert automaton.process_char('"') == True
    assert automaton.process_char('H') == True
    assert automaton.process_char('o') == True
    assert automaton.process_char('l') == True
    assert automaton.process_char('a') == True
    assert automaton.process_char(' ') == True
    assert automaton.process_char('m') == True
    assert automaton.process_char('u') == True
    assert automaton.process_char('n') == True
    assert automaton.process_char('d') == True
    assert automaton.process_char('o') == True
    assert automaton.process_char('"') == True
    assert automaton.is_accepting() == True

def test_automaton_assignment():
    """Prueba el reconocimiento de asignaciones."""
    automaton = Automaton()
    
    # Procesar ":="
    assert automaton.process_char(':') == True
    assert automaton.process_char('=') == True
    assert automaton.is_accepting() == True

def test_automaton_invalid():
    """Prueba el manejo de caracteres inválidos."""
    automaton = Automaton()
    
    # Procesar "@"
    assert automaton.process_char('@') == False
    assert automaton.current_state == State.ERROR
    assert automaton.is_accepting() == False

def test_automaton_reset():
    """Prueba el reinicio del autómata."""
    automaton = Automaton()
    
    # Procesar algunos caracteres
    automaton.process_char('v')
    automaton.process_char('a')
    automaton.process_char('r')
    
    # Reiniciar
    automaton.reset()
    assert automaton.current_state == State.INITIAL