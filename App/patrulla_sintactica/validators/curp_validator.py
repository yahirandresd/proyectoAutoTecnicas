from .afd_base import AFD
from datetime import datetime

def crear_afd_curp() -> AFD:
    # Alfabeto
    alfabeto = set('ABCDEFGHIJKLMNÑOPQRSTUVWXYZ0123456789')
    
    # Estados
    estados = {
        'q0',   # Estado inicial
        'q1',   # Después de la primera letra
        'q2',   # Después de la segunda letra
        'q3',   # Después de la tercera letra
        'q4',   # Después de la cuarta letra
        'q5',   # Después del primer dígito de la fecha
        'q6',   # Después del segundo dígito de la fecha
        'q7',   # Después del tercer dígito de la fecha
        'q8',   # Después del cuarto dígito de la fecha
        'q9',   # Después del quinto dígito de la fecha
        'q10',  # Después del sexto dígito de la fecha
        'q11',  # Después de H/M
        'q12',  # Después de la primera letra del estado
        'q13',  # Después de la segunda letra del estado
        'q14',  # Después de la primera letra interna
        'q15',  # Después de la segunda letra interna
        'q16',  # Después de la tercera letra interna
        'q17',  # Después del primer dígito verificador
        'q18'   # Estado final (después del segundo dígito verificador)
    }
    
    # Estado inicial
    estado_inicial = 'q0'
    
    # Estados finales
    estados_finales = {'q18'}
    
    # Lista de estados válidos
    estados_validos = [
        'AS','BC','BS','CC','CL','CM','CS','CH','DF','DG','GT','GR','HG','JC',
        'MC','MN','MS','NT','NL','OC','PL','QT','QR','SP','SL','SR','TC','TS','TL','VZ','YN','ZS'
    ]
    
    # Transiciones
    transiciones = {}
    
    # Transiciones para las primeras 4 letras
    for i in range(4):
        estado_actual = f'q{i}'
        for letra in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ':
            transiciones[(estado_actual, letra)] = f'q{i+1}'
    
    # Transiciones para los 6 dígitos de la fecha
    for i in range(6):
        estado_actual = f'q{4+i}'
        for digito in '0123456789':
            transiciones[(estado_actual, digito)] = f'q{5+i}'
    
    # Transiciones para H/M
    for letra in 'HM':
        transiciones[('q10', letra)] = 'q11'
    
    # Transiciones para el estado
    for estado in estados_validos:
        transiciones[('q11', estado[0])] = 'q12'
        transiciones[('q12', estado[1])] = 'q13'
    
    # Transiciones para las letras internas
    for i in range(3):
        estado_actual = f'q{13+i}'
        for letra in 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ':
            transiciones[(estado_actual, letra)] = f'q{14+i}'
    
    # Transiciones para los dígitos verificadores
    for i in range(2):
        estado_actual = f'q{16+i}'
        for digito in '0123456789':
            transiciones[(estado_actual, digito)] = f'q{17+i}'
    
    return AFD(alfabeto, estados, estado_inicial, estados_finales, transiciones)

def validar_digito_verificador(curp):
    # Tabla de valores para el cálculo del dígito verificador
    valores = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
        'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'Ñ': 24, 'O': 25, 'P': 26, 'Q': 27,
        'R': 28, 'S': 29, 'T': 30, 'U': 31, 'V': 32, 'W': 33, 'X': 34, 'Y': 35, 'Z': 36
    }
    
    # Factores para el cálculo
    factores = [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    # Calcular suma
    suma = 0
    for i in range(17):
        suma += valores[curp[i]] * factores[i]
    
    # Calcular dígito verificador
    residuo = suma % 10
    if residuo == 0:
        digito_verificador = '0'
    else:
        digito_verificador = str(10 - residuo)
    
    # Comparar con el último dígito de la CURP
    return digito_verificador == curp[-1]

def validate_curp(s):
    # Asegurarse de que la entrada esté en mayúsculas
    s = s.upper()
    
    # Validar longitud
    if len(s) != 18:
        return {
            "valid": False,
            "error": {"line": 1, "char": '-', "reason": "La CURP debe tener exactamente 18 caracteres"}
        }
    
    # Validar con AFD
    afd = crear_afd_curp()
    es_valida, pos_error, razon = afd.validar_cadena(s)
    
    if not es_valida:
        return {
            "valid": False,
            "error": {"line": 1, "char": pos_error, "reason": razon}
        }
    
    # Validar fecha de nacimiento
    try:
        fecha = s[4:10]
        año = int(fecha[:2])
        año_completo = 1900 + año if año > 50 else 2000 + año
        fecha_completa = f"{año_completo}{fecha[2:]}"
        fecha_nac = datetime.strptime(fecha_completa, '%Y%m%d')
        
        if fecha_nac > datetime.now():
            return {
                "valid": False,
                "error": {"line": 1, "char": 4, "reason": "La fecha de nacimiento no puede ser futura"}
            }
    except ValueError:
        return {
            "valid": False,
            "error": {"line": 1, "char": 4, "reason": "Fecha de nacimiento inválida"}
        }
    
    # Validar palabras altisonantes
    palabras_altisonantes = ['BACA', 'BAKA', 'BUEI', 'BUEY', 'CACA', 'CACO', 'CAGA', 'CAGO', 'CAKA', 'CAKO', 
                           'COGE', 'COJA', 'COJE', 'COJI', 'COJO', 'CULO', 'FETO', 'GUEY', 'KACA', 'KACO', 
                           'KAGA', 'KAGO', 'KAKA', 'KAKO', 'MAME', 'MAMO', 'MATA', 'MECO', 'MULA', 'PEDA', 
                           'PEDO', 'PENE', 'PUTA', 'PUTO', 'QULO', 'RATA', 'RUIN']
    
    letras_internas = s[13:16]
    if letras_internas in palabras_altisonantes:
        return {
            "valid": False,
            "error": {"line": 1, "char": 13, "reason": "Las letras internas forman una palabra no permitida"}
        }
    
    # Validar dígito verificador
    if not validar_digito_verificador(s):
        return {
            "valid": False,
            "error": {"line": 1, "char": 17, "reason": "Dígito verificador inválido"}
        }
    
    return {"valid": True}