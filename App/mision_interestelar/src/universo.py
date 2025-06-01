import json

class Universo:
    def __init__(self, ruta_json):
        self.ruta_json = ruta_json
        self.matriz = []
        self.filas = 0
        self.columnas = 0
        self.origen = []
        self.destino = []
        self.agujerosNegros = []
        self.estrellasGigantes = []
        self.agujerosGusano = []
        self.portales = []
        self.zonasRecarga = []
        self.celdasCargaRequerida = []
        self.cargaInicial = 0
        self.matrizInicial = []

        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.ruta_json, 'r') as f:
                datos = json.load(f)

            matriz_info = datos.get("matriz", {})
            self.filas = matriz_info.get("filas", 0)
            self.columnas = matriz_info.get("columnas", 0)

            self.origen = datos.get("origen", [])
            self.destino = datos.get("destino", [])
            self.agujerosNegros = datos.get("agujerosNegros", [])
            self.estrellasGigantes = datos.get("estrellasGigantes", [])
            self.portales = datos.get("portales", [])
            self.agujerosGusano = datos.get("agujerosGusano", [])
            self.zonasRecarga = datos.get("zonasRecarga", [])
            self.celdasCargaRequerida = datos.get("celdasCargaRequerida", [])
            self.cargaInicial = datos.get("cargaInicial", 0)
            self.matrizInicial = datos.get("matrizInicial", [])
            self.matriz = self.matrizInicial  # <-- AÑADE ESTA LÍNEA

            # Imprime para depuración
            print("Agujeros Negros:", self.agujerosNegros)
            print("Estrellas Gigantes:", self.estrellasGigantes)
            print("Portales:", self.portales)
            print("Agujeros Gusano:", self.agujerosGusano)
            print("Filas:", self.filas)
            print("Columnas:", self.columnas)
            if self.matrizInicial:
              self.filas = len(self.matrizInicial)
              self.columnas = len(self.matrizInicial[0])
              self.matriz = self.matrizInicial
              print("matrizInicial:", self.filas, "x", self.columnas)
            else:
              print("matrizInicial está vacía")

        except Exception as e:
            print(f"Error al cargar el archivo JSON: {e}")
