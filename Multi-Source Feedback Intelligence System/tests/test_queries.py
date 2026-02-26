import sys
import os
from datetime import datetime, timezone

import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import init_db, SessionLocal
from src.models import FeedbackData, FeedbackModel
from src.processing.pipeline import process_feedback
from src.analytics.queries import (
    get_kpis,
    get_sentiment_timeseries,
    get_trend_status,
    get_top_categories,
    get_high_priority_feedback,
)

# Test data seeding function
def seed_test_data(db):
    db.query(FeedbackModel).delete()
    db.commit()

    samples = [
        FeedbackData(
            source="unit_test",
            external_id="t1",
            raw_text="Amazing app, love the design and features!",
            created_at=datetime.now(timezone.utc),
            rating=5.0,
        ),
        FeedbackData(
            source="unit_test",
            external_id="t2",
            raw_text="App crashes frequently. Completely broken.",
            created_at=datetime.now(timezone.utc),
            rating=1.0,
        ),
        FeedbackData(
            source="unit_test",
            external_id="t3",
            raw_text="Too expensive for what it offers.",
            created_at=datetime.now(timezone.utc),
            rating=2.0,
        ),
    ]

    for feedback in samples:
        process_feedback(feedback, db)


def test_analytics_layer():
    print("\nPhase 4 Analytics Isolation Test")

    init_db()
    db = SessionLocal()

    seed_test_data(db)

    # KPI Test 
    kpis = get_kpis(db)
    print("KPIs:", kpis)

    assert isinstance(kpis, dict)
    assert kpis["total_feedback"] == 3
    assert 0 <= kpis["percent_negative"] <= 100
    assert kpis["average_rating"] > 0

    # Time Series Test
    ts_df = get_sentiment_timeseries(db, days=30)
    print("\nTime Series DataFrame:")
    print(ts_df)

    assert isinstance(ts_df, pd.DataFrame)
    assert "date" in ts_df.columns
    assert "avg_sentiment" in ts_df.columns

    if not ts_df.empty:
        assert pd.api.types.is_datetime64_any_dtype(ts_df["date"])

    # Trend Test
    trend = get_trend_status(db, days=7)
    print("\nTrend Status:", trend)

    assert trend in ["Improving", "Degrading", "Stable"]

    #Category Distribution Test
    cat_df = get_top_categories(db)
    print("\nTop Categories:")
    print(cat_df)

    assert isinstance(cat_df, pd.DataFrame)
    assert "category" in cat_df.columns
    assert "count" in cat_df.columns

    # High Priority Test
    hp_df = get_high_priority_feedback(db)
    print("\nHigh Priority Feedback:")
    print(hp_df)

    assert isinstance(hp_df, pd.DataFrame)
    if not hp_df.empty:
        assert pd.api.types.is_datetime64_any_dtype(hp_df["created_at"])

    print("\nAnalytics layer validation passed.")

    db.close()


if __name__ == "__main__":
    test_analytics_layer()