from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.database import get_db
from app.models import User
from app.utils.errors import InvalidTokenException, unauthorized_exception
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Dependency to get current authenticated user from JWT token."""
    try:
        user_id = AuthService.verify_token(credentials.credentials)
    except InvalidTokenException:
        raise unauthorized_exception()

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.is_active:
        raise unauthorized_exception()

    return user


def get_current_user_optional(
    credentials: HTTPAuthCredentials = None,
    db: Session = Depends(get_db),
) -> User:
    """Get current user if authenticated, otherwise return None."""
    if not credentials:
        return None

    try:
        user_id = AuthService.verify_token(credentials.credentials)
        user = db.query(User).filter(User.id == user_id).first()
        if user and user.is_active:
            return user
    except Exception as e:
        logger.debug(f"Optional auth failed: {e}")

    return None
