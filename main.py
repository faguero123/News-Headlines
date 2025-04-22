import requests
import datetime
import time
from analysis import analyze_sentiment
import os

api_key = os.environ.get("NEWSAPI_KEY")

source_list = [
    "cnn", "bbc-news", "reuters", "the-verge", "the-washington-post",
    "nbc-news", "cbs-news", "abc-news", "fox-news", "bloomberg",
    "al-jazeera-english", "axios", "engadget", "financial-times",
    "fortune", "independent", "msnbc", "national-geographic",
    "politico", "time"
]

today = datetime.datetime.now(datetime.timezone.utc)
html_file = "index.html"
all_articles = []
url = "https://newsapi.org/v2/top-headlines"

for source in source_list:
    params = {
        "sources": source,
        "pageSize": 1,
        "apiKey": api_key
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data["status"] != "ok" or not data.get("articles"):
            print(f"No articles from {source}")
            continue

        article = data["articles"][0]

        article = data["articles"][0]
        title = article["title"]
        link = article["url"]
        name = article["source"]["name"]

        sentiment_label, sentiment_score = analyze_sentiment(title)

        all_articles.append({
            "source": name,
            "title": title,
            "url": link,
            "sentiment_label": sentiment_label,
            "sentiment_score": sentiment_score
        })

        time.sleep(1)

    except Exception as e:
        print(f"Error fetching from {source}: {e}")
        continue

# Write HTML put
with open(html_file, "w", encoding="utf-8") as file:
    file.write(f"<h1> Most Recent News for {today.date()}</h1>\n<ul>\n")

    for article in all_articles:
        sentiment = article['sentiment_label'].lower()  # 'positive', 'neutral', 'negative'
        file.write(f"<li data-sentiment='{sentiment}'>")
        file.write(f"<strong>{article['source']}</strong>: ")
        file.write(f"<a href='{article['url']}'>{article['title']}</a><br>")
        file.write(f"<em>Sentiment:</em> {article['sentiment_label']} ({article['sentiment_score']:.3f})")
        file.write("</li>\n")

    file.write("</ul>\n")

print(f"\nSaved to {html_file}")
