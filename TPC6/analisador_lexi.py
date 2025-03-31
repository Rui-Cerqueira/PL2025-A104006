import ply.lex as lex

tokens = ('NUM', 'PLUS', 'TIMES', 'MINUS', 'LPAREN', 'RPAREN')

t_PLUS   = r'\+'
t_TIMES  = r'\*'
t_MINUS  = r'-'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)  # Converte para inteiro
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Caracter desconhecido: {t.value[0]} na linha {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()