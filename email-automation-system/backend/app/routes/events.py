from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import ExtractedEvent, User
from app.schemas.event import EventResponse, EventCreate
from app.middleware.auth import get_current_user
from app.models.event import EventType
from typing import List, Optional
from datetime import datetime, date

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("", response_model=List[EventResponse])
async def list_events(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    event_type: Optional[EventType] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    """List extracted events for current user with optional filters."""
    query = db.query(ExtractedEvent).filter(
        ExtractedEvent.user_id == current_user.id
    )

    if event_type:
        query = query.filter(ExtractedEvent.event_type == event_type)

    if start_date:
        query = query.filter(ExtractedEvent.extracted_date >= start_date)

    if end_date:
        query = query.filter(ExtractedEvent.extracted_date <= end_date)

    events = query.order_by(
        ExtractedEvent.extracted_date.asc(),
        ExtractedEvent.extracted_time.asc(),
    ).offset(skip).limit(limit).all()

    return events


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get specific event details."""
    event = db.query(ExtractedEvent).filter(
        ExtractedEvent.id == event_id,
        ExtractedEvent.user_id == current_user.id,
    ).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    return event


@router.post("", response_model=EventResponse)
async def create_event(
    event_create: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new event manually."""
    email = db.query(db.query(db.models.Email)).filter(
        db.query(db.models.Email).id == event_create.email_id
    ).first()

    if email and email.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create event for this email",
        )

    event = ExtractedEvent(
        user_id=current_user.id,
        email_id=event_create.email_id,
        event_type=event_create.event_type,
        title=event_create.title,
        description=event_create.description,
        extracted_date=event_create.extracted_date,
        extracted_time=event_create.extracted_time,
        confidence_score=1.0,
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: str,
    event_update: EventCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an existing event."""
    event = db.query(ExtractedEvent).filter(
        ExtractedEvent.id == event_id,
        ExtractedEvent.user_id == current_user.id,
    ).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    event.event_type = event_update.event_type
    event.title = event_update.title
    event.description = event_update.description
    event.extracted_date = event_update.extracted_date
    event.extracted_time = event_update.extracted_time

    db.commit()
    db.refresh(event)

    return event


@router.delete("/{event_id}")
async def delete_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an event."""
    event = db.query(ExtractedEvent).filter(
        ExtractedEvent.id == event_id,
        ExtractedEvent.user_id == current_user.id,
    ).first()

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    db.delete(event)
    db.commit()

    return {"message": "Event deleted"}


@router.get("/summary/stats")
async def get_event_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get event statistics for current user."""
    stats = db.query(
        ExtractedEvent.event_type,
        func.count(ExtractedEvent.id).label("count"),
    ).filter(
        ExtractedEvent.user_id == current_user.id
    ).group_by(
        ExtractedEvent.event_type
    ).all()

    return {
        "total_events": sum(s[1] for s in stats),
        "by_type": {s[0]: s[1] for s in stats},
    }
