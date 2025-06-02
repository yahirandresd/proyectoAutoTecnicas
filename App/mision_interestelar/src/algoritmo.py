from PyQt6.QtWidgets import QMessageBox, QGraphicsRectItem, QGraphicsTextItem
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QBrush, QPen, QFont
from copy import deepcopy

class Algoritmo:
    def __init__(self, universo, nave):
        self.universo = universo
        self.nave = nave
        self.filas = universo.filas
        self.columnas = universo.columnas
        self.tam_celda = 60
        self.escena = None
        self.vista = None
        self.contador = 0
        self.max_llamadas = 100000
        self.max_profundidad = 200
        self.agujeros_negros_destruidos = set()
        self.gusanos_usados = set()
        self.mejor_camino = None
        self.mejor_energia = float('-inf')
        self.items_camino = []
        self.timer = None
        self.paso_actual = 0
        self.debug = True
        self.visitados_con_energia = {}
        self.log_pasos = []

    def configurar_grafica(self, escena, vista):
        self.escena = escena
        self.vista = vista
        self.escena.clear()
        # Configurar el tamaño de la escena basado en el tamaño de la matriz
        ancho = self.columnas * self.tam_celda
        alto = self.filas * self.tam_celda
        self.escena.setSceneRect(0, 0, ancho, alto)
        # Ajustar la vista para mostrar toda la escena
        self.vista.setSceneRect(self.escena.sceneRect())
        self.vista.fitInView(self.escena.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        self.dibujar_grid()

    def dibujar_grid(self):
        # Dibuja el grid base
        for i in range(self.filas):
            for j in range(self.columnas):
                # Crear el rectángulo base
                rect = QGraphicsRectItem(j * self.tam_celda, i * self.tam_celda, 
                                       self.tam_celda, self.tam_celda)
                rect.setPen(QPen(Qt.GlobalColor.white))
                
                # Colorear según el tipo de celda
                color = self.obtener_color_celda(i, j)
                if color:
                    rect.setBrush(QBrush(color))
                
                self.escena.addItem(rect)
                
                # Añadir el símbolo si es una celda especial
                simbolo = self.obtener_simbolo_celda(i, j)
                if simbolo:
                    texto_simbolo = QGraphicsTextItem(simbolo)
                    texto_simbolo.setDefaultTextColor(Qt.GlobalColor.white)
                    font = QFont()
                    font.setPointSize(16)
                    texto_simbolo.setFont(font)
                    # Centrar el símbolo en la celda
                    pos_x = j * self.tam_celda + (self.tam_celda - texto_simbolo.boundingRect().width()) / 2
                    pos_y = i * self.tam_celda + (self.tam_celda - texto_simbolo.boundingRect().height()) / 2
                    texto_simbolo.setPos(pos_x, pos_y)
                    self.escena.addItem(texto_simbolo)
                
                # Añadir texto con el costo de energía
                costo = str(self.universo.matriz[i][j])
                texto_costo = QGraphicsTextItem(costo)
                texto_costo.setDefaultTextColor(Qt.GlobalColor.white)
                font = QFont()
                font.setPointSize(12)
                texto_costo.setFont(font)
                # Posicionar el costo en la esquina superior izquierda con un pequeño margen
                texto_costo.setPos(j * self.tam_celda + 5, i * self.tam_celda + 5)
                self.escena.addItem(texto_costo)

    def obtener_color_celda(self, i, j):
        pos = [i, j]
        if pos == self.universo.origen:
            return QColor(0, 255, 0, 127)  # Verde transparente
        if pos == self.universo.destino:
            return QColor(255, 0, 0, 127)  # Rojo transparente
        if pos in self.universo.agujerosNegros:
            return QColor(0, 0, 0, 200)    # Negro semi-transparente
        if pos in self.universo.estrellasGigantes:
            return QColor(255, 255, 0, 127) # Amarillo transparente
        for gusano in self.universo.agujerosGusano:
            if pos == gusano['entrada'] or pos == gusano['salida']:
                return QColor(0, 0, 255, 127)  # Azul transparente
        for rec in self.universo.zonasRecarga:
            if pos == [rec[0], rec[1]]:
                return QColor(0, 255, 255, 127) # Cian transparente
        return None

    def obtener_simbolo_celda(self, i, j):
        pos = [i, j]
        if pos == self.universo.origen:
            return "O"
        if pos == self.universo.destino:
            return "D"
        if pos in self.universo.agujerosNegros:
            return "🕳️"
        if pos in self.universo.estrellasGigantes:
            return "⭐"
        for gusano in self.universo.agujerosGusano:
            if pos == gusano['entrada']:
                return "🌌↓"  # Entrada del agujero de gusano
            if pos == gusano['salida']:
                return "🌌↑"  # Salida del agujero de gusano
        for rec_x, rec_y, _ in self.universo.zonasRecarga:
            if pos == [rec_x, rec_y]:
                return "⚡"
        return ""

    def verificar_teletransporte(self, x, y):
        # Verificar agujeros de gusano no usados
        for gusano in self.universo.agujerosGusano:
            entrada = tuple(gusano['entrada'])
            if (x, y) == entrada and entrada not in self.gusanos_usados:
                self.gusanos_usados.add(entrada)
                return tuple(gusano['salida'])
        return x, y

    def puede_destruir_agujero_negro(self, x, y):
        # Verifica si hay una estrella gigante adyacente
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas:
                if [nx, ny] in self.universo.estrellasGigantes:
                    # Mostrar efecto de destrucción
                    self.animar_destruccion_agujero(x, y, nx, ny)
                    return True
        return False

    def animar_destruccion_agujero(self, agujero_x, agujero_y, estrella_x, estrella_y):
        # Crear efecto visual de destrucción
        rect = QGraphicsRectItem(agujero_y * self.tam_celda, agujero_x * self.tam_celda, 
                               self.tam_celda, self.tam_celda)
        rect.setBrush(QBrush(QColor(255, 0, 0, 127)))
        rect.setPen(QPen(Qt.GlobalColor.white, 2))
        self.escena.addItem(rect)
        
        # Añadir texto de explosión
        texto_explosion = QGraphicsTextItem("💥")
        font = QFont()
        font.setPointSize(24)
        texto_explosion.setFont(font)
        texto_explosion.setDefaultTextColor(Qt.GlobalColor.white)
        pos_x = agujero_y * self.tam_celda + (self.tam_celda - texto_explosion.boundingRect().width()) / 2
        pos_y = agujero_x * self.tam_celda + (self.tam_celda - texto_explosion.boundingRect().height()) / 2
        texto_explosion.setPos(pos_x, pos_y)
        self.escena.addItem(texto_explosion)
        
        # Programar la eliminación del efecto visual después de 1 segundo
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self.escena.removeItem(rect))
        timer.timeout.connect(lambda: self.escena.removeItem(texto_explosion))
        timer.start(1000)

    def iniciar_busqueda(self, x, y):
        """Inicia la búsqueda con estado limpio"""
        self.contador = 0
        self.mejor_camino = None
        self.mejor_energia = float('-inf')
        self.agujeros_negros_destruidos.clear()
        self.gusanos_usados.clear()
        self.visitados_con_energia.clear()
        return self.backtracking(x, y, [], set(), 0)

    def registrar_paso(self, x, y, tipo="movimiento", detalle=None):
        """Registra un paso en el camino con detalles"""
        energia_actual = self.nave.energia
        paso = {
            "posicion": [x, y],
            "tipo": tipo,
            "energia": energia_actual,
            "detalle": detalle
        }
        self.log_pasos.append(paso)

    def obtener_log_camino(self):
        """Retorna el log completo del camino en formato legible"""
        if not self.log_pasos:
            return "No hay pasos registrados."
        
        log = ["Registro detallado del camino:"]
        for i, paso in enumerate(self.log_pasos, 1):
            pos = paso["posicion"]
            tipo = paso["tipo"]
            energia = paso["energia"]
            detalle = paso["detalle"] or ""
            
            log_paso = f"Paso {i}: [{pos[0]},{pos[1]}] - {tipo}"
            if detalle:
                log_paso += f" ({detalle})"
            log_paso += f" | Energía: {energia}"
            log.append(log_paso)
        
        return "\n".join(log)

    def backtracking(self, x, y, camino, visitados, profundidad):
        self.contador += 1
        if self.contador > self.max_llamadas:
            if self.debug:
                print(f"Límite de llamadas alcanzado: {self.max_llamadas}")
            return False, camino

        if profundidad > self.max_profundidad:
            if self.debug:
                print(f"Límite de profundidad alcanzado: {self.max_profundidad}")
            return False, camino

        # Verificar si la posición está fuera de los límites
        if not (0 <= x < self.filas and 0 <= y < self.columnas):
            return False, camino

        # Verificar si ya visitamos esta posición con mejor energía
        pos_key = (x, y)
        if pos_key in self.visitados_con_energia and self.nave.energia <= self.visitados_con_energia[pos_key]:
            return False, camino

        # Si ya encontramos un camino y este tiene menos energía que el mejor, no seguimos
        if self.mejor_camino and self.nave.energia <= self.mejor_energia:
            return False, camino

        # Verificar si es un agujero negro y si puede ser destruido
        if [x, y] in self.universo.agujerosNegros and (x, y) not in self.agujeros_negros_destruidos:
            puede_destruir = self.puede_destruir_agujero_negro(x, y)
            if not puede_destruir:
                return False, camino
            else:
                self.agujeros_negros_destruidos.add((x, y))
                self.registrar_paso(x, y, "destrucción", "Agujero negro destruido")
                print(f"¡Agujero negro en ({x}, {y}) destruido!")

        # Verificar si la nave puede moverse a la coordenada actual
        if not self.nave.puede_moverse(x, y):
            return False, camino

        # Guardar estado actual
        energia_anterior = self.nave.energia
        gusanos_usados_anterior = deepcopy(self.gusanos_usados)
        agujeros_destruidos_anterior = deepcopy(self.agujeros_negros_destruidos)
        recargas_usadas_anterior = deepcopy(self.nave.recargas_usadas)
        visitados_anterior = deepcopy(visitados)
        visitados_energia_anterior = deepcopy(self.visitados_con_energia)

        # Actualizar estado
        camino.append((x, y))
        visitados.add(pos_key)
        self.nave.mover_a(x, y)
        self.visitados_con_energia[pos_key] = self.nave.energia

        # Registrar el paso normal
        self.registrar_paso(x, y, "movimiento")

        # Verificar si es una zona de recarga
        for rec_x, rec_y, factor in self.universo.zonasRecarga:
            if [x, y] == [rec_x, rec_y]:
                coord_str = f"{rec_x},{rec_y}"
                if coord_str not in self.nave.recargas_usadas or self.nave.recargas_usadas[coord_str] < 3:
                    self.registrar_paso(x, y, "recarga", f"Energía multiplicada x{factor}")

        # Verificar si es una celda con carga requerida
        for celda in self.universo.celdasCargaRequerida:
            if [x, y] == celda['coordenada']:
                self.registrar_paso(x, y, "gasto especial", f"Gasto de {celda['cargaGastada']} unidades")

        # Verificar si llegó al destino
        if [x, y] == self.universo.destino:
            if self.nave.energia > self.mejor_energia:
                self.mejor_energia = self.nave.energia
                self.mejor_camino = list(camino)
                self.registrar_paso(x, y, "destino", f"¡Meta alcanzada! Energía final: {self.nave.energia}")
                if self.debug:
                    print(f"¡Destino alcanzado! Energía final: {self.nave.energia}")
            return True, list(camino)

        # Verificar teletransporte después del movimiento
        nx, ny = self.verificar_teletransporte(x, y)
        if (nx, ny) != (x, y):
            if not (nx, ny) in visitados:
                self.registrar_paso(x, y, "teletransporte", f"Teletransportado a [{nx},{ny}]")
                exito, nuevo_camino = self.backtracking(nx, ny, camino, visitados, profundidad + 1)
                if exito:
                    return True, nuevo_camino

        # Obtener y ordenar las direcciones posibles
        direcciones = self.obtener_direcciones_ordenadas(x, y)
        
        for siguiente_x, siguiente_y in direcciones:
            if self.es_movimiento_valido(siguiente_x, siguiente_y):
                exito, nuevo_camino = self.backtracking(siguiente_x, siguiente_y, camino, visitados, profundidad + 1)
                if exito:
                    return True, nuevo_camino

        # Retroceder si no hay solución desde esta ruta
        self.nave.energia = energia_anterior
        self.gusanos_usados = gusanos_usados_anterior
        self.agujeros_negros_destruidos = agujeros_destruidos_anterior
        self.nave.recargas_usadas = recargas_usadas_anterior
        self.visitados_con_energia = visitados_energia_anterior
        camino.pop()
        visitados.clear()
        visitados.update(visitados_anterior)
        return False, camino

    def obtener_direcciones_ordenadas(self, x, y):
        """Obtiene y ordena las direcciones posibles según prioridad"""
        direcciones = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.filas and 0 <= ny < self.columnas:
                # Calcular prioridad
                prioridad = self.calcular_prioridad(nx, ny)
                direcciones.append((prioridad, (nx, ny)))
        
        # Ordenar por prioridad (menor es mejor)
        direcciones.sort()
        return [pos for _, pos in direcciones]

    def calcular_prioridad(self, x, y):
        """Calcula la prioridad de una celda basada en varios factores"""
        if not (0 <= x < self.filas and 0 <= y < self.columnas):
            return float('inf')
        
        prioridad = 0
        
        # Distancia Manhattan al destino
        distancia = abs(x - self.universo.destino[0]) + abs(y - self.universo.destino[1])
        prioridad += distancia
        
        # Bonus para zonas de recarga
        for rec_x, rec_y, factor in self.universo.zonasRecarga:
            if [x, y] == [rec_x, rec_y]:
                coord_str = f"{rec_x},{rec_y}"
                if coord_str not in self.nave.recargas_usadas or self.nave.recargas_usadas[coord_str] < 3:
                    # Priorizar zonas de recarga no usadas o con usos disponibles
                    prioridad -= 20 * factor  # Factor más alto = más prioridad
                break
        
        # Penalizar celdas con alto costo de energía
        costo = self.universo.matriz[x][y]
        prioridad += costo * 2
        
        return prioridad

    def es_movimiento_valido(self, x, y):
        """Verifica si un movimiento es válido antes de intentarlo"""
        if not (0 <= x < self.filas and 0 <= y < self.columnas):
            return False
            
        # Verificar si tenemos suficiente energía para el movimiento
        return self.nave.puede_moverse(x, y)

    def animar_camino(self, camino):
        # Detener timer existente si hay uno
        if hasattr(self, 'timer') and self.timer is not None:
            self.timer.stop()
            
        # Limpiar items existentes
        self.limpiar_items_camino()
        
        self.items_camino = []
        self.paso_actual = 0
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.animar_paso(camino))
        self.timer.start(500)  # Medio segundo entre pasos

    def limpiar_items_camino(self):
        """Limpia de manera segura los items de la animación"""
        if hasattr(self, 'items_camino'):
            for item in self.items_camino:
                try:
                    if item in self.escena.items():
                        self.escena.removeItem(item)
                except:
                    pass  # Ignorar si el item ya no existe
            self.items_camino.clear()

    def animar_paso(self, camino):
        if self.paso_actual >= len(camino):
            self.timer.stop()
            return

        # Limpiar paso anterior de manera segura
        self.limpiar_items_camino()

        # Dibujar nuevo paso
        try:
            x, y = camino[self.paso_actual]

            # Verificar si es un agujero negro que necesita ser destruido
            if [x, y] in self.universo.agujerosNegros:
                # Buscar estrella gigante adyacente
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.filas and 0 <= ny < self.columnas:
                        if [nx, ny] in self.universo.estrellasGigantes:
                            # Mostrar animación de destrucción
                            self.animar_destruccion_agujero(x, y, nx, ny)
                            # Esperar un momento antes de continuar
                            QTimer.singleShot(1000, lambda: self.continuar_animacion(camino, x, y))
                            return

            # Si no es un agujero negro o ya fue destruido, continuar normalmente
            self.dibujar_paso_normal(x, y)
            self.paso_actual += 1

        except Exception as e:
            print(f"Error en animación: {e}")
            self.timer.stop()

    def continuar_animacion(self, camino, x, y):
        """Continúa la animación después de la destrucción del agujero negro"""
        self.dibujar_paso_normal(x, y)
        self.paso_actual += 1

    def dibujar_paso_normal(self, x, y):
        """Dibuja un paso normal de la animación"""
        rect = QGraphicsRectItem(y * self.tam_celda, x * self.tam_celda, 
                               self.tam_celda, self.tam_celda)
        rect.setBrush(QBrush(QColor(0, 255, 0, 127)))
        rect.setPen(QPen(Qt.GlobalColor.white, 2))
        self.escena.addItem(rect)
        self.items_camino.append(rect)

        # Añadir símbolo de nave
        texto_nave = QGraphicsTextItem("🚀")
        font = QFont()
        font.setPointSize(20)
        texto_nave.setFont(font)
        texto_nave.setDefaultTextColor(Qt.GlobalColor.white)
        pos_x = y * self.tam_celda + (self.tam_celda - texto_nave.boundingRect().width()) / 2
        pos_y = x * self.tam_celda + (self.tam_celda - texto_nave.boundingRect().height()) / 2
        texto_nave.setPos(pos_x, pos_y)
        self.escena.addItem(texto_nave)
        self.items_camino.append(texto_nave)

    def es_objetivo(self, x, y):
        return (x, y) == self.universo.destino

