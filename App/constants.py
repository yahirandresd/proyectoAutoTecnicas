"""
Constantes globales utilizadas en toda la aplicación.
"""

# Colores
COLOR_BACKGROUND = "#2E3440"  # Fondo oscuro para la interfaz
COLOR_TEXT = "#ECEFF4"        # Texto claro
COLOR_ACCENT = "#88C0D0"      # Color de acento principal
COLOR_ERROR = "#BF616A"       # Color para errores
COLOR_SUCCESS = "#A3BE8C"     # Color para éxito
COLOR_WARNING = "#EBCB8B"     # Color para advertencias

# Tamaños
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 800
DEFAULT_CELL_SIZE = 20        # Tamaño predeterminado de las celdas en la matriz

# Tiempos
ANIMATION_SPEED = 300         # Tiempo en ms entre pasos de animación

# Elementos del universo
ELEMENTO_ORIGEN = "origen"
ELEMENTO_DESTINO = "destino"
ELEMENTO_VACIO = "vacio"
ELEMENTO_AGUJERO_NEGRO = "agujero_negro"
ELEMENTO_ESTRELLA_GIGANTE = "estrella_gigante"
ELEMENTO_PORTAL_ENTRADA = "portal_entrada"
ELEMENTO_PORTAL_SALIDA = "portal_salida"
ELEMENTO_GUSANO_ENTRADA = "gusano_entrada"
ELEMENTO_GUSANO_SALIDA = "gusano_salida"
ELEMENTO_RECARGA = "recarga"
ELEMENTO_CARGA_REQUERIDA = "carga_requerida"
ELEMENTO_CAMINO = "camino"
ELEMENTO_EXPLORADO = "explorado"

# Nombres de pestañas
TAB_MISION = "Misión Interestelar"
TAB_SINTAXIS = "Sintaxis Galáctica"

# Textos de la UI
TEXT_LOAD_UNIVERSE = "Cargar Universo"
TEXT_START_SEARCH = "Iniciar Búsqueda"
TEXT_STEP_BY_STEP = "Paso a Paso"
TEXT_ENERGY = "Energía:"
TEXT_STEPS = "Pasos:"
TEXT_LOAD_CODE = "Cargar Código"
TEXT_VALIDATE_CODE = "Validar Código"
TEXT_CLEAR = "Limpiar"
TEXT_SOLUTION_FOUND = "¡Solución encontrada!"
TEXT_NO_SOLUTION = "No existe solución"
TEXT_CODE_VALID = "El código es válido"
TEXT_CODE_INVALID = "Error en el código"

# Rutas de archivos
DEFAULT_UNIVERSE_FILE = "data/universe_example.json"
DEFAULT_CODE_FILE = "data/neutrino_example.txt"