# Tokenizador de Consultas SPARQL

## Acerca de
Este programa lê um ficheiro de entrada (`input.txt`), realiza a tokenização de uma consulta SPARQL e gera um ficheiro de saída (`output.txt`) com os tokens reconhecidos. A tokenização é feita através de expressões regulares (Regex) que identificam diferentes componentes da consulta.

## Estrutura do Código

### `main()`
A função principal executa os seguintes passos:
1. Lê o conteúdo do ficheiro `input.txt`.
2. Aplica uma série de expressões regulares para identificar tokens na consulta SPARQL.
3. Exibe os tokens reconhecidos no terminal e escreve o resultado no ficheiro `output.txt`.

## Explicação das Expressões Regulares

### Comentários (`# comentário`)
```python
('COMMENT', r'^\#.*')
```
- Captura qualquer linha que comece com `#`.

### Strings (`"texto"`)
```python
('STRING', r'"[^"]*"')
```
- Captura qualquer texto entre aspas `"`.

### Variáveis (`?variavel`)
```python
('VAR', r'\?[\w]+')
```
- Captura identificadores que começam com `?`.

### Dois Pontos (`:`)
```python
('DOISPONTOS', r':')
```
- Identifica o caractere `:`.

### Prefixos e Sufixos (`prefixo:sufixo`)
```python
('PREFIX', r'\w+(?=:)')
('SUFIX', r'(?<=:)\w+')
```
- O prefixo é a parte antes de `:`.
- O sufixo é a parte depois de `:`.

### Números (`1000`)
```python
('NUMERO', r'\d+')
```
- Captura qualquer sequência de dígitos.

### Chavetas (`{}`)
```python
('CHAVETAS', r'[{}]')
```
- Captura os caracteres `{` e `}`.

### Palavras Reservadas (`SELECT`, `WHERE`, `LIMIT`)
```python
('SELECT', r'\bselect\b')
('WHERE', r'\bwhere\b')
('LIMIT', r'\bLIMIT\b')
```
- Identifica palavras reservadas em SPARQL.

### Idiomas (`@en`)
```python
('AT', r'@\w+')
```
- Captura especificadores de idioma (`@en`).

### Ponto Final (`.`)
```python
('PONTO', r'\.')
```
- Captura o caractere `.`.

### Ignorar Espaços (` `)
```python
('SKIP', r'[\s\t]+')
```
- Ignora espaços e tabulações.

### Caracteres Inválidos (`ERRO`)
```python
('ERRO', r'.')
```
- Captura qualquer outro caractere não reconhecido.

## Exemplo de Entrada e Saída

### Entrada (`input.txt`)
```sparql
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
 ?s a dbo:MusicalArtist.
 ?s foaf:name "Chuck Berry"@en .
 ?w dbo:artist ?s.
 ?w foaf:name ?nome.
 ?w dbo:abstract ?desc
} LIMIT 1000
```

### Saída (`output.txt`)
```plaintext
('COMMENT', '# DBPedia: obras de Chuck Berry', 1, (0, 31))
('SELECT', 'select', 2, (0, 6))
('VAR', '?nome', 2, (7, 12))
('VAR', '?desc', 2, (13, 18))
('WHERE', 'where', 2, (19, 24))
('CHAVETAS', '{', 2, (25, 26))
('VAR', '?s', 3, (1, 3))
('ERRO', 'a', 3, (4, 5))
('PREFIX', 'dbo', 3, (6, 9))
('DOISPONTOS', ':', 3, (9, 10))
('SUFIX', 'MusicalArtist', 3, (10, 23))
('PONTO', '.', 3, (23, 24))
('VAR', '?s', 4, (1, 3))
('PREFIX', 'foaf', 4, (4, 8))
('DOISPONTOS', ':', 4, (8, 9))
('SUFIX', 'name', 4, (9, 13))
('STRING', '"Chuck Berry"', 4, (14, 27))
('AT', '@en', 4, (27, 30))
('PONTO', '.', 4, (31, 32))
('VAR', '?w', 5, (1, 3))
('PREFIX', 'dbo', 5, (4, 7))
('DOISPONTOS', ':', 5, (7, 8))
('SUFIX', 'artist', 5, (8, 14))
('VAR', '?s', 5, (15, 17))
('PONTO', '.', 5, (17, 18))
('VAR', '?w', 6, (1, 3))
('PREFIX', 'foaf', 6, (4, 8))
('DOISPONTOS', ':', 6, (8, 9))
('SUFIX', 'name', 6, (9, 13))
('VAR', '?nome', 6, (14, 19))
('PONTO', '.', 6, (19, 20))
('VAR', '?w', 7, (1, 3))
('PREFIX', 'dbo', 7, (4, 7))
('DOISPONTOS', ':', 7, (7, 8))
('SUFIX', 'abstract', 7, (8, 16))
('VAR', '?desc', 7, (17, 22))
('CHAVETAS', '}', 8, (0, 1))
('LIMIT', 'LIMIT', 8, (2, 7))
('NUMERO', '1000', 8, (8, 12))
```

## Conclusão
Este programa realiza a tokenização de consultas SPARQL usando expressões regulares. Ele pode ser expandido para reconhecer mais elementos da linguagem, como operadores lógicos e funções específicas.

