---

📦 **Completed Demo Project** 📦 ⚠️ **Work-in-Progress (WIP)** ⚠️

This repository is both a finalized demonstration of a basic RAG pipeline/feature set and part of my ongoing personal learning journey as I explore development tools, concepts, and practices. Its purpose is to provide a simple, lightweight example for learning and reference.

While there may be other tools available that achieve similar tasks, this repository serves an educational purpose, showcasing my exploration and development skills.e other tools available that achieve similar tasks, this repository serves an educational purpose, showcasing my exploration and development skills.

I'm sharing this repository to:pository to:
- Invite constructive feedback to accelerate my learninglearning.
- Help others who might benefit from similar exploration similar exploration.
- Engage potential collaborators or employers who value growth and curiosity who value growth and curiosity.

💡 While no active development or collaboration is planned for this repository, I welcome discussions, suggestions, and connections that could help refine and expand my work. Minor fixes or refinements may still occur.💡 While no active development or collaboration is planned for this repository, I welcome discussions, suggestions, and connections that could help refine and expand my work. Minor fixes or refinements may still occur.

If you find value in this project and believe it could grow into something impactful, feel free to explore or get in touch with any questions!If you find value in this project and believe it could grow into something impactful, feel free to explore or get in touch with any questions!

---

# Local-RAG-Ollama Basic Demo

> 📦 **Completed Demo Project** | No Further Development PlannedA minimal demonstration of implementing a local RAG (Retrieval-Augmented Generation) system using Ollama. This basic demo illustrates foundational RAG concepts with minimal complexity and will remain unchanged to serve as a learning reference - for active development, see [local-rag-ollama](https://github.com/ResurgentDev/local-rag-ollama).

A minimal demonstration of implementing a local RAG (Retrieval-Augmented Generation) system using Ollama. This basic demo illustrates foundational RAG concepts with minimal complexity and will remain unchanged to serve as a learning reference - for active development, see [local-rag-ollama](https://github.com/ResurgentDev/local-rag-ollama).

## Project Statuspython -m venv venv

This repository is:source venv/bin/activate # Linux/Mac
- A finalized demonstration of basic RAG concepts
- Part of my ongoing learning journeythub.com/ResurgentDev/local-rag-ollama-basic-demo.git
- Open for feedback but not active developmentemo
- A reference implementation for educational purposests.txt

While no active development is planned, feedback and questions are welcome!ama pull deepseek-r1:1.5b  # smallest model (~1.5GB)

## Quick Startpython fetch_docs.py
```bashpy
python -m venv venvpython create_embeddings.py
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

git clone https://github.com/ResurgentDev/local-rag-ollama-basic-demo.gitRT.md) for a beginner-friendly command list.
cd local-rag-ollama-basic-demo
pip install -r requirements.txt

ollama pull deepseek-r1:1.5b  # smallest model (~1.5GB)asic demo** for learning purposes
- This demo has been successfully tested on Python 3.13
python fetch_docs.py
python chunk_docs.py
python create_embeddings.pyry
python setup_retriever.pyments, see [local-rag-ollama](https://github.com/ResurgentDev/local-rag-ollama)
python query_model.py
```
See [QUICKSTART.md](QUICKSTART.md) for a beginner-friendly command list.
g example of RAG implementation
## Important Notes- Uses Ollama's documentation as example data
ieval and LLM integration
- This is a **basic demo** for learning purposesplified for learning purposes
- This demo has been successfully tested on Python 3.13hints used to keep code approachable for beginners
- Uses default settings throughoutality over advanced features
- Response accuracy may vary
- No further development will occur on this repository## What This Isn't
- For an actively developed version with improvements, see [local-rag-ollama](https://github.com/ResurgentDev/local-rag-ollama)
- Not production-ready code
## What This Is

- A minimal working example of RAG implementation
- Uses Ollama's documentation as example data- Not optimized for accuracy or performance
- Shows basic document retrieval and LLM integration
- Intentionally simplified for learning purposes## Prerequisites
- No type hints used to keep code approachable for beginners
- Focuses on core functionality over advanced features [Ollama](https://ollama.ai)
 versions like 3.8 may have type hinting compatibility issues)
## What This Isn'tGit (for cloning the repository)

- Not production-ready code
- No error handling
- No testsvate a virtual environment:
- No configuration options
- Not optimized for accuracy or performancehon -m venv venv
   
## Prerequisites
Scripts\activate
1. Install [Ollama](https://ollama.ai)
2. Python 3.13+ (older versions like 3.8 may have type hinting compatibility issues)
3. Git (for cloning the repository)rce venv/bin/activate
   ```
## Setup and Installation
nd enter the repository:
1. Create and activate a virtual environment:
   ```bash clone https://github.com/ResurgentDev/local-rag-ollama-basic-demo.git
   python -m venv venv   cd local-rag-ollama-basic-demo
   
   # On Windows:
   .\venv\Scripts\activate
   
   # On Linux/Mac:
   source venv/bin/activate
   ```
nload an Ollama model:
2. Clone and enter the repository:   ```bash
   ```bashllama3.2:latest
   git clone https://github.com/ResurgentDev/local-rag-ollama-basic-demo.git   # Other models should work, for example smaller ones:
   cd local-rag-ollama-basic-demo
   ```   ollama pull llama2:7b           # ~3.8GB

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
ntial steps:
4. Download an Ollama model:
   ```bash
   # Tested with llama3.2:latesttHub to `~/RAG/Docs/Raw/`
   # Other models should work, for example smaller ones:   - Source: **GitHub** Ollama docs repository
   ollama pull deepseek-r1:1.5b    # ~1.5GB
   ollama pull llama2:7b           # ~3.8GB
   ollama pull mistral:7b          # ~4.1GB
   ```/RAG/Docs/Chunked/`
   - Uses **NLTK** for sentence boundary detection
## Pipeline Steps

The RAG pipeline consists of these sequential steps:dings.py`)

1. **Fetch Documentation** (`fetch_docs.py`)   - Processes chunks from `~/RAG/Docs/Chunked/`
   - Downloads Ollama's documentation from GitHub to `~/RAG/Docs/Raw/`beddings/`
   - Source: **GitHub** Ollama docs repository
   - Output: Raw markdown files
ity index
2. **Chunk Documents** (`chunk_docs.py`)ings
   - Splits documents into smaller chunks in `~/RAG/Docs/Chunked/`   - Saves index to `~/RAG/Docs/Embeddings/Indexes/`
   - Uses **NLTK** for sentence boundary detection
   - Preserves semantic context within chunks**Query Model** (`query_model.py`)
nteractive query interface using **Ollama**
3. **Create Embeddings** (`create_embeddings.py`)ieves relevant chunks via FAISS search
   - Uses **BERT** model for embedding generation
   - Processes chunks from `~/RAG/Docs/Chunked/`
   - Stores vectors in `~/RAG/Docs/Embeddings/`

4. **Setup Retriever** (`setup_retriever.py`)
   - Creates **FAISS** vector similarity index~/RAG/
   - Maps document chunks to embeddings
   - Saves index to `~/RAG/Docs/Embeddings/Indexes/`    ├── Raw/         # Original markdown files

5. **Query Model** (`query_model.py`)    └── Embeddings/  # Document embeddings
   - Interactive query interface using **Ollama**ISS indexes
   - Retrieves relevant chunks via FAISS search
   - Combines context with user query
   - Returns AI-generated responsesd punkt

Default data storage structure:This project uses the Natural Language Toolkit (NLTK), specifically the punkt tokenizer. The punkt tokenizer is a pre-trained model used for splitting text into sentences. It is not included with the default NLTK installation and must be downloaded separately.
```
~/RAG/How Does It Work Offline?
├── Docs/ the punkt tokenizer is downloaded, it is stored locally on your machine (in the default NLTK data directory, e.g., ~/.nltk_data). After this initial download, the tool can function offline without needing an internet connection.
    ├── Raw/         # Original markdown files
    ├── Chunked/     # Split documents
    └── Embeddings/  # Document embeddingsyou run this tool for the first time on a new machine, the required punkt tokenizer will be automatically downloaded. Make sure you are online for this initial setup.
        └── Indexes/ # FAISS indexes
```You can pre-download the resource manually with the following command:

## About NLTK and punkt
```
This project uses the Natural Language Toolkit (NLTK), specifically the punkt tokenizer. The punkt tokenizer is a pre-trained model used for splitting text into sentences. It is not included with the default NLTK installation and must be downloaded separately.nload('punkt')"

How Does It Work Offline?cks if the resource is already downloaded before attempting to fetch it dynamically. See the source code for more details.
Once the punkt tokenizer is downloaded, it is stored locally on your machine (in the default NLTK data directory, e.g., ~/.nltk_data). After this initial download, the tool can function offline without needing an internet connection.

First-Time Setup
If you run this tool for the first time on a new machine, the required punkt tokenizer will be automatically downloaded. Make sure you are online for this initial setup.
ctor similarity search
You can pre-download the resource manually with the following command:- Simple prompt templates

bash- No error handling



















MIT License - See LICENSE.txt for details## License- Limited document processing- Fixed configurations- No error handling- Variable response accuracy- Simple prompt templates- Basic vector similarity search## Known LimitationsAlternatively, this tool checks if the resource is already downloaded before attempting to fetch it dynamically. See the source code for more details.```python -c "import nltk; nltk.download('punkt')"```- Fixed configurations
- Limited document processing

## Project Status

This repository is a static demonstration of basic RAG concepts. It will not receive updates or improvements. For an actively developed implementation with improved features, error handling, and better accuracy, please see:

- Active Project: [local-rag-ollama](https://github.com/ResurgentDev/local-rag-ollama)
- Future Plans: See FUTURE_PLANS.md in the active project repository

## License

MIT License - See LICENSE.txt for details
