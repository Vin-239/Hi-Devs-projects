import nltk
from nltk.sentiment import SentimentIntensityAnalyzer


# Ensure VADER lexicon exists (indomitable initialization)
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon", quiet=True)

_analyzer = SentimentIntensityAnalyzer()

# Analyze sentiment using VADER. Returns: (compound_score, sentiment_label)
def analyze_sentiment(text: str) -> tuple[float, str]:
    if not text:
        return 0.0, "Neutral"

    scores = _analyzer.polarity_scores(text)
    compound = scores.get("compound", 0.0)

    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    return compound, label