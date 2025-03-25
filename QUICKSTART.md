# Quick Start Guide

Prerequisites:
- Install [Python 3.13](https://www.python.org/downloads/)
- Install [Ollama](https://ollama.ai)
- Install [Git](https://git-scm.com/downloads)

Run these commands in order:

```bash
# 1. Setup Python environment
python -m venv venv

# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2. Get the code
git clone https://github.com/ResurgentDev/local-rag-ollama-basic-demo.git
cd local-rag-ollama-basic-demo

# 3. Install dependencies
pip install -r requirements.txt

# 4. Get a model (choose one)
ollama pull deepseek-r1:1.5b  # smallest (~1.5GB)

# 5. Run the pipeline
python fetch_docs.py
python chunk_docs.py
python create_embeddings.py
python setup_retriever.py
python query_model.py
```

That's it! When `query_model.py` starts, type your question about Ollama.
