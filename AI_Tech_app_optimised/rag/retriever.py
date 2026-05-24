"""
retriever.py – Query ChromaDB and return context strings for the chatbot.
"""

from rag.vector_store import collection

_FALLBACK = ["No articles indexed yet — please refresh the dashboard first."]


def retrieve_context(query: str, n_results: int = 3) -> list[str]:
    """
    Return up to n_results document strings most relevant to `query`.
    Degrades gracefully when the collection is empty.
    """
    count = collection.count()
    if count == 0:
        return _FALLBACK

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, count),
    )
    return results["documents"][0]


if __name__ == "__main__":
    query = "What are the latest trends in AI?"
    for i, doc in enumerate(retrieve_context(query), 1):
        print(f"{i}. {doc[:200]}…")
