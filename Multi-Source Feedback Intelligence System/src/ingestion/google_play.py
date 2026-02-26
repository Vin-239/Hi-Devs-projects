import hashlib
from datetime import datetime, timezone
from typing import List

from google_play_scraper import reviews, Sort
from src.models import FeedbackData

# Fetch reviews from Google Play and normalize into FeedbackData objects.
# Fully defensive. Never raises unhandled exceptions.
def fetch_google_play_reviews(
    app_id: str,
    count: int = 100
) -> List[FeedbackData]:
    feedback_list: List[FeedbackData] = []

    try:
        result, _ = reviews(
            app_id,
            lang="en",
            country="us",
            sort=Sort.NEWEST,
            count=count
        )
    except Exception as e:
        print(f"[ERROR] Google Play fetch failed: {e}")
        return []

    for review in result:
        try:
            raw_text = review.get("content", "")
            if not raw_text:
                continue

            raw_text = raw_text.strip()
            if not raw_text:
                continue

            created_at = review.get("at")

            if isinstance(created_at, datetime):
                if created_at.tzinfo is None:
                    created_at = created_at.replace(tzinfo=timezone.utc)
            else:
                created_at = datetime.now(timezone.utc)

            rating = review.get("score")
            rating = float(rating) if rating is not None else None

            external_id = review.get("reviewId")
            if not external_id:
                external_id = hashlib.sha256(
                    raw_text.encode("utf-8")
                ).hexdigest()

            feedback = FeedbackData(
                source="google_play",
                external_id=external_id,
                raw_text=raw_text,
                created_at=created_at,
                rating=rating,
            )

            feedback_list.append(feedback)

        except Exception as inner_error:
            print(f"[WARNING] Skipping malformed review: {inner_error}")
            continue

    return feedback_list