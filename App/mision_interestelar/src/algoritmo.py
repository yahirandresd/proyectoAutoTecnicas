from PyQt6.QtWidgets import QGraphicsPixmapItem, QMessageBox
from PyQt6.QtWidgets import ( QGraphicsScene, QGraphicsView, QVBoxLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
from universo import Universo
class Algoritmo:
 def __init__(self, universo, nave):
        self.universo = universo
        self.nave = nave
        self.filas = universo.filas
        self.columnas = universo.columnas
        self.tam_celda = 25
        self.escena = None
        self.vista = None
 def configurar_grafica(self, escena, vista):
        self.escena = escena
        self.vista = vista


 def backtracking(self, x, y, camino):
    if not self.nave.puede_moverse(x, y):
        return False, []

    self.nave.mover_a(x, y)
    camino.append((x, y))

    if (x, y) == tuple(self.universo.destino):
        return True, camino

    # Aplicar portales y agujeros de gusano
    x_actual, y_actual = self.verificar_teletransporte(x, y)

    # Intentar moverse en las 4 direcciones
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x_actual + dx, y_actual + dy
        resultado, nuevo_camino = self.backtracking(nx, ny, camino.copy())
        if resultado:
            return True, nuevo_camino

    # Retroceder si no encontró camino
    self.nave.retroceder_de(x, y)
    return False, []





 def verificar_teletransporte(self, x, y):
    for portal in self.universo.portales:
        if [x, y] == portal['desde']:
            return tuple(portal['hasta'])
    for gusano in self.universo.agujerosGusano:
        if [x, y] == gusano['entrada']:
            return tuple(gusano['salida'])
    return x, y



 def animar_camino(self, camino):
    self.paso = 0
    self.camino = camino
    self.timer = QTimer()
    self.timer.timeout.connect(self.mostrar_paso)
    self.timer.start(500)  # medio segundo por paso

 def mostrar_paso(self):
    if self.paso >= len(self.camino):
        self.timer.stop()
        return

    x, y = self.camino[self.paso]
    self.dibujar_nave_en(x, y)  # método tuyo que pinta la nave
    self.paso += 1

 def dibujar_nave_en(self, x, y):
    if hasattr(self, 'nave_actual') and self.nave_actual:
        self.escena.removeItem(self.nave_actual)

    item = QGraphicsPixmapItem(QPixmap("img/nave.png").scaled(self.tam_celda, self.tam_celda))
    item.setPos(y * self.tam_celda, x * self.tam_celda)
    self.escena.addItem(item)
    self.nave_actual = item