#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Universo de Algoritmos - Proyecto Principal
Aplicación de Autómatas y Técnicas de Programación

Este archivo es el punto de entrada principal de la aplicación.
"""

import sys
from PyQt5.QtWidgets import QApplication
from App.main_window import MainWindow  # Asegúrate de que 'App' esté en mayúscula


def main():
    """Función principal que inicia la aplicación."""
    app = QApplication(sys.argv)
    
    # Establecer información de la aplicación
    app.setApplicationName("Universo de Algoritmos")
    app.setOrganizationName("Estudiantes de Autómatas y Técnicas de Programación")
    
    # Crear y mostrar la ventana principal
    window = MainWindow()
    window.show()
    
    # Ejecutar el bucle principal de la aplicación
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()