from src.database import init_db, SessionLocal
from src.ingestion.google_play import fetch_google_play_reviews
from src.processing.pipeline import process_feedback


def run_ingestion(app_id: str, count: int = 50):
    init_db()

    with SessionLocal() as db:
        reviews = fetch_google_play_reviews(app_id, count=count)

        for review in reviews:
            process_feedback(review, db)

    print(f"Ingested and processed {len(reviews)} reviews.")


if __name__ == "__main__":
    run_ingestion("com.spotify.music", count=50)