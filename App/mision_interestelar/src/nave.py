class Nave:
    def __init__(self, universo):
        self.energia = universo.cargaInicial
        self.universo = universo
        self.visitados = set()

    def puede_moverse(self, x, y):
     if not (0 <= x < self.universo.filas and 0 <= y < self.universo.columnas):
        return False

     if (x, y) in self.visitados:
        return False

     if (x, y) in self.universo.agujerosNegros:
        return False

     for celda in self.universo.celdasCargaRequerida:
        if (x, y) == tuple(celda['coordenada']) and self.energia < celda['cargaGastada']:
            return False

     gasto = self.universo.matriz[x][y]
     if self.energia < gasto:
        return False

     return True


    def mover_a(self, x, y):
        self.visitados.add((x, y))

        # Aplicar recarga si es celda de recarga
        for rec_x, rec_y, factor in self.universo.zonasRecarga:
            if (x, y) == (rec_x, rec_y):
                self.energia *= factor
                return

        # Aplicar gasto de energía
        self.energia -= self.universo.matriz[x][y]

    def retroceder_de(self, x, y):
        self.visitados.remove((x, y))

        # Revertir gasto de energía
        for rec_x, rec_y, factor in self.universo.zonasRecarga:
            if (x, y) == (rec_x, rec_y):
                self.energia /= factor
                return

        self.energia += self.universo.matriz[x][y]
