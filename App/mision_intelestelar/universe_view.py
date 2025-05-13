"""
Vista del universo para el módulo Misión Interestelar.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, 
    QPushButton, QFileDialog, QMessageBox, QScrollArea, QFrame
)
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, QSize, QTimer

from App.constants import (
    DEFAULT_CELL_SIZE, COLOR_ACCENT, COLOR_BACKGROUND,
    TEXT_LOAD_UNIVERSE, TEXT_START_SEARCH, TEXT_STEP_BY_STEP,
    TEXT_ENERGY, TEXT_STEPS, TEXT_SOLUTION_FOUND, TEXT_NO_SOLUTION,
    ELEMENTO_ORIGEN, ELEMENTO_DESTINO, ELEMENTO_AGUJERO_NEGRO,
    ELEMENTO_ESTRELLA_GIGANTE, ELEMENTO_PORTAL_ENTRADA, ELEMENTO_PORTAL_SALIDA,
    ELEMENTO_GUSANO_ENTRADA, ELEMENTO_GUSANO_SALIDA, ELEMENTO_RECARGA,
    ELEMENTO_CARGA_REQUERIDA, ELEMENTO_CAMINO, ELEMENTO_VACIO, ELEMENTO_EXPLORADO,
    ANIMATION_SPEED
)

class CellWidget(QWidget):
    """Widget que representa una celda en la matriz del universo."""
    
    def __init__(self, cell_type=ELEMENTO_VACIO, energy_cost=0, parent=None):
        """
        Inicializa una celda del universo.
        
        Args:
            cell_type: Tipo de celda
            energy_cost: Costo de energía de la celda
            parent: Widget padre
        """
        super(CellWidget, self).__init__(parent)
        self.cell_type = cell_type
        self.energy_cost = energy_cost
        self.setFixedSize(DEFAULT_CELL_SIZE, DEFAULT_CELL_SIZE)
        
    def paintEvent(self, event):
        """Dibuja la celda según su tipo."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Definir colores y formas según el tipo de celda
        if self.cell_type == ELEMENTO_ORIGEN:
            # Origen: verde
            background_color = QColor("#A3BE8C")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, 0, self.width(), self.height())
            self._draw_text(painter, "O")
            
        elif self.cell_type == ELEMENTO_DESTINO:
            # Destino: azul
            background_color = QColor("#5E81AC")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, 0, self.width(), self.height())
            self._draw_text(painter, "D")
            
        elif self.cell_type == ELEMENTO_AGUJERO_NEGRO:
            # Agujero negro: negro
            background_color = QColor("#000000")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(2, 2, self.width() - 4, self.height() - 4)
            
        elif self.cell_type == ELEMENTO_ESTRELLA_GIGANTE:
            # Estrella gigante: amarillo
            background_color = QColor("#EBCB8B")
            pen = QPen(QColor("#D08770"), 1)
            painter.setBrush(QBrush(background_color))
            painter.setPen(pen)
            
            # Dibujar estrella
            center_x = self.width() / 2
            center_y = self.height() / 2
            radius = (self.width() - 4) / 2
            painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
            
            # Líneas de la estrella
            for i in range(8):
                angle = i * 45 * 3.14159 / 180
                x = center_x + radius * 0.8 * 1.4 * 0.7 * \
                    (1 if i % 2 == 0 else 0.8) * 0.707 * (1 if i < 4 else -1)
                y = center_y + radius * 0.8 * 1.4 * 0.7 * \
                    (1 if i % 2 == 0 else 0.8) * 0.707 * (1 if i % 4 < 2 else -1)
                painter.drawLine(center_x, center_y, x, y)
            
        elif self.cell_type == ELEMENTO_PORTAL_ENTRADA:
            # Portal entrada: púrpura
            background_color = QColor("#B48EAD")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(2, 2, self.width() - 4, self.height() - 4)
            self._draw_text(painter, "P")
            
        elif self.cell_type == ELEMENTO_PORTAL_SALIDA:
            # Portal salida: púrpura claro
            background_color = QColor("#D5BADB")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(2, 2, self.width() - 4, self.height() - 4)
            self._draw_text(painter, "P")
            
        elif self.cell_type == ELEMENTO_GUSANO_ENTRADA:
            # Agujero de gusano entrada: naranja
            background_color = QColor("#D08770")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(2, 2, self.width() - 4, self.height() - 4)
            self._draw_text(painter, "W")
            
        elif self.cell_type == ELEMENTO_GUSANO_SALIDA:
            # Agujero de gusano salida: naranja claro
            background_color = QColor("#E5A890")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(2, 2, self.width() - 4, self.height() - 4)
            self._draw_text(painter, "W")
            
        elif self.cell_type == ELEMENTO_RECARGA:
            # Zona de recarga: verde claro
            background_color = QColor("#8FBCBB")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, 0, self.width(), self.height())
            self._draw_text(painter, "R")
            
        elif self.cell_type == ELEMENTO_CARGA_REQUERIDA:
            # Celda con carga requerida: rojo
            background_color = QColor("#BF616A")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, 0, self.width(), self.height())
            self._draw_text(painter, "E")
            
        elif self.cell_type == ELEMENTO_CAMINO:
            # Camino solución: azul claro
            background_color = QColor("#88C0D0")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, 0, self.width(), self.height())
            self._draw_text(painter, str(self.energy_cost), QColor("#2E3440"))
            
        elif self.cell_type == ELEMENTO_EXPLORADO:
            # Celda explorada: gris claro
            background_color = QColor("#4C566A")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, 0, self.width(), self.height())
            
        else:  # ELEMENTO_VACIO
            # Celda vacía: gris oscuro
            background_color = QColor("#3B4252")
            painter.setBrush(QBrush(background_color))
            painter.setPen(Qt.NoPen)
            painter.drawRect(0, 0, self.width(), self.height())
            self._draw_text(painter, str(self.energy_cost), QColor("#D8DEE9"))
    
    def _draw_text(self, painter, text, color=QColor("#ECEFF4")):
        """Dibuja texto en el centro de la celda."""
        painter.setPen(color)
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)
        painter.drawText(self.rect(), Qt.AlignCenter, text)
    
    def update_cell(self, cell_type, energy_cost=None):
        """
        Actualiza el tipo de celda y su costo de energía.
        
        Args:
            cell_type: Nuevo tipo de celda
            energy_cost: Nuevo costo de energía (opcional)
        """
        self.cell_type = cell_type
        if energy_cost is not None:
            self.energy_cost = energy_cost
        self.update()


class UniverseView(QWidget):
    """Vista principal del universo."""
    
    def __init__(self, parent=None):
        """
        Inicializa la vista del universo.
        
        Args:
            parent: Widget padre
        """
        super(UniverseView, self).__init__(parent)
        
        # Inicializar variables
        self.rows = 0
        self.cols = 0
        self.grid_layout = None
        self.cells = []
        self.animation_timer = QTimer(self)
        self.animation_step = 0
        self.solution_path = []
        
        # Configurar la interfaz de usuario
        self._init_ui()
    
    def _init_ui(self):
        """Inicializa los componentes de la interfaz de usuario."""
        # Layout principal
        main_layout = QVBoxLayout(self)
        
        # Panel de controles
        control_layout = QHBoxLayout()
        
        # Botón para cargar universo
        self.load_button = QPushButton(TEXT_LOAD_UNIVERSE)
        control_layout.addWidget(self.load_button)
        
        # Botón para iniciar búsqueda
        self.search_button = QPushButton(TEXT_START_SEARCH)
        self.search_button.setEnabled(False)
        control_layout.addWidget(self.search_button)
        
        # Botón para animación paso a paso
        self.step_button = QPushButton(TEXT_STEP_BY_STEP)
        self.step_button.setEnabled(False)
        control_layout.addWidget(self.step_button)
        
        # Espaciador
        control_layout.addStretch()
        
        # Etiquetas de información
        self.energy_label = QLabel(f"{TEXT_ENERGY} N/A")
        control_layout.addWidget(self.energy_label)
        
        self.steps_label = QLabel(f"{TEXT_STEPS} 0")
        control_layout.addWidget(self.steps_label)
        
        main_layout.addLayout(control_layout)
        
        # Área de desplazamiento para la matriz
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # Contenedor para la matriz
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(1)
        
        scroll_area.setWidget(self.grid_container)
        main_layout.addWidget(scroll_area)
        
        # Etiqueta de resultado
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: bold;")
        main_layout.addWidget(self.result_label)
        
        # Conectar el temporizador de animación
        self.animation_timer.timeout.connect(self._animate_step)
    
    def create_universe_grid(self, rows, cols):
        """
        Crea una matriz vacía para el universo.
        
        Args:
            rows: Número de filas
            cols: Número de columnas
        """
        # Limpiar la matriz existente
        self._clear_grid()
        
        # Guardar dimensiones
        self.rows = rows
        self.cols = cols
        
        # Crear nuevas celdas
        self.cells = []
        for row in range(rows):
            row_cells = []
            for col in range(cols):
                cell = CellWidget()
                self.grid_layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)
        
        # Habilitar el botón de búsqueda
        self.search_button.setEnabled(True)
    
    def _clear_grid(self):
        """Limpia la matriz actual."""
        if not self.cells:
            return
            
        # Remover todas las celdas
        for row_cells in self.cells:
            for cell in row_cells:
                self.grid_layout.removeWidget(cell)
                cell.deleteLater()
        
        self.cells = []
    
    def update_cell(self, row, col, cell_type, energy_cost=None):
        """
        Actualiza una celda específica en la matriz.
        
        Args:
            row: Fila de la celda
            col: Columna de la celda
            cell_type: Tipo de celda
            energy_cost: Costo de energía (opcional)
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.cells[row][col].update_cell(cell_type, energy_cost)
    
    def update_energy_label(self, energy):
        """
        Actualiza la etiqueta de energía.
        
        Args:
            energy: Valor de energía a mostrar
        """
        self.energy_label.setText(f"{TEXT_ENERGY} {energy}")
    
    def update_steps_label(self, steps):
        """
        Actualiza la etiqueta de pasos.
        
        Args:
            steps: Número de pasos a mostrar
        """
        self.steps_label.setText(f"{TEXT_STEPS} {steps}")
    
    def show_result(self, success):
        """
        Muestra el resultado de la búsqueda.
        
        Args:
            success: True si se encontró una solución, False en caso contrario
        """
        message = TEXT_SOLUTION_FOUND if success else TEXT_NO_SOLUTION
        self.result_label.setText(message)
        
        # Habilitar o deshabilitar el botón de animación
        self.step_button.setEnabled(success)
    
    def set_solution_path(self, path):
        """
        Establece el camino solución para la animación.
        
        Args:
            path: Lista de coordenadas del camino solución
        """
        self.solution_path = path.copy()
        self.animation_step = 0
    
    def start_animation(self):
        """Inicia la animación paso a paso."""
        # Reiniciar la animación
        self.animation_step = 0
        
        # Iniciar el temporizador
        self.animation_timer.start(ANIMATION_SPEED)
    
    def _animate_step(self):
        """Anima un paso de la solución."""
        if not self.solution_path or self.animation_step >= len(self.solution_path):
            self.animation_timer.stop()
            return
            
        # Obtener la posición actual
        row, col = self.solution_path[self.animation_step]
        
        # Actualizar la celda como parte del camino
        self.update_cell(row, col, ELEMENTO_CAMINO)
        
        # Avanzar al siguiente paso
        self.animation_step += 1