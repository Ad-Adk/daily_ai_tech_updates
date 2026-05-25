"""
config.py – Central configuration for the AI Tech Intelligence Pipeline.
All tuneable constants live here; no magic numbers in application code.
"""

from pathlib import Path

# ── Project root ────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH  = ROOT_DIR / "config" / ".env"
DB_PATH   = str(ROOT_DIR / "chroma_db")

# ── Dashboard ────────────────────────────────────────────────────────────────
TOP_N = 20

# ── Relevance filter ─────────────────────────────────────────────────────────
KEYWORDS: list[str] = [
    "ai", "machine learning", "data science", "gpt", "llm", "agent",
    "multimodal", "reasoning", "openai", "anthropic", "gemini",
    "fine-tuning", "inference", "rag", "retrieval-augmented generation",
    "langchain", "mlops",
]

# ── Scoring weights ───────────────────────────────────────────────────────────
HIGH_VALUE_TOPICS: dict[str, int] = {
    "LLM": 5,
    "Generative AI": 5,
    "Agentic AI": 5,
    "MLOps": 4,
    "Computer Vision": 4,
    "AI Infrastructure": 4,
    "Robotics": 3,
    "Cybersecurity": 3,
    "Cloud AI": 3,
    "General": 1,
}

HIGH_VALUE_SKILLS: dict[str, int] = {
    "Fine-tuning": 3,
    "Prompt Engineering": 3,
    "RAG": 3,
    "Transformers": 3,
    "Vector Databases": 3,
    "LLMOps": 3,
    "LangChain": 2,
    "Docker": 2,
    "Kubernetes": 2,
    "PyTorch": 2,
    "TensorFlow": 2,
    "OpenCV": 2,
}

# ── LLM ──────────────────────────────────────────────────────────────────────
LLM_MODEL    = "llama-3.1-8b-instant"
LLM_TEMP     = 0
MAX_SKILLS   = 5
