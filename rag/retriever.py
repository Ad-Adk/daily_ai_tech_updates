"""
retriever.py
Queries the ChromaDB collection and returns relevant context strings.
"""

from rag.vector_store import collection


def retrieve_context(query: str, n_results: int = 3) -> list[str]:
    """
    Return up to n_results document strings most relevant to `query`.
    Falls back gracefully if the collection is empty.
    """
    if collection.count() == 0:
        return ["No articles have been indexed yet. Please refresh the dashboard first."]

    actual_n = min(n_results, collection.count())

    results = collection.query(
        query_texts=[query],
        n_results=actual_n,
    )

    return results["documents"][0]   # list of matching strings


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    sample_query = "What are the latest trends in AI?"
    context = retrieve_context(sample_query)

    print(f"Query: {sample_query}")
    print("Retrieved Context:")
    for idx, doc in enumerate(context, 1):
        print(f"{idx}. {doc[:200]}...")
