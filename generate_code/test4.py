import asyncio
import aiohttp
from bs4 import BeautifulSoup
from transformers import pipeline
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

sentiment_analyzer = pipeline("sentiment-analysis")

NEWS_SOURCES = [
    "https://news.google.com/search?q=climate+change",
    "https://news.yahoo.com/tagged/climate-change"
]

async def fetch_html(session, url):
    async with session.get(url) as response:
        return await response.text()

def extract_articles(html):
    soup = BeautifulSoup(html, 'html.parser')
    titles = [tag.get_text() for tag in soup.find_all('h3')[:10]]
    return titles

async def scrape_articles():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_html(session, url) for url in NEWS_SOURCES]
        html_pages = await asyncio.gather(*tasks)
        articles = []
        for html in html_pages:
            articles.extend(extract_articles(html))
        return articles

def analyze_sentiments(texts):
    results = sentiment_analyzer(texts)
    sentiment_scores = [1 if r['label'] == 'POSITIVE' else -1 for r in results]
    return sentiment_scores

def group_by_day(sentiments):
    today = datetime.today().date()
    return {today: sentiments}

def plot_sentiments(grouped):
    for day, sentiments in grouped.items():
        plt.bar(str(day), sum(sentiments) / len(sentiments))
    plt.title("Average Sentiment Over Time")
    plt.ylabel("Sentiment Score")
    plt.show()

async def main():
    articles = await scrape_articles()
    sentiments = analyze_sentiments(articles)
    grouped = group_by_day(sentiments)
    plot_sentiments(grouped)

asyncio.run(main())
