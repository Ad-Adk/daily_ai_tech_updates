"""
vector_store.py – ChromaDB-backed article store for RAG retrieval.

Uses a PersistentClient so data survives Streamlit reruns.
ChromaDB's built-in embedder is used — no external embedding model needed.
"""

import chromadb
from config.config import DB_PATH

_client    = chromadb.PersistentClient(path=DB_PATH)
collection = _client.get_or_create_collection(name="tech_trends")


def _article_to_doc(article: dict) -> str:
    """Serialise an article dict to a single searchable string."""
    return (
        f"Title: {article['title']}\n"
        f"Summary: {article.get('summary', article.get('description', ''))}\n"
        f"Topic: {article.get('topic', '')}\n"
        f"Skills: {', '.join(article.get('skills', []))}"
    )


def store_articles(articles: list[dict]) -> None:
    """
    Upsert articles into ChromaDB.
    Uses article URL as a stable ID to prevent duplicate ingestion.
    """
    if not articles:
        return

    documents, ids, metadatas = [], [], []
    for article in articles:
        doc_id = article.get("url") or article["title"]
        documents.append(_article_to_doc(article))
        ids.append(doc_id)
        metadatas.append({
            "title": article["title"],
            "topic": article.get("topic", ""),
            "url":   article.get("url", ""),
        })

    collection.upsert(documents=documents, ids=ids, metadatas=metadatas)


def article_count() -> int:
    return collection.count()


if __name__ == "__main__":
    _samples = [
        {"url": "https://example.com/1", "title": "AI breakthrough", "summary": "New SOTA LLM",        "topic": "LLM",   "skills": ["LLM fine-tuning"]},
        {"url": "https://example.com/2", "title": "MLOps strategies", "summary": "Deploy AI models",   "topic": "MLOps", "skills": ["MLOps"]},
    ]
    store_articles(_samples)
    print(f"Collection size: {article_count()}")
