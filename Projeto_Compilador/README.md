# Projeto: Compilador Pascal Simplificado

Etapas do Projeto
- Análise Léxica
- Análise Sintática
- Geração de Código (Máquina Virtual)

## Análise Léxica

A análise léxica é a primeira etapa do compilador, responsável por transformar o código-fonte escrito em Pascal em uma sequência de tokens. Cada token representa uma unidade léxica significativa, como palavras-chave, operadores, identificadores, números e símbolos.

### Implementação

Para esta etapa, utilizamos a biblioteca `ply.lex` em Python, que permite definir os tokens por meio de expressões regulares e funções.

### Definição dos Tokens

Foi criada uma lista de tokens que inclui palavras-chave (`program`, `function`, `begin`, `end`, etc.), operadores (`:=`, `+`, `-`, `*`, `/`, `div`, `mod`, etc.), delimitadores (`;`, `.`, `:`, `,`, `(`, `)`, `[`, `]`), identificadores e literais como números inteiros, booleanos e strings.

**Exemplo de tokens definidos:**

```python
tokens = (
    'PROGRAM', 'END', 'VAR', 'TYPEINTEGER', 'TYPESTRING', 'TYPEBOOLEAN', 'BEGIN',
    'STRING', 'LPAREN', 'RPAREN', 'PONTO', 'IF', 'THEN', 'ELSE', 
    'FOR', 'TO', 'DO', 'DOWNTO', 'WHILE', 'FUNCTION', 
    'VIRGULA', 'PONTOVIRGULA', 'DOISPONTOS',
    'ASSIGN', 'EQUAL', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL', 'DIFFERENT',
    'SUM', 'SUB', 'MUL', 'DIVREAL', 'DIV', 'MOD', 'AND', 'OR', 'NOT', 'NUMBER',
    'BOOLEAN', 'ARRAY', 'OF', 'LBRACKET', 'RBRACKET', 'IDENTIFIER'
)
```

### Expressões Regulares para Tokens

Cada token tem sua expressão regular associada, por exemplo:

```python
t_ASSIGN = r':='
t_NUMBER = r'\d+'
t_STRING = r'\'.*?\''
t_SUM = r'\+'
t_SUB = r'-'
```

Palavras-chave são reconhecidas através de funções específicas, para diferenciar de identificadores:

```python
def t_PROGRAM(t):
    r'program'
    return t

def t_IF(t):
    r'if'
    return t

def t_BOOLEAN(t):
    r'true|false'
    return t
```

### Tratamento de espaços, quebras de linha e comentários

Espaços em branco e quebras de linha são ignorados com:

```python
t_ignore = ' \t\n'
```

Comentários no formato Pascal `{...}` também são ignorados:

```python
def t_COMMENT(t): 
    r'{.*}' 
    pass
```

### Tratamento de erros léxicos

Se um caractere inválido for encontrado, o lexer imprime uma mensagem e ignora o caractere:

```python
def t_error(t):
    print(f"Caractere ilegal: {t.value[0]}")
    t.lexer.skip(1)
```

---

## Exemplo de uso

Para testar o lexer, foi utilizado um trecho de código Pascal que define uma função para converter uma string binária em inteiro:

```pascal
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
```

Este código é alimentado no lexer com:

```python
lexer.input(data)
```

O lexer converte o código em tokens para serem usados nas próximas etapas.

## Análise Sintática

O objetivo é reconhecer a estrutura gramatical do código-fonte, gerando uma representação em árvore (AST - Abstract Syntax Tree) que possa ser usada para etapas posteriores de compilação, como semântica e geração de código.

## Definição da Gramática

A gramática foi definida de acordo com a sintaxe da linguagem Pascal, contemplando:

- Declaração de programa (`program IDENTIFIER ;`)
- Declaração de variáveis e funções
- Tipos básicos (inteiro, booleano, string)
- Estruturas de controle: if-then-else, for, while
- Expressões aritméticas e lógicas
- Chamadas de função

A gramática foi expressa em regras de produção no formato Yacc, com manipulação das precedências para operadores lógicos e aritméticos.

## Principais Produções

- **program**: representa o início do programa com nome, declaração de funções, variáveis e corpo principal.
- **declaracaoFunctions**: lista as funções declaradas, possibilitando zero ou mais funções.
- **declaracaoVars**: captura a declaração de variáveis simples e arrays.
- **Corpo e Conteudo**: representam o bloco principal e comandos internos.
- **Comando**: engloba estruturas de controle, atribuições e chamadas de funções.
- **Cond, CondL1, CondL2, CondL3, CondR1, etc.**: definem a hierarquia para expressões condicionais e lógicas com operadores and, or, not e comparações.

## Tratamento de Precedência

Foi implementada uma tabela de precedências para:

- Operadores lógicos (`OR`, `AND`, `NOT`)
- Operadores relacionais (`=`, `<`, `>`, `<=`, `>=`, `<>`)
- Operadores aritméticos (`+`, `-`, `*`, `/`, `div`, `mod`)
- A associação correta de comandos condicionais if-then-else para evitar ambiguidades.

## Construção da Árvore Sintática

Cada produção retorna uma estrutura (geralmente uma lista ou tupla) que representa a árvore sintática abstrata do programa:

- O programa é uma lista contendo nome, funções, variáveis e corpo.
- As funções são representadas por tuplas com nome, argumentos, tipo, variáveis locais e corpo.
- Os comandos condicionais retornam uma estrutura aninhada com as partes `cond`, `then` e opcionalmente `else`.
- Expressões e atribuições são estruturadas em tuplas que representam operadores binários e unários, além de valores e identificadores.

## Exemplo de Entrada e Saída

**Entrada:**

```pascal
program BinarioParaInteiro;
var
  bin: string;
  i, valor, potencia: integer;
begin
  writeln('Introduza uma string binária:');
  readln(bin);
  valor := 0;
  potencia := 1;
  for i := length(bin) downto 1 do
  begin
    if bin[i] = '1' then
      valor := valor + potencia;
    potencia := potencia * 2;
  end;
  writeln('O valor inteiro correspondente é: ', valor);
end.
```

**Saída (AST simplificada):**

```python
[('nome_programa', 'BinarioParaInteiro'),
 ('functions', []),
 ('vars', [(['bin'], 'string'), (['i', 'valor', 'potencia'], 'integer')]),
 ('corpo',
  [('func', ('writeln', ['Introduza uma string binaria:'])),
   ('func', ('readln', ['bin'])),
   ('atrib', 'valor', '0'),
   ('atrib', 'potencia', '1'),
   ('for_downto',
    [('inicio', ('atrib', 'i', ('func', ('length', ['bin'])))),
     ('fim', '1'),
     ('conteudo',
      [('if',
        [('cond', ('rel', '=', ('array', 'bin', 'i'), '1')),
         ('then', [('atrib', 'valor', ('binop', '+', 'valor', 'potencia'))])]),
       ('atrib', 'potencia', ('binop', '*', 'potencia', '2'))])]),
   ('func', ('writeln', ['O valor inteiro correspondente e: ', 'valor']))])]
```
## Geração de Código (Máquina Virtual)

A Máquina Virtual (VM) utilizada neste projeto é uma máquina de pilha (stack machine) projetada para executar instruções intermediárias geradas pelo compilador do subconjunto Pascal. Ela simula um ambiente de execução simples, manipulando variáveis, estruturas de controle e chamadas de função.

### Funcionamento Geral

- **Arquitetura de Pilha:**  
  Todas as operações aritméticas, lógicas e de controle são realizadas sobre uma pilha. Os operandos são empilhados e as instruções consomem e produzem valores na pilha.

- **Memória:**  
  A VM possui áreas de memória para variáveis globais (`gp`), variáveis locais de função (`fp`), heap para strings e arrays, além de uma pilha de execução para controle de chamadas de função.

- **Instruções:**  
  O código intermediário gerado pelo compilador é composto por instruções como `PUSHI` (empilha inteiro), `PUSHG` (empilha variável global), `PUSHL` (empilha variável local), `ADD`, `SUB`, `MUL`, `DIV`, `MOD`, `STRLEN`, `CHARAT`, `CALL`, `RETURN`, entre outras.

- **Controle de Fluxo:**  
  Instruções como `JUMP`, `JZ` (jump if zero), e rótulos (`label:`) permitem a implementação de estruturas como `if`, `while`, `for`, e chamadas de função.

- **Entrada e Saída:**  
  Instruções como `READ`, `WRITES`, `WRITEI`, `WRITELN` permitem interação com o usuário para entrada e saída de dados.

### Exemplo de Execução

Ao compilar um programa Pascal (como o exemplo 5 do enunciado do projeto) o compilador gera uma sequência de instruções para a VM. Por exemplo:

```plaintext
PUSHI 0
PUSHI 0
PUSHI 0
STOREG 0
STOREG 1
STOREG 2
PUSHI 0
STOREG 6
PUSHS "Introduza 5 numeros inteiros:"
WRITES
WRITELN
PUSHI 1
STOREG 5
label0:
PUSHG 5
PUSHI 5
INFEQ
JZ label1
PUSHGP
PUSHI 0
PADD
PUSHG 5
PUSHI 1
SUB
READ
ATOI
STOREN
PUSHG 6
PUSHGP
PUSHI 0
PADD
PUSHG 5
PUSHI 1
SUB
LOADN
ADD
STOREG 6
PUSHG 5
PUSHI 1
ADD
STOREG 5
JUMP label0
label1:
PUSHS "A soma dos numeros e: "
WRITES
PUSHG 6
WRITEI
WRITELN
STOP
```

