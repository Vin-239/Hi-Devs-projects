import sys
import os
from datetime import datetime, timezone

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import init_db, SessionLocal
from src.models import FeedbackData, FeedbackModel
from src.processing.pipeline import process_feedback


def test_phase3_pipeline():
    print("\n--- Phase 3 Isolation Test ---")

    # Initialize DB
    init_db()
    db = SessionLocal()

    # Ensure deterministic state
    db.query(FeedbackModel).delete()
    db.commit()

    # Create controlled test feedback
    feedback = FeedbackData(
        source="unit_test",
        external_id="test_001",
        raw_text="The app crashes and is very slow. Completely broken experience.",
        created_at=datetime.now(timezone.utc),
        rating=1.0,
    )

    # Run processing
    latency = process_feedback(feedback, db)

    print(f"Latency: {latency:.6f} seconds")

    # Fetch stored record
    stored = db.query(FeedbackModel).filter_by(external_id="test_001").first()

    assert stored is not None, "Record was not saved."

    print("Sentiment:", stored.sentiment_label)
    print("Category:", stored.category)
    print("Priority Score:", stored.priority_score)
    print("Priority Label:", stored.priority_label)

    # Assertions (Hard Checks) 

    # Sentiment should be Negative
    assert stored.sentiment_label == "Negative", "Sentiment misclassified."

    # Category should detect Bug (crashes/broken)
    assert stored.category == "Bug", "Category detection failed."

    # Priority must be bounded
    assert 0.0 <= stored.priority_score <= 1.0, "Priority out of bounds."

    # Latency under 2 seconds
    assert latency < 2.0, "Latency exceeded 2 seconds."

    print("Primary validation passed.")

    # Test Idempotency (Duplicate processing) 
    print("\nTesting idempotency...")

    latency_2 = process_feedback(feedback, db)

    count = db.query(FeedbackModel).filter_by(external_id="test_001").count()

    assert count == 1, "Duplicate record inserted."

    print("Idempotency confirmed.")
    print(f"Second run latency: {latency_2:.6f} seconds")

    db.close()


if __name__ == "__main__":
    test_phase3_pipeline()