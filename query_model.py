import os
import faiss
import numpy as np
import subprocess
import sys  # Add this import
from config import *  # Import all config settings

def load_faiss_index():
    """Load the FAISS index and chunk mapping from file."""
    if not os.path.exists(INDEX_FILE):
        raise FileNotFoundError(f"FAISS index not found at {INDEX_FILE}. Please run setup_retriever.py first.")
    
    # Load the index
    index = faiss.read_index(INDEX_FILE)
    
    # Load the chunk mapping
    map_file = os.path.join(INDEXES_PATH, "chunk_map.txt")
    if not os.path.exists(map_file):
        raise FileNotFoundError(f"Chunk mapping not found at {map_file}. Please run setup_retriever.py first.")
    
    chunk_map = {}
    with open(map_file) as f:
        for line in f:
            idx, name = line.strip().split('\t')
            chunk_map[int(idx)] = name
            
    print("FAISS index and chunk mapping loaded.")
    return index, chunk_map

def embed_query(query):
    """Generate an embedding for the query using the embedding script."""
    print("Generating embedding for query...")
    embedding_file = os.path.join(BASE_DIR, 'query_embedding.npy')
    
    # Use the same Python interpreter that's running this script
    python_exe = sys.executable
    subprocess.run([python_exe, EMBEDDING_SCRIPT, '--query', query, '--output', embedding_file], check=True)
    
    # Load and return the embedding
    if not os.path.exists(embedding_file):
        raise FileNotFoundError(f"Query embedding file not found at {embedding_file}.")
    query_embedding = np.load(embedding_file)
    print("Query embedding generated.")
    return query_embedding

def retrieve_chunk(index, chunk_map, query_embedding, query, k=8, relevance_threshold=0.15, max_context_chars=20000):
    """Search FAISS index and retrieve the most relevant chunks based on query."""
    print(f"Searching FAISS index for relevant chunks...")
    
    # Ensure query_embedding is a 2D array with shape (1, embedding_dim)
    if len(query_embedding.shape) == 2 and query_embedding.shape[0] == 1:
        search_vector = query_embedding
    else:
        search_vector = query_embedding.reshape(1, -1)
    
    # Search for top k results
    D, I = index.search(search_vector, k=k)
    
    # Convert distances to similarity scores
    distances = D[0]
    max_dist = np.max(np.abs(distances)) if len(distances) > 0 else 1.0
    similarity_scores = 1.0 - (np.abs(distances) / max_dist)
    results = list(zip(I[0], similarity_scores))
    
    # List all files and build file info
    chunk_files = os.listdir(CHUNKED_DOCS_PATH)
    file_info = []
    query_words = set(word.lower() for word in query.split())
    
    for file_name in chunk_files:
        chunk_idx = None
        file_base = os.path.splitext(file_name)[0]
        
        if "_chunk_" in file_base:
            try:
                chunk_idx = int(file_base.split("_chunk_")[1])
            except (IndexError, ValueError):
                pass
        
        file_words = set(word.lower() for word in file_base.split('_') 
                        if word.lower() not in ['chunk'])
        keyword_match_ratio = len(file_words.intersection(query_words)) / len(file_words) if file_words else 0
        exact_match_bonus = 0.3 if any(keyword in file_base.lower() for keyword in query_words) else 0
        
        match_idx = -1
        similarity = 0.0
        for idx, score in results:
            if chunk_idx == idx:
                match_idx = idx
                similarity = score
                break
        
        if match_idx == -1 and (keyword_match_ratio > 0 or exact_match_bonus > 0):
            similarity = 0.5
        
        relevance = similarity + (keyword_match_ratio * 0.2) + exact_match_bonus
        
        if relevance > 0:
            file_info.append({
                'file_name': file_name,
                'relevance': relevance,
                'faiss_idx': match_idx,
                'keyword_match': keyword_match_ratio
            })
    
    for idx, score in results:
        if idx in chunk_map:
            file_name = chunk_map[idx]
            relevance = score
            file_info.append({
                'file_name': file_name,
                'relevance': relevance,
                'faiss_idx': idx,
                'keyword_match': 0
            })

    file_info.sort(key=lambda x: x['relevance'], reverse=True)
    
    relevant_files = [f for f in file_info if f['relevance'] >= relevance_threshold]
    
    if not relevant_files and file_info:
        relevant_files = [file_info[0]]
    
    chunks_content = []
    total_chars = 0
    
    for file_info in relevant_files:
        if total_chars >= max_context_chars:
            break
        
        file_path = os.path.join(CHUNKED_DOCS_PATH, file_info['file_name'])
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                if total_chars + len(content) > max_context_chars:
                    if not chunks_content:
                        content = content[:max_context_chars]
                    else:
                        continue
                
                chunks_content.append(content)
                total_chars += len(content)
        except Exception as e:
            continue
    
    combined_content = "\n\n---\n\n".join(chunks_content)
    return combined_content

def query_model(model, context, question):
    """Send the query and context to the specified model."""
    if not context.strip():
        return "No relevant content found to answer the question."
    
    prompt = f"""
    You are a helpful assistant that answers questions based only on the provided documents.
    If the answer is in the documents, provide it accurately.
    If the answer is not in the documents, say "I don't have that information."
    
    Documents:
    {context}
    
    User question:
    {question}
    
    Answer (be specific and direct):
    """
    result = subprocess.run(['ollama', 'run', model], input=prompt, capture_output=True, encoding='utf-8')
    
    if result.returncode != 0:
        raise RuntimeError(f"Model query failed: {result.stderr}")
    
    return result.stdout.strip()

import json
import subprocess
from config import *

def get_available_models():
    """Get list of available Ollama models."""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError("Failed to get model list")
        models = [line.split()[0] for line in result.stdout.strip().split('\n')[1:]]
        return models
    except FileNotFoundError:
        raise RuntimeError("Ollama not found. Please install Ollama first.")

def select_model():
    """Interactive model selection."""
    models = get_available_models()
    
    if not models:
        print("No models found. Installing default model...")
        subprocess.run(['ollama', 'pull', DEFAULT_MODEL], check=True)
        return DEFAULT_MODEL
    
    if len(models) == 1:
        return models[0]
    
    print("\nAvailable models:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    while True:
        try:
            choice = input("\nSelect model number (or press Enter for default): ").strip()
            if not choice:
                return DEFAULT_MODEL
            idx = int(choice) - 1
            if 0 <= idx < len(models):
                return models[idx]
        except ValueError:
            pass
        print("Invalid selection. Please try again.")

# Update main to use model selection
if __name__ == "__main__":
    try:
        model = select_model()
        print(f"Using model: {model}")
        
        # Step 1: Load the FAISS index and chunk mapping
        index, chunk_map = load_faiss_index()

        # Step 2: Get the user's query
        query = input("Enter your query: ")

        # Step 3: Embed the query
        query_embedding = embed_query(query)

        # Step 4: Retrieve the most relevant chunks using config defaults
        chunk_content = retrieve_chunk(
            index, 
            chunk_map,
            query_embedding, 
            query, 
            k=DEFAULT_TOP_K,
            relevance_threshold=DEFAULT_RELEVANCE_THRESHOLD, 
            max_context_chars=DEFAULT_MAX_CONTEXT_CHARS
        )

        # Step 5: Query the model with the retrieved chunks and user's question
        response = query_model(model, chunk_content, query)  # Use selected model, not DEFAULT_MODEL

        # Step 6: Display the model's response
        print(f"Model Response:\n{response}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
