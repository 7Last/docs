import re, os

glossary_tex = '2_RTB/documentazione_interna/glossario/glossario.tex'
root_folder = '../'
glossary_url = 'https://7last.github.io/docs/rtb/glossario'

def parse_glossary(glossary_tex):
    with open(root_folder + glossary_tex, 'r') as f:
        file = f.read()
    file = re.sub(r'[\n\t\r]', '', file)
    rows = re.findall(r'\\newglossaryentry{(.*?)}{\s*name={(.*?)},\s*description={(.*?)},\s*plural={(.*?)},\s*feminine={(.*?)},\s*feminine_plural={(.*?)}', file)
    glossary = {}
    ordered_glossary = {}
    for word, name, _, plural, feminine, feminine_plural in rows:
        glossary[word] = {
            'name': name,
            'plural': plural,
            'feminine': feminine,
            'feminine_plural': feminine_plural}
    for k in sorted(glossary, key=len, reverse=True):
        ordered_glossary[k] = glossary[k]
    return ordered_glossary

def search_tex_files(root_folder):
    glossary = parse_glossary(glossary_tex)
    for root, _, files in os.walk(root_folder):
        for file in files:
            path = os.path.join(root, file)
            if "glossario" in path or "0_template" in path or "1_candidatura" in path or file == "variables.tex" or file == "title.tex" or file == "header.tex" or file == "packages.tex":
                continue
            if file.endswith('.tex'):
                replace_word(path, glossary)

def is_within_section(file_content, start):
    matches = [m for m in re.finditer(r'section{[^}]*', file_content[:start])]
    for match in reversed(matches):
        match_end = match.end()
        if '}' not in file_content[match_end:start]:
            return True
    return False

def is_already_subscripted(file_content, end):
    matches = [m for m in re.finditer(r'[^}]*\\textsubscript{G}', file_content[end:])]
    for match in matches:
        match_start = match.start()
        if '}' not in file_content[end:end+match_start]:
            return True
    return False

def is_within_href(file_content, start):
    matches = [m for m in re.finditer(r'\\href{[^}]*', file_content[:start])]
    for match in reversed(matches):
        match_end = match.end()
        if '}' not in file_content[match_end:start]:
            return True
    return False

def style_command(file_content, start):
    style_commands = ['\\textit{', '\\itshape{', '\\emph{', '\\textbf{', '\\bfseries{']
    for command in style_commands:
        if command in file_content[max(0, start-len(command)):start]:
            return command
    return ''

def replace_word(path, glossary):
    with open(path, 'r') as f:
        file_content = f.read()
        if not glossary:
            print("Empty glossary. Exiting...")
            return
    for word in glossary:
        file_content_lower = file_content.lower()
        parole = [glossary[word]['name'],
                  glossary[word]['plural'],
                  glossary[word]['feminine'],
                  glossary[word]['feminine_plural']]
        for parola in parole:
            if parola == '' or parola.lower() not in file_content_lower:
                continue
            pattern = r'\b' + re.escape(parola) + r'\b'
            matches = [m for m in re.finditer(pattern, file_content, re.IGNORECASE)]
            for match in reversed(matches):
                match_start = match.start()
                match_end = match.end()
                while True:
                    len_style_command = len(style_command(file_content, match_start))
                    if len_style_command > 0:
                        match_start -= len_style_command
                        match_end += 1
                    else:
                        break
                if is_within_href(file_content, match_start) or is_within_section(file_content, match_start) or is_already_subscripted(file_content, match_end):
                    continue
                url = glossary_url + "#" + word.lower().replace(' ', '-')
                replacement = '\\href{' + url + '}{' + file_content[match_start:match_end] + '\\textsubscript{G}}'
                file_content = file_content[:match_start] + replacement + file_content[match_end:]
    with open(path, 'w') as f:
        f.write(file_content)

def main():
    search_tex_files(root_folder)

if __name__ == '__main__':
    main()