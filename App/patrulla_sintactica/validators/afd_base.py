from typing import Set, Dict, List, Tuple
import json

class AFD:
    def __init__(self, 
                 alfabeto: Set[str],
                 estados: Set[str],
                 estado_inicial: str,
                 estados_finales: Set[str],
                 transiciones: Dict[Tuple[str, str], str]):
        self.alfabeto = alfabeto
        self.estados = estados
        self.estado_inicial = estado_inicial
        self.estados_finales = estados_finales
        self.transiciones = transiciones
        
    def validar_cadena(self, cadena: str) -> Tuple[bool, int, str]:
        """
        Valida una cadena y retorna (es_válida, posición_error, razón_error)
        """
        estado_actual = self.estado_inicial
        
        for i, simbolo in enumerate(cadena):
            if simbolo not in self.alfabeto:
                return False, i, f"Símbolo '{simbolo}' no pertenece al alfabeto"
                
            if (estado_actual, simbolo) not in self.transiciones:
                return False, i, f"No hay transición definida para el estado '{estado_actual}' con el símbolo '{simbolo}'"
                
            estado_actual = self.transiciones[(estado_actual, simbolo)]
            
        if estado_actual not in self.estados_finales:
            return False, len(cadena), f"El estado final '{estado_actual}' no es un estado de aceptación"
            
        return True, -1, ""
        
    def validar_archivo(self, ruta_archivo: str) -> List[Dict]:
        """
        Valida todas las cadenas en un archivo y retorna una lista de resultados
        """
        resultados = []
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            for num_linea, linea in enumerate(f, 1):
                cadena = linea.strip()
                es_valida, pos_error, razon = self.validar_cadena(cadena)
                
                resultado = {
                    "linea": num_linea,
                    "cadena": cadena,
                    "es_valida": es_valida
                }
                
                if not es_valida:
                    resultado.update({
                        "posicion_error": pos_error,
                        "razon_error": razon
                    })
                    
                resultados.append(resultado)
                
        return resultados
        
    def guardar_afd(self, ruta_archivo: str):
        """
        Guarda la definición del AFD en un archivo JSON
        """
        datos = {
            "alfabeto": list(self.alfabeto),
            "estados": list(self.estados),
            "estado_inicial": self.estado_inicial,
            "estados_finales": list(self.estados_finales),
            "transiciones": {f"{k[0]},{k[1]}": v for k, v in self.transiciones.items()}
        }
        
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4)
            
    @classmethod
    def cargar_afd(cls, ruta_archivo: str) -> 'AFD':
        """
        Carga un AFD desde un archivo JSON
        """
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            
        transiciones = {}
        for k, v in datos["transiciones"].items():
            estado, simbolo = k.split(',')
            transiciones[(estado, simbolo)] = v
            
        return cls(
            alfabeto=set(datos["alfabeto"]),
            estados=set(datos["estados"]),
            estado_inicial=datos["estado_inicial"],
            estados_finales=set(datos["estados_finales"]),
            transiciones=transiciones
        ) 