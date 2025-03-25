# Local-RAG-Ollama

A simple demonstration of implementing a local RAG (Retrieval-Augmented Generation) system using Ollama. This project shows how to set up basic RAG functionality with minimal complexity.

## What This Is

- A **demo project** showing basic RAG implementation
- Uses Ollama's documentation as example data
- Shows how to implement basic document retrieval and LLM integration
- Kept intentionally simple for learning purposes

## What This Isn't

- Not production-ready code
- Minimal error handling
- No tests
- No complex configurations
- Not optimized for performance

## Prerequisites

1. Install [Ollama](https://ollama.ai)
2. Python 3.7+
3. Required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Download an Ollama model:
   ```bash
   # Any of these models will work:
   ollama pull llama2:latest
   ollama pull deepseek-coder:latest
   ollama pull mistral:latest
   ```

## Quick Start

By default, the project stores all data in:
```
~/RAG/
├── Docs/
    ├── Raw/         # Original markdown files
    ├── Chunked/     # Split documents
    └── Embeddings/  # Document embeddings
        └── Indexes/ # FAISS indexes
```

You can override these locations in `config.py`.

1. Fetch example docs:
```bash
python fetch_docs.py
```

2. Process docs into chunks:
```bash
python chunk_docs.py
```

3. Create embeddings:
```bash
python create_embeddings.py
```

4. Set up retriever:
```bash
python setup_retriever.py
```

5. Query the system:
```bash
python query_model.py
```

## Known Limitations

- Basic indexing and retrieval logic
- Simple prompt engineering
- LLM responses may sometimes hallucinate
- Limited error handling
- Hard-coded configurations
- Document matching may not prioritize exact filename matches (e.g., when querying about README.md)

## Project Status

This is a basic demonstration project designed to show core RAG concepts with minimal complexity. For a more feature-rich implementation with error handling, improved matching, and additional features, see [local-rag-ollama](https://github.com/ResurgentDev/local-rag-ollama).

This repository will remain as-is to serve as a learning tool for understanding basic RAG implementation.

## License

MIT License - See LICENSE.txt for details
