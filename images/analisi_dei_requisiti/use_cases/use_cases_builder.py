from html2image import Html2Image
import os, re

root_folder = os.path.dirname(os.path.abspath(__file__))
out_folder = os.path.dirname(root_folder)
template_folder = os.path.join(root_folder, 'templates')
in_folder = os.path.join(root_folder, 'csv')
hti = Html2Image(output_path=out_folder)

html = open(f'{root_folder}/template.html', 'r').read()

def load_uc_csv(uc_type):
    lines = open(f'{in_folder}/{uc_type}.csv', 'r').readlines()
    if len(lines) == 0:
        return
    headers = lines[0].strip().split(',')
    for line in lines[1:]:
        if line.strip() == '':
            continue
        values = line.strip().split(',')
        yield dict(zip(headers, values))


def create_uc(filename, template, mappings):
    for key,val in mappings.items():
        template = template.replace('{{'+key+'}}', val)

    html_template = html.replace('{{svg}}', template)
    os.makedirs(out_folder, exist_ok=True)
    hti.screenshot(html_str=html_template, save_as=f'{filename}.png')
    print(f'Created {filename}')


def main():
    # remove all .png files in out folder
    for f in os.listdir(out_folder):
        if re.match(r'.*\.png', f):
            os.remove(os.path.join(out_folder, f))

    out_filenames = {
        'parent_child': ('uc_child_code', (500, 180)),
        'extends': ('uc_code', (500, 370)),
        'simple': ('uc_code', (500, 230)),
    }


    for uc_type, (filename, size) in out_filenames.items():
        template = open(f'{template_folder}/{uc_type}.svg', 'r').read()
        hti.size = size
        for uc in load_uc_csv(uc_type):
            if uc != None:
                create_uc(uc[filename], template, uc)

if __name__ == '__main__':
    main()
