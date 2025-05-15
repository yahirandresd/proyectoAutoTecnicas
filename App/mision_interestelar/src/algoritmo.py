from nave import Nave

# Movimientos: arriba, abajo, izquierda, derecha
DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def backtracking(universo):
    nave = Nave(universo)
    camino = []

    def resolver(x, y):
        if (x, y) == universo.destino:
            camino.append((x, y))
            return True

        if not nave.puede_moverse(x, y):
            return False

        nave.mover_a(x, y)
        camino.append((x, y))

        # Portales (unidireccionales)
        for desde, hasta in universo.portales:
            if (x, y) == desde:
                if resolver(*hasta):
                    return True

        # Agujeros de gusano (se consumen)
        for i, (entrada, salida) in enumerate(universo.agujeros_gusano):
            if (x, y) == entrada:
                original = universo.agujeros_gusano.pop(i)
                if resolver(*salida):
                    return True
                universo.agujeros_gusano.insert(i, original)

        # Exploración normal
        for dx, dy in DIRECCIONES:
            nx, ny = x + dx, y + dy
            if resolver(nx, ny):
                return True

        # Retroceso
        camino.pop()
        nave.retroceder_de(x, y)
        return False

    if resolver(*universo.origen):
        return camino
    else:
        return None
