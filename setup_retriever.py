import os
import faiss
import numpy as np
from config import EMBEDDINGS_PATH, CHUNKED_DOCS_PATH, INDEXES_PATH, INDEX_FILE

def setup_faiss_index() -> tuple[faiss.IndexFlatL2, list[str]]:
    """
    Set up and populate the FAISS index with document embeddings.
    
    Returns:
        tuple: (FAISS index, List of indexed filenames)
    
    Raises:
        FileNotFoundError: If embedding or chunk files are missing
    """
    embedding_dim = 768  # Adjust based on your embedding dimension (default BERT is 768)
    os.makedirs(INDEXES_PATH, exist_ok=True)  # Ensure the 'Indexes' directory exists
    index = faiss.IndexFlatL2(embedding_dim)  # L2 distance (Euclidean)
    filenames = []

    for file in os.listdir(EMBEDDINGS_PATH):
        if file.endswith('.npy'):
            # Derive corresponding chunk filename
            chunk_name = file.replace('.npy', '.txt')
            chunk_file = os.path.join(CHUNKED_DOCS_PATH, chunk_name)

            # Check if the chunk file exists
            if os.path.exists(chunk_file):
                # Add embedding to FAISS index
                embedding = np.load(os.path.join(EMBEDDINGS_PATH, file))
                index.add(embedding)
                filenames.append(chunk_name)  # Record the valid chunk file
            else:
                print(f"Skipping embedding '{file}' as no corresponding chunk file '{chunk_file}' exists.")

    # Save the FAISS index
    normalized_index_file = os.path.normpath(INDEX_FILE)
    faiss.write_index(index, normalized_index_file)

    print(f"FAISS index created and saved as '{normalized_index_file}'")
    print(f"Indexed {len(filenames)} document chunks.")
    return filenames

if __name__ == "__main__":
    filenames = setup_faiss_index()
