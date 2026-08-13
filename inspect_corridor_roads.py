import re
from pathlib import Path

text = Path('/home/ubuntu/idaho-highway-map/client/src/data/roadData.ts').read_text(encoding='utf-8')
patterns = [r'"name":"([^"]*(?:16|Sweet|Ola|High Valley|Council|Emmett|I-84|Interstate 84)[^"]*)"', r'"ref":"([^"]+)"']
for pattern in patterns:
    values = sorted(set(re.findall(pattern, text, flags=re.I)))
    print(pattern)
    for value in values[:250]:
        print(value)
