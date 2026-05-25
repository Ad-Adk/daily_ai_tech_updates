"""
app.py – AI Tech Intelligence Dashboard (Streamlit entry-point).

Pipeline:
  fetch_news / fetch_arxiv
    → clean_articles → filter_relevant → summarize → extract_insights
    → rank_articles → store_articles (ChromaDB)
    → render dashboard

Sidebar chatbot:
  user query → retrieve_context → Groq LLM → answer
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st

from ingestion.news_api    import fetch_news
from ingestion.arxiv       import fetch_arxiv
from processing.cleaner    import clean_articles
from processing.classifier import filter_relevant
from processing.summarizer import summarize
from intelligence.insights       import extract_insights
from intelligence.personalization import rank_articles
from rag.vector_store      import store_articles
from rag.chatbot           import ask_chatbot
from config.config         import TOP_N

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI Tech Dashboard", layout="wide")
st.title("🚀 AI Tech Intelligence Dashboard")


# ── Data pipeline ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Fetching & processing articles…")
def load_data() -> list[dict]:
    raw      = fetch_news() + fetch_arxiv()
    clean    = clean_articles(raw)
    relevant = filter_relevant(clean)

    enriched = [
        extract_insights({**a, "description": summarize(a["description"])})
        for a in relevant
    ]

    ranked = rank_articles(enriched)
    store_articles(ranked)   # feed RAG store for the chatbot
    return ranked


data = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.header("Filters")
topics = sorted({d["topic"] for d in data})
selected_topic = st.sidebar.selectbox("Select Topic", ["All"] + topics)

filtered = data if selected_topic == "All" else [d for d in data if d["topic"] == selected_topic]

# ── Article cards ─────────────────────────────────────────────────────────────
for item in filtered[:TOP_N]:
    with st.container():
        st.subheader(item["title"])
        st.write(f"**Topic:** {item['topic']}")
        st.write(item.get("summary") or item.get("description", ""))

        if skills := item.get("skills"):
            st.write("**Skills to Learn:**")
            for skill in skills:
                st.markdown(f"- {skill}")

        st.markdown(f"[Read more]({item['url']})")
        st.markdown("---")

# ── RAG chatbot (sidebar) ─────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.title("🤖 AI Career Assistant")

if query := st.sidebar.text_input("Ask anything about AI trends"):
    with st.sidebar, st.spinner("Thinking…"):
        st.sidebar.write(ask_chatbot(query))
