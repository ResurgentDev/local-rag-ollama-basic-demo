import os

# Base paths - users can override these as needed
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAG_DIR = os.path.join(os.path.expanduser("~"), "RAG")

# Derived paths for data storage
DOCS_DIR = os.path.join(RAG_DIR, "Docs")
RAW_DOCS_PATH = os.path.join(DOCS_DIR, "Raw")
CHUNKED_DOCS_PATH = os.path.join(DOCS_DIR, "Chunked")
EMBEDDINGS_PATH = os.path.join(DOCS_DIR, "Embeddings")
INDEXES_PATH = os.path.join(EMBEDDINGS_PATH, "Indexes")

# File paths
INDEX_FILE = os.path.join(INDEXES_PATH, "retriever.index")
EMBEDDING_SCRIPT = os.path.join(BASE_DIR, "create_embeddings.py")

# Default documentation source
DEFAULT_DOCS_URL = 'https://github.com/ollama/ollama/tree/main/docs'

# Create required directories
def ensure_directories():
    """Create all required directories if they don't exist."""
    directories = [RAW_DOCS_PATH, CHUNKED_DOCS_PATH, EMBEDDINGS_PATH, INDEXES_PATH]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Model settings
DEFAULT_MODEL = "llama2:latest"  
# Query settings
DEFAULT_TOP_K = 8
DEFAULT_RELEVANCE_THRESHOLD = 0.15  # Lower threshold to match typical similarity scores
DEFAULT_MAX_CONTEXT_CHARS = 20000

# Initialize directories when config is imported
ensure_directories()
