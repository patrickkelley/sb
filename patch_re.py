with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'r') as f:
    content = f.read()
if 'import re' not in content:
    content = content.replace('import os\n', 'import os\nimport re\n')
    with open('.agents/skills/check_wiki_health/scripts/check_health.py', 'w') as f:
        f.write(content)
