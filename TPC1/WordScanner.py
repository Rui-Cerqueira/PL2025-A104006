def read_file_to_string_array(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

def word_scanner(text: str, conta_final: int, reading_on: int):
    # reading_on = 1
    # conta_final = 0
    i = 0

    while i < len(text):
        if text[i] == '=':
            return conta_final , reading_on  # Retorna imediatamente quando encontra '='

        if reading_on == 1:
            if text[i].isdigit():  # Captura números completos
                start = i
                while i < len(text) and text[i].isdigit():
                    i += 1
                conta_final += int(text[start:i])
                continue  # Evita incrementar `i` duas vezes
            
            elif i + 2 < len(text) and text[i].lower() == 'o' and text[i+1].lower() == 'f' and text[i+2].lower() == 'f':
                reading_on = 0
                i += 3  # Pular 'off'
                continue

        else:  # Se reading_on == 0, procurar 'on'
            if i + 1 < len(text) and text[i].lower() == 'o' and text[i+1].lower() == 'n':
                reading_on = 1
                i += 2  # Pular 'on'
                continue
        
        i += 1  # Incrementar sempre que nenhuma outra condição for satisfeita

    return conta_final, reading_on

def main():
    file_path = "TPC1/Exemplo.txt"
    test_strings = read_file_to_string_array(file_path)

    for string in test_strings:
        print(string)
    soma = 0;
    estado = 1;
    for test in test_strings:
        soma, estado = word_scanner(test, soma, estado)
        print(f"Input: {test} -> Output: {soma}")

if __name__ == "__main__":
    main()
