# Decision Log: Local RAG Pipeline

## Model Selection
- **Chosen LLM:** `qwen3.5:4b-q4_K_M`, thinking off
- **Benchmark** (`benchmark_results.json`): 4B 36.3 tok/s, 2B 63.7 tok/s (mean, thinking off for both)
- **Why 4B:** It is slower than the 2B, but I expect better answers. 36 tok/s is still fast enough for short answers.

## Embedding Model
- **Chosen:** `nomic-embed-text` (768 dimensions)
- **Why:** It is small, runs locally in Ollama, and turns text into vectors so I can find the chunks closest in meaning to a question.

## Parsing
- **Extractor:** pypdf, default `extract_text()`
- **Tables looked like:** Messy. The rows and columns lost their layout, so numbers were separated from their labels.

## Chunking Strategy
- **Chunk size:** 512 characters, **overlap:** 50 characters → 335 chunks
- **Why:** Small chunks keep one idea each, and 5 of them fit easily in the context window. These are common default values; I did not tune them.

## Retrieval Configuration
- **Top-K:** 5
- **Context window:** 8192; prompt_tokens 593–840 (`pipeline_outputs.json`)

## Observations
- **Passed:** ___ of 17 (`pipeline_outputs.json`)
- **What worked:** q16 and q17 (unanswerable) were correctly refused.
- **What failed:** q09 (Copilot budget breakdown) refused, though the answer is in `meeting_notes.pdf`. My guess why: it is a table, and the table text was messy or split across chunks.
- **Traps I hit:** context was 4096 until I restarted Ollama; moving the folder broke the imports.

## If I Had More Time
- Use a better PDF parser for tables.
- Check which chunks were retrieved for the failed questions.
- Test the 2B model on the same 17 questions.