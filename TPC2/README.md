# TPC2

## Acerca de
Este programa lê um ficheiro CSV contendo informações sobre obras musicais e permite listar compositores, obras organizadas por período e a quantidade de obras por período.

## Estrutura do Código

### Funções

#### `read_csv(file_path: str, compositores: set, obras_periodo: dict) -> tuple`
Lê o ficheiro CSV e extrai as informações necessárias:
- Ignora a primeira linha (cabeçalho).
- Usa expressões regulares para extrair:
  - Nome da obra
  - Período
  - Autor (compositor)
- Armazena os compositores num conjunto (ordenado posteriormente).
- Organiza as obras num dicionário por período.

#### `main()`
Função principal que:
1. Define o caminho do ficheiro CSV.
2. Chama `read_csv` para obter os dados processados.
3. Apresenta um menu com as seguintes opções:
   - `1`: Listar compositores.
   - `2`: Listar obras organizadas por período.
   - `3`: Exibir a quantidade de obras por período.
   - `4`: Sair do programa.
4. Processa a escolha do utilizador e exibe os resultados.

## Explicação da Expressão Regular
A expressão regular utilizada no código é:
```
([^;]+);(?:".*?"|.*?);\d*;([^;]*);([^;]*);[^;]*;.*?(?:\n|$)
```
Esta expressão é usada para extrair três elementos principais de cada linha do CSV:
1. **Nome da obra**: `([^;]+)`
   - Captura qualquer sequência de caracteres que não contenha `;` (delimitador do CSV).
2. **Período**: `([^;]*)`
   - Captura qualquer sequência de caracteres antes do próximo `;`.
3. **Compositor**: `([^;]*)`
   - Captura o nome do compositor.

A regex ignora alguns campos intermediários usando `(?:".*?"|.*?)` para campos possivelmente entre aspas e `\d*` para números opcionais, garantindo que apenas os três elementos necessários sejam extraídos corretamente.

## Exemplo de Entrada e Saída

### Entrada (`obras.csv`)
```
Título;OutroCampo;Ano;Período;Compositor;OutroCampo;OutroCampo
"Sinfonia Nº5";"Descrição descritiva opcional";1804;Clássico;Beethoven;;
"Lago dos Cisnes";"Descrição descritiva opcional"exemplo entre aspas"";1876;Romantismo;Tchaikovsky;;
"Bolero";""Descrição descritiva opcional"";1928;Modernismo;Ravel;;
```

### Saída Esperada
```
Escolha uma opção:
1 - Listar compositores
2 - Listar obras por período
3 - Quantidade de obras por período
4 - Sair
Opção: 1
-----------------
Beethoven
Ravel
Tchaikovsky
```
