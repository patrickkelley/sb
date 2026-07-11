import re

with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'r') as f:
    content = f.read()

# I will find the block I added last time and replace it with a better one.
import re
start_marker = '    # Clean up raw text (remove headers, page numbers, etc.) to match wiki'
end_marker = '    raw_sentences = nltk.sent_tokenize(raw_text)'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker) + len(end_marker)

old_block = content[start_idx:end_idx]

new_block = """    # Clean up raw text safely without deleting paragraphs
    raw_text = re.sub(r"THE IMITATION OF CHRIST\.?", " ", raw_text)
    raw_text = re.sub(r"BOOK [A-ZIVX]+\\. CHAP\\.", " ", raw_text)
    
    raw_sentences = nltk.sent_tokenize(raw_text)"""

content = content.replace(old_block, new_block)

with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'w') as f:
    f.write(content)
