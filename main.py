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
    file.write(f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Most Recent News for {today.date()}</title>
   <style>
    #sentiment-filter {{
      margin-bottom: 1em;
      font-size: 1em;
    }}

    li[data-sentiment="negative"] {{
      color: crimson;
    }}

    li[data-sentiment="positive"] {{
      color: darkgreen;
    }}

    li[data-sentiment="neutral"] {{
      color: gray;
    }}
  </style>
</head>
<body>
  <h1> Most Recent News for {today.date()}</h1>
  <label for="sentiment-filter">Filter by Sentiment:</label>
  <select id="sentiment-filter" onchange="filterSentiment()">
    <option value="all">All</option>
    <option value="positive-neutral">Positive/Neutral</option>
    <option value="negative">Negative</option>
  </select>

  <ul>
""")
    for article in all_articles:
        sentiment = article['sentiment_label'].lower()
        file.write(f"<li data-sentiment='{sentiment}'>")
        file.write(f"<strong>{article['source']}</strong>: ")
        file.write(f"<a href='{article['url']}'>{article['title']}</a><br>")
        file.write(f"<em>Sentiment:</em> {article['sentiment_label']} ({article['sentiment_score']:.3f})")
        file.write("</li>\n")

    file.write(f"""</ul>
  <p><em>Last updated: {today.strftime('%Y-%m-%d %H:%M UTC')}</em></p>

  <script>
    function filterSentiment() {{
      const filter = document.getElementById("sentiment-filter").value;
      const items = document.querySelectorAll("li[data-sentiment]");
      items.forEach(item => {{
        const sentiment = item.getAttribute("data-sentiment");
        const isPosOrNeutral = sentiment === "positive" || sentiment === "neutral";
        if (filter === "all") {{
          item.style.display = "list-item";
        }} else if (filter === "positive-neutral") {{
          item.style.display = isPosOrNeutral ? "list-item" : "none";
        }} else if (filter === "negative") {{
          item.style.display = sentiment === "negative" ? "list-item" : "none";
        }}
      }});
    }}
  </script>
</body>
</html>""")


print(f"\nSaved to {html_file}")
