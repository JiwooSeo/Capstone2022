from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from app.database import Base
import enum


class ProcessingLogStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class ProcessingLogType(str, enum.Enum):
    EMAIL_FETCH = "email_fetch"
    EMAIL_EXTRACTION = "email_extraction"
    TOKEN_REFRESH = "token_refresh"
    ERROR = "error"


class ProcessingLog(Base):
    __tablename__ = "processing_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    email_id = Column(String, ForeignKey("emails.id"), nullable=True)
    log_type = Column(Enum(ProcessingLogType), nullable=False)
    status = Column(Enum(ProcessingLogStatus), default=ProcessingLogStatus.PENDING)
    message = Column(Text, nullable=True)
    details = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="logs")
