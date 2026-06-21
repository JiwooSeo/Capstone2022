from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Email, User
from app.schemas.email import EmailResponse
from app.middleware.auth import get_current_user
from app.services.email_processor import EmailProcessor
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api/emails", tags=["emails"])


@router.get("", response_model=List[EmailResponse])
async def list_emails(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    """List emails for current user (paginated)."""
    emails = db.query(Email).filter(
        Email.user_id == current_user.id,
        Email.is_deleted == False,
    ).order_by(Email.received_at.desc()).offset(skip).limit(limit).all()

    return emails


@router.get("/{email_id}", response_model=EmailResponse)
async def get_email(
    email_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get specific email details."""
    email = db.query(Email).filter(
        Email.id == email_id,
        Email.user_id == current_user.id,
        Email.is_deleted == False,
    ).first()

    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )

    return email


@router.post("/sync")
async def sync_emails(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Manually trigger email fetch for current user."""
    try:
        count = EmailProcessor.fetch_and_store_emails(
            user_id=current_user.id,
            db=db,
            limit=50,
        )
        return {
            "message": f"Fetched {count} new emails",
            "count": count,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email fetch failed: {str(e)}",
        )


@router.delete("/{email_id}")
async def delete_email(
    email_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Soft delete email."""
    email = db.query(Email).filter(
        Email.id == email_id,
        Email.user_id == current_user.id,
    ).first()

    if not email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found",
        )

    EmailProcessor.soft_delete_email(email_id, db)
    return {"message": "Email deleted"}
