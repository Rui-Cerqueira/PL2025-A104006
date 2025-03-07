import re

#text_Exemple:
# # DBPedia: obras de Chuck Berry
# select ?nome ?desc where {
#  ?s a dbo:MusicalArtist.
#  ?s foaf:name "Chuck Berry"@en .
#  ?w dbo:artist ?s.
#  ?w foaf:name ?nome.
#  ?w dbo:abstract ?desc
# } LIMIT 1000

def tokenization(text):

    token_specification = [
        ('COMMENT', r'^\#.*'),               # Comentários começados com #
        ('STRING', r'"[^"]*"'),              # Strings entre aspas
        ('VAR', r'\?[\w]+'),                 # Variáveis começadas com ?
        ('DOISPONTOS', r':'),                # Dois pontos (:)
        ('PREFIX', r'\w+(?=:)'),             # Prefixo (parte antes de :)
        ('SUFIX', r'(?<=:)\w+'),             # Sufixo (parte depois de :)
        ('NUMERO', r'\d+'),                  # Números
        ('CHAVETAS', r'[{}]'),               # { e }
        ('SELECT', r'\bselect\b'),           # Palavra reservada SELECT
        ('WHERE', r'\bwhere\b'),             # Palavra reservada WHERE
        ('LIMIT', r'\bLIMIT\b'),             # Palavra reservada LIMIT
        ('AT', r'@\w+'),                     # @idioma (ex: @en)
        ('PONTO', r'\.'),                    # Ponto final
        ('SKIP', r'[\s\t]+'),                # Espaços e tabs
        ('ERRO', r'.')                       # Qualquer outro caractere inválido
    ]
    tok_regex = '|'.join([f'(?P<{id}>{expreg})' for (id, expreg) in token_specification])
    reconhecidos = []
    linha = 1

    for line in text.splitlines():
        mo = re.finditer(tok_regex, line)

        for m in mo:
            dic = m.groupdict()
            if dic['VAR'] is not None:
                t = ("VAR" , dic['VAR'] , linha , m.span())
            elif dic['STRING'] is not None:
                t = ("STRING" , dic['STRING'] , linha , m.span())
            elif dic['DOISPONTOS'] is not None:
                t = ("DOISPONTOS" , dic['DOISPONTOS'] , linha , m.span())
            elif dic['COMMENT'] is not None:
                t = ("COMMENT" , dic['COMMENT'] , linha , m.span())
            elif dic['PREFIX'] is not None:
                t = ("PREFIX" , dic['PREFIX'] , linha , m.span())
            elif dic['SUFIX'] is not None:
                t = ("SUFIX" , dic['SUFIX'] , linha , m.span())
            elif dic['NUMERO'] is not None:
                t = ("NUMERO" , dic['NUMERO'] , linha , m.span())
            elif dic['CHAVETAS'] is not None:
                t = ("CHAVETAS" , dic['CHAVETAS'] , linha , m.span())
            elif dic['SELECT'] is not None:
                t = ("SELECT" , dic['SELECT'] , linha , m.span())
            elif dic['WHERE'] is not None:
                t = ("WHERE" , dic['WHERE'] , linha , m.span())
            elif dic['LIMIT'] is not None:
                t = ("LIMIT" , dic['LIMIT'] , linha , m.span())
            elif dic['AT'] is not None:
                t = ("AT" , dic['AT'] , linha , m.span())
            elif dic['PONTO'] is not None:
                t = ("PONTO" , dic['PONTO'] , linha , m.span())
            elif dic['SKIP'] is not None:
                pass
            else:
                t = ("ERRO" , dic['ERRO'] , linha , m.span())

            if not dic['SKIP']: reconhecidos.append(t)
        linha += 1
    return reconhecidos

def main():
    with open("input.txt", "r", encoding="utf-8") as f:
        content = f.read()

    tokens = tokenization(content)
    
    for token in tokens:
        print(token)  # Exibe cada token reconhecido no terminal

    with open("output.txt", "w", encoding="utf-8") as f:
        for token in tokens:
            f.write(str(token) + "\n")  # Salva os tokens no ficheiro de saída

if __name__ == "__main__":
    main()