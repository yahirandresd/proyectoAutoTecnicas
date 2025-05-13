"""
Módulo que implementa la ventana principal de la aplicación.
"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QVBoxLayout, QWidget,
    QMessageBox, QAction, QFileDialog
)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt

from App.constants import (
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT, 
    TAB_MISION, TAB_SINTAXIS
)
from App.mision_intelestelar.universe_controller import UniverseController
from App.sintaxis_galactica.editor_view import EditorView


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación Universo de Algoritmos.
    Contiene los dos módulos del proyecto en pestañas separadas.
    """
    
    def __init__(self):
        """Inicializa la ventana principal."""
        super(MainWindow, self).__init__()
        
        # Configuración de la ventana
        self.setWindowTitle("Universo de Algoritmos")
        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        
        # Inicializar la UI
        self._init_ui()
        self._create_menu_bar()
        
    def _init_ui(self):
        """Inicializa los componentes de la interfaz de usuario."""
        # Widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Widget de pestañas
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Pestaña 1: Misión Interestelar
        self.universe_controller = UniverseController()
        self.tab_widget.addTab(self.universe_controller.get_view(), TAB_MISION)
        
        # Pestaña 2: Sintaxis Galáctica
        self.editor_view = EditorView()
        self.tab_widget.addTab(self.editor_view, TAB_SINTAXIS)
        
    def _create_menu_bar(self):
        """Crea la barra de menú de la aplicación."""
        menu_bar = self.menuBar()
        
        # Menú Archivo
        file_menu = menu_bar.addMenu("&Archivo")
        
        # Acción: Cargar Universo
        load_universe_action = QAction("Cargar &Universo", self)
        load_universe_action.setShortcut(QKeySequence("Ctrl+U"))
        load_universe_action.triggered.connect(self._on_load_universe)
        file_menu.addAction(load_universe_action)
        
        # Acción: Cargar Código
        load_code_action = QAction("Cargar &Código", self)
        load_code_action.setShortcut(QKeySequence("Ctrl+L"))
        load_code_action.triggered.connect(self._on_load_code)
        file_menu.addAction(load_code_action)
        
        file_menu.addSeparator()
        
        # Acción: Salir
        exit_action = QAction("&Salir", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Menú Ayuda
        help_menu = menu_bar.addMenu("A&yuda")
        
        # Acción: Acerca de
        about_action = QAction("&Acerca de", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)
        
    def _on_load_universe(self):
        """Maneja la acción de cargar un archivo de universo."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Cargar archivo de universo", "", "Archivos JSON (*.json)"
        )
        
        if file_path:
            try:
                self.universe_controller.load_universe_from_file(file_path)
                self.tab_widget.setCurrentIndex(0)  # Cambiar a la pestaña de universo
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar el universo: {str(e)}")
    
    def _on_load_code(self):
        """Maneja la acción de cargar un archivo de código."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Cargar archivo de código", "", "Archivos de texto (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    code = file.read()
                self.editor_view.set_code(code)
                self.tab_widget.setCurrentIndex(1)  # Cambiar a la pestaña de código
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar el archivo: {str(e)}")
    
    def _show_about_dialog(self):
        """Muestra el diálogo 'Acerca de'."""
        about_text = (
            "Universo de Algoritmos\n\n"
            "Proyecto para la materia de Autómatas y Técnicas de Programación.\n\n"
            "Desarrollado por:\n"
            "- [Tu Nombre]\n"
            "- [Nombre del Compañero 1]\n"
            "- [Nombre del Compañero 2]\n\n"
            "© 2025"
        )
        
        QMessageBox.about(self, "Acerca de Universo de Algoritmos", about_text)