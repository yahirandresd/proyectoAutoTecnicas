Universo de Algoritmos
Proyecto para la materia de Autómatas y Técnicas de Programación.
Descripción
Este proyecto implementa dos módulos principales:

Misión Interestelar: Un sistema que resuelve problemas de exploración galáctica utilizando algoritmos de backtracking recursivo en una matriz que representa el universo.
Sintaxis Galáctica: Un analizador sintáctico basado en un autómata finito determinista (AFD) para validar la sintaxis del lenguaje Neutrino.

Requisitos

Python 3.8+
PyQt5
NumPy
jsonschema

Instalación

Clonar este repositorio:
git clone https://github.com/yahirandresd/proyectoAutoTecnicas.git
cd universo-algoritmos

Instalar las dependencias:
pip install -r requirements.txt


Ejecución
Para iniciar la aplicación:
python main.py
Módulos
Módulo 1: Misión Interestelar

Implementa un algoritmo de backtracking recursivo para encontrar rutas en un universo.
Carga mapas desde archivos JSON con diferentes elementos: agujeros negros, estrellas gigantes, agujeros de gusano, etc.
Muestra gráficamente la ejecución del algoritmo.

Módulo 2: Sintaxis Galáctica

Implementa un autómata finito determinista para validar la sintaxis del lenguaje Neutrino.
Verifica la corrección sintáctica de programas escritos en este lenguaje.
Muestra errores de sintaxis y su ubicación en el código.

Estructura de los archivos de entrada
Formato JSON para el Módulo 1
json{
  "matriz": { "filas": 35, "columnas": 40 },
  "origen": [0, 0],
  "destino": [34, 39],
  "agujerosNegros": [[3,5], [10,20], [8,8]],
  "estrellasGigantes": [[7,7], [14,14], [20,20]],
  "portales": [
    { "desde": [5,10], "hasta": [25,30] },
    { "desde": [12,3], "hasta": [2,39] }
  ],
  "agujerosGusano": [
    { "entrada": [11,11], "salida": [13,13] },
    { "entrada": [18,5], "salida": [21,6] }
  ],
  "zonasRecarga": [[4,4,3], [15,15,2]],
  "celdasCargaRequerida": [
    { "coordenada": [9,9], "cargaGastada": 30 },
    { "coordenada": [22,22], "cargaGastada": 22 }
  ],
  "cargaInicial": 200,
  "matrizInicial": [[...],[...],[...],...,[...]]
}
Formato de código Neutrino para el Módulo 2
iniciar
  número contador;
  contador := 0;
  para contador := 0 hasta 10 hacer
    mostrar "Iteración";
  fin
finalizar

Autores

Cesar Abdres Rebolledo Lasso
Jesus David Milian Saza
yahir Andres Rangel