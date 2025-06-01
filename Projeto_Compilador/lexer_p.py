import re
import ply.lex as lex

tokens = (
    'PROGRAM', 'END', 'VAR', 'TYPEINTEGER', 'TYPESTRING', 'TYPEBOOLEAN', 'BEGIN',
    'STRING', 'LPAREN', 'RPAREN', 'PONTO', 'IF', 'THEN', 'ELSE', 
    'FOR', 'TO', 'DO', 'DOWNTO', 'WHILE', 'FUNCTION', 
    'VIRGULA', 'PONTOVIRGULA', 'DOISPONTOS',
    'ASSIGN', 'EQUAL', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL', 'DIFFERENT',
    'SUM', 'SUB', 'MUL', 'DIVREAL', 'DIV', 'MOD', 'AND', 'OR', 'NOT', 'NUMBER',
    'BOOLEAN', 'ARRAY', 'OF', 'LBRACKET', 'RBRACKET', 'IDENTIFIER'
)

t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_ASSIGN = r':='      
t_EQUAL = r'='         
t_LESS = r'<'         
t_GREATER = r'>'       
t_LESSEQUAL = r'<='    
t_GREATEREQUAL = r'>=' 
t_DIFFERENT = r'<>'    
t_NUMBER = r'\d+'    
t_SUM = r'\+'         
t_SUB = r'-'         
t_MUL = r'\*'         
t_DIVREAL = r'/'       
t_VIRGULA = r','
t_DOISPONTOS = r':'

def t_ARRAY(t):
    r'array'
    return t

def t_OF(t):
    r'of'
    return t

def t_DIV(t):
    r'div'
    return t

def t_MOD(t):
    r'mod'
    return t

def t_AND(t):
    r'and'
    return t

def t_OR(t):
    r'or'
    return t

def t_NOT(t):
    r'not'
    return t

def t_PONTO(t):
    r'\.'
    return t

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_FOR(t):
    r'for'
    return t

def t_TO(t):
    r'to'
    return t

def t_DOWNTO(t):
    r'downto'
    return t

def t_DO(t):
    r'do'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_FUNCTION(t):
    r'function'

    return t

def t_BOOLEAN(t):
    r'true|false'
    return t

def t_LPAREN(t):
    r'\('
    return t

def t_RPAREN(t):
    r'\)'
    return t

def t_END(t):
    r'end'
    return t

def t_BEGIN(t):
    r'begin'
    return t

def t_PROGRAM(t):
    r'program'
    return t

def t_VAR(t):
    r'var'
    return t

def t_PONTOVIRGULA(t):
    r';'
    return t

def t_TYPEINTEGER(t):
    r'[iI]nteger'
    return t

def t_TYPEBOOLEAN(t):
    r'[bB]oolean'
    return t

def t_TYPESTRING(t):
    r'[sS]tring'
    return t

def t_STRING(t):
    r'\'.*?\''
    match = re.match(r'\'(.*?)\'', t.value)
    if match:
        t.value = match.group(1)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    return t

t_ignore = ' \t\n'

def t_COMMENT(t): 
    r'{.*}' 
    pass  

def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

data = '''
program BinarioParaInteiro; 
function BinToInt(bin: string): integer; 
var 
  i, valor, potencia: integer; 
begin 
  valor := 0; 
  potencia := 1; 
for i := length(bin) downto 1 do 
begin 
if bin[i] = '1' then 
      valor := valor + potencia; 
    potencia := potencia * 2; 
end; 
  BinToInt := valor; 
end; 
var 
  bin: string; 
  valor: integer; 
begin 
  writeln('Introduza uma string binária:'); 
  readln(bin);
  valor := BinToInt(bin); 
  writeln('O valor inteiro correspondente é: ', valor); 
end.
'''

lexer.input(data)

