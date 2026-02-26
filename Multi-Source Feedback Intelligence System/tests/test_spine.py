import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.exc import IntegrityError

from src.models import FeedbackData, FeedbackModel
from src.database import SessionLocal, init_db


def test_vertical_slice():
    print("\nTesting Phase 1: The Database Spine")

    init_db()
    db = SessionLocal()

    # Ensure deterministic test state
    db.query(FeedbackModel).delete()
    db.commit()

    # 1. Create DataClass instance
    dummy_data = FeedbackData(
        source="google_play",
        external_id="gp_12345_hash",
        raw_text="The app crashes every time I try to checkout. Fix it!",
        created_at=datetime.utcnow(),
        rating=1.0,
        model_version="v1-vader"
    )

    # 2. Map to ORM model
    db_record = FeedbackModel(
        id=dummy_data.id,
        source=dummy_data.source,
        external_id=dummy_data.external_id,
        created_at=dummy_data.created_at,
        ingested_at=dummy_data.ingested_at,
        raw_text=dummy_data.raw_text,
        clean_text=dummy_data.clean_text,
        rating=dummy_data.rating,
        model_version=dummy_data.model_version
    )

    # 3. Insert record
    try:
        db.add(db_record)
        db.commit()
        print(f"Success: Record '{db_record.id}' written to DB.")
    except Exception as e:
        db.rollback()
        print(f"Unexpected failure inserting record: {e}")
        db.close()
        return

    # 4. Test Unique Constraint
    print("\nTesting Unique Constraint (Double Ingestion Defense)")

    duplicate_record = FeedbackModel(
        id="another_uuid",
        source=dummy_data.source,
        external_id=dummy_data.external_id,
        created_at=datetime.utcnow(),
        ingested_at=datetime.utcnow(),
        raw_text="Different text, same external ID.",
        model_version="v1-vader"
    )

    try:
        db.add(duplicate_record)
        db.commit()
        print("Failure: Duplicate was allowed (Constraint broken).")
    except IntegrityError:
        db.rollback()
        print("Success: Duplicate ingestion correctly blocked.")
    except Exception as e:
        db.rollback()
        print(f"Unexpected error type caught: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    test_vertical_slice()