import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import List

import pandas as pd

from src.models import FeedbackData


REQUIRED_COLUMNS = {"text", "created_at"}


# Parse CSV file and normalize rows into FeedbackData objects.
# Strict validation. Fully defensive.
def parse_csv_feedback(file_path: str) -> List[FeedbackData]:
    feedback_list: List[FeedbackData] = []

    path = Path(file_path)

    if not path.exists():
        print(f"[ERROR] File not found: {file_path}")
        return []

    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        return []

    if not REQUIRED_COLUMNS.issubset(set(df.columns)):
        print("[ERROR] CSV missing required columns: text, created_at")
        return []

    for _, row in df.iterrows():
        try:
            raw_text = str(row["text"]).strip()
            if not raw_text:
                continue

            created_at = pd.to_datetime(row["created_at"], errors="coerce")

            if pd.isna(created_at):
                created_at = datetime.now(timezone.utc)
            else:
                created_at = created_at.to_pydatetime()
                if created_at.tzinfo is None:
                    created_at = created_at.replace(tzinfo=timezone.utc)

            rating = row.get("rating")

            if pd.notna(rating):
                rating = float(rating)
                if not (0 <= rating <= 5):
                    rating = None
            else:
                rating = None

            hash_input = f"{raw_text}{created_at}{rating}"
            external_id = hashlib.sha256(
                hash_input.encode("utf-8")
            ).hexdigest()

            feedback = FeedbackData(
                source="csv",
                external_id=external_id,
                raw_text=raw_text,
                created_at=created_at,
                rating=rating,
            )

            feedback_list.append(feedback)

        except Exception as inner_error:
            print(f"[WARNING] Skipping malformed CSV row: {inner_error}")
            continue

    return feedback_list