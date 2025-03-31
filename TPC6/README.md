# Analisador Léxico e Sintático para Expressões Aritméticas

## Acerca de
Este programa implementa um analisador léxico e um analisador sintático recursivo para expressões aritméticas simples, suportando operações de soma, subtração e multiplicação, além do uso de parênteses para definir a precedência das operações.

O analisador léxico (lexer) utiliza a biblioteca `ply.lex` para identificar tokens numéricos e operadores. O analisador sintático (parser) usa descida recursiva para processar a gramática das expressões e calcular o seu resultado.

## Estrutura do Código

### `analisador_lexi.py`
Responsável pela análise léxica, transforma a expressão de entrada numa sequência de tokens.

#### Tokens Definidos:
- `NUM` - Números inteiros
- `PLUS` - Operador de soma (`+`)
- `MINUS` - Operador de subtração (`-`)
- `TIMES` - Operador de multiplicação (`*`)
- `LPAREN` - Parêntese de abertura (`(`)
- `RPAREN` - Parêntese de fechamento (`)`)

#### Funções principais:
- `t_NUM(t)`: Captura números inteiros e converte-os para valores inteiros.
- `t_ignore`: Ignora espaços em branco e tabulações.
- `t_newline`: Atualiza o número da linha ao encontrar quebras de linha.
- `t_error`: Trata caracteres desconhecidos.
- `lexer`: Instância do analisador léxico.

### `analisador_rec.py`
Implementa o analisador sintático baseado em descida recursiva para avaliar expressões.

#### Funções principais:
- `parser_error(simb)`: Reporta erros sintáticos e interrompe a execução.
- `rec_term(simb)`: Verifica se o token atual corresponde ao esperado e avança para o próximo.
- `factor()`: Processa fatores na gramática (`NUM` ou expressões entre parênteses).
- `term()`: Processa termos com multiplicação (`factor (TIMES factor)*`).
- `expr()`: Processa expressões completas, incluindo soma e subtração (`term ((PLUS | MINUS) term)*`).
- `parse(data)`: Função principal para processar uma expressão e calcular seu resultado.

## Gramática Suportada
A gramática implementada segue as seguintes regras:
```plaintext
expr   → term ((PLUS | MINUS) term)*
term   → factor (TIMES factor)*
factor → NUM | '(' expr ')'
```

## Exemplos de Entrada e Saída
### Entrada:
```
parse("2+3")
parse("67-(2+3*4)")
parse("(9-2)*(13-4)")
parse("2*(3+4)-13")
```

### Saída:
```
Expressão '2+3' avaliada como: 5
Expressão '67-(2+3*4)' avaliada como: 54
Expressão '(9-2)*(13-4)' avaliada como: 63
Expressão '2*(3+4)-13' avaliada como: 1
```
## Conclusão
Este programa demonstra um analisador léxico e sintático funcional para expressões matemáticas simples. Ele pode ser expandido para suportar operações adicionais, números decimais ou outras funcionalidades como variáveis e atribuições.
