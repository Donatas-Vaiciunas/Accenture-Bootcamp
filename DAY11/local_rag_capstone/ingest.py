from pathlib import Path

import chromadb
from chromadb.errors import NotFoundError
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from pypdf import PdfReader

import config

DOCUMENTS_DIR = Path("documents")
CHROMA_PATH = "chroma_db"
BATCH_SIZE = 32

embed_client = OpenAI(base_url=config.EMBEDDING_BASE_URL, api_key="ollama")


def embed(texts: list[str]) -> list[list[float]]:
    response = embed_client.embeddings.create(model=config.EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(config.COLLECTION_NAME, metadata={"hnsw:space": "cosine"})


def load_chunks() -> tuple[list[str], list[str], list[dict]]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=config.CHUNK_SIZE, chunk_overlap=config.CHUNK_OVERLAP)
    ids, texts, metadatas = [], [], []
    for pdf in sorted(DOCUMENTS_DIR.glob("*.pdf")):
        for page_number, page in enumerate(PdfReader(pdf).pages, start=1):
            for index, chunk in enumerate(splitter.split_text(page.extract_text() or "")):
                ids.append(f"{pdf.name}-p{page_number}-c{index}")  # stable ID: no duplicates on re-ingest
                texts.append(chunk)
                metadatas.append({"source": pdf.name, "page": page_number})
    return ids, texts, metadatas


def ingest() -> None:
    ids, texts, metadatas = load_chunks()

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    try:
        client.delete_collection(config.COLLECTION_NAME)
    except NotFoundError:
        pass
    collection = get_collection()

    for start in range(0, len(texts), BATCH_SIZE):
        end = start + BATCH_SIZE
        collection.add(
            ids=ids[start:end],
            documents=texts[start:end],
            embeddings=embed(texts[start:end]),
            metadatas=metadatas[start:end],
        )
    print(f"Stored {collection.count()} chunks from {len({m['source'] for m in metadatas})} documents "
          f"(chunk size {config.CHUNK_SIZE} chars, overlap {config.CHUNK_OVERLAP} chars, "
          f"embedding model {config.EMBEDDING_MODEL})")


if __name__ == "__main__":
    ingest()
