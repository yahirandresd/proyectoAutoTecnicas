class Nave:
    def __init__(self, universo):
        self.energia = universo.carga_inicial
        self.universo = universo
        self.visitados = set()

    def puede_moverse(self, x, y):
        # Verifica límites de la matriz
        if not (0 <= x < self.universo.filas and 0 <= y < self.universo.columnas):
            return False

        # Verifica si ya visitó
        if (x, y) in self.visitados:
            return False

        # Verifica si es un agujero negro
        if (x, y) in self.universo.agujeros_negros:
            return False

        # Verifica si tiene suficiente carga para una celda con requerimiento especial
        for req_x, req_y, carga_req in self.universo.requisitos:
            if (x, y) == (req_x, req_y) and self.energia < carga_req:
                return False

        # Verifica si tiene suficiente energía para pasar por la celda
        gasto = self.universo.matriz[x][y]
        if self.energia < gasto:
            return False

        return True

    def mover_a(self, x, y):
        self.visitados.add((x, y))

        # Aplicar recarga si es celda de recarga
        for rec_x, rec_y, factor in self.universo.recargas:
            if (x, y) == (rec_x, rec_y):
                self.energia *= factor
                return

        # Aplicar gasto de energía
        self.energia -= self.universo.matriz[x][y]

    def retroceder_de(self, x, y):
        self.visitados.remove((x, y))

        # Revertir gasto de energía
        for rec_x, rec_y, factor in self.universo.recargas:
            if (x, y) == (rec_x, rec_y):
                self.energia /= factor
                return

        self.energia += self.universo.matriz[x][y]
