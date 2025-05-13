"""
Modelo de datos para el universo del Módulo 1.
Define la estructura y comportamiento del universo y sus elementos.
"""

import json
import numpy as np
from typing import List, Dict, Tuple, Optional, Any, Set


class UniverseModel:
    """
    Modelo que representa el universo para la Misión Interestelar.
    Contiene la estructura de la matriz y los diferentes elementos del universo.
    """
    
    def __init__(self):
        """Inicializa un nuevo modelo de universo."""
        # Dimensiones de la matriz
        self.rows = 0
        self.cols = 0
        
        # Matriz de costos de energía
        self.energy_matrix = None
        
        # Coordenadas especiales
        self.origin = (0, 0)
        self.destination = (0, 0)
        
        # Elementos especiales
        self.black_holes = set()
        self.giant_stars = set()
        self.portals = {}  # {desde: hasta}
        self.wormholes = {}  # {entrada: salida}
        self.recharge_zones = {}  # {coordenada: multiplicador}
        self.required_energy_cells = {}  # {coordenada: energía_requerida}
        
        # Configuración de la nave
        self.initial_energy = 0
        
        # Estado de la solución
        self.solution_path = []
        self.explored_cells = set()
        
    def load_from_json(self, json_data: Dict[str, Any]) -> None:
        """
        Carga el modelo desde un diccionario de datos JSON.
        
        Args:
            json_data: Diccionario con los datos del universo
        """
        # Cargar dimensiones
        self.rows = json_data['matriz']['filas']
        self.cols = json_data['matriz']['columnas']
        
        # Inicializar matriz de energía
        self.energy_matrix = np.array(json_data['matrizInicial'], dtype=int)
        
        # Verificar dimensiones de la matriz
        if self.energy_matrix.shape != (self.rows, self.cols):
            raise ValueError(f"La matriz inicial debe tener {self.rows}x{self.cols} elementos")
        
        # Cargar coordenadas especiales
        self.origin = tuple(json_data['origen'])
        self.destination = tuple(json_data['destino'])
        
        # Cargar agujeros negros
        self.black_holes = set(tuple(coord) for coord in json_data['agujerosNegros'])
        
        # Cargar estrellas gigantes
        self.giant_stars = set(tuple(coord) for coord in json_data['estrellasGigantes'])
        
        # Cargar portales
        self.portals = {
            tuple(portal["desde"]): tuple(portal["hasta"])
            for portal in json_data['portales']
        }
        
        # Cargar agujeros de gusano
        self.wormholes = {
            tuple(wormhole["entrada"]): tuple(wormhole["salida"])
            for wormhole in json_data['agujerosGusano']
        }
        
        # Cargar zonas de recarga
        self.recharge_zones = {
            (zone[0], zone[1]): zone[2]
            for zone in json_data['zonasRecarga']
        }
        
        # Cargar celdas con carga requerida
        self.required_energy_cells = {
            tuple(cell["coordenada"]): cell["cargaGastada"]
            for cell in json_data['celdasCargaRequerida']
        }
        
        # Cargar energía inicial
        self.initial_energy = json_data['cargaInicial']
        
        # Reiniciar solución
        self.solution_path = []
        self.explored_cells = set()
    
    def load_from_file(self, file_path: str) -> None:
        """
        Carga el modelo desde un archivo JSON.
        
        Args:
            file_path: Ruta al archivo JSON que contiene los datos del universo
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        self.load_from_json(json_data)
        
    def is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """
        Verifica si una posición está dentro de los límites de la matriz.
        
        Args:
            pos: Tupla (fila, columna) que representa la posición a verificar
            
        Returns:
            bool: True si la posición es válida, False en caso contrario
        """
        row, col = pos
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def is_black_hole(self, pos: Tuple[int, int]) -> bool:
        """
        Verifica si una posición contiene un agujero negro.
        
        Args:
            pos: Tupla (fila, columna) que representa la posición a verificar
            
        Returns:
            bool: True si la posición contiene un agujero negro, False en caso contrario
        """
        return pos in self.black_holes
    
    def get_energy_cost(self, pos: Tuple[int, int]) -> int:
        """
        Obtiene el costo de energía para una celda específica.
        
        Args:
            pos: Tupla (fila, columna) que representa la posición
            
        Returns:
            int: Costo de energía para la celda
        """
        if pos in self.recharge_zones:
            # Las zonas de recarga no tienen costo de energía
            return 0
        
        row, col = pos
        return self.energy_matrix[row, col]
    
    def get_required_energy(self, pos: Tuple[int, int]) -> int:
        """
        Obtiene la energía requerida para acceder a una celda.
        
        Args:
            pos: Tupla (fila, columna) que representa la posición
            
        Returns:
            int: Energía requerida o 0 si la celda no tiene requisitos especiales
        """
        return self.required_energy_cells.get(pos, 0)
    
    def get_cell_type(self, pos: Tuple[int, int]) -> str:
        """
        Determina el tipo de celda en una posición dada.
        
        Args:
            pos: Tupla (fila, columna) que representa la posición
            
        Returns:
            str: Tipo de celda según las constantes definidas
        """
        from App.constants import (
            ELEMENTO_ORIGEN, ELEMENTO_DESTINO, ELEMENTO_AGUJERO_NEGRO,
            ELEMENTO_ESTRELLA_GIGANTE, ELEMENTO_PORTAL_ENTRADA, ELEMENTO_PORTAL_SALIDA,
            ELEMENTO_GUSANO_ENTRADA, ELEMENTO_GUSANO_SALIDA, ELEMENTO_RECARGA,
            ELEMENTO_CARGA_REQUERIDA, ELEMENTO_CAMINO, ELEMENTO_VACIO
        )
        
        if pos == self.origin:
            return ELEMENTO_ORIGEN
        elif pos == self.destination:
            return ELEMENTO_DESTINO
        elif pos in self.black_holes:
            return ELEMENTO_AGUJERO_NEGRO
        elif pos in self.giant_stars:
            return ELEMENTO_ESTRELLA_GIGANTE
        elif pos in self.portals:
            return ELEMENTO_PORTAL_ENTRADA
        elif pos in self.portals.values():
            return ELEMENTO_PORTAL_SALIDA
        elif pos in self.wormholes:
            return ELEMENTO_GUSANO_ENTRADA
        elif pos in self.wormholes.values():
            return ELEMENTO_GUSANO_SALIDA
        elif pos in self.recharge_zones:
            return ELEMENTO_RECARGA
        elif pos in self.required_energy_cells:
            return ELEMENTO_CARGA_REQUERIDA
        elif pos in self.solution_path:
            return ELEMENTO_CAMINO
        else:
            return ELEMENTO_VACIO
    
    def clear_solution(self) -> None:
        """Limpia la solución actual."""
        self.solution_path = []
        self.explored_cells = set()
    
    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Obtiene las posiciones vecinas válidas de una celda.
        
        Args:
            pos: Tupla (fila, columna) que representa la posición
            
        Returns:
            List[Tuple[int, int]]: Lista de posiciones vecinas válidas
        """
        row, col = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
        
        neighbors = []
        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if self.is_valid_position(new_pos) and not self.is_black_hole(new_pos):
                neighbors.append(new_pos)
        
        return neighbors
    
    def apply_special_effects(self, pos: Tuple[int, int], energy: int) -> Tuple[Tuple[int, int], int]:
        """
        Aplica efectos especiales de la celda actual (portales, agujeros de gusano, recargas).
        
        Args:
            pos: Posición actual (fila, columna)
            energy: Nivel de energía actual
            
        Returns:
            Tuple[Tuple[int, int], int]: Nueva posición y nuevo nivel de energía
        """
        new_pos = pos
        new_energy = energy
        
        # Aplicar portal (teletransporte)
        if pos in self.portals:
            new_pos = self.portals[pos]
        
        # Aplicar agujero de gusano (teletransporte de un solo uso)
        if pos in self.wormholes:
            new_pos = self.wormholes[pos]
            # Eliminar el agujero de gusano después de usarlo
            del self.wormholes[pos]
        
        # Aplicar recarga de energía
        if pos in self.recharge_zones:
            multiplier = self.recharge_zones[pos]
            new_energy = new_energy * multiplier
        
        return new_pos, new_energy
    
    def has_adjacent_black_hole(self, pos: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Verifica si una estrella gigante tiene agujeros negros adyacentes.
        Si existe, devuelve la posición del primer agujero negro adyacente.
        
        Args:
            pos: Posición de la estrella gigante
            
        Returns:
            Optional[Tuple[int, int]]: Posición del agujero negro adyacente o None
        """
        if pos not in self.giant_stars:
            return None
            
        row, col = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Arriba, abajo, izquierda, derecha
        
        for dr, dc in directions:
            black_hole_pos = (row + dr, col + dc)
            if black_hole_pos in self.black_holes:
                return black_hole_pos
                
        return None
    
    def destroy_black_hole(self, pos: Tuple[int, int]) -> None:
        """
        Destruye un agujero negro.
        
        Args:
            pos: Posición del agujero negro a destruir
        """
        if pos in self.black_holes:
            self.black_holes.remove(pos)
    
    def set_solution(self, path: List[Tuple[int, int]], explored: Set[Tuple[int, int]]) -> None:
        """
        Establece la solución encontrada.
        
        Args:
            path: Lista de coordenadas que forman el camino solución
            explored: Conjunto de celdas exploradas durante la búsqueda
        """
        self.solution_path = path
        self.explored_cells = explored