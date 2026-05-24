"""
app.py  –  AI Tech Intelligence Dashboard
Streamlit entry-point.

Pipeline:
  fetch_news / fetch_arxiv
    → clean_articles → filter_relevant → summarize → extract_insights
    → rank_articles
    → store_articles (ChromaDB)          ← NEW: feeds the RAG chatbot
    → display in dashboard

Chatbot (sidebar):
  user query → retrieve_context (ChromaDB) → Groq LLM → answer
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st

from ingestion.news_api import fetch_news
from ingestion.arxiv import fetch_arxiv

from processing.cleaner import clean_articles
from processing.classifier import filter_relevant
from processing.summarizer import summarize

from intelligence.insights import extract_insights
from intelligence.personalization import rank_articles

from config.config import TOP_N

# RAG components (same package — relative imports work from project root)
from rag.vector_store import store_articles
from rag.chatbot import ask_chatbot

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Tech Dashboard", layout="wide")
st.title("🚀 AI Tech Intelligence Dashboard")


# ---------------------------------------------------------------------------
# Data pipeline
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner="Fetching & processing articles…")
def load_data() -> list[dict]:
    news   = fetch_news()
    papers = fetch_arxiv()

    data     = news + papers
    clean    = clean_articles(data)
    relevant = filter_relevant(clean)

    enriched = []
    for article in relevant:
        article["description"] = summarize(article["description"])
        enriched.append(extract_insights(article))

    ranked = rank_articles(enriched)

    # ── Feed the RAG vector store so the chatbot has fresh context ──
    store_articles(ranked)

    return ranked


data = load_data()


# ---------------------------------------------------------------------------
# Sidebar filters
# ---------------------------------------------------------------------------
st.sidebar.header("Filters")
topics = sorted(set(d["topic"] for d in data))
selected_topic = st.sidebar.selectbox("Select Topic", ["All"] + topics)

filtered = data if selected_topic == "All" else [d for d in data if d["topic"] == selected_topic]


# ---------------------------------------------------------------------------
# Article display
# ---------------------------------------------------------------------------
for item in filtered[:TOP_N]:
    with st.container():
        st.subheader(item["title"])
        st.write(f"**Topic:** {item['topic']}")
        st.write(item.get("summary", item.get("description", "")))

        skills = item.get("skills", [])
        if skills:
            st.write("**Skills to Learn:**")
            for skill in skills:
                st.markdown(f"- {skill}")

        st.markdown(f"[Read more]({item['url']})")
        st.markdown("---")


# ---------------------------------------------------------------------------
# RAG Chatbot (sidebar)
# ---------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.title("🤖 AI Career Assistant")

query = st.sidebar.text_input("Ask anything about AI trends")

if query:
    with st.sidebar:
        with st.spinner("Thinking…"):
            response = ask_chatbot(query)
    st.sidebar.write(response)
