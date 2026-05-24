"""
vector_store.py
Manages the ChromaDB collection for article storage and retrieval.

Uses ChromaDB's built-in embedding (no external embedder needed).
Switched to PersistentClient so data survives app restarts.
"""

import chromadb
from pathlib import Path

# Persist DB to disk so articles survive Streamlit reruns
DB_PATH = str(Path(__file__).resolve().parent.parent / "chroma_db")

client = chromadb.PersistentClient(path=DB_PATH)

collection = client.get_or_create_collection(
    name="tech_trends"
)


def store_articles(articles: list[dict]) -> None:
    """
    Upsert articles into ChromaDB.
    Uses article URL as a stable ID so re-ingestion doesn't create duplicates.
    """
    if not articles:
        return

    documents, ids, metadatas = [], [], []

    for article in articles:
        doc_id = article.get("url", article["title"])  # stable unique key

        text = (
            f"Title: {article['title']}\n"
            f"Summary: {article.get('summary', article.get('description', ''))}\n"
            f"Topic: {article.get('topic', '')}\n"
            f"Skills: {', '.join(article.get('skills', []))}"
        )

        documents.append(text)
        ids.append(doc_id)
        metadatas.append({
            "title": article["title"],
            "topic": article.get("topic", ""),
            "url": article.get("url", ""),
        })

    # upsert = add if new, update if ID already exists
    collection.upsert(documents=documents, ids=ids, metadatas=metadatas)


def article_count() -> int:
    return collection.count()


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_articles = [
        {
            "url": "https://example.com/1",
            "title": "AI breakthrough",
            "summary": "New AI model achieves state-of-the-art results",
            "topic": "LLM",
            "skills": ["LLM fine-tuning"],
        },
        {
            "url": "https://example.com/2",
            "title": "MLOps strategies",
            "summary": "Best practices for deploying AI models",
            "topic": "MLOps",
            "skills": ["MLOps"],
        },
    ]
    store_articles(sample_articles)
    print(f"Stored. Collection size: {article_count()}")
