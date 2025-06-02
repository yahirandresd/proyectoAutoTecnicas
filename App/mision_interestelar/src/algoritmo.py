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
        self.contador = 0  # contador de llamadas
        self.max_llamadas = 10000  # límite para evitar bucles infinitos
 def configurar_grafica(self, escena, vista):
        self.escena = escena
        self.vista = vista


 def backtracking(self, x, y, camino, visitados=None):
    if visitados is None:
        visitados = set()
        self.contador = 0  # Reiniciar contador al iniciar

    self.contador += 1
    print(f"Visitando: ({x}, {y}) - Total llamadas: {self.contador}")

    if self.contador > self.max_llamadas:
        QMessageBox.critical(None, "Error", "Se ha alcanzado el límite de búsqueda. Posible bucle infinito.")
        return False, []

    if not self.nave.puede_moverse(x, y) or (x, y) in visitados:
        return False, []

    self.nave.mover_a(x, y)
    camino.append((x, y))
    visitados.add((x, y))

    if (x, y) == tuple(self.universo.destino):
        return True, camino

    tx, ty = self.verificar_teletransporte(x, y)
    if (tx, ty) != (x, y):
        if (tx, ty) in visitados or not self.nave.puede_moverse(tx, ty):
            self.nave.retroceder_de(x, y)
            camino.pop()
            visitados.remove((x, y))
            return False, []
        self.nave.mover_a(tx, ty)
        camino.append((tx, ty))
        visitados.add((tx, ty))
        x, y = tx, ty

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        resultado, nuevo_camino = self.backtracking(nx, ny, camino, visitados)
        if resultado:
            return True, nuevo_camino

    visitados.remove((x, y))
    camino.pop()
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