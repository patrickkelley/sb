import re

with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'r') as f:
    content = f.read()

# We want to replace the part where wiki_text is loaded and tokenized
old_code = """    for wiki_file in wiki_files:
        wiki_text = load_text_from_file(wiki_file)
        wiki_sentences = nltk.sent_tokenize(wiki_text)
        wiki_sentences = [s.strip() for s in wiki_sentences if len(s.strip()) > 15] # Skip very short snippets/headers"""

new_code = """    for wiki_file in wiki_files:
        wiki_text = load_text_from_file(wiki_file)
        
        # Strip structural lines
        clean_lines = []
        for line in wiki_text.split('\\n'):
            line = line.strip()
            if line.startswith(('#', '>', '**', '---')):
                continue
            clean_lines.append(line)
        wiki_text = ' '.join(clean_lines)
        
        wiki_sentences = nltk.sent_tokenize(wiki_text)
        wiki_sentences = [s.strip() for s in wiki_sentences if len(s.strip()) > 15] # Skip very short snippets/headers"""

content = content.replace(old_code, new_code)

with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'w') as f:
    f.write(content)
