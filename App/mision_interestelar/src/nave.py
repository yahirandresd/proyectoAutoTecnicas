class Nave:
    def __init__(self, universo):
        self.energia = universo.cargaInicial
        self.energia_inicial = universo.cargaInicial
        self.universo = universo
        self.visitados = set()
        self.historial = []  # Guardamos coordenada, energía y si fue primera visita
        self.recargas_usadas = {}  # Diccionario para contar usos de zonas de recarga
        self.log_movimientos = []  # Lista para registrar todos los movimientos y cambios de energía

    def puede_moverse(self, x, y):
        # Verificar límites del universo
        if not (0 <= x < self.universo.filas and 0 <= y < self.universo.columnas):
            self._registrar_log(f"Movimiento fuera de límites a ({x}, {y})")
            return False

        # Verificar carga requerida
        for celda in self.universo.celdasCargaRequerida:
            if [x, y] == celda['coordenada']:
                if self.energia < celda['cargaGastada']:
                    self._registrar_log(f"Energía insuficiente para celda especial en ({x}, {y}). " +
                                      f"Requerida: {celda['cargaGastada']}, Actual: {self.energia}")
                    return False
                break

        # Si es una zona de recarga, verificar si aún se puede usar
        for rec_x, rec_y, _ in self.universo.zonasRecarga:
            if [x, y] == [rec_x, rec_y]:
                coord_str = f"{rec_x},{rec_y}"
                if coord_str in self.recargas_usadas and self.recargas_usadas[coord_str] >= 3:
                    self._registrar_log(f"Zona de recarga en ({x}, {y}) ya usada máximo número de veces")
                    return False
                return True

        # Verificar si tenemos suficiente energía para el movimiento
        gasto = self.universo.matriz[x][y]
        if self.energia < gasto:
            self._registrar_log(f"Energía insuficiente para mover a ({x}, {y}). " +
                              f"Requerida: {gasto}, Actual: {self.energia}")
            return False

        return True

    def mover_a(self, x, y):
        energia_anterior = self.energia
        ya_visitado = (x, y) in self.visitados
        if not ya_visitado:
            self.visitados.add((x, y))

        # Verificar si es una zona de recarga
        for rec_x, rec_y, factor in self.universo.zonasRecarga:
            if [x, y] == [rec_x, rec_y]:
                coord_str = f"{rec_x},{rec_y}"
                if coord_str not in self.recargas_usadas:
                    self.recargas_usadas[coord_str] = 0
                if self.recargas_usadas[coord_str] < 3:  # Límite de 3 usos por zona de recarga
                    energia_nueva = self.energia * factor
                    self.recargas_usadas[coord_str] += 1
                    self._registrar_log(f"Recarga en ({x}, {y}). Energía: {self.energia} -> {energia_nueva}")
                    self.energia = energia_nueva
                    self.historial.append(((x, y), energia_anterior, ya_visitado))
                    return

        # Verificar si es una celda con carga requerida
        for celda in self.universo.celdasCargaRequerida:
            if [x, y] == celda['coordenada']:
                self.energia -= celda['cargaGastada']
                self._registrar_log(f"Gasto especial en ({x}, {y}). Energía: {energia_anterior} -> {self.energia}")
                self.historial.append(((x, y), energia_anterior, ya_visitado))
                return

        # Movimiento normal
        gasto = self.universo.matriz[x][y]
        self.energia -= gasto
        self._registrar_log(f"Movimiento a ({x}, {y}). Energía: {energia_anterior} -> {self.energia}")
        self.historial.append(((x, y), energia_anterior, ya_visitado))

    def retroceder_de(self, x, y):
        if self.historial:
            pos, energia_anterior, ya_visitado = self.historial.pop()
            # Si estamos retrocediendo de una zona de recarga, decrementar su contador
            for rec_x, rec_y, _ in self.universo.zonasRecarga:
                if [x, y] == [rec_x, rec_y]:
                    coord_str = f"{rec_x},{rec_y}"
                    if coord_str in self.recargas_usadas and self.recargas_usadas[coord_str] > 0:
                        self.recargas_usadas[coord_str] -= 1

            self.energia = energia_anterior
            if not ya_visitado and (x, y) in self.visitados:
                self.visitados.remove((x, y))
            self._registrar_log(f"Retroceso de ({x}, {y}). Energía restaurada a: {self.energia}")

    def _registrar_log(self, mensaje):
        """Registra un mensaje en el log de movimientos"""
        self.log_movimientos.append(mensaje)

    def obtener_log(self):
        """Retorna el log completo de movimientos"""
        return "\n".join(self.log_movimientos)

    def reiniciar(self):
        """Reinicia el estado de la nave a sus valores iniciales"""
        self.energia = self.energia_inicial
        self.visitados.clear()
        self.historial.clear()
        self.recargas_usadas.clear()
        self.log_movimientos.clear()
        self._registrar_log("Nave reiniciada a estado inicial")
