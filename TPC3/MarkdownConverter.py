import re

def main():

    with open("Exemplo.md", "r") as file:
        markdown = file.read()

        #Cabeçalho
    markdown = re.sub(r'^(#{1,3})\s*(.*)', 
                    lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', 
                    markdown, flags=re.M)

    #Bold
    markdown =  re.sub(r'\*\*(.+)\*\*' , r'<b>\1</b>', markdown , flags = re.M)

    #Itálico
    markdown = re.sub(r'\*(.+)\*' , r'<i>\1</i>', markdown , flags = re.M)

    #Listas ordenadas
    markdown = re.sub(r'^\d+\.\s+(.+)' , r'<li>\1</li>', markdown, flags = re.M)
    markdown = re.sub(r'(<li>.*?</li>(?:\n<li>.*?</li>)*)', r'<ol>\n\1\n</ol>', markdown, flags = re.S)

    #imagens
    markdown = re.sub(r'!\[(.+)\]\((.+)\)' , r'<img src="\2" alt="\1">', markdown, flags = re.M)

    #URL's
    markdown = re.sub(r'\[(.+)\]\((.+)\)' , r'<a href="\2">\1</a>', markdown, flags = re.M)

    result = open("Resultado.html", "w")
    result.write(markdown)
    result.close()

if __name__ == "__main__":
    main()


    