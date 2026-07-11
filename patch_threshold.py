with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'r') as f:
    content = f.read()
content = content.replace('similarity_threshold = 0.75', 'similarity_threshold = 0.65')
with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'w') as f:
    f.write(content)
