from lexer_p import tokens
import ply.yacc as yacc
from pprint import pprint

start = 'program'

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('nonassoc', 'EQUAL', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL', 'DIFFERENT'),
    ('left', 'SUM', 'SUB'),
    ('left', 'MUL', 'DIVREAL', 'DIV', 'MOD'),
    ('nonassoc', 'THEN'),
    ('nonassoc', 'ELSE'),
)

def p_program(p):
    '''program : PROGRAM IDENTIFIER PONTOVIRGULA declaracaoFunctions declaracaoVars Corpo'''
    p[0] = [('nome_programa', p[2]),
            ('functions', p[4]),
            ('vars', p[5]),
            ('corpo', p[6])]

# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
# FUNCTIONS
# FUNCTIONS

def p_declaracaoFunctions(p):
    '''declaracaoFunctions : declaracaoFunctions declaracaoFunction
                 | declaracaoFunction
                 | '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []

def p_declaracaoFunction(p):
    '''declaracaoFunction : FUNCTION IDENTIFIER LPAREN argsFunction RPAREN DOISPONTOS Tipo PONTOVIRGULA declaracaoVars BEGIN Conteudo END PONTOVIRGULA'''
    p[0] = [('nome_function', p[2]) , ('argsFunction', p[4]), ('tipoFunction', p[7]), ('varsFunction', p[9]), ('corpoFunction', p[11])]

def p_argsFunction_noargs(p):
    '''argsFunction : '''
    p[0] = []

def p_argsFunction_args(p):
    '''argsFunction : vars'''
    p[0] = p[1]


# VARS
# VARS
# VARS
# VARS
# VARS
# VARS

def p_declaracaoVars(p):
    '''declaracaoVars : VAR vars'''
    p[0] = p[2]
def p_declaracaoVars_nula(p):
    '''declaracaoVars : '''
    p[0] = []
def p_vars_lista(p):
    '''vars : vars var'''
    p[0] = p[1] + [p[2]]
def p_vars_simples(p):
    '''vars : var'''
    p[0] = [p[1]]
def p_var_simples(p):
    '''var : listaVars DOISPONTOS Tipo PONTOVIRGULA
            | listaVars DOISPONTOS Tipo'''
    p[0] = (p[1], p[3])
def p_var_array(p):
    '''var : listaVars DOISPONTOS ARRAY LBRACKET NUMBER PONTO PONTO NUMBER RBRACKET OF Tipo PONTOVIRGULA'''
    p[0] = (p[1], ('array', p[5], p[8], p[11]))
def p_listaVars_uma(p):
    '''listaVars : IDENTIFIER'''
    p[0] = [p[1]]
def p_listaVars_varias(p):
    '''listaVars : listaVars VIRGULA IDENTIFIER'''
    p[0] = p[1] + [p[3]]
def p_Tipo(p):
    '''Tipo : TYPEINTEGER
            | TYPESTRING
            | TYPEBOOLEAN'''
    p[0] = p[1]



# Corpo | Conteudo
# Corpo | Conteudo
# Corpo | Conteudo
# Corpo | Conteudo
# Corpo | Conteudo
# Corpo | Conteudo
# Corpo | Conteudo
# Corpo | Conteudo
# Corpo | Conteudo



def p_corpo(p):
    '''Corpo : BEGIN Conteudo END PONTO
             | BEGIN Conteudo END'''
    p[0] = p[2]

def p_Conteudo_unico(p):
    '''Conteudo : Comando'''
    p[0] = [p[1]]

def p_Conteudo_lista(p):
    '''Conteudo : Conteudo Comando'''
    p[0] = p[1] + [p[2]]

def p_Comando_if(p):
    '''Comando : declaracaoIf
              | For
              | While
              | Function'''
    p[0] = p[1]

def p_Comando_atribuicao(p):
    '''Comando : IDENTIFIER ASSIGN Valor PONTOVIRGULA
               | IDENTIFIER ASSIGN Valor
               | IDENTIFIER ASSIGN CondA1 PONTOVIRGULA
               | IDENTIFIER ASSIGN CondA1'''
    p[0] = ('atrib', p[1], p[3])

def p_Identifier(p):
    '''Identifier : IDENTIFIER
                | IDENTIFIER LBRACKET Valor RBRACKET'''
    if len(p) == 2: p[0] = p[1]
    else: p[0] = ('array', p[1], p[3])

def p_Valor(p):
    '''Valor : Identifier
             | NUMBER
             | BOOLEAN
             | STRING
             | Function'''
    p[0] = p[1]

def p_Function_args(p):
    '''Function : IDENTIFIER LPAREN Valores RPAREN PONTOVIRGULA
                | IDENTIFIER LPAREN Valores RPAREN'''
    p[0] = ('func', (p[1], p[3]))

def p_Function_noargs(p):
    '''Function : IDENTIFIER LPAREN RPAREN PONTOVIRGULA
                | IDENTIFIER LPAREN RPAREN'''
    p[0] = ('func', (p[1], []))



#IF THEN ELSE
#IF THEN ELSE
#IF THEN ELSE
#IF THEN ELSE
#IF THEN ELSE
#IF THEN ELSE


def p_declaracaoIf(p):
    '''declaracaoIf : IF Cond THEN Conteudo %prec THEN'''
    p[0] = ('if', [
        ('cond', p[2]),
        ('then', p[4])
    ])

def p_declaracaoIfElse(p):
    '''declaracaoIf : IF Cond THEN Conteudo ELSE Conteudo'''
    p[0] = ('if_else', [
        ('cond', p[2]),
        ('then', p[4]),
        ('else', p[6])
    ])

def p_Cond_paren(p):
    'Cond : LPAREN Cond RPAREN'
    p[0] = p[2]

def p_Cond_base(p):
    'Cond : CondL1'
    p[0] = p[1]

def p_CondL1_paren(p):
    'CondL1 : LPAREN CondL1 RPAREN'
    p[0] = p[2]

def p_CondL1_or(p):
    'CondL1 : CondL1 OR CondL2'
    p[0] = ('or', p[1], p[3])

def p_CondL1_base(p):
    'CondL1 : CondL2'
    p[0] = p[1]

def p_CondL2_paren(p):
    'CondL2 : LPAREN CondL2 RPAREN'
    p[0] = p[2]

def p_CondL2_and(p):
    'CondL2 : CondL2 AND CondL3'
    p[0] = ('and', p[1], p[3])

def p_CondL2_base(p):
    'CondL2 : CondL3'
    p[0] = p[1]

def p_CondL3_paren(p):
    'CondL3 : LPAREN CondL3 RPAREN'
    p[0] = p[2]

def p_CondL3_not(p):
    'CondL3 : NOT CondR1'
    p[0] = ('not', p[2])

def p_CondL3_base(p):
    'CondL3 : CondR1'
    p[0] = p[1]

def p_CondR1_paren(p):
    'CondR1 : LPAREN CondR1 RPAREN'
    p[0] = p[2]

def p_CondR1_rel(p):
    '''CondR1 : CondA1 EQUAL CondA1
              | CondA1 LESS CondA1
              | CondA1 GREATER CondA1
              | CondA1 LESSEQUAL CondA1
              | CondA1 GREATEREQUAL CondA1
              | CondA1 DIFFERENT CondA1'''
    p[0] = ('rel', p[2], p[1], p[3])

def p_CondR1_base(p):
    'CondR1 : CondA1'
    p[0] = p[1]

def p_CondA1_paren(p):
    'CondA1 : LPAREN CondA1 RPAREN'
    p[0] = p[2]

def p_CondA1_add_sub(p):
    '''CondA1 : CondA1 SUM CondA2
              | CondA1 SUB CondA2'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_CondA1_base(p):
    'CondA1 : CondA2'
    p[0] = p[1]

def p_CondA2_paren(p):
    'CondA2 : LPAREN CondA2 RPAREN'
    p[0] = p[2]

def p_CondA2_mul_div(p):
    '''CondA2 : CondA2 MUL CondA3
              | CondA2 DIVREAL CondA3
              | CondA2 DIV CondA3
              | CondA2 MOD CondA3'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_CondA2_base(p):
    'CondA2 : CondA3'
    p[0] = p[1]

def p_CondA3_paren(p):
    'CondA3 : LPAREN CondA3 RPAREN'
    p[0] = p[2]

def p_CondA3_valor(p):
    'CondA3 : Valor'
    p[0] = p[1]

def p_Valores_varios(p):
    'Valores : Valores VIRGULA Valor'
    p[0] = p[1] + [p[3]]

def p_Valores_um(p):
    'Valores : Valor'
    p[0] = [p[1]]

# FOR
# FOR
# FOR
# FOR
# FOR
# FOR
# FOR
# FOR
# FOR

def p_for(p):
    '''For : FOR InicioFor TO FimFor DO BEGIN Conteudo END PONTOVIRGULA
           | FOR InicioFor DOWNTO FimFor DO BEGIN Conteudo END PONTOVIRGULA
           | FOR InicioFor TO FimFor DO Comando
           | FOR InicioFor DOWNTO FimFor DO Comando'''
    if len(p) != 10: 
        if p.slice[3].type == 'TO':
            p[0] = ('for', [('inicio' , p[2]), ('fim', p[4]), ('conteudo', p[6])])
        else:
            p[0] = ('for_downto', [('inicio' , p[2]), ('fim', p[4]), ('conteudo', p[6])])
    else:
        if p.slice[3].type == 'TO':
            p[0] = ('for', [('inicio' , p[2]), ('fim', p[4]), ('conteudo', p[7])])
        else:
            p[0] = ('for_downto', [('inicio' , p[2]), ('fim', p[4]), ('conteudo', p[7])])

def p_InicioFor(p):
    '''InicioFor : Comando'''
    p[0] = p[1]

def p_FimFor(p):
    '''FimFor : Valor'''
    p[0] = p[1]

# WHILE
# WHILE
# WHILE
# WHILE
# WHILE
# WHILE
# WHILE

def p_While(p):
    '''While : WHILE Cond DO BEGIN Conteudo END PONTOVIRGULA
             | WHILE Cond DO Comando'''
    if len(p) != 5: p[0] = ('while', [('cond' , p[2]), ('conteudo', p[5])])
    else: p[0] = ('while', [('cond' , p[2]), ('conteudo', p[4])])

def p_error(p):
    print(f'Erro na expressão: {p.value}')

parser = yacc.yacc()

# data = '''
# program BinarioParaInteiro; 
# function BinToInt(bin: string): integer; 
# var 
#   i, valor, potencia: integer; 
# begin 
#   valor := 0; 
#   potencia := 1; 
# for i := length(bin) downto 1 do 
# begin 
# if bin[i] = '1' then 
#       valor := valor + potencia; 
#     potencia := potencia * 2; 
# end; 
#   BinToInt := valor; 
# end; 
# var 
#   bin: string; 
#   valor: integer; 
# begin 
#   writeln('Introduza uma string binária:'); 
#   readln(bin);
#   valor := BinToInt(bin); 
#   writeln('O valor inteiro correspondente é: ', valor); 
# end. '''

data = '''
program SomaArray;
var
numeros: array[1..5] of integer;
i, soma: integer;
begin
soma := 0;
writeln('Introduza 5 números inteiros:');
for i := 1 to 5 do
begin
readln(numeros[i]);
soma := soma + numeros[i];
end;
writeln('A soma dos números é: ', soma);
end.
'''

val = parser.parse(data)

pprint(val)