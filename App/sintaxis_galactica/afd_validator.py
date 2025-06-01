import re
from typing import List, Set, Tuple

class ValidadorNeutrino:
    def __init__(self):
        self.declaradas: Set[str] = set()
        self.operadores_aritmeticos = {'+', '-', '*', '/'}
        self.operadores_comparacion = {'==', '!=', '<', '>', '<=', '>='}
        self.operadores_logicos = {'y', 'o', 'no'}
        
    def es_variable_valida(self, nombre: str) -> bool:
        """Valida si el nombre de la variable cumple con las reglas."""
        return bool(re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_]*", nombre))

    def validar_expresion(self, expr: str) -> List[str]:
        """Valida una expresión aritmética, lógica o de comparación."""
        errores = []
        tokens = expr.split()
        for token in tokens:
            if (token not in self.operadores_aritmeticos and 
                token not in self.operadores_comparacion and 
                token not in self.operadores_logicos and 
                not token.isnumeric() and 
                not token in self.declaradas and 
                not (token.startswith('"') and token.endswith('"'))):
                errores.append(f"Token inválido en la expresión: '{token}'")
        return errores

    def validar_codigo(self, codigo: str) -> List[str]:
        """Valida el código completo del lenguaje Neutrino."""
        errores = []
        lineas = codigo.strip().split("\n")
        en_bloque = False
        en_estructura_control = False
        nivel_anidamiento = 0

        for i, linea in enumerate(lineas, 1):
            linea = linea.strip()
            if not linea:
                continue

            # Validación de bloques
            if linea == "iniciar":
                if en_bloque:
                    errores.append(f"Línea {i}: Ya se inició un bloque.")
                en_bloque = True
                continue

            if linea == "finalizar":
                if not en_bloque:
                    errores.append(f"Línea {i}: No se ha iniciado el bloque con 'iniciar'.")
                if nivel_anidamiento > 0:
                    errores.append(f"Línea {i}: Hay estructuras de control sin cerrar.")
                en_bloque = False
                continue

            # Validación de punto y coma
            if not linea.endswith(";") and not any(linea.startswith(x) for x in ["para", "mientras", "si"]) and linea != "fin":
                errores.append(f"Línea {i}: Falta ';' al final.")

            # Validación de declaraciones
            if re.fullmatch(r"(número|cadena|booleano) [a-zA-Z][a-zA-Z0-9_]*;", linea):
                var = linea.split()[1][:-1]
                if not self.es_variable_valida(var):
                    errores.append(f"Línea {i}: Nombre de variable inválido '{var}'")
                self.declaradas.add(var)
                continue

            # Validación de estructuras de control
            if linea.startswith(("para ", "mientras ", "si ")):
                nivel_anidamiento += 1
                if not any(x in linea for x in ["hacer", "entonces"]):
                    errores.append(f"Línea {i}: Estructura de control mal formada")
                continue

            if linea == "fin":
                nivel_anidamiento -= 1
                if nivel_anidamiento < 0:
                    errores.append(f"Línea {i}: 'fin' sin estructura de control correspondiente")
                continue

            # Validación de asignaciones
            if ":=" in linea:
                partes = linea[:-1].split(":=")
                if len(partes) != 2:
                    errores.append(f"Línea {i}: Asignación mal formada")
                    continue
                var, expr = partes[0].strip(), partes[1].strip()
                if var not in self.declaradas:
                    errores.append(f"Línea {i}: Variable '{var}' no declarada")
                errores.extend(self.validar_expresion(expr))
                continue

            # Validación de E/S
            if not (re.fullmatch(r'mostrar\s+"[^"]*";', linea) or 
                   re.fullmatch(r"leer [a-zA-Z][a-zA-Z0-9_]*;", linea)):
                errores.append(f"Línea {i}: Instrucción no válida o mal formada")

        if en_bloque:
            errores.append("Error: Falta 'finalizar' al final del código")
        
        return errores
