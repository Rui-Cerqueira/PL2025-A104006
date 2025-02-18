import re

def read_csv (file_path: str, compositores: set, obras_periodo: dict) -> list:
    with open(file_path, 'r', encoding='utf-8') as file:
    #ignorar a primeira linha
        file.readline()

        conteudo = file.read()
        formula = re.compile(
        r'([^;]+);(?:".*?"|.*?);\d*;([^;]*);([^;]*);[^;]*;.*?(?:\n|$)',re.DOTALL         
        )
        
        print(conteudo)
        for correspondencia in formula.finditer(conteudo):
            
            nome_obra , periodo , autor = correspondencia.groups()
            compositores.add(autor)
            if periodo not in obras_periodo:
                obras_periodo[periodo] = []
            obras_periodo[periodo].append(nome_obra)
    #ordem alfabetica dos compositores
    compositores = sorted(compositores)
    #ordem alfabetica das obras no dicionario periodo - obra
    for periodo in obras_periodo:
        obras_periodo[periodo] = sorted(obras_periodo[periodo])

    return compositores , obras_periodo

def main():
    file_path = "TPC2/obras.csv"
    compositores = set()
    obras_periodo = dict()
    compositores , obras_periodo = read_csv(file_path, compositores, obras_periodo)
    
    print("Escolha uma opção:")
    print("1 - Listar compositores")
    print("2 - Listar obras por período")
    print("3- Quantidade de obras por período")
    print("4 - Sair")

    opcao = input("Opção: ")
    print("-----------------")
    match opcao:
        case "1":
            for compositor in compositores:
                print(compositor)
        case "2":
            for periodo in obras_periodo:
                print(periodo)
                for obra in obras_periodo[periodo]:
                    print(obra)
        case "3":
            for periodo in obras_periodo:
                print(f"{periodo}: {len(obras_periodo[periodo])}")
        case "4":
            return

if __name__ == "__main__":
    main()