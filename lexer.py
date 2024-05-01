# lexer.py
import ply.lex as lex

# Lista de tokens
tokens = (
    'NUMERO',
    'DECIMAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    'IGUAL',
)

# Definición de tokens
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVIDIDO = r'/'
t_PARENTESIS_IZQ = r'\('
t_PARENTESIS_DER = r'\)'
t_IGUAL = r'='

# Ignorar espacios en blanco
t_ignore = ' \t'

# Definición de token para números
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Definición de token para números decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()
