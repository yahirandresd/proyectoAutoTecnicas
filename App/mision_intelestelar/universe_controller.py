"""
Controlador para la vista del universo en el módulo Misión Interestelar.
"""

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QObject

from App.mision_intelestelar.universe_model import UniverseModel
from App.mision_intelestelar.universe_view import UniverseView
from App.mision_intelestelar.backtracking import BacktrackingPathfinder
from App.constants import (
    ELEMENTO_ORIGEN, ELEMENTO_DESTINO, ELEMENTO_AGUJERO_NEGRO,
    ELEMENTO_ESTRELLA_GIGANTE, ELEMENTO_PORTAL_ENTRADA, ELEMENTO_PORTAL_SALIDA,
    ELEMENTO_GUSANO_ENTRADA, ELEMENTO_GUSANO_SALIDA, ELEMENTO_RECARGA,
    ELEMENTO_CARGA_REQUERIDA, ELEMENTO_VACIO, ELEMENTO_EXPLORADO,
    DEFAULT_UNIVERSE_FILE
)


class UniverseController(QObject):
    """
    Controlador que gestiona la interacción entre el modelo y la vista del universo.
    Coordina las acciones del usuario con la lógica del algoritmo de backtracking.
    """
    
    def __init__(self):
        """Inicializa el controlador del universo."""
        super(UniverseController, self).__init__()
        
        # Crear modelo y vista
        self.model = UniverseModel()
        self.view = UniverseView()
        self.pathfinder = None
        
        # Conectar señales
        self._connect_signals()
        
        # Intentar cargar un universo de ejemplo
        try:
            self.load_universe_from_file(DEFAULT_UNIVERSE_FILE)
        except Exception:
            pass  # No hacer nada si falla la carga del archivo de ejemplo
    
    def _connect_signals(self):
        """Conecta las señales de la vista con los métodos del controlador."""
        self.view.load_button.clicked.connect(self._on_load_universe)
        self.view.search_button.clicked.connect(self._on_start_search)
        self.view.step_button.clicked.connect(self._on_step_animation)
    
    def get_view(self):
        """
        Obtiene la referencia a la vista.
        
        Returns:
            UniverseView: Referencia a la vista
        """
        return self.view
    
    def load_universe_from_file(self, file_path):
        """
        Carga el universo desde un archivo JSON.
        
        Args:
            file_path: Ruta al archivo JSON que contiene los datos del universo
        """
        try:
            # Cargar el modelo desde el archivo
            self.model.load_from_file(file_path)
            
            # Actualizar la vista con la nueva matriz
            self._update_universe_view()
            
            # Crear un nuevo buscador de caminos
            self.pathfinder = BacktrackingPathfinder(self.model)
            
            # Actualizar etiqueta de energía
            self.view.update_energy_label(self.model.initial_energy)
            self.view.update_steps_label(0)
            self.view.result_label.setText("")
            
            # Habilitar el botón de búsqueda
            self.view.search_button.setEnabled(True)
            self.view.step_button.setEnabled(False)
            
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al cargar el universo: {str(e)}")
            raise
    
    def _update_universe_view(self):
        """Actualiza la vista con el estado actual del modelo."""
        # Crear la matriz en la vista
        self.view.create_universe_grid(self.model.rows, self.model.cols)
        
        # Actualizar todas las celdas
        for row in range(self.model.rows):
            for col in range(self.model.cols):
                pos = (row, col)
                cell_type = self.model.get_cell_type(pos)
                energy_cost = self.model.get_energy
    
    def _on_load_universe(self):
        """Maneja el evento de cargar un universo desde archivo."""
        file_path, _ = QFileDialog.getOpenFileName(
        self.view, "Cargar archivo de universo", "", "Archivos JSON (*.json)"
        )
    
        if file_path:
            try:
                self.load_universe_from_file(file_path)
            except Exception as e:
                QMessageBox.critical(self.view, "Error", f"Error al cargar el universo: {str(e)}")
                
    def _on_start_search(self):
        """Maneja el evento de iniciar la búsqueda."""
        if self.pathfinder:
            self.pathfinder.solve()
            self.view.show_result(self.pathfinder.solution_found)
            if self.pathfinder.solution_found:
                self.view.set_solution_path(self.pathfinder.solution_path)
                self.view.step_button.setEnabled(True)

    def _on_step_animation(self):
        """Maneja el evento de animación paso a paso."""
        self.view.start_animation()