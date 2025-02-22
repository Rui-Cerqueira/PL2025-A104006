# TPC1

## Data: 2025-02-07

## Acerca de
Este programa lê um ficheiro de texto e processa cada linha para somar números conforme um estado de leitura controlado pelas palavras "on" e "off". O objetivo é somar apenas os números encontrados enquanto a leitura está ativa (estado "on") e ignorar quando está desativada (estado "off").

## Estrutura do Código

### Funções

#### `read_file_to_string_array(file_path: str) -> list`
Lê o conteúdo de um ficheiro e retorna uma lista de strings, onde cada elemento corresponde a uma linha do ficheiro.

#### `word_scanner(text: str, conta_final: int, reading_on: int) -> tuple`
Percorre a string fornecida e processa números de acordo com um estado de leitura:
- Se encontrar "on", ativa a leitura.
- Se encontrar "off", desativa a leitura.
- Enquanto a leitura estiver ativa, soma os números encontrados.
- Se encontrar "=", interrompe imediatamente o processamento e retorna os valores acumulados.

#### `main()`
Função principal que:
1. Define o caminho do ficheiro de entrada.
2. Lê as linhas do ficheiro.
3. Processa cada linha utilizando `word_scanner`.
4. Exibe os resultados.

3. O programa irá exibir as linhas lidas e os resultados da soma de números conforme a lógica de ativação/desativação da leitura.

## Exemplo de Entrada e Saída

### Entrada (Exemplo.txt)
```
Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagens
deu-nos
este trabalho para fazer.=OfF
E deu-nos 7=
dias para o fazer... ON
Cada trabalho destes vale 0.25 valores da nota final!
```

### Saída Esperada
```
Input: Hoje, 7 de Fevereiro de 2025, o professor de Processamento de Linguagens -> Output: 2032
Input: deu-nos -> Output: 2032
Input: este trabalho para fazer.=OfF -> Output: 2032
Input: E deu-nos 7= -> Output: 2039
Input: dias para o fazer... ON -> Output: 2039
Input: Cada trabalho destes vale 0.25 valores da nota final! -> Output: 2064
```
