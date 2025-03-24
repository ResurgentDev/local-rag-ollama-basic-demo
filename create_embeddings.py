import os
import numpy as np
import torch
import argparse
from transformers import AutoTokenizer, AutoModel
from config import CHUNKED_DOCS_PATH, EMBEDDINGS_PATH

# Load pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

def process_files():
    for filename in os.listdir(CHUNKED_DOCS_PATH):
        if filename.endswith('.txt'):
            with open(os.path.join(CHUNKED_DOCS_PATH, filename), 'r', encoding='utf-8') as f:
                document = f.read()

            embedding = get_embeddings(document)
            embedding_filename = filename.replace('.txt', '.npy')
            embedding_path = os.path.join(EMBEDDINGS_PATH, embedding_filename)
            os.makedirs(os.path.dirname(embedding_path), exist_ok=True)
            np.save(embedding_path, embedding)
            print(f'Saved embedding for {filename}')

def process_query(query_text, output_path):
    embedding = get_embeddings(query_text)
    dir_path = os.path.dirname(output_path)
    if dir_path:  # Only create directories if there's an actual directory path
        os.makedirs(dir_path, exist_ok=True)
    np.save(output_path, embedding)
    print(f'Saved query embedding to {output_path}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate embeddings for documents or queries')
    parser.add_argument('--query', type=str, help='Query text to embed')
    parser.add_argument('--output', type=str, help='Output file path for the query embedding')
    args = parser.parse_args()
    
    if args.query and args.output:
        process_query(args.query, args.output)
    else:
        process_files()
