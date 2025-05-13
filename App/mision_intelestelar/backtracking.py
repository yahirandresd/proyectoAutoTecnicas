"""
Implementación del algoritmo de backtracking para resolver la misión interestelar.
"""

from typing import List, Tuple, Set, Dict, Optional
import copy
from App.mision_intelestelar.universe_model import UniverseModel


class BacktrackingPathfinder:
    """
    Implementa el algoritmo de backtracking recursivo para encontrar una ruta
    desde el origen hasta el destino en el universo.
    """
    
    def __init__(self, universe_model: UniverseModel):
        """
        Inicializa el algoritmo con un modelo de universo.
        
        Args:
            universe_model: Modelo del universo a explorar
        """
        self.universe = universe_model
        self.solution_path = []
        self.explored_cells = set()
        self.steps = 0
        self.solution_found = False
        self.path_memory = {}  # Para evitar repetir cálculos en caminos ya explorados
        
    def solve(self) -> bool:
        """
        Inicia el algoritmo de backtracking para encontrar una solución.
        
        Returns:
            bool: True si se encontró una solución, False en caso contrario
        """
        # Reiniciar estado
        self.solution_path = []
        self.explored_cells = set()
        self.steps = 0
        self.solution_found = False
        self.path_memory = {}
        
        # Crear una copia del universo para no modificar el original durante la búsqueda
        universe_copy = copy.deepcopy(self.universe)
        
        # Iniciar la búsqueda desde la posición de origen con la energía inicial
        initial_energy = universe_copy.initial_energy
        initial_pos = universe_copy.origin
        
        # Manejar estrellas gigantes - destruir agujeros negros adyacentes
        self._process_giant_stars(universe_copy)
        
        # Comenzar la búsqueda recursiva
        path = []
        self.solution_found = self._backtrack(universe_copy, initial_pos, initial_energy, path)
        
        # Si se encontró una solución, actualizar el modelo principal
        if self.solution_found:
            self.universe.set_solution(self.solution_path, self.explored_cells)
            
        return self.solution_found
    
    def _process_giant_stars(self, universe: UniverseModel) -> None:
        """
        Procesa las estrellas gigantes y destruye un agujero negro adyacente a cada una.
        
        Args:
            universe: Modelo del universo a modificar
        """
        for star_pos in list(universe.giant_stars):
            black_hole_pos = universe.has_adjacent_black_hole(star_pos)
            if black_hole_pos:
                universe.destroy_black_hole(black_hole_pos)
    
    def _backtrack(
        self, 
        universe: UniverseModel, 
        current_pos: Tuple[int, int], 
        energy: int, 
        path: List[Tuple[int, int]]
    ) -> bool:
        """
        Función recursiva de backtracking.
        
        Args:
            universe: Modelo del universo actual
            current_pos: Posición actual (fila, columna)
            energy: Nivel de energía actual
            path: Camino recorrido hasta ahora
            
        Returns:
            bool: True si se encontró una solución, False en caso contrario
        """
        # Incrementar el contador de pasos
        self.steps += 1
        
        # Verificar si ya visitamos esta posición con igual o más energía
        state_key = (current_pos, energy)
        if state_key in self.path_memory:
            return False
        
        # Registrar la posición como explorada
        self.explored_cells.add(current_pos)
        path.append(current_pos)
        
        # Verificar si hemos llegado al destino
        if current_pos == universe.destination:
            self.solution_path = path.copy()
            return True
        
        # Verificar si hay suficiente energía para la celda actual
        required_energy = universe.get_required_energy(current_pos)
        if energy < required_energy:
            path.pop()  # Retroceder
            return False
        
        # Aplicar efectos especiales de la celda (portales, agujeros de gusano, recargas)
        new_pos, new_energy = universe.apply_special_effects(current_pos, energy)
        
        # Si la posición cambió debido a un portal o agujero de gusano
        if new_pos != current_pos:
            # Verificar si la nueva posición ya está en el camino (ciclo)
            if new_pos in path:
                path.pop()
                return False
                
            # Continuar desde la nueva posición
            return self._backtrack(universe, new_pos, new_energy, path)
        
        # Explorar las posiciones vecinas
        neighbors = universe.get_neighbors(current_pos)
        for next_pos in neighbors:
            # Verificar si la celda vecina ya está en el camino actual
            if next_pos in path:
                continue
                
            # Calcular la energía restante después de moverse a la celda vecina
            energy_cost = universe.get_energy_cost(next_pos)
            remaining_energy = new_energy - energy_cost
            
            # Verificar si hay suficiente energía para moverse
            if remaining_energy <= 0:
                continue
                
            # Intentar moverse a la celda vecina
            if self._backtrack(universe, next_pos, remaining_energy, path):
                return True
        
        # Registrar este estado para evitar repetir cálculos
        self.path_memory[state_key] = False
        
        # No se encontró solución desde esta posición, retroceder
        path.pop()
        return False