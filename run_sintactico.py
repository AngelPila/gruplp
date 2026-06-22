import sys
import ply.yacc as yacc
from run_lexico import tokens, construir_lexer
from logger import generar_log

errores_sintacticos = []

start = 'programa'

precedence = (
    ('left', 'OR_LOGICO'),
    ('left', 'AND_LOGICO'),
    ('left', 'IGUAL_IGUAL', 'DIFERENTE', 'IGUAL_ESTRICTO'),
    ('left', 'MENOR_QUE', 'MAYOR_QUE', 'MENOR_IGUAL', 'MAYOR_IGUAL'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIR', 'MODULO'),
    ('right', 'NOT_LOGICO'),
)

def p_error(p):
    if p:
        msg = f"Error sintáctico: token inesperado '{p.value}' en línea {p.lineno}"
    else:
        msg = "Error sintáctico: fin de archivo inesperado"
    errores_sintacticos.append(msg)
    print(msg)

def p_expresion(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIR expresion
                 | expresion MODULO expresion
                 | PARENTESIS_IZQ expresion PARENTESIS_DER
                 | VARIABLE
                 | LITERAL_ENTERO
                 | LITERAL_DECIMAL
                 | LITERAL_CADENA
                 | TRUE
                 | FALSE
                 | NULL'''

def p_expresion_llamada(p):
    'expresion : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER'

def p_expresion_llamada_vacia(p):
    'expresion : IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER'

def p_expresion_array_acceso(p):
    'expresion : VARIABLE CORCHETE_IZQ expresion CORCHETE_DER'

def p_argumentos(p):
    '''argumentos : argumentos COMA expresion
                  | expresion'''

def p_condicion(p):
    '''condicion : expresion IGUAL_IGUAL expresion
                 | expresion IGUAL_ESTRICTO expresion
                 | expresion DIFERENTE expresion
                 | expresion MENOR_QUE expresion
                 | expresion MAYOR_QUE expresion
                 | expresion MENOR_IGUAL expresion
                 | expresion MAYOR_IGUAL expresion
                 | condicion AND_LOGICO condicion
                 | condicion OR_LOGICO condicion
                 | NOT_LOGICO condicion
                 | PARENTESIS_IZQ condicion PARENTESIS_DER
                 | expresion'''

# Sebastian Barco - Inicio de aporte (sintáctico)

def p_si(p):
    '''si : IF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER
          | IF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER sino'''

def p_sino(p):
    '''sino : ELSE LLAVE_IZQ bloque LLAVE_DER
            | ELSEIF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER
            | ELSEIF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER sino'''

def p_array_indexado(p):
    '''array_indexado : CORCHETE_IZQ lista_elementos CORCHETE_DER
                      | CORCHETE_IZQ CORCHETE_DER'''

def p_lista_elementos(p):
    '''lista_elementos : lista_elementos COMA expresion
                       | expresion'''

def p_expresion_array(p):
    'expresion : array_indexado'

def p_funcion(p):
    '''funcion : FUNCTION IDENTIFICADOR PARENTESIS_IZQ parametros PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER
               | FUNCTION IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER'''

def p_parametros(p):
    '''parametros : parametros COMA VARIABLE
                  | VARIABLE'''

def p_retorno(p):
    'retorno : RETURN expresion PUNTO_Y_COMA'

# Sebastian Barco - Fin de aporte (sintáctico)

def p_programa(p):
    '''programa : APERTURA_PHP bloque CIERRE_PHP
                | APERTURA_PHP bloque'''

def p_bloque(p):
    '''bloque : bloque sentencia
              | sentencia'''

def p_sentencia(p):
    '''sentencia : asignacion
                 | asignacion_compuesta
                 | si
                 | funcion
                 | retorno
                 | impresion
                 | incremento
                 | expresion PUNTO_Y_COMA'''

def p_asignacion(p):
    '''asignacion : VARIABLE ASIGNACION expresion PUNTO_Y_COMA
                  | VARIABLE ASIGNACION condicion PUNTO_Y_COMA'''

def p_asignacion_compuesta(p):
    '''asignacion_compuesta : VARIABLE MAS_IGUAL expresion PUNTO_Y_COMA
                            | VARIABLE MENOS_IGUAL expresion PUNTO_Y_COMA
                            | VARIABLE POR_IGUAL expresion PUNTO_Y_COMA
                            | VARIABLE DIV_IGUAL expresion PUNTO_Y_COMA'''

def p_impresion(p):
    '''impresion : ECHO expresion PUNTO_Y_COMA
                 | PRINT expresion PUNTO_Y_COMA'''

def p_incremento(p):
    '''incremento : VARIABLE INCREMENTO PUNTO_Y_COMA
                  | VARIABLE DECREMENTO PUNTO_Y_COMA'''

parser = yacc.yacc()

def analizar_archivo(ruta_archivo, nombre_autor):
    global errores_sintacticos
    errores_sintacticos = []

    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        codigo = f.read()

    lexer = construir_lexer()
    parser.parse(codigo, lexer=lexer)

    ruta_log = generar_log(
        tipo_analisis="sintactico",
        nombre=nombre_autor,
        tokens_encontrados=[],
        errores=errores_sintacticos,
    )

    if errores_sintacticos:
        print(f"\n{len(errores_sintacticos)} error(es) encontrado(s)")
    else:
        print("\nAnalisis sintactico correcto")

    print(f"Log generado en: {ruta_log}")

def main():
    if len(sys.argv) < 3:
        print("Uso: python run_sintactico.py <archivo.php> <NombreApellido>")
        sys.exit(1)

    ruta_archivo = sys.argv[1]
    nombre_autor = sys.argv[2]
    analizar_archivo(ruta_archivo, nombre_autor)

if __name__ == "__main__":
    main()
