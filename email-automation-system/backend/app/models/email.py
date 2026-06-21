from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from app.database import Base


class Email(Base):
    __tablename__ = "emails"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    gmail_message_id = Column(String, nullable=False, index=True)
    subject = Column(String, nullable=True)
    sender = Column(String, nullable=True)
    body = Column(Text, nullable=True)
    received_at = Column(DateTime, nullable=False)
    processed_at = Column(DateTime, nullable=True)
    raw_payload = Column(JSON, nullable=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="emails")
    events = relationship("ExtractedEvent", back_populates="email", cascade="all, delete-orphan")
