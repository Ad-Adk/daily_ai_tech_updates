"""
chatbot.py – RAG-powered AI career assistant using Groq + ChromaDB.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from config.config import ENV_PATH, LLM_MODEL, LLM_TEMP
from rag.retriever import retrieve_context

load_dotenv(dotenv_path=ENV_PATH)

_llm = ChatGroq(
    temperature=LLM_TEMP,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name=LLM_MODEL,
)

_PROMPT = """You are an AI career assistant helping users understand AI trends and skills.

Context (from indexed articles):
{context}

Question: {query}

Answer based only on the context above. Be concise and actionable.
If the context does not contain relevant information, say "Sorry, I don't have that information."
Do NOT add a preamble."""


def ask_chatbot(query: str) -> str:
    """Retrieve relevant context and answer `query`. Returns a plain string."""
    context = "\n\n".join(retrieve_context(query))
    response = _llm.invoke(_PROMPT.format(context=context, query=query))
    return response.content.strip()
