import os
import faiss
import numpy as np
from config import EMBEDDINGS_PATH, CHUNKED_DOCS_PATH, INDEXES_PATH, INDEX_FILE

def setup_faiss_index() -> tuple[faiss.IndexFlatL2, list[str]]:
    """
    Set up and populate the FAISS index with document embeddings.
    """
    embedding_dim = 768  # Adjust based on your embedding dimension (default BERT is 768)
    os.makedirs(INDEXES_PATH, exist_ok=True)
    index = faiss.IndexFlatL2(embedding_dim)
    chunk_map = {}  # Map to store index -> filename mapping
    
    # First, sort files to ensure consistent indexing
    files = sorted(os.listdir(EMBEDDINGS_PATH))
    for idx, file in enumerate(files):
        if file.endswith('.npy'):
            # Derive corresponding chunk filename
            chunk_name = file.replace('.npy', '.txt')
            chunk_file = os.path.join(CHUNKED_DOCS_PATH, chunk_name)

            if os.path.exists(chunk_file):
                # Add embedding to FAISS index
                embedding = np.load(os.path.join(EMBEDDINGS_PATH, file))
                index.add(embedding)
                chunk_map[idx] = chunk_name  # Store mapping
                print(f"Added {chunk_name} at index {idx}")

    # Save both the FAISS index and the chunk mapping
    faiss.write_index(index, INDEX_FILE)
    
    # Save mapping next to the index
    map_file = os.path.join(INDEXES_PATH, "chunk_map.txt")
    with open(map_file, 'w') as f:
        for idx, name in chunk_map.items():
            f.write(f"{idx}\t{name}\n")

    print(f"Indexed {len(chunk_map)} document chunks")
    return index, chunk_map

if __name__ == "__main__":
    index, chunk_map = setup_faiss_index()
