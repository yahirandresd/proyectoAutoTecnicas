import sys
import json
from validators.credit_card_validator import crear_afd_tarjeta
from validators.curp_validator import crear_afd_curp

def validar_archivo(ruta_archivo, tipo_validador):
    """
    Valida las cadenas en un archivo usando el validador especificado.
    
    Args:
        ruta_archivo: Ruta al archivo con las cadenas a validar
        tipo_validador: 'curp' o 'tarjeta'
    """
    # Crear el AFD correspondiente
    if tipo_validador == 'curp':
        afd = crear_afd_curp()
    elif tipo_validador == 'tarjeta':
        afd = crear_afd_tarjeta()
    else:
        print(f"Error: Tipo de validador '{tipo_validador}' no reconocido")
        return
    
    # Validar todas las cadenas
    resultados = afd.validar_archivo(ruta_archivo)
    
    # Imprimir resultados
    print(f"\nResultados de validación para {tipo_validador.upper()}:")
    print("-" * 80)
    
    for resultado in resultados:
        print(f"\nLínea {resultado['linea']}: {resultado['cadena']}")
        if resultado['es_valida']:
            print("✅ VÁLIDO")
        else:
            print(f"❌ INVÁLIDO")
            print(f"  Error en posición {resultado['posicion_error']}: {resultado['razon_error']}")
    
    # Guardar resultados en archivo JSON
    nombre_archivo = f"resultados_{tipo_validador}.json"
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"\nResultados guardados en {nombre_archivo}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python validar_archivo.py <ruta_archivo> <tipo_validador>")
        print("  tipo_validador: 'curp' o 'tarjeta'")
        sys.exit(1)
        
    ruta_archivo = sys.argv[1]
    tipo_validador = sys.argv[2].lower()
    
    validar_archivo(ruta_archivo, tipo_validador) 