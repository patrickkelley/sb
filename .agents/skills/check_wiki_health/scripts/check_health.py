import os
import re
import glob
import torch
import nltk
from sentence_transformers import SentenceTransformer, util

# Ensure nltk punkt data is available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def load_text_from_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    print("Initializing models...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    similarity_threshold = 0.65
    
    workspace_dir = '/workspaces/sb'
    raw_file = os.path.join(workspace_dir, 'raw/imitation_of_christ/imitation_of_christ.md')
    wiki_dir = os.path.join(workspace_dir, 'wiki')
    output_dir = os.path.join(workspace_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    report_file = os.path.join(output_dir, 'wiki-health-report.md')
    
    if not os.path.exists(raw_file):
        print(f"Error: Raw file not found at {raw_file}")
        return

    print("Loading raw material...")
    raw_text = load_text_from_file(raw_file)
    
    # Clean up raw text safely without deleting paragraphs
    raw_text = re.sub(r"THE IMITATION OF CHRIST\.?", " ", raw_text)
    raw_text = re.sub(r"BOOK [A-ZIVX]+\. CHAP\.", " ", raw_text)
    
    raw_sentences = nltk.sent_tokenize(raw_text)
    
    # Filter out very short strings which might just be whitespace or punctuation
    raw_sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 5]
    
    print(f"Extracted {len(raw_sentences)} sentences from raw text.")
    print("Encoding raw sentences (this may take a moment)...")
    raw_embeddings = model.encode(raw_sentences, convert_to_tensor=True)
    
    wiki_files = glob.glob(os.path.join(wiki_dir, '**/*.md'), recursive=True)
    
    violations = []
    
    print(f"Found {len(wiki_files)} wiki files. Validating...")
    
    for wiki_file in wiki_files:
        wiki_text = load_text_from_file(wiki_file)
        
        # Strip structural lines
        clean_lines = []
        for line in wiki_text.split('\n'):
            line = line.strip()
            if line.startswith(('#', '>', '**', '---', '- ', '* ', '*See also:*')):
                continue
            clean_lines.append(line)
        wiki_text = ' '.join(clean_lines)
        
        wiki_sentences = nltk.sent_tokenize(wiki_text)
        wiki_sentences = [s.strip() for s in wiki_sentences if len(s.strip()) > 15] # Skip very short snippets/headers
        
        if not wiki_sentences:
            continue
            
        # Encode wiki sentences
        wiki_embeddings = model.encode(wiki_sentences, convert_to_tensor=True)
        
        # Compute cosine similarities against all raw sentences
        cosine_scores = util.cos_sim(wiki_embeddings, raw_embeddings)
        
        for i in range(len(wiki_sentences)):
            max_score_item = torch.max(cosine_scores[i])
            max_score = max_score_item.item()
            best_match_idx = torch.argmax(cosine_scores[i]).item()
            
            if max_score < similarity_threshold:
                violations.append({
                    'file': os.path.relpath(wiki_file, workspace_dir),
                    'wiki_sentence': wiki_sentences[i],
                    'best_match': raw_sentences[best_match_idx],
                    'score': max_score
                })

    print(f"Validation complete. Found {len(violations)} potential hallucinations.")
    
    # Generate report
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Wiki Health Report\n\n")
        f.write("This report details potential hallucination violations in the wiki where the text significantly deviates from the raw source material.\n\n")
        f.write(f"**Similarity Threshold:** {similarity_threshold}\n\n")
        
        if len(violations) == 0:
            f.write("✅ **Excellent health!** No hallucination violations found.\n")
        else:
            f.write(f"❌ **Found {len(violations)} violations.**\n\n")
            
            # Group violations by file
            violations_by_file = {}
            for v in violations:
                file_name = v['file']
                if file_name not in violations_by_file:
                    violations_by_file[file_name] = []
                violations_by_file[file_name].append(v)
                
            for file_name, file_violations in violations_by_file.items():
                f.write(f"## {file_name}\n\n")
                for v in file_violations:
                    f.write(f"**Wiki Sentence:**\n> {v['wiki_sentence']}\n\n")
                    f.write(f"**Closest Match in Raw Text (Score: {v['score']:.4f}):**\n> {v['best_match']}\n\n")
                    f.write("---\n\n")
                    
    print(f"Report saved to {report_file}")

if __name__ == "__main__":
    main()
