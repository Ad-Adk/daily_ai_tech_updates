"""
insights.py – Extract topic and skill tags from article text using an LLM.
"""

import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from config.config import ENV_PATH, LLM_MODEL, LLM_TEMP, MAX_SKILLS

load_dotenv(dotenv_path=ENV_PATH)

_llm = ChatGroq(
    temperature=LLM_TEMP,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name=LLM_MODEL,
)

_PROMPT = """You are an AI news analyst.

Analyze the following article and return ONLY valid JSON in this exact format:
{{
    "topic": "short category",
    "skills": ["skill1", "skill2"]
}}

Rules:
- topic: concise AI/tech category (e.g. LLM, Computer Vision, MLOps)
- skills: up to {max_skills} technical skills/tools/concepts
- Output ONLY JSON — no markdown, no explanation

Article:
{text}"""


def _parse_response(content: str) -> dict:
    """Strip any accidental markdown fences and parse JSON."""
    clean = content.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


def extract_insights(article: dict) -> dict:
    """
    Enrich an article dict with 'topic' and 'skills' fields via LLM.
    Falls back to safe defaults on any error.
    """
    base = {
        "title":   article["title"],
        "summary": article["description"],
        "url":     article["url"],
        "topic":   "General",
        "skills":  [],
    }

    try:
        response = _llm.invoke(
            _PROMPT.format(text=article["description"], max_skills=MAX_SKILLS)
        )
        parsed = _parse_response(response.content)
        base["topic"]  = parsed.get("topic", "General")
        base["skills"] = parsed.get("skills", [])
    except Exception as e:
        print(f"[insights] Extraction error: {e}")

    return base


if __name__ == "__main__":
    sample = {
        "title":       "New LLM breakthrough",
        "description": "A new LLM achieves state-of-the-art results in NLP tasks.",
        "url":         "http://example.com/llm-breakthrough",
    }
    result = extract_insights(sample)
    print(f"Topic:  {result['topic']}")
    print(f"Skills: {', '.join(result['skills'])}")
