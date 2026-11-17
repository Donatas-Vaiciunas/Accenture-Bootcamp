# Local Document Q&A Service

A RAG pipeline that answers questions about five internal company PDFs, running entirely on local
models through Ollama. Switching to a cloud model changes only environment variables read by `config.py`.

## Setup
1. Install Ollama (https://ollama.com/download) and pull the models:
   ```bash
   ollama pull qwen3.5:4b-q4_K_M
   ollama pull qwen3.5:2b-q4_K_M
   ollama pull nomic-embed-text
   ```
2. Raise the context window to 8192 (macOS): `launchctl setenv OLLAMA_CONTEXT_LENGTH 8192`, then restart Ollama.
3. Install dependencies: `uv sync`
4. Check: `uv run python test_api.py` prints one sentence and `stop`; `ollama ps` shows CONTEXT 8192.

## Run
| What | Command |
|------|---------|
| Rebuild `chroma_db/` | `uv run python ingest.py` |
| Benchmark models | `uv run python benchmark.py` -> `benchmark_results.json` |
| Ask one question | `uv run python pipeline.py "your question"` |
| Run all test questions | `uv run python pipeline.py` -> `pipeline_outputs.json` |

## Structure
| File | Purpose |
|------|---------|
| `config.py` | All settings: provider, models, chunking, top-K, prompt |
| `ingest.py` | Load PDFs, chunk, embed, store in ChromaDB |
| `retrieve.py` | Query the vector DB, return chunks with source, page and score |
| `generate.py` | Answer from retrieved chunks with the local LLM |
| `pipeline.py` | Retrieve + generate; runs the test set |
| `benchmark.py` | Model comparison (Exercise 1) |
| `test_questions.json` | Test set |
| `decision_log.md` | Decisions and reasoning |