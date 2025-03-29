import os
import nltk
from typing import List  
from nltk.tokenize import sent_tokenize
from config import RAW_DOCS_PATH, CHUNKED_DOCS_PATH
from nltk.data import find

# Download necessary NLTK resources
def ensure_punkt():
    """
    Ensures the 'punkt' tokenizer resource from NLTK is available for use.

    The 'punkt' tokenizer is part of NLTK's corpus resources and is required
    for tokenizing text into sentences. It is not included by default with the 
    base NLTK package and must be downloaded separately.

    This function dynamically checks if the 'punkt' tokenizer is already 
    downloaded on the user's machine. If not, it automatically downloads the 
    resource. Once downloaded, it is stored locally and does not require 
    re-downloading for future use, allowing the tool to function offline.

    Key Features:
    - Dynamically verifies the availability of the 'punkt' resource using
      `nltk.data.find('tokenizers/punkt')`.
    - Provides informative messaging to users about the status of the resource
      (e.g., whether it is already available or being downloaded).
    - Only downloads the resource when necessary, minimizing redundant operations.

    Advantages:
    - Supports scenarios where the tool is run in environments with limited or 
      pre-configured resources, avoiding unnecessary downloads.
    - Improves user experience by ensuring the necessary resource is available 
      without requiring manual intervention.

    Usage Notes:
    - Users must have an active internet connection for the initial download of 
      the 'punkt' tokenizer. Once downloaded, the tool can operate offline.
    - The downloaded resource is typically stored in the default NLTK data 
      directory (e.g., `~/.nltk_data` or `%APPDATA%/nltk_data`).
    - If distributing the tool, developers may pre-download the 'punkt' resource 
      and package it with the tool to eliminate the need for dynamic downloads.

    Example:
    >>> ensure_punkt()
    [INFO] 'punkt' tokenizer is already downloaded and available for use.

    Implementation:
    This function is designed to be reusable and modular, allowing it to be 
    integrated seamlessly into any NLTK-based application.

    """
    try:
        # Check if 'punkt' tokenizer is already available
        find('tokenizers/punkt')
        print("[INFO] 'punkt' tokenizer is already downloaded and available for use.")
    except LookupError:
        # If not found, download the resource
        print("[INFO] 'punkt' tokenizer not found. Downloading now...")
        nltk.download('punkt')
        print("[INFO] 'punkt' tokenizer successfully downloaded.")

# Ensure the necessary NLTK resource is available
ensure_punkt()

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
