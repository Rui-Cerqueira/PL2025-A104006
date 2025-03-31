from analisador_lexi import lexer

prox_simb = None  # Guarda o próximo token

def parser_error(simb):
    print(f"Erro sintático: Token inesperado '{simb.type}'")
    exit(1)

def rec_term(simb):
    """Verifica se o token atual é o esperado e avança."""
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parser_error(prox_simb)

def factor():
    """ factor → NUM | '(' expr ')' """
    global prox_simb
    if prox_simb.type == 'NUM':
        valor = prox_simb.value
        rec_term('NUM')
        return valor
    elif prox_simb.type == 'LPAREN':
        rec_term('LPAREN')
        valor = expr()
        rec_term('RPAREN')
        return valor
    else:
        parser_error(prox_simb)
        return 0

def term():
    """ term → factor (TIMES factor)* """
    valor = factor()
    while prox_simb and prox_simb.type == 'TIMES':
        rec_term('TIMES')
        valor *= factor()
    return valor

def expr():
    """ expr → term ((PLUS | MINUS) term)* """
    valor = term()
    while prox_simb and prox_simb.type in ('PLUS', 'MINUS'):
        op = prox_simb.type
        rec_term(op)
        if op == 'PLUS':
            valor += term()
        elif op == 'MINUS':
            valor -= term()
    return valor

def parse(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    resultado = expr()
    if prox_simb is not None:
        parser_error(prox_simb)
    print(f"Expressão '{data}' avaliada como: {resultado}")
    return resultado

# ----------------- TESTES -----------------

testes = [
    "2+3",
    "67-(2+3*4)",
    "(9-2)*(13-4)",
    "2*(3+4)-13"
]

for teste in testes:
    parse(teste)