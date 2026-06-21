from pydantic import BaseModel
from datetime import datetime, date, time
from typing import Optional
from app.models.event import EventType


class EventCreate(BaseModel):
    email_id: str
    event_type: EventType
    title: str
    description: Optional[str] = None
    extracted_date: Optional[date] = None
    extracted_time: Optional[time] = None


class EventResponse(BaseModel):
    id: str
    event_type: EventType
    title: str
    description: Optional[str]
    extracted_date: Optional[date]
    extracted_time: Optional[time]
    confidence_score: float
    created_at: datetime

    class Config:
        from_attributes = True
