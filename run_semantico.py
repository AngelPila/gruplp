import sys

import ply.yacc as yacc

from logger import generar_log
from run_lexico import construir_lexer, tokens

# Lista donde se acumulan los errores semánticos encontrados
errores_semanticos = []

# Sebastian Barco - Inicio de aporte (semántico)
# Tabla de símbolos: aquí se anotan los identificadores declarados.
tabla_variables = {}   # variables declaradas: { "$edad": True, ... }
tabla_funciones = {}   # funciones declaradas: { "suma": True, ... }
# Sebastian Barco - Fin de aporte (semántico)


start = 'programa'

precedence = (
    ('left', 'OR_LOGICO'),
    ('left', 'AND_LOGICO'),
    ('left', 'IGUAL_IGUAL', 'DIFERENTE', 'IGUAL_ESTRICTO'),
    ('left', 'MENOR_QUE', 'MAYOR_QUE', 'MENOR_IGUAL', 'MAYOR_IGUAL'),
    ('left', 'CONCATENACION'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIR', 'MODULO'),
    ('right', 'NOT_LOGICO'),
)


def p_error(p):
    if p:
        msg = f"Error sintáctico: token inesperado '{p.value}' en línea {p.lineno}"
    else:
        msg = "Error sintáctico: fin de archivo inesperado"
    print(msg)


def p_expresion(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIR expresion
                 | expresion MODULO expresion
                 | expresion CONCATENACION expresion
                 | PARENTESIS_IZQ expresion PARENTESIS_DER
                 | LITERAL_ENTERO
                 | LITERAL_DECIMAL
                 | LITERAL_CADENA
                 | TRUE
                 | FALSE
                 | NULL
                 | STDIN'''


def p_expresion_llamada(p):
    'expresion : IDENTIFICADOR PARENTESIS_IZQ argumentos PARENTESIS_DER'


def p_expresion_llamada_vacia(p):
    'expresion : IDENTIFICADOR PARENTESIS_IZQ PARENTESIS_DER'


def p_expresion_array_acceso(p):
    'expresion : VARIABLE CORCHETE_IZQ expresion CORCHETE_DER'


def p_array_indexado(p):
    '''array_indexado : CORCHETE_IZQ lista_elementos CORCHETE_DER
                      | CORCHETE_IZQ CORCHETE_DER'''


def p_lista_elementos(p):
    '''lista_elementos : lista_elementos COMA expresion
                       | expresion'''


def p_expresion_array(p):
    'expresion : array_indexado'


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


def p_parametros(p):
    '''parametros : parametros COMA parametro
                  | parametro'''


def p_parametro(p):
    '''parametro : VARIABLE
                 | VARIABLE ASIGNACION expresion'''


def p_vacio(p):
    'vacio :'


def p_retorno(p):
    'retorno : RETURN expresion PUNTO_Y_COMA'


def p_while(p):
    'while : WHILE PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER'


def p_for(p):
    'for : FOR PARENTESIS_IZQ for_inicializacion PUNTO_Y_COMA for_condicion PUNTO_Y_COMA for_actualizacion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER'


def p_for_inicializacion(p):
    '''for_inicializacion : VARIABLE ASIGNACION expresion
                          | vacio'''


def p_for_condicion(p):
    '''for_condicion : condicion
                     | vacio'''


def p_for_actualizacion(p):
    '''for_actualizacion : VARIABLE INCREMENTO
                         | VARIABLE DECREMENTO
                         | VARIABLE ASIGNACION expresion
                         | VARIABLE MAS_IGUAL expresion
                         | VARIABLE MENOS_IGUAL expresion
                         | VARIABLE POR_IGUAL expresion
                         | VARIABLE DIV_IGUAL expresion
                         | vacio'''


def p_si(p):
    '''si : IF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER
          | IF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER sino'''


def p_sino(p):
    '''sino : ELSE LLAVE_IZQ bloque LLAVE_DER
            | ELSEIF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER
            | ELSEIF PARENTESIS_IZQ condicion PARENTESIS_DER LLAVE_IZQ bloque LLAVE_DER sino'''


def p_ingreso_teclado(p):
    '''ingreso_teclado : IDENTIFICADOR PARENTESIS_IZQ STDIN PARENTESIS_DER
                       | IDENTIFICADOR PARENTESIS_IZQ STDIN COMA LITERAL_ENTERO PARENTESIS_DER'''


def p_expresion_ingreso(p):
    'expresion : ingreso_teclado'


def p_asignacion_array(p):
    '''asignacion_array : VARIABLE CORCHETE_IZQ expresion CORCHETE_DER ASIGNACION expresion PUNTO_Y_COMA
                        | VARIABLE CORCHETE_IZQ CORCHETE_DER ASIGNACION expresion PUNTO_Y_COMA'''


def p_switch(p):
    'switch : SWITCH PARENTESIS_IZQ expresion PARENTESIS_DER LLAVE_IZQ casos LLAVE_DER'


def p_casos(p):
    '''casos : casos caso
             | caso'''


def p_caso(p):
    '''caso : CASE expresion DOS_PUNTOS bloque
            | CASE expresion DOS_PUNTOS bloque break_sentencia
            | DEFAULT DOS_PUNTOS bloque
            | DEFAULT DOS_PUNTOS bloque break_sentencia'''


def p_break_sentencia(p):
    'break_sentencia : BREAK PUNTO_Y_COMA'


def p_programa(p):
    '''programa : APERTURA_PHP bloque CIERRE_PHP
                | APERTURA_PHP bloque'''


def p_bloque(p):
    '''bloque : bloque sentencia
              | sentencia
              | vacio'''


def p_sentencia(p):
    '''sentencia : asignacion
                 | asignacion_compuesta
                 | asignacion_array
                 | si
                 | while
                 | for
                 | switch
                 | funcion
                 | retorno
                 | impresion
                 | incremento
                 | expresion PUNTO_Y_COMA'''


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
    

#Sebastian Barco Reglas Semanticas:

def p_
