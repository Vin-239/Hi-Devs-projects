import math
import time
import dataclasses
from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models import FeedbackData, FeedbackModel
from src.processing.sentiment import analyze_sentiment
from src.processing.category import categorize_text


URGENCY_KEYWORDS = ["crash", "scam", "broken", "charged", "fraud"]

# Enrich feedback with sentiment, category, and priority.
# Persist safely.Returns processing latency (seconds)
def process_feedback(feedback: FeedbackData, db: Session) -> float:
    
    start = time.perf_counter()

    # Minimal Cleaning (Preserve sentiment signal) 
    clean_text = feedback.raw_text.lower().strip()
    feedback.clean_text = clean_text

    # Sentiment 
    sentiment_score, sentiment_label = analyze_sentiment(clean_text)
    feedback.sentiment_score = sentiment_score
    feedback.sentiment_label = sentiment_label

    # Categorization
    category = categorize_text(clean_text)
    feedback.category = category

    # Frequency (7-day strict window) 
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

    category_count = (
        db.query(FeedbackModel)
        .filter(
            FeedbackModel.category == category,
            FeedbackModel.created_at >= seven_days_ago
        )
        .count()
    )

    # Urgency Detection
    urgency_flag = 1 if any(word in clean_text for word in URGENCY_KEYWORDS) else 0

    # Priority Calculation
    normalized_sentiment = (sentiment_score + 1) / 2  # scale to [0,1]

    raw_priority = (
        (1 - normalized_sentiment) * 0.5
        + math.log10(category_count + 1) * 0.3
        + urgency_flag * 0.2
    )

    priority_score = round(min(1.0, raw_priority), 4)
    feedback.priority_score = priority_score

    if priority_score >= 0.7:
        feedback.priority_label = "Critical"
    elif priority_score >= 0.4:
        feedback.priority_label = "High"
    elif priority_score >= 0.2:
        feedback.priority_label = "Medium"
    else:
        feedback.priority_label = "Low"

    feedback.processed_at = datetime.now(timezone.utc)

    # Safe Persistence (Idempotent)
    existing = (
        db.query(FeedbackModel)
        .filter_by(
            source=feedback.source,
            external_id=feedback.external_id
        )
        .first()
    )

    if not existing:
        db_record = FeedbackModel(**dataclasses.asdict(feedback))
        try:
            db.add(db_record)
            db.commit()
        except IntegrityError:
            db.rollback()
        except Exception:
            db.rollback()
            raise
    else:
        # Record already exists — idempotent safe
        db.rollback()

    end = time.perf_counter()
    return end - start