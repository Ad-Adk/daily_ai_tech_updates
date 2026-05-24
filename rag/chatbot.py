"""
chatbot.py
RAG-powered AI career assistant using Groq + ChromaDB retrieval.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from rag.retriever import retrieve_context

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant",
)

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def ask_chatbot(query: str) -> str:
    """
    Retrieve relevant context from the vector store and answer `query`.
    Returns a plain string answer.
    """
    context_docs = retrieve_context(query)
    context = "\n\n".join(context_docs)

    prompt = f"""You are an AI career assistant helping users understand AI trends and skills.

            Context (from indexed articles):
            {context}

            Question: {query}

            Answer based only on the context above. Be concise and actionable.
            If the context does not contain relevant information, say "Sorry, I don't have that information."
            Do NOT add a preamble."""

    response = llm.invoke(prompt)
    return response.content.strip()
