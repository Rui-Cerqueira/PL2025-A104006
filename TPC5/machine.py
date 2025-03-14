import json
import re
# [ 
#     {"cod": "A23", "nome": "água 0.5L", "quant": 8, "preco": 0.7}, 
#     {"cod": "B34", "nome": "chocolate", "quant": 2, "preco": 1.0},
#     {"cod": "C45", "nome": "compal", "quant": 5, "preco": 1.2}
# ]
class product:
    def __init__(self, cod, nome, quant, preco):
        self.cod = cod
        self.nome = nome
        self.quant = quant
        self.preco = preco

class machine:
    def __init__(self, credit , products):
        self.credit = credit
        self.products = products

    def add_credit (self , moedas):
        values = {"1e": 1.0, "2e": 2.0, "50c": 0.50, "20c": 0.20, "10c": 0.10, "5c": 0.5, "2c": 0.2, "1c": 0.1}
        for moeda in moedas:
            self.credit += values[moeda]
        print("maq: Saldo = " , self.credit)

    def select_product (self , cod):
        if cod not in self.products:
            print("maq: Produto inexistente")
            return
        product = self.products[cod]

        if product.quant == 0:
            print("maq: Produto esgotado")
            return
        elif product.preco > self.credit:
            print("maq: Saldo insuficiente")
            return
        else:
            self.credit -= product.preco
            product.quant -= 1
            print("maq: Produto entregue")
            print("maq: Saldo = " , self.credit)

    def list_products (self):
        print ("maq:")
        print ("cod | nome | quantidade | preço")
        for product in self.products:
            print("maq: " , product.cod , product.nome , product.quant , product.preco)

    def exit_machine(self):

        print ("Pode retirar o seu troco: " , self.credit)
        print("maq: Ate breve")
        return



def json_parser (file_path):
    
    produtos = []
    with open(file_path, 'r' , encoding = 'utf-8') as file:
        dados = json.load(file)

    produtos = [product(**item) for item in dados]
    return produtos
        
def interpret_input(file_path, machine):
    token_specification = [
        ('SELECIONAR' , r'>> SELECIONAR ([A-Z]\d{2})\s*$'),
        ('MOEDA' , r'^>>\s*MOEDA\s+((?:\d+e|\d+c)(?:,\s*(?:\d+e|\d+c))*)\s*\.$'),
        ('LISTAR' , r'>> LISTAR'),
        ('SAIR' , r'>> SAIR')
    ]

    tok_regex = '|'.join([f'(?P<{id}>{expreg})' for (id, expreg) in token_specification])
    reconhecidos = [] 
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for line in content.splitlines():   

        match = re.match(tok_regex, line)

        if not match:
            continue
        
        if match.lastgroup == "MOEDA":
            print(match)
            moedas_str = match.group(1)
            if moedas_str:
                moedas = moedas_str.split(", ")
                machine.add_credit(moedas)
            else:
                print("maq: Erro ao capturar as moedas. Formato incorreto.")
        elif match.lastgroup == "SELECIONAR":
            cod = match.group(1)
            machine.select_product(cod)
        elif match.lastgroup == "LISTAR":
            machine.list_products()
        elif match.lastgroup == "SAIR":
            machine.exit_machine()
            break

def main():

    file_path = "TPC5/stock.json"
    produtos = json_parser(file_path)
    for product in produtos:
        print(product.cod, product.nome, product.quant, product.preco)
    
    machine_instance = machine(0.0 , produtos)
    file_path = "TPC5/input.txt"
    interpret_input(file_path, machine_instance)


if __name__ == "__main__":
    main()