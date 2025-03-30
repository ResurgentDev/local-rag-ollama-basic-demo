---

📦 Completed Demo Project 📦 ⚠️ Work-in-Progress (WIP) ⚠️

This repository is both a finalized demonstration of a basic [RAG pipeline/feature set] and part of my ongoing personal learning journey as I explore development tools, concepts, and practices. Its purpose is to provide a simple, lightweight example for learning and reference.

While there may be other tools available that achieve similar tasks, this repository serves an educational purpose, showcasing my exploration and development skills.

I’m sharing this repository to:

Invite constructive feedback to accelerate my learning.

Help others who might benefit from similar exploration.

Engage potential collaborators or employers who value growth and curiosity.

💡 While no active development or collaboration is planned for this repository, I welcome discussions, suggestions, and connections that could help refine and expand my work. Minor fixes or refinements may still occur.

If you find value in this project and believe it could grow into something impactful, feel free to explore or get in touch with any questions!

---

# Local-RAG-Ollama Basic Demo

A minimal demonstration of implementing a local RAG (Retrieval-Augmented Generation) system using Ollama. This basic demo illustrates foundational RAG concepts with minimal complexity and will remain unchanged to serve as a learning reference - for active development, see [local-rag-ollama](https://github.com/ResurgentDev/local-rag-ollama).

## Quick Start
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

git clone https://github.com/ResurgentDev/local-rag-ollama-basic-demo.git
cd local-rag-ollama-basic-demo
pip install -r requirements.txt

ollama pull deepseek-r1:1.5b  # smallest model (~1.5GB)

python fetch_docs.py
python chunk_docs.py
python create_embeddings.py
python setup_retriever.py
python query_model.py
```
See [QUICKSTART.md](QUICKSTART.md) for a beginner-friendly command list.

## Important Notes

- This is a **basic demo** for learning purposes
- This demo has been successfully tested on Python 3.13
- Uses default settings throughout
- Response accuracy may vary
- No further development will occur on this repository
- For an actively developed version with improvements, see [local-rag-ollama](https://github.com/ResurgentDev/local-rag-ollama)

## What This Is

- A minimal working example of RAG implementation
- Uses Ollama's documentation as example data
- Shows basic document retrieval and LLM integration
- Intentionally simplified for learning purposes
- No type hints used to keep code approachable for beginners
- Focuses on core functionality over advanced features

## What This Isn't

- Not production-ready code
- No error handling
- No tests
- No configuration options
- Not optimized for accuracy or performance

## Prerequisites

1. Install [Ollama](https://ollama.ai)
2. Python 3.13+ (older versions like 3.8 may have type hinting compatibility issues)
3. Git (for cloning the repository)

## Setup and Installation

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows:
   .\venv\Scripts\activate
   
   # On Linux/Mac:
   source venv/bin/activate
   ```

2. Clone and enter the repository:
   ```bash
   git clone https://github.com/ResurgentDev/local-rag-ollama-basic-demo.git
   cd local-rag-ollama-basic-demo
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Download an Ollama model:
   ```bash
   # Tested with llama3.2:latest
   # Other models should work, for example smaller ones:
   ollama pull deepseek-r1:1.5b    # ~1.5GB
   ollama pull llama2:7b           # ~3.8GB
   ollama pull mistral:7b          # ~4.1GB
   ```

## Pipeline Steps

The RAG pipeline consists of these sequential steps:

1. **Fetch Documentation** (`fetch_docs.py`)
   - Downloads Ollama's documentation from GitHub to `~/RAG/Docs/Raw/`
   - Source: **GitHub** Ollama docs repository
   - Output: Raw markdown files

2. **Chunk Documents** (`chunk_docs.py`)
   - Splits documents into smaller chunks in `~/RAG/Docs/Chunked/`
   - Uses **NLTK** for sentence boundary detection
   - Preserves semantic context within chunks

3. **Create Embeddings** (`create_embeddings.py`)
   - Uses **BERT** model for embedding generation
   - Processes chunks from `~/RAG/Docs/Chunked/`
   - Stores vectors in `~/RAG/Docs/Embeddings/`

4. **Setup Retriever** (`setup_retriever.py`)
   - Creates **FAISS** vector similarity index
   - Maps document chunks to embeddings
   - Saves index to `~/RAG/Docs/Embeddings/Indexes/`

5. **Query Model** (`query_model.py`)
   - Interactive query interface using **Ollama**
   - Retrieves relevant chunks via FAISS search
   - Combines context with user query
   - Returns AI-generated responses

Default data storage structure:
```
~/RAG/
├── Docs/
    ├── Raw/         # Original markdown files
    ├── Chunked/     # Split documents
    └── Embeddings/  # Document embeddings
        └── Indexes/ # FAISS indexes
```

## About NLTK and punkt

This project uses the Natural Language Toolkit (NLTK), specifically the punkt tokenizer. The punkt tokenizer is a pre-trained model used for splitting text into sentences. It is not included with the default NLTK installation and must be downloaded separately.

How Does It Work Offline?
Once the punkt tokenizer is downloaded, it is stored locally on your machine (in the default NLTK data directory, e.g., ~/.nltk_data). After this initial download, the tool can function offline without needing an internet connection.

First-Time Setup
If you run this tool for the first time on a new machine, the required punkt tokenizer will be automatically downloaded. Make sure you are online for this initial setup.

You can pre-download the resource manually with the following command:

bash
```
python -c "import nltk; nltk.download('punkt')"
```
Alternatively, this tool checks if the resource is already downloaded before attempting to fetch it dynamically. See the source code for more details.


## Known Limitations

- Basic vector similarity search
- Simple prompt templates
- Variable response accuracy
- No error handling
- Fixed configurations
- Limited document processing

## Project Status

This repository is a static demonstration of basic RAG concepts. It will not receive updates or improvements. For an actively developed implementation with improved features, error handling, and better accuracy, please see:

- Active Project: [local-rag-ollama](https://github.com/ResurgentDev/local-rag-ollama)
- Future Plans: See FUTURE_PLANS.md in the active project repository

## License

MIT License - See LICENSE.txt for details
