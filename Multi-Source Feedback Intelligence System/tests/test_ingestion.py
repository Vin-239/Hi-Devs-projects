import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion.google_play import fetch_google_play_reviews
from src.ingestion.csv_parser import parse_csv_feedback


def test_adapters():
    print("\nTesting Google Play Adapter")

    gp_reviews = fetch_google_play_reviews("com.spotify.music", count=5)
    print(f"Fetched {len(gp_reviews)} Google reviews.")

    if gp_reviews:
        print(f"Sample: {gp_reviews[0].raw_text[:50]}...")
        print(f"Created At: {gp_reviews[0].created_at}")
        print(f"Rating: {gp_reviews[0].rating}")

    print("\nTesting CSV Adapter")

    csv_path = "data/raw/sample.csv"

    if not os.path.exists(csv_path):
        import pandas as pd
        os.makedirs("data/raw", exist_ok=True)
        pd.DataFrame({
            "text": [
                "This app is great!",
                "Terrible experience, crashed immediately."
            ],
            "created_at": ["2026-02-20", "2026-02-21"],
            "rating": [5.0, 1.0]
        }).to_csv(csv_path, index=False)
        print(f"Created temporary dummy CSV at {csv_path}")

    csv_reviews = parse_csv_feedback(csv_path)
    print(f"Parsed {len(csv_reviews)} CSV reviews.")

    if csv_reviews:
        print(f"Sample: {csv_reviews[0].raw_text[:50]}...")
        print(f"External ID: {csv_reviews[0].external_id[:10]}...")


if __name__ == "__main__":
    test_adapters()