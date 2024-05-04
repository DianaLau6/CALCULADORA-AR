# lexer.py
import ply.lex as lex


# Lista de tokens
tokens = (
    'NUMERO',
    'DECIMAL',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'PARENTESIS_IZQ',
    'PARENTESIS_DER',
    
)

# Ignorar espacios en blanco
t_ignore = ' \t'

def t_SUMA(t):
    r'\+'
    t.value = str(t.value)
    return t

def t_RESTA(t):
    r'-'
    t.value = str(t.value)
    return t

def t_MULTIPLICACION(t):
    r'\*'
    t.value = str(t.value)
    return t

def t_DIVISION(t):
    r'/'
    t.value = str(t.value)
    return t

def t_PARENTESIS_IZQ(t):
    r'\('
    t.value = str(t.value)
    return t

def t_PARENTESIS_DER(t):
    r'\)'
    t.value = str(t.value)
    return t

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
