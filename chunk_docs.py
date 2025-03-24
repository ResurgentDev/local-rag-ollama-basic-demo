import os
import nltk
from typing import List  
from nltk.tokenize import sent_tokenize
from config import RAW_DOCS_PATH, CHUNKED_DOCS_PATH

# Download necessary NLTK resources
nltk.download('punkt')

def chunk_document(text: str, chunk_size: int = 200) -> List[str]:  
    """
    Split document into chunks while preserving sentence boundaries.
    
    Args:
        text: The document text to chunk
        chunk_size: Target number of sentences per chunk
        
    Returns:
        List of text chunks
    """
    sentences = sent_tokenize(text)
    chunks = [' '.join(sentences[i:i + chunk_size]) for i in range(0, len(sentences), chunk_size)]
    return chunks

def process_files() -> None:
    """Process all markdown files in the raw docs directory into chunks."""
    for filename in os.listdir(RAW_DOCS_PATH):
        if filename.endswith('.md'):
            with open(os.path.join(RAW_DOCS_PATH, filename), 'r', encoding='utf-8') as f:
                document = f.read()

            chunks = chunk_document(document)
            for i, chunk in enumerate(chunks):
                chunk_filename = f"{filename.replace('.md', '')}_chunk_{i}.txt"
                chunk_path = os.path.join(CHUNKED_DOCS_PATH, chunk_filename)
                os.makedirs(os.path.dirname(chunk_path), exist_ok=True)
                with open(chunk_path, 'w', encoding='utf-8') as chunk_file:
                    chunk_file.write(chunk)
                print(f'Saved chunk {i} for {filename}')

if __name__ == "__main__":
    process_files()
