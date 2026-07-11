---
name: check_wiki_health
description: Validates the factual integrity of the generated wiki by comparing it against the raw source text to identify hallucinations.
---

When the user asks you to check the health of the wiki or check for hallucinations, you must follow this standard operating procedure:

1. **Setup**:
   - Ensure the required python dependencies are installed by running `pip install -r .agents/skills/check_wiki_health/scripts/requirements.txt` in the workspace root.
   - If nltk punkt data is required, the script handles its downloading automatically, but be aware of it.

2. **Execute Validation**:
   - Run the validation script: `python .agents/skills/check_wiki_health/scripts/check_health.py`
   - The script will evaluate all markdown files in the `wiki/` directory against the raw text in `raw/imitation_of_christ/imitation_of_christ.md`.
   - It will use sentence embeddings to check that each sentence in the wiki has a semantic similarity score of > 0.75 compared to at least one sentence in the raw text.

3. **Report Review**:
   - The script outputs a report to `output/wiki-health-report.md`.
   - Read this report using the file viewing tools.
   - Summarize the key findings for the user, highlighting the number of hallucination violations and pointing them to the full report artifact for details.
