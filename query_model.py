import os
import faiss
import numpy as np
import subprocess
from config import *  # Import all config settings

def load_faiss_index():
    """Load the FAISS index from file."""
    if not os.path.exists(INDEX_FILE):
        raise FileNotFoundError(f"FAISS index not found at {INDEX_FILE}. Please run setup_retriever.py first.")
    index = faiss.read_index(INDEX_FILE)
    print("FAISS index loaded.")
    return index

def embed_query(query):
    """Generate an embedding for the query using the embedding script."""
    print("Generating embedding for query...")
    embedding_file = os.path.join(BASE_DIR, 'query_embedding.npy')
    
    # Call the embedding script with proper path handling
    subprocess.run(['python', EMBEDDING_SCRIPT, '--query', query, '--output', embedding_file], check=True)
    
    # Load and return the embedding
    if not os.path.exists(embedding_file):
        raise FileNotFoundError(f"Query embedding file not found at {embedding_file}.")
    query_embedding = np.load(embedding_file)
    print("Query embedding generated.")
    return query_embedding

def retrieve_chunk(index, query_embedding, query, k=8, relevance_threshold=0.7, max_context_chars=20000):
    """Search FAISS index and retrieve the most relevant chunks based on query.
    
    Args:
        index: The FAISS index to search
        query_embedding: The embedding of the query
        query: The original text query for keyword matching
        k: Number of top results to search (default=8)
        relevance_threshold: Minimum relevance score to include a chunk (default=0.7)
        max_context_chars: Maximum total characters to include in context (default=20000)
        
    Returns:
        A string containing the combined content of the most relevant chunks
    """
    print(f"Searching FAISS index for relevant chunks...")
    # Ensure query_embedding is a 2D array with shape (1, embedding_dim)
    if len(query_embedding.shape) == 2 and query_embedding.shape[0] == 1:
        # Already correctly shaped (1, embedding_dim)
        search_vector = query_embedding
    else:
        # Reshape to ensure it's (1, embedding_dim)
        search_vector = query_embedding.reshape(1, -1)
    
    # Search for top k results
    D, I = index.search(search_vector, k=k)
    
    # FAISS returns negative distances, convert to similarity scores (0-1 scale)
    # The smaller the L2 distance, the more similar the vectors
    # Convert distances to similarity scores where 1.0 is perfect match and 0.0 is completely dissimilar
    # First, ensure all distances are positive (they might be negative depending on FAISS config)
    distances = D[0]
    max_dist = np.max(np.abs(distances)) if len(distances) > 0 else 1.0
    # Normalize to 0-1 range and invert (smaller distance = higher similarity)
    similarity_scores = 1.0 - (np.abs(distances) / max_dist)
    
    # Combine indices with their similarity scores
    results = list(zip(I[0], similarity_scores))
    print(f"Top {k} FAISS indices with similarity scores: {results}")
    
    # List all files in the CHUNK_PATH directory
    chunk_files = os.listdir(CHUNKED_DOCS_PATH)
    
    # Create a comprehensive mapping from all chunk files to indices
    # This handles both exact index matches and keyword matches
    file_info = []
    
    # Extract query keywords for file name matching
    query_words = set(word.lower() for word in query.split())
    
    # Process all chunk files to build the file_info list
    for file_name in chunk_files:
        # Try to extract chunk index from filename
        chunk_idx = None
        file_base = os.path.splitext(file_name)[0]  # Get filename without extension
        
        # Find the chunk number (e.g., extract '0' from 'api_chunk_0.txt')
        if "_chunk_" in file_base:
            try:
                chunk_idx = int(file_base.split("_chunk_")[1])
            except (IndexError, ValueError):
                pass
        
        # Calculate name relevance based on matching query keywords
        file_words = set(word.lower() for word in file_base.split('_') 
                        if word.lower() not in ['chunk'])
        keyword_match_ratio = len(file_words.intersection(query_words)) / len(file_words) if file_words else 0
        
        # Add bonus for exact keyword matches
        exact_match_bonus = 0.3 if any(keyword in file_base.lower() for keyword in query_words) else 0
        
        # Find if this file matches any of our top FAISS results
        match_idx = -1
        similarity = 0.0
        for idx, score in results:
            if chunk_idx == idx:
                match_idx = idx
                similarity = score
                break
        
        # If no direct index match but file has keyword relevance, assign a default similarity
        if match_idx == -1 and (keyword_match_ratio > 0 or exact_match_bonus > 0):
            similarity = 0.5  # Base similarity for keyword matches
        
        # Calculate final relevance score combining embedding similarity and keyword matching
        relevance = similarity + (keyword_match_ratio * 0.2) + exact_match_bonus
        
        if relevance > 0:  # Only include files with some relevance
            file_info.append({
                'file_name': file_name,
                'relevance': relevance,
                'faiss_idx': match_idx,
                'keyword_match': keyword_match_ratio
            })
    
    # Sort files by relevance score (highest first)
    file_info.sort(key=lambda x: x['relevance'], reverse=True)
    
    print(f"Found {len(file_info)} potentially relevant files")
    for info in file_info[:5]:  # Print top 5 for debugging
        print(f"  {info['file_name']}: relevance={info['relevance']:.2f}, "
            f"keyword_match={info['keyword_match']:.2f}, faiss_idx={info['faiss_idx']}")
    
    # Only keep chunks above the relevance threshold
    relevant_files = [f for f in file_info if f['relevance'] >= relevance_threshold]
    print(f"Keeping {len(relevant_files)} files above relevance threshold {relevance_threshold}")
    
    # If no relevant chunks found, take the top chunk only if it exists
    if not relevant_files and file_info:
        print("No files above threshold, using only the top match")
        relevant_files = [file_info[0]]
    
    # Read content from relevant chunks
    chunks_content = []
    total_chars = 0
    
    for file_info in relevant_files:
        # Stop adding chunks if we exceed max context size
        if total_chars >= max_context_chars:
            print(f"Reached maximum context size ({max_context_chars} chars)")
            break
        
        file_path = os.path.join(CHUNKED_DOCS_PATH, file_info['file_name'])
        print(f"Reading chunk: {file_info['file_name']} (relevance: {file_info['relevance']:.2f})")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # Check if adding this chunk would exceed max context size
                if total_chars + len(content) > max_context_chars:
                    # If this is the first chunk, include a portion
                    if not chunks_content:
                        content = content[:max_context_chars]
                        print(f"Truncated first chunk to {len(content)} chars")
                    else:
                        # Skip this chunk as it would exceed limit
                        print(f"Skipping chunk to stay within context limit")
                        continue
                
                chunks_content.append(content)
                total_chars += len(content)
                print(f"Added chunk ({len(content)} chars)")
        except Exception as e:
            print(f"Error reading file {file_info['file_name']}: {e}")
            continue
    
    # Combine retrieved chunks
    combined_content = "\n\n---\n\n".join(chunks_content)
    print(f"Retrieved {len(chunks_content)} chunks with total length: {len(combined_content)} characters")
    return combined_content

def query_model(model, context, question):
    """Send the query and context to the specified model.
    
    Args:
        model: The model name to use for querying
        context: Combined context from relevant chunks
        question: The user's question
        
    Returns:
        The model's response
    """
    print("Querying the model...")
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
    # Use the Ollama CLI to query the model
    result = subprocess.run(['ollama', 'run', model], input=prompt, capture_output=True, encoding='utf-8')
    
    if result.returncode != 0:
        raise RuntimeError(f"Model query failed: {result.stderr}")
    
    print("Model queried successfully.")
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
        # Parse the output - format depends on Ollama version
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
        # Step 1: Load the FAISS index
        index = load_faiss_index()

        # Step 2: Get the user's query
        query = input("Enter your query: ")

        # Step 3: Embed the query
        query_embedding = embed_query(query)

        # Step 4: Retrieve the most relevant chunks using config defaults
        chunk_content = retrieve_chunk(
            index, 
            query_embedding, 
            query, 
            k=DEFAULT_TOP_K,
            relevance_threshold=DEFAULT_RELEVANCE_THRESHOLD, 
            max_context_chars=DEFAULT_MAX_CONTEXT_CHARS
        )

        # Step 5: Query the model with the retrieved chunks and user's question
        response = query_model(DEFAULT_MODEL, chunk_content, query)

        # Step 6: Display the model's response
        print(f"Model Response:\n{response}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
