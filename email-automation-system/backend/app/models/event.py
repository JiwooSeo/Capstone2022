from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Date, Time, Float, Text
from sqlalchemy.orm import relationship
from datetime import datetime, date
from uuid import uuid4
from app.database import Base
import enum


class EventType(str, enum.Enum):
    MEETING = "meeting"
    DEADLINE = "deadline"
    ACTION_ITEM = "action_item"
    OTHER = "other"


class ExtractedEvent(Base):
    __tablename__ = "extracted_events"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email_id = Column(String, ForeignKey("emails.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    event_type = Column(Enum(EventType), default=EventType.OTHER)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    extracted_date = Column(Date, nullable=True)
    extracted_time = Column(Time, nullable=True)
    confidence_score = Column(Float, default=0.0)
    raw_text = Column(Text, nullable=True)
    processed_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    email = relationship("Email", back_populates="events")
    user = relationship("User", back_populates="events")
