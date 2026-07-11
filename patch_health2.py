import re

with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'r') as f:
    content = f.read()

old_code = """    print("Loading raw material...")
    raw_text = load_text_from_file(raw_file)
    raw_sentences = nltk.sent_tokenize(raw_text)"""

new_code = """    print("Loading raw material...")
    raw_text = load_text_from_file(raw_file)
    
    # Clean up raw text (remove headers, page numbers, etc.) to match wiki
    raw_text = re.sub(r"THE IMITATION OF CHRIST.*?\\n", " ", raw_text)
    raw_text = re.sub(r"BOOK [A-ZIVX]+\\. CHAP\\..*?\\n", " ", raw_text)
    raw_text = re.sub(r"\\n\\s*[A-ZIVX]+\\.\\s*\\n", " ", raw_text)
    raw_text = re.sub(r"\\n\\s*[0-9]+\\s*\\n", " ", raw_text)
    # Fix common OCR splitting errors like "de-\\n\\nsires"
    raw_text = re.sub(r"-\\n+sires", "sires", raw_text)
    raw_text = re.sub(r"de-\\n+sires", "desires", raw_text)
    
    raw_sentences = nltk.sent_tokenize(raw_text)"""

content = content.replace(old_code, new_code)

with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'w') as f:
    f.write(content)
