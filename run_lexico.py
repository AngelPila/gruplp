from __future__ import annotations

import sys

import ply.lex as lex

from logger import generar_log


# Angel Pilataxi - Inicio de aporte
tokens = [
    "APERTURA_PHP",
    "CIERRE_PHP",
    "VARIABLE",
    "IDENTIFICADOR",
    "IF",
    "ELSE",
    "WHILE",
    "FOR",
    "FUNCTION",
    "RETURN",
    "ECHO",
    "TRUE",
    "FALSE",
    "NULL",
    "LITERAL_ENTERO",
    "LITERAL_DECIMAL",
    "LITERAL_CADENA",
    "ASIGNACION",
    "IGUAL_IGUAL",
    "DIFERENTE",
    "MENOR_QUE",
    "MAYOR_QUE",
    "MENOR_IGUAL",
    "MAYOR_IGUAL",
    "MAS",
    "MENOS",
    "POR",
    "DIVIDIR",
    # Sebastian Barco - Inicio de aporte (tokens)
    "MODULO",
    "IGUAL_ESTRICTO",
    "MAS_IGUAL",
    "MENOS_IGUAL",
    "POR_IGUAL",
    "DIV_IGUAL",
    "INCREMENTO",
    "DECREMENTO",
    # Sebastian Barco - Fin de aporte (tokens)
    "PARENTESIS_IZQ",
    "PARENTESIS_DER",
    "LLAVE_IZQ",
    "LLAVE_DER",
    "PUNTO_Y_COMA",
    "COMA",
    "PUNTO",
    #Angel Cedeño - Inicio de aporte (tokens)
    "VARIABLE",
    "CONCATENACION",
    #Angel Cedeño - Fin d aporte (tokens)
]

reserved = {
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "for": "FOR",
    "function": "FUNCTION",
    "return": "RETURN",
    "echo": "ECHO",
    "true": "TRUE",
    "false": "FALSE",
    "null": "NULL",
}
# Angel Pilataxi - Fin de aporte


def t_APERTURA_PHP(t):
    r'<\?php'
    return t


def t_CIERRE_PHP(t):
    r'\?>'
    return t


def t_VARIABLE(t):
    r'\$[a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_LITERAL_DECIMAL(t):
    r'\d+\.\d+'
    return t


def t_LITERAL_ENTERO(t):
    r'\d+'
    return t


def t_LITERAL_CADENA(t):
    r"(\"([^\\\n]|(\\.))*?\"|\'([^\\\n]|(\\.))*?\')"
    return t


# Sebastian Barco - Inicio de aporte (funciones de token)

def t_IGUAL_ESTRICTO(t):
    r'==='
    return t


def t_INCREMENTO(t):
    r'\+\+'
    return t


def t_DECREMENTO(t):
    r'--'
    return t


def t_MAS_IGUAL(t):
    r'\+='
    return t


def t_MENOS_IGUAL(t):
    r'-='
    return t


def t_POR_IGUAL(t):
    r'\*='
    return t


def t_DIV_IGUAL(t):
    r'/='
    return t


def t_MODULO(t):
    r'%'
    return t
# Sebastian Barco - Fin de aporte (funciones de token)

#Angel Cedeño - Inicio de aporte
def t_DIVIDIR(t):
    r'/(?![/*=])'
    return t
#Angel Cedeño - Inicio de aporte

def t_IGUAL_IGUAL(t):
    r'=='
    return t

def t_DIFERENTE(t):
    r'!='
    return t


def t_MENOR_IGUAL(t):
    r'<='
    return t


def t_MAYOR_IGUAL(t):
    r'>='
    return t


def t_MENOR_QUE(t):
    r'<'
    return t


def t_MAYOR_QUE(t):
    r'>'
    return t


def t_ASIGNACION(t):
    r'='
    return t


def t_MAS(t):
    r'\+'
    return t


def t_MENOS(t):
    r'-'
    return t


def t_POR(t):
    r'\*'
    return t


def t_DIVIDIR(t):
    r'/(?![/*])'
    return t


def t_PARENTESIS_IZQ(t):
    r'\('
    return t


def t_PARENTESIS_DER(t):
    r'\)'
    return t


def t_LLAVE_IZQ(t):
    r'\{'
    return t


def t_LLAVE_DER(t):
    r'\}'
    return t


def t_PUNTO_Y_COMA(t):
    r';'
    return t


def t_COMA(t):
    r','
    return t


def t_PUNTO(t):
    r'\.'
    return t


def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_ignore_WHITESPACE(t):
    r'[ \t\r]+'
    pass


def t_comment_line(t):
    r'//[^\n]*|\#[^\n]*'
    pass


def t_comment_block(t):
    r'/\*([^*]|\*+[^*/])*\*+/'
    t.lexer.lineno += t.value.count('\n')


def find_column(input_text, token):
    line_start = input_text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    columna = find_column(t.lexer.lexdata, t)
    mensaje = (
        f"Error léxico: carácter no reconocido {repr(t.value[0])} "
        f"en la línea {t.lineno}, columna {columna}"
    )
    t.lexer.errors.append(mensaje)
    t.lexer.skip(1)


def construir_lexer():
    lexer = lex.lex()
    lexer.errors = []
    return lexer


def analizar_archivo(ruta_archivo, nombre_autor):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        codigo = archivo.read()

    lexer = construir_lexer()
    lexer.input(codigo)

    tokens_encontrados = []
    for token in lexer:
        tokens_encontrados.append(token)
        columna = find_column(codigo, token)
        print(f"[{token.type}] {repr(token.value)}  línea {token.lineno}  columna {columna}")

    ruta_log = generar_log(
        tipo_analisis="lexico",
        nombre=nombre_autor,
        tokens_encontrados=tokens_encontrados,
        errores=lexer.errors,
    )
    print(f"\nLog generado en: {ruta_log}")


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 run_lexico.py <archivo.php> <NombreApellido>")
        sys.exit(1)

    ruta_archivo = sys.argv[1]
    nombre_autor = sys.argv[2]
    analizar_archivo(ruta_archivo, nombre_autor)


if __name__ == "__main__":
    main()