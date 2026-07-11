import os
import re
from pathlib import Path

wiki_dir = Path('/workspaces/sb/wiki')

def fix_content(content, filepath):
    # 1. Extract the Book/Chapter block
    block_regex = r'(> \*\*Book \d+, Chapter \d+\*\* — \*The Imitation of Christ\* by \[\[Thomas à Kempis\]\]\n\n## Text\n\n?)'
    block_match = re.search(block_regex, content)
    if block_match:
        block_text = block_match.group(1)
        content = content.replace(block_text, '')
    else:
        block_text = ''

    # 2. Extract H1 and insert the block after it
    # Find `# Title. I.` and split it so the block can be inserted.
    content = re.sub(r'^(# [^\n]+?)(?=\s*I\.\s)', r'\1\n\n' + block_text.strip() + r'\n\n', content, count=1)
    if block_text.strip() not in content:
        content = re.sub(r'^(# [^\n]+?\.)\s', r'\1\n\n' + block_text.strip() + r'\n\n', content, count=1)

    # 3. Remove known OCR garbage and running headers
    content = re.sub(r'\b\d+\s+THE IMITATION OF CHAI?8?S?T\.\s*', '', content)
    content = re.sub(r'\bBOOK [IV]+\.? CHAP\.?(?: [XVIIV]+)?\b\.?\s*', '', content)
    content = re.sub(r'\bBOOK [IV]+\.\s*', '', content)
    content = re.sub(r'The text on this page is estimated to be only \d+\.\d+% accurate', '', content)
    
    # Specific OCR error fixes identified in the health report
    content = re.sub(r' dc1\) 2 ', ' de', content) 
    content = re.sub(r'\bd2\b\s*', '', content) 
    content = re.sub(r'\ba \.\s+', '', content) 
    content = re.sub(r'\bao \.\s+', '', content) 
    content = content.replace('P^ace', 'Peace')
    content = content.replace('o?h ^^ peace j they are troublesome to the^*^ ^ut', 'others in peace; they are troublesome to them but')
    content = content.replace('Ml peace', 'all peace')
    content = content.replace('maUi sweet', 'how sweet')
    content = content.replace('«>r himself* **^ ««>««ii to', '')
    content = content.replace(' \ T', '')
    content = content.replace('I J', '')

    # 4. Fix Next link
    def fix_next(match):
        link = match.group(1)
        trunc = re.split(r'\.\s*(?:I\.|II\.|III\.|IV\.|V\.|VI\.|•)', link)
        return f"**Next:** [[{trunc[0].strip()}]]"

    content = re.sub(r'\*\*Next:\*\*\s*\[\[(.*?)\]\]', fix_next, content, flags=re.DOTALL)

    # 5. Fix trailing spaces on each line and strip the file
    content = "\n".join(line.rstrip() for line in content.splitlines())
    content = content.strip() + "\n"

    return content

if __name__ == '__main__':
    modified_count = 0
    for root, dirs, files in os.walk(wiki_dir):
        for file in files:
            if file.endswith('.md'):
                filepath = Path(root) / file
                with open(filepath, 'r') as f:
                    original = f.read()
                
                fixed = fix_content(original, filepath)
                
                if original != fixed:
                    with open(filepath, 'w') as f:
                        f.write(fixed)
                    modified_count += 1
    
    print(f"Fixed {modified_count} markdown files.")
