from sqlalchemy.orm import Session
from app.models import Email, User, GmailToken, ExtractedEvent
from app.services.gmail_service import GmailService
from app.utils.crypto import get_token_encryption
from app.utils.errors import EmailProcessingException
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
encryption = get_token_encryption()


class EmailProcessor:
    """Service for fetching and storing emails from Gmail."""

    @staticmethod
    def fetch_and_store_emails(
        user_id: str,
        db: Session,
        since: datetime = None,
        limit: int = 50,
    ) -> int:
        """Fetch emails from Gmail and store in database."""
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise EmailProcessingException(f"User {user_id} not found")

            gmail_token = db.query(GmailToken).filter(
                GmailToken.user_id == user_id
            ).first()
            if not gmail_token:
                raise EmailProcessingException(f"No Gmail token for user {user_id}")

            decrypted_access = encryption.decrypt(gmail_token.access_token)
            decrypted_refresh = encryption.decrypt(gmail_token.refresh_token)

            gmail_service = GmailService(
                access_token=decrypted_access,
                refresh_token=decrypted_refresh,
            )

            if gmail_service.credentials.expired:
                if not gmail_service.refresh_credentials():
                    raise EmailProcessingException("Failed to refresh Gmail credentials")

            query = "is:unread" if since is None else f"after:{since.strftime('%Y/%m/%d')}"
            messages_result = gmail_service.get_messages(query=query, max_results=limit)

            messages = messages_result.get("messages", [])
            stored_count = 0

            for message_id_data in messages:
                message_id = message_id_data["id"]

                existing = db.query(Email).filter(
                    Email.gmail_message_id == message_id,
                    Email.user_id == user_id,
                ).first()
                if existing:
                    continue

                try:
                    full_message = gmail_service.get_message(message_id)
                    parsed = gmail_service.parse_message(full_message)

                    email = Email(
                        user_id=user_id,
                        gmail_message_id=parsed["gmail_message_id"],
                        subject=parsed["subject"],
                        sender=parsed["sender"],
                        body=parsed["body"],
                        received_at=parsed["received_at"],
                        raw_payload=parsed["raw_payload"],
                    )
                    db.add(email)
                    db.commit()
                    db.refresh(email)
                    stored_count += 1
                    logger.info(f"Stored email: {parsed['subject']}")

                except Exception as e:
                    logger.error(f"Failed to fetch/store message {message_id}: {e}")
                    db.rollback()
                    continue

            return stored_count

        except Exception as e:
            logger.error(f"Email fetch failed for user {user_id}: {e}")
            raise EmailProcessingException(f"Failed to fetch emails: {e}")

    @staticmethod
    def mark_email_processed(email_id: str, db: Session) -> bool:
        """Mark email as processed."""
        try:
            email = db.query(Email).filter(Email.id == email_id).first()
            if email:
                email.processed_at = datetime.utcnow()
                db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to mark email {email_id} as processed: {e}")
            return False

    @staticmethod
    def soft_delete_email(email_id: str, db: Session) -> bool:
        """Soft delete email."""
        try:
            email = db.query(Email).filter(Email.id == email_id).first()
            if email:
                email.is_deleted = True
                db.commit()
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete email {email_id}: {e}")
            return False
