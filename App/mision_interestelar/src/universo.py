import json

class Universo:
    def __init__(self, ruta_json):
        self.ruta_json = ruta_json
        self.matriz = []
        self.filas = 0
        self.columnas = 0
        self.origen = []
        self.destino = []
        self.agujerosNegros = []  # Cambiado para coincidir con el JSON
        self.estrellasGigantes = []  # Cambiado para coincidir con el JSON
        self.agujerosGusano = []  # Cambiado para coincidir con el JSON
        self.portales = []  # Cambiado para coincidir con el JSON
        self.zonasRecarga = []  # Cambiado para coincidir con el JSON
        self.celdasCargaRequerida = []  # Cambiado para coincidir con el JSON
        self.cargaInicial = 0
        self.matrizInicial = []  # Cambiado para coincidir con el JSON

        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.ruta_json, 'r') as f:
                datos = json.load(f)
                self.filas = datos["matriz"]["filas"]
                self.columnas = datos["matriz"]["columnas"]
                self.origen = datos["origen"]
                self.destino = datos["destino"]
                self.agujerosNegros = datos["agujerosNegros"]  # Ahora coincide con el JSON
                self.estrellasGigantes = datos["estrellasGigantes"]  # Ahora coincide con el JSON
                self.portales = datos["portales"]  # Ahora coincide con el JSON
                self.agujerosGusano = datos["agujerosGusano"]  # Ahora coincide con el JSON
                self.zonasRecarga = datos["zonasRecarga"]  # Ahora coincide con el JSON
                self.celdasCargaRequerida = datos["celdasCargaRequerida"]  # Ahora coincide con el JSON
                self.cargaInicial = datos["cargaInicial"]
                self.matrizInicial = datos["matrizInicial"]  # Cambiado para coincidir con el JSON
                print("Agujeros Negros:", self.agujerosNegros)
                print("Estrellas Gigantes:", self.estrellasGigantes)
                print("Portales:", self.portales)
                print("Agujeros Gusano:", self.agujerosGusano)

                print("Filas:", self.filas)
                print("Columnas:", self.columnas)
                print("matrizInicial:", len(self.matrizInicial), "x", len(self.matrizInicial[0]))

        except Exception as e:
            print(f"Error al cargar el archivo JSON: {e}")
