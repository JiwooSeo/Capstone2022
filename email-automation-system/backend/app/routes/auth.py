from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models import User, GmailToken
from app.schemas import UserResponse, TokenResponse
from app.services.auth_service import AuthService, OAuthService
from app.services.gmail_service import GmailService
from app.middleware.auth import get_current_user
from app.config import get_settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)
settings = get_settings()
router = APIRouter(prefix="/api/auth", tags=["auth"])
auth_service = AuthService()
oauth_service = OAuthService()


@router.post("/google-callback", response_model=TokenResponse)
async def google_oauth_callback(
    code: str = Query(...),
    state: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """Handle Google OAuth callback and create/update user."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.id_token import verify_oauth2_token

        try:
            from google_auth_oauthlib.flow import Flow

            flow = Flow.from_client_config(
                {
                    "installed": {
                        "client_id": settings.gmail_client_id,
                        "client_secret": settings.gmail_client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [settings.gmail_redirect_uri],
                    }
                },
                scopes=GmailService.SCOPES,
                state=state,
            )
            flow.redirect_uri = settings.gmail_redirect_uri
            flow.fetch_token(code=code)

            credentials = flow.credentials
            id_token = credentials.id_token

            user_info = verify_oauth2_token(id_token, Request())

            google_id = user_info.get("sub")
            email = user_info.get("email")
            name = user_info.get("name", email.split("@")[0])

            user = db.query(User).filter(User.google_id == google_id).first()

            if not user:
                user = User(
                    email=email,
                    name=name,
                    google_id=google_id,
                    is_active=True,
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                logger.info(f"Created new user: {email}")
            else:
                logger.info(f"Authenticated existing user: {email}")

            old_token = db.query(GmailToken).filter(
                GmailToken.user_id == user.id
            ).first()
            if old_token:
                db.delete(old_token)

            encrypted_access = oauth_service.encrypt_token(credentials.token)
            encrypted_refresh = oauth_service.encrypt_token(credentials.refresh_token)

            token_expiry = datetime.utcfromtimestamp(credentials.expiry.timestamp())

            gmail_token = GmailToken(
                user_id=user.id,
                access_token=encrypted_access,
                refresh_token=encrypted_refresh,
                token_expiry=token_expiry,
                scopes=GmailService.SCOPES,
            )
            db.add(gmail_token)
            db.commit()

            access_token = AuthService.create_access_token(user.id)

            return TokenResponse(access_token=access_token)

        except Exception as e:
            logger.error(f"OAuth flow failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"OAuth authentication failed: {e}",
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in OAuth callback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth authentication failed",
        )


@router.get("/user", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """Get current authenticated user info."""
    return UserResponse.from_orm(current_user)


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (client-side token deletion)."""
    return {"message": "Successfully logged out"}
