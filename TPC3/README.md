# Conversor de Markdown para HTML

## Acerca de
Este programa lê um ficheiro Markdown (`Exemplo.md`) e converte-o para HTML, gerando um ficheiro `Resultado.html`. A conversão é feita através de expressões regulares (Regex) que identificam elementos específicos do Markdown e os substituem pelas suas equivalências em HTML.

## Estrutura do Código

### `main()`
A função principal executa os seguintes passos:
1. Lê o conteúdo do ficheiro `Exemplo.md`.
2. Aplica uma série de expressões regulares para converter elementos do Markdown em HTML.
3. Escreve o resultado no ficheiro `Resultado.html`.

## Explicação das Expressões Regulares

### Cabeçalhos (`#`, `##`, `###`)
```python
markdown = re.sub(r'^(#{1,3})\s*(.*)', 
                lambda m: f'<h{len(m.group(1))}>{m.group(2)}</h{len(m.group(1))}>', 
                markdown, flags=re.M)
```
- Captura um a três `#` seguidos de um espaço e o texto do cabeçalho.
- `#{1,3}`: Captura entre um e três `#`.
- `\s*`: Captura qualquer número de espaços após os `#`.
- `(.*)`: Captura o texto do cabeçalho.
- Substitui pelo elemento `<h1>`, `<h2>` ou `<h3>` conforme o número de `#`.

### Negrito (`**texto**`)
```python
markdown = re.sub(r'\*\*(.+)\*\*' , r'<b>\1</b>', markdown , flags = re.M)
```
- `\*\*(.+)\*\*`: Captura qualquer texto entre `**`.
- `(.+)`: Captura qualquer sequência de caracteres.
- Substitui por `<b>texto</b>` para negrito.

### Itálico (`*texto*`)
```python
markdown = re.sub(r'\*(.+)\*' , r'<i>\1</i>', markdown , flags = re.M)
```
- `\*(.+)\*`: Captura qualquer texto entre `*`.
- `(.+)`: Captura qualquer sequência de caracteres.
- Substitui por `<i>texto</i>` para itálico.

### Listas Ordenadas (`1. Item`)
```python
markdown = re.sub(r'^\d+\.\s+(.+)' , r'<li>\1</li>', markdown, flags = re.M)
markdown = re.sub(r'(<li>.*?</li>(?:\n<li>.*?</li>)*)', r'<ol>\n\1\n</ol>', markdown, flags = re.S)
```
- `^\d+\.\s+(.+)`: Captura números seguidos de `.` e espaço no início da linha.
- `(.+)`: Captura o texto do item.
- Primeiro substitui por `<li>Item</li>`.
- Depois, agrupa todos os `<li>` consecutivos dentro de `<ol>` para criar uma lista ordenada.

### Imagens (`![alt](url)`) 
```python
markdown = re.sub(r'!\[(.+)\]\((.+)\)' , r'<img src="\2" alt="\1">', markdown, flags = re.M)
```
- `!\[(.+)\]\((.+)\)`: Captura imagens no formato Markdown.
- `(.+)`: Captura o texto alternativo.
- `(.+)`: Captura o URL da imagem.
- Substitui por `<img src="url" alt="alt">`.

### Links (`[texto](url)`) 
```python
markdown = re.sub(r'\[(.+)\]\((.+)\)' , r'<a href="\2">\1</a>', markdown, flags = re.M)
```
- `\[(.+)\]\((.+)\)`: Captura links no formato Markdown.
- `(.+)`: Captura o texto do link.
- `(.+)`: Captura a URL.
- Substitui por `<a href="url">texto</a>`.

## Exemplo de Entrada e Saída

### Entrada (`Exemplo.md`)
```markdown
# Título Principal

## Subtítulo Importante

### Cabeçalho Menor

Texto normal no documento.

**Texto em negrito**

*Texto em itálico*

Lista ordenada:
1. Primeiro item
2. Segundo item
3. Terceiro item

Texto entre listas.

1. Outro item numerado
2. Mais um item

Imagem de exemplo:
![Gato fofo](https://example.com/gato.jpg)

Link para um site:
[Visita este site](https://example.com)

```

### Saída (`Resultado.html`)
```html
<h1>Título Principal</h1>

<h2>Subtítulo Importante</h2>

<h3>Cabeçalho Menor</h3>

Texto normal no documento.

<b>Texto em negrito</b>

<i>Texto em itálico</i>

Lista ordenada:
<ol>
<li>Primeiro item</li>
<li>Segundo item</li>
<li>Terceiro item</li>
</ol>

Texto entre listas.

<ol>
<li>Outro item numerado</li>
<li>Mais um item</li>
</ol>

Imagem de exemplo:
<img src="https://example.com/gato.jpg" alt="Gato fofo">

Link para um site:
<a href="https://example.com">Visita este site</a>

```

## Conclusão
Este programa realiza uma conversão básica de Markdown para HTML utilizando expressões regulares. Ele pode ser expandido para suportar mais elementos do Markdown, como listas não ordenadas, blocos de código e citações.

