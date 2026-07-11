---
name: build_wiki
description: Process unorganized raw text sources into highly-focused Zettelkasten wiki nodes and thematic maps.
---

When the user asks you to build or update the wiki with a new raw text source, you must follow this standard operating procedure:

1. **Analyze the Source**: 
   - Read the target raw file using file viewing or searching tools.
   - Identify the source's structural markers (e.g., chapters, sections, articles).
   - Actively scan for OCR corruption, stray marks, page headers, footers, or formatting anomalies that would break a naive parsing script.

2. **Draft a Custom Extraction Script**: 
   - Do NOT try to manually extract the entire text using file editing tools. 
   - Instead, write a robust Python script (using state-machine logic, fuzzy-regex matching, or similar strategies) to partition the text into atomic nodes (one markdown file per chapter/section).
   - Ensure your script explicitly strips out page headers, footers, and OCR anomalies.

3. **Thematic Mapping**: 
   - Dynamically identify key concepts in the text and map the extracted nodes to the existing core themes located in `wiki/themes/`.
   - Only generate novel themes if the text introduces completely new concepts not adequately covered by the core themes.

4. **Enforce the Three-Tier Architecture**:
   - The extraction script must save the output into the Zettelkasten permanent network: `wiki/[source_name]/` as atomic `.md` files.
   - The script must also update or create the relevant theme hub files in `wiki/themes/`.
   - Ensure all nodes and themes are connected bi-directionally using standard `[[WikiLink]]` syntax.

5. **Execution and Verification**: 
   - Execute the python script you wrote.
   - Verify the generated file structure and ensure the contents look clean.
   - End by creating a `walkthrough.md` artifact summarizing what was processed and any edge cases you had to handle.
