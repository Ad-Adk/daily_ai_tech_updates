import feedparser

def fetch_arxiv():
    url = "http://export.arxiv.org/api/query?search_query=ai&start=0&max_results=5"
    feed = feedparser.parse(url)

    papers = []
    for entry in feed.entries:
        papers.append({
            "title": entry.title,
            "description": entry.summary,
            "url": entry.link
        })

    return papers

if __name__ == "__main__":
    papers = fetch_arxiv()

    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Description: {paper['description']}")
        print(f"URL: {paper['url']}")
        print("-" * 80)