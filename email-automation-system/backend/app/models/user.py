from sqlalchemy import Column, String, DateTime, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    email = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    google_id = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
    settings = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    gmail_tokens = relationship("GmailToken", back_populates="user", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="user", cascade="all, delete-orphan")
    events = relationship("ExtractedEvent", back_populates="user", cascade="all, delete-orphan")
    logs = relationship("ProcessingLog", back_populates="user", cascade="all, delete-orphan")
