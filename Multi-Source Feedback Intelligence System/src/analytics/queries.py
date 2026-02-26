from datetime import datetime, timezone, timedelta
from typing import Dict, Optional

import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models import FeedbackModel
from src.processing.trends import compute_trend



# Internal Helper: Apply Filters
# Apply optional source and sentiment filtersto a SQLAlchemy query safely.
def _apply_filters(query, source: Optional[str], sentiment: Optional[str]):
    if source:
        query = query.filter(FeedbackModel.source == source)

    if sentiment:
        query = query.filter(FeedbackModel.sentiment_label == sentiment)

    return query

# KPI Aggregation
# Returns high-level KPI metrics. Safe even if database is empty.
def get_kpis(db: Session, source: Optional[str] = None, sentiment: Optional[str] = None,) -> Dict:
    base_query = db.query(FeedbackModel)
    base_query = _apply_filters(base_query, source, sentiment)

    total_feedback = base_query.count()

    negative_query = db.query(FeedbackModel).filter(
        FeedbackModel.sentiment_label == "Negative"
    )
    negative_query = _apply_filters(negative_query, source, sentiment)

    negative_count = negative_query.count()

    rating_query = db.query(func.avg(FeedbackModel.rating)).filter(
        FeedbackModel.rating.isnot(None)
    )
    rating_query = _apply_filters(rating_query, source, sentiment)

    avg_rating = rating_query.scalar()

    percent_negative = (
        (negative_count / total_feedback) * 100
        if total_feedback > 0
        else 0
    )

    return {
        "total_feedback": total_feedback,
        "percent_negative": round(percent_negative, 2),
        "average_rating": round(avg_rating, 2) if avg_rating is not None else 0,
    }

# Sentiment Time Series
# Returns daily average sentiment.
# Output columns: ['date', 'avg_sentiment']
    
def get_sentiment_timeseries(db: Session,days: int = 30,source: Optional[str] = None,sentiment: Optional[str] = None,) -> pd.DataFrame:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    query = db.query(
        func.strftime('%Y-%m-%d', FeedbackModel.created_at).label("date"),
        func.avg(FeedbackModel.sentiment_score).label("avg_sentiment"),
    ).filter(FeedbackModel.created_at >= cutoff)

    query = _apply_filters(query, source, sentiment)

    results = (
        query
        .group_by(func.strftime('%Y-%m-%d', FeedbackModel.created_at))
        .order_by(func.strftime('%Y-%m-%d', FeedbackModel.created_at))
        .all()
    )

    if not results:
        return pd.DataFrame(columns=["date", "avg_sentiment"])

    df = pd.DataFrame(results, columns=["date", "avg_sentiment"])

    # Ensure chronological axis in Plotly
    df["date"] = pd.to_datetime(df["date"])

    return df

# Trend Status
# Compute overall sentiment trend over last N days.
    
def get_trend_status(db: Session,days: int = 7,source: Optional[str] = None,sentiment: Optional[str] = None,) -> str:
    df = get_sentiment_timeseries(
        db,
        days=days,
        source=source,
        sentiment=sentiment,
    )

    if df.empty:
        return "Stable"

    daily_values = df["avg_sentiment"].tolist()

    return compute_trend(daily_values)

# Category Distribution
# Returns most frequent categories.
# Output columns: ['category', 'count']   
def get_top_categories(db: Session,limit: int = 5,source: Optional[str] = None,sentiment: Optional[str] = None,) -> pd.DataFrame:
    query = db.query(
        FeedbackModel.category,
        func.count(FeedbackModel.id).label("count"),
    )

    query = _apply_filters(query, source, sentiment)

    results = (
        query
        .group_by(FeedbackModel.category)
        .order_by(func.count(FeedbackModel.id).desc())
        .limit(limit)
        .all()
    )

    if not results:
        return pd.DataFrame(columns=["category", "count"])

    df = pd.DataFrame(results, columns=["category", "count"])

    return df

# High Priority Feedback
# Returns most urgent feedback entries.
# Output columns: ['created_at', 'source', 'sentiment_label', 'category', 'priority_label', 'priority_score', 'raw_text']
def get_high_priority_feedback(db: Session,limit: int = 10,source: Optional[str] = None,sentiment: Optional[str] = None,) -> pd.DataFrame:
    query = db.query(
        FeedbackModel.created_at,
        FeedbackModel.source,
        FeedbackModel.sentiment_label,
        FeedbackModel.category,
        FeedbackModel.priority_label,
        FeedbackModel.priority_score,
        FeedbackModel.raw_text,
    ).filter(
        FeedbackModel.priority_label.in_(["Critical", "High"])
    )

    query = _apply_filters(query, source, sentiment)

    results = (
        query
        .order_by(FeedbackModel.priority_score.desc())
        .limit(limit)
        .all()
    )

    columns = [
        "created_at",
        "source",
        "sentiment_label",
        "category",
        "priority_label",
        "priority_score",
        "raw_text",
    ]

    if not results:
        return pd.DataFrame(columns=columns)

    df = pd.DataFrame(results, columns=columns)

    # Ensure proper datetime formatting for UI
    df["created_at"] = pd.to_datetime(df["created_at"])

    return df