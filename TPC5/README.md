# Interpretador de Operações de uma Máquina de Vending

## Acerca de
Este programa simula o funcionamento de uma máquina de vending, permitindo a adição de crédito, seleção de produtos, listagem de produtos disponíveis e saída da máquina com devolução de troco. O programa lê um ficheiro de entrada (`input.txt`) que contém uma série de comandos e um ficheiro de stock (`stock.json`) que contém a informação dos produtos disponíveis na máquina.

## Estrutura do Código

### `main()`
A função principal executa os seguintes passos:
1. Lê o conteúdo do ficheiro `stock.json` e inicializa a máquina com os produtos e crédito inicial de 0.
2. Lê o conteúdo do ficheiro `input.txt` e interpreta os comandos para interagir com a máquina.

### Classes

#### `product`
Representa um produto na máquina de vending.
- `__init__(self, cod, nome, quant, preco)`: Inicializa um produto com código, nome, quantidade e preço.

#### `machine`
Representa a máquina de vending.
- `__init__(self, credit, products)`: Inicializa a máquina com crédito e lista de produtos.
- `add_credit(self, moedas)`: Adiciona crédito à máquina com base nas moedas inseridas, através do uso de um mapa de valores entre os inputs do user e do valor real das moedas.
- `select_product(self, cod)`: Seleciona um produto com base no código fornecido e entrega-o ao utilizador. Tem verificações para os casos de: produto inexistente, produto esgotado e saldo insuficiente.
- `list_products(self)`: Lista todos os produtos disponíveis na máquina.
- `exit_machine(self)`: Sai da máquina e devolve o troco.

### Funções

#### `json_parser(file_path)`
Lê o ficheiro `stock.json` e retorna uma lista de objetos "Product". Ficheiro .json exemplo:
```
[ 
    {"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7}, 
    {"cod": "B34", "nome": "chocolate", "quant": 0, "preco": 1.0},
    {"cod": "C45", "nome": "compal", "quant": 5, "preco": 1.2}
]
```

#### `interpret_input(file_path, machine)`
Lê o ficheiro `input.txt` e interpreta os comandos para interagir com a máquina.
### Expressões Regulares Usadas

- **`>> SELECIONAR ([A-Z]\d{2})\s*$`**  
  Captura o comando de seleção de um produto. O padrão verifica se o código do produto segue o formato de uma letra seguida de dois números, como "A23".

- **`^>>\s*(MOEDA)\s+((?:\d+e|\d+c)(?:\s*,\s*(?:\d+e|\d+c))*)\s*\.$`**  
  Captura o comando de inserção de moedas. Este padrão reconhece moedas expressas em euros e centavos (ex: "1e", "50c") e pode lidar com múltiplas moedas separadas por vírgula.

- **`>> LISTAR`**  
  Captura o comando para listar todos os produtos disponíveis na máquina de vending.

- **`>> SAIR`**  
  Captura o comando para sair da máquina de vending e retirar o troco.

## Exemplo de Entrada e Saída

### Entrada (`input.txt`)
```txt
maq: 2024-03-08, Stock carregado, Estado atualizado.
maq: Bom dia. Estou disponível para atender o seu pedido.
>> LISTAR
maq:
cod | nome | quantidade | preço
---------------------------------
A23 água 0.5L 8 0.7
...
>> MOEDA 1e, 20c, 5c, 5c .
maq: Saldo = 1e30c
>> SELECIONAR A23
maq: Pode retirar o produto dispensado "água 0.5L"
maq: Saldo = 60c
>> SELECIONAR A23
maq: Saldo insufuciente para satisfazer o seu pedido
maq: Saldo = 60c; Pedido = 70c
>> ...
...
maq: Saldo = 74c
>> SELECIONAR B34
>> SAIR
maq: Pode retirar o troco: 1x 50c, 1x 20c e 2x 2c.
maq: Até à próxima
```
### Saída:
```
maq:
cod | nome | quantidade | preço
maq:  A23 água 0.5L 8 0.7
maq:  B34 chocolate 0 1.0
maq:  C45 compal 5 1.2
maq: Saldo =  1.3
maq: Produto entregue
maq: Saldo =  0.60
maq: Saldo insuficiente
maq: Produto esgotado
Pode retirar o seu troco:  0.60
maq: Ate breve
```
### Conclusão:
Este programa simula uma máquina de vending, permitindo a interação com o utilizador através de comandos definidos num ficheiro de entrada. Ele pode ser expandido para incluir mais funcionalidades, como a adição de novos produtos e a remoção de produtos existentes.