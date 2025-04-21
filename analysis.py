from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

sia = SentimentIntensityAnalyzer()

nltk.download('vader_lexicon', quiet=True)

def analyze_sentiment(text: str) -> tuple[str, float]:

    score = sia.polarity_scores(text)["compound"]
    if score >= 0.05:
        label = "Positive"
    elif score <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    return label, score

