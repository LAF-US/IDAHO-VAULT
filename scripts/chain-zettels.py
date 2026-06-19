import os
import re
import frontmatter

# Find all markdown files matching pattern
for root, dirs, files in os.walk('.'):
    for f in files:
        if not f.endswith('.md'):
            continue
        name = f[:-3]  # Remove .md
        if not re.match(r'^[A-Za-z0-9]+$', name) or len(name) < 2:
            continue
        
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        links = ''.join(f'[[{c}]]' for c in name)
        
        if links in content:
            continue  # Already has links
        
        # Add after frontmatter or at start
        if content.lstrip().startswith('---'):
            match = re.search(r'^---
.*
---', content, re.DOTALL)
            if match:
                end = match.end()
                new_content = content[:end] + '

' + links + ('

' + content[end:] if content[end:] else '')
            else:
                new_content = links + ('

' + content if content else '')
        else:
            new_content = links + ('

' + content if content else '')
        
        with open(path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        
        print(f'Updated: {path}')
