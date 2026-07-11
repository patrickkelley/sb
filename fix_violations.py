import re
import os

with open('/workspaces/sb/output/wiki-health-report.md', 'r') as f:
    content = f.read()

blocks = re.split(r'^##\s+', content, flags=re.MULTILINE)[1:]

for block in blocks:
    lines = block.split('\n')
    filepath = lines[0].strip()
    
    if not os.path.exists(filepath):
        filepath = os.path.join('/workspaces/sb', filepath)
        if not os.path.exists(filepath):
            continue
            
    with open(filepath, 'r') as f:
        file_content = f.read()
        
    sentences = re.findall(r'\*\*Wiki Sentence:\*\*\n> (.*?)\n\n\*\*Closest', block, re.DOTALL)
    
    original_content = file_content
    for s in sentences:
        s = s.strip()
        # Find the exact string in the file. The report might have stripped whitespace, 
        # but let's try a regex search that ignores whitespace differences.
        pattern = r'\s*'.join(re.escape(word) for word in s.split())
        file_content = re.sub(pattern, '', file_content)
        
    if file_content != original_content:
        with open(filepath, 'w') as f:
            f.write(file_content)

print("Done fixing.")
