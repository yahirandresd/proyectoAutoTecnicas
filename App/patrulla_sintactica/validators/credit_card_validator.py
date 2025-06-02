from .afd_base import AFD

def crear_afd_matricula() -> AFD:
    # Alfabeto: dígitos, guiones y letras mayúsculas
    alfabeto = set('0123456789-ABCDEFGHIJKLMNÑOPQRSTUVWXYZ')
    
    # Estados
    estados = {
        'q0',  # Estado inicial
        'q1',  # Después del primer dígito del año
        'q2',  # Después del segundo dígito del año
        'q3',  # Después del tercer dígito del año
        'q4',  # Después del cuarto dígito del año
        'q5',  # Después del primer guion
        'q6',  # Después de la primera letra del tipo
        'q7',  # Después de la segunda letra del tipo
        'q8',  # Después del segundo guion
        'q9',  # Después del primer dígito del código
        'q10', # Después del segundo dígito del código
        'q11', # Después del tercer dígito del código
        'q12'  # Estado final (después del cuarto dígito del código)
    }
    
    # Estado inicial
    estado_inicial = 'q0'
    
    # Estados finales
    estados_finales = {'q12'}
    
    # Transiciones
    transiciones = {}
    
    # Transiciones para los 4 dígitos del año
    for i in range(4):
        estado_actual = f'q{i}'
        for digito in '0123456789':
            transiciones[(estado_actual, digito)] = f'q{i+1}'
    
    # Transición para el primer guion
    transiciones[('q4', '-')] = 'q5'
    
    # Transiciones para las dos letras del tipo
    for letra in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ':
        transiciones[('q5', letra)] = 'q6'
        transiciones[('q6', letra)] = 'q7'
    
    # Transición para el segundo guion
    transiciones[('q7', '-')] = 'q8'
    
    # Transiciones para los 4 dígitos del código
    for i in range(4):
        estado_actual = f'q{8+i}'
        for digito in '0123456789':
            transiciones[(estado_actual, digito)] = f'q{9+i}'
    
    return AFD(alfabeto, estados, estado_inicial, estados_finales, transiciones)

def validate_matricula(s):
    # Asegurarse de que la entrada esté en mayúsculas
    s = s.strip().upper()
    
    # Validar longitud total
    if len(s) != 13:  # 4 dígitos + guion + 2 letras + guion + 4 dígitos
        return {
            "valid": False,
            "error": {
                "line": 1,
                "char": 0,
                "reason": "La longitud debe ser de 13 caracteres (formato: AAAA-TT-CCCC)"
            }
        }
    
    # Validar formato básico
    partes = s.split('-')
    if len(partes) != 3:
        return {
            "valid": False,
            "error": {
                "line": 1,
                "char": 0,
                "reason": "Formato inválido. Use: AAAA-TT-CCCC"
            }
        }
    
    # Validar año
    try:
        año = int(partes[0])
        if año < 2000 or año > 2024:  # Ajustar según el rango de años válidos
            return {
                "valid": False,
                "error": {
                    "line": 1,
                    "char": 0,
                    "reason": "Año inválido. Debe estar entre 2000 y 2024"
                }
            }
    except ValueError:
        return {
            "valid": False,
            "error": {
                "line": 1,
                "char": 0,
                "reason": "Año inválido"
            }
        }
    
    # Validar tipo de carrera (2 letras)
    if not partes[1].isalpha() or len(partes[1]) != 2:
        return {
            "valid": False,
            "error": {
                "line": 1,
                "char": 5,
                "reason": "Tipo de carrera inválido. Debe ser 2 letras"
            }
        }
    
    # Validar código (4 dígitos)
    if not partes[2].isdigit() or len(partes[2]) != 4:
        return {
            "valid": False,
            "error": {
                "line": 1,
                "char": 8,
                "reason": "Código inválido. Debe ser 4 dígitos"
            }
        }
    
    # Validar con AFD
    afd = crear_afd_matricula()
    es_valida, pos_error, razon = afd.validar_cadena(s)
    
    if es_valida:
        return {"valid": True}
    else:
        return {
            "valid": False,
            "error": {
                "line": 1,
                "char": pos_error,
                "reason": razon
            }
        }
