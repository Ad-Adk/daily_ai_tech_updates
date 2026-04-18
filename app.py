import streamlit as st

from ingestion.news_api import fetch_news
from ingestion.arxiv import fetch_arxiv

from processing.cleaner import clean_articles
from processing.classifier import filter_relevant
from processing.summarizer import summarize

from intelligence.insights import extract_insights
from intelligence.personalization import rank_articles


st.set_page_config(page_title="AI Tech Dashboard", layout="wide")

st.title("🚀 AI Tech Intelligence Dashboard")

# Load data
@st.cache_data
def load_data():
    news = fetch_news()
    papers = fetch_arxiv()

    data = news + papers

    clean = clean_articles(data)
    relevant = filter_relevant(clean)

    enriched = []
    for a in relevant:
        a["description"] = summarize(a["description"])
        enriched.append(extract_insights(a))

    ranked = rank_articles(enriched)

    return ranked


data = load_data()

# Sidebar filters
st.sidebar.header("Filters")

topics = list(set([d["topic"] for d in data]))
selected_topic = st.sidebar.selectbox("Select Topic", ["All"] + topics)

# Filter logic
if selected_topic != "All":
    data = [d for d in data if d["topic"] == selected_topic]

# Display
for item in data[:10]:
    with st.container():
        st.subheader(item["title"])
        
        st.write(f"**Topic:** {item['topic']}")
        st.write(item["summary"])

        st.write("**Skills to Learn:**")
        for skill in item["skills"]:
            st.markdown(f"- {skill}")

        st.markdown(f"[Read more]({item['url']})")

        st.markdown("---")