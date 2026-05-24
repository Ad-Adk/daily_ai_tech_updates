"""
summarizer.py – LLM-powered article summarisation via Groq.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from config.config import ENV_PATH, LLM_MODEL, LLM_TEMP

load_dotenv(dotenv_path=ENV_PATH)

_llm = ChatGroq(
    temperature=LLM_TEMP,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name=LLM_MODEL,
)

_MIN_LENGTH = 50
_PROMPT = (
    "Summarize the following news article in 2-3 concise sentences. "
    "Focus on the main development, why it matters, and any AI or tech impact. "
    "No preamble.\n\nArticle:\n{text}"
)


def summarize(text: str) -> str:
    """Return a 2-3 sentence summary, or the original text if it's already short."""
    if len(text) < _MIN_LENGTH:
        return text
    response = _llm.invoke(_PROMPT.format(text=text))
    return response.content.strip()


if __name__ == "__main__":
    sample = (
        "Artificial intelligence companies are releasing new large language models "
        "with better reasoning, lower latency, and wider enterprise adoption. "
        "These improvements are changing how teams build assistants and automate tasks."
    )
    print(summarize(sample))
