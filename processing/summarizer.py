import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY


llm = ChatGroq(
    temperature=0,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
)


def summarize(text):
    if len(text) < 50:
        return text
    else:
        prompt = f"""
            Summarize the following news article in 2-3 concise sentences.
            Focus on the main development, why it matters, and any AI or tech impact.NO Preamble
            Article:
            {text}
            """.strip()

        response = llm.invoke(prompt)
        return response.content.strip()


if __name__ == "__main__":
    sample_text = (
        "Artificial intelligence companies are releasing new large language models "
        "with better reasoning, lower latency, and wider enterprise adoption. "
        "These improvements are changing how teams build assistants, automate tasks, "
        "and evaluate model safety in production systems."
    )

    summary = summarize(sample_text)
    print("Summary:")
    print(summary)
