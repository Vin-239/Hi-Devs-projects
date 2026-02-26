import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    UniqueConstraint,
    Index,
    Text
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


@dataclass
class FeedbackData:
    """Canonical internal representation of user feedback."""
    
    source: str
    external_id: str
    raw_text: str
    created_at: datetime

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ingested_at: datetime = field(default_factory=datetime.utcnow)
    clean_text: str = ""
    rating: Optional[float] = None
    sentiment_score: float = 0.0
    sentiment_label: str = "Neutral"
    category: str = "Other"
    priority_score: float = 0.0
    priority_label: str = "Low"
    processed_at: Optional[datetime] = None
    model_version: str = "v1-vader"

# SQLAlchemy ORM Model for SQLite Persistence.
class FeedbackModel(Base):
    
    __tablename__ = "feedback"

    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)
    external_id = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    ingested_at = Column(DateTime, nullable=False)

    raw_text = Column(Text, nullable=False)
    clean_text = Column(Text, nullable=False, default="")

    rating = Column(Float, nullable=True)

    sentiment_score = Column(Float, nullable=False, default=0.0)
    sentiment_label = Column(String, nullable=False, default="Neutral")

    category = Column(String, nullable=False, default="Other")

    priority_score = Column(Float, nullable=False, default=0.0)
    priority_label = Column(String, nullable=False, default="Low")

    processed_at = Column(DateTime, nullable=True)
    model_version = Column(String, nullable=False, default="v1-vader")

    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_source_external_id"),
        Index("idx_created_at", "created_at"),
        Index("idx_source", "source"),
        Index("idx_category", "category"),
        Index("idx_sentiment_priority", "sentiment_label", "priority_label"),
    )