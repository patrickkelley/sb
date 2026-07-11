import os
import re
import glob

raw_file = "/workspaces/sb/raw/imitation_of_christ/imitation_of_christ.md"
with open(raw_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove Google watermarks
text = re.sub(r'\*\*The text on this page is estimated to be only [0-9.%]+ accurate\*\*', '', text)
# Remove page headers
text = re.sub(r'BOOK\s+[IVX]+\.\s+CHAP(?:TER|\.)\s+[IVXLC]+\.?\s+\d+', '', text)
text = re.sub(r'BOOR\s+[IVX]+\.\s+CHAP(?:TER|\.)\s+[IVXLC]+\.?\s+\d+', '', text)
text = re.sub(r'BOOK\s+[IVX]+\.\s+CBAF\.\s+[IVXLC]+\.?\s+\d+', '', text)
text = re.sub(r'\b\d+\s+THE IMITATION OF CHRIST\.?', '', text)
text = re.sub(r'THE IMITATION OF CHRIST\.?\s+\d+\b', '', text)
text = re.sub(r'THE IMITATION OF CHRIST,?', '', text)
text = re.sub(r'TBB IMITATION OF CHRIST\.?', '', text)

# Define Book delimiters
book_delims = [
    (1, r'§ook I\.'),
    (2, r'§aah II\.'),
    (3, r'§00klll\.'),
    (4, r'§ooK IV\.')
]

# Find the start indices of each book
book_starts = []
for b, delim in book_delims:
    match = re.search(delim, text)
    if match:
        book_starts.append((b, match.start()))

book_starts.sort(key=lambda x: x[1])

themes = {
    'detachment': ['detach', 'world', 'vanity', 'creature'],
    'divine_consolation': ['consolation', 'comfort', 'joy'],
    'grace': ['grace', 'gift'],
    'humility': ['humble', 'humility', 'pride', 'vain'],
    'obedience': ['obedien', 'subject', 'superior'],
    'patience': ['patient', 'patience', 'bear', 'suffer', 'tribulation'],
    'prayer': ['pray', 'prayer', 'devotion'],
    'self_denial': ['deny', 'cross', 'mortif', 'flesh']
}

theme_names = {
    'detachment': 'Detachment',
    'divine_consolation': 'Divine Consolation',
    'grace': 'Grace',
    'humility': 'Humility',
    'obedience': 'Obedience',
    'patience': 'Patience',
    'prayer': 'Prayer',
    'self_denial': 'Self-Denial'
}

# Ensure directories exist
for i in range(1, 5):
    os.makedirs(f"/workspaces/sb/wiki/imitation_of_christ/book_{i}", exist_ok=True)

# Also clear the old contents of the directories
for f in glob.glob("/workspaces/sb/wiki/imitation_of_christ/book_*/*.md"):
    os.remove(f)

theme_links = {t: [] for t in themes.keys()}

def roman_to_int(s):
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val

chapters_info = []

for idx, (b_num, start) in enumerate(book_starts):
    end = book_starts[idx+1][1] if idx+1 < len(book_starts) else len(text)
    book_text = text[start:end]
    
    chapter_matches = list(re.finditer(r'CHAPTER\s+([IVXLC]+)\.\s*(.*?)(?=(?:CHAPTER\s+[IVXLC]+\.|$))', book_text, re.DOTALL))
    
    for match in chapter_matches:
        c_num = match.group(1)
        c_int = roman_to_int(c_num)
        c_content = match.group(2).strip()
        
        lines = c_content.split('\n')
        raw_title = lines[0].strip()
        if raw_title.endswith('.'):
            raw_title = raw_title[:-1]
        
        body = '\n'.join(lines[1:]).strip()
        
        # Clean up some stray characters
        body = re.sub(r'^\s*I\.\s*', '', body)  # Remove leading I. 
        body = re.sub(r'\s{2,}', ' ', body) # Normalize spaces
        body = body.replace(' 5 ', ' ; ') # common OCR error
        body = body.replace(' 3 ', ' ; ')
        
        # Detect themes
        c_themes = []
        body_lower = body.lower()
        title_lower = raw_title.lower()
        for t, keywords in themes.items():
            if any(re.search(r'\b' + k + r'[a-z]*\b', body_lower) or re.search(r'\b' + k + r'[a-z]*\b', title_lower) for k in keywords):
                c_themes.append(t)
        
        clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', raw_title).lower().replace(' ', '_')
        clean_title = clean_title[:45].strip('_')
        filename = f"ch{c_int:02d}_{clean_title}.md"
        filepath = f"/workspaces/sb/wiki/imitation_of_christ/book_{b_num}/{filename}"
        
        node_name = f"Book {b_num} Ch {c_int:02d} — {raw_title}"
        
        chapters_info.append({
            'book': b_num,
            'chap_num': c_int,
            'title': raw_title,
            'filepath': filepath,
            'node_name': node_name,
            'themes': c_themes,
            'body': body
        })

# Now write them and link them sequentially
for i, chap in enumerate(chapters_info):
    for t in chap['themes']:
        theme_links[t].append(f"[[{chap['node_name']}]]")
        
    next_node = f"[[{chapters_info[i+1]['node_name']}]]" if i+1 < len(chapters_info) else "None"
    
    themes_str = ", ".join([f"[[{theme_names[t]}]]" for t in chap['themes']]) if chap['themes'] else "None"
    
    content = f"# {chap['title']}\n\n"
    content += f"> **Book {chap['book']}, Chapter {chap['chap_num']}** — *The Imitation of Christ* by [[Thomas à Kempis]]\n\n"
    content += f"## Text\n\n{chap['body']}\n\n---\n\n"
    content += f"**Themes:** {themes_str}\n"
    content += f"**Next:** {next_node}\n"
    
    with open(chap['filepath'], 'w', encoding='utf-8') as f:
        f.write(content)

# Update theme files
for t, links in theme_links.items():
    theme_file = f"/workspaces/sb/wiki/themes/{t}.md"
    if os.path.exists(theme_file):
        with open(theme_file, 'r', encoding='utf-8') as f:
            t_content = f.read().rstrip()
        
        links_str = "\n".join([f"- {l}" for l in links])
        
        if "### Imitation of Christ (Extracted)" in t_content:
            t_content = re.sub(r'### Imitation of Christ \(Extracted\).*', f"### Imitation of Christ (Extracted)\n\n{links_str}", t_content, flags=re.DOTALL)
        else:
            t_content += f"\n\n### Imitation of Christ (Extracted)\n\n{links_str}"
            
        with open(theme_file, 'w', encoding='utf-8') as f:
            f.write(t_content + "\n")

print(f"Successfully processed {len(chapters_info)} chapters.")
