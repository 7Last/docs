import re, os

root_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
glossary_tex = f'{root_folder}/2_RTB/documentazione_interna/glossario/glossario.tex'
glossary_url = 'https://7last.github.io/docs/rtb/documentazione-interna/glossario'


def parse_glossary():
    file = open(glossary_tex, 'r').read()
    file = re.sub(r'[\n\t\r]', '', file)

    name = r'(?=.*name=(?:{?)([^,}]+)(?:}?))'
    description = r'(?=.*description=(?:{?)([^,}]+)(?:}?))'
    plural = '(?:.*plural=(?:{?)([^,}]+)(?:}?))?'
    feminine = '(?:.*plural=(?:{?)([^,}]+)(?:}?))?'
    feminine_plural = '(?:.*feminine_plural=(?:{?)([^,}]+)(?:}?))?'

    pattern = r'\\newglossaryentry{([^{}]+)}' + fr'{name}{description}{plural}{feminine}{feminine_plural}'
    matches = re.findall(pattern, file)

    glossary = {}
    for word, name, _, plural, feminine, feminine_plural in matches:
        glossary[word] = {
            'name': name,
            'plural': plural,
            'feminine': feminine,
            'feminine_plural': feminine_plural,
        }

    ordered_glossary = {}
    for k in sorted(glossary, key=len, reverse=True):
        ordered_glossary[k] = glossary[k]
    return ordered_glossary


def search_tex_files():
    exclude = ['glossario', '0_template', '1_candidatura', 'variables.tex', 'title.tex', 'header.tex', 'packages.tex']
    glossary = parse_glossary()
    for root, _, files in os.walk(root_folder):
        for file in files:
            path = os.path.join(root, file)
            if any([e in path for e in exclude]):
                continue
            if file.endswith('.tex'):
                replace_words(path, glossary)


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
        if '}' not in file_content[end:end + match_start]:
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
    style_commands = ['\\textit{', '\\itshape{', '\\emph{', '\\textbf{', '\\bfseries{', '\\uline{', '\\underline{',
                      '\\textsc{', '\\scshape{']
    for command in style_commands:
        if command in file_content[max(0, start - len(command)):start]:
            return command
    return ''


def replace_words(path, glossary):
    with open(path, 'r') as f:
        file_content = f.read()
        if not glossary:
            print("Empty glossary. Exiting...")
            return

    for word in glossary:
        file_content_lower = file_content.lower()
        word_variants = glossary[word].values()

        for variant in word_variants:
            if variant == '' or variant.lower() not in file_content_lower:
                continue
            pattern = r'\b' + re.escape(variant) + r'\b'
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

                if is_within_href(file_content, match_start) \
                        or is_within_section(file_content, match_start) \
                        or is_already_subscripted(file_content, match_end):
                    continue
                url = glossary_url + "#" + word.lower().replace(' ', '-')
                replacement = '\\href{' + url + '}{' + file_content[match_start:match_end] + '\\textsubscript{G}}'
                file_content = file_content[:match_start] + replacement + file_content[match_end:]

    open(path, 'w').write(file_content)


def main():
    search_tex_files()


if __name__ == '__main__':
    main()
