import re
tex = 'requisiti.tex'
lines = open(tex).read()
# split by subsection
subs = lines.split('\\subsection')

obj = {}

for s in subs:
    type = re.findall(r'^\{Requisiti (.*)\}', s)
    if not type:
        continue
    else:
        type = type[0]

    obj[type] = {}
    print(type)
    lines = re.findall(r'.*([^\\].*)&(.*)&(.*)&.*\s+\\\\', s)
    for code, priority, source in lines:
        if '\\' in code:
            continue

        priority = priority.strip()
        source = source.strip()

        if not priority in obj[type]:
            obj[type][priority] = 1
        else:
            obj[type][priority] += 1

print(obj)
