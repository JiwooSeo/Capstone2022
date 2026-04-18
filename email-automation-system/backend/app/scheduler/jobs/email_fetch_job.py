from app.database import SessionLocal
from app.models import User, ProcessingLog
from app.services.email_processor import EmailProcessor
from app.models.processing_log import ProcessingLogStatus, ProcessingLogType
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def fetch_emails_for_all_users():
    """Background job to fetch emails for all active users."""
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.is_active == True).all()
        logger.info(f"Starting email fetch for {len(users)} users")

        for user in users:
            try:
                count = EmailProcessor.fetch_and_store_emails(
                    user_id=user.id,
                    db=db,
                    limit=50,
                )

                log_entry = ProcessingLog(
                    user_id=user.id,
                    log_type=ProcessingLogType.EMAIL_FETCH,
                    status=ProcessingLogStatus.SUCCESS,
                    message=f"Fetched {count} new emails",
                    details={"count": count},
                )
                db.add(log_entry)
                db.commit()
                logger.info(f"Fetched {count} emails for user {user.id}")

            except Exception as e:
                logger.error(f"Failed to fetch emails for user {user.id}: {e}")

                log_entry = ProcessingLog(
                    user_id=user.id,
                    log_type=ProcessingLogType.EMAIL_FETCH,
                    status=ProcessingLogStatus.FAILED,
                    message=f"Email fetch failed: {str(e)}",
                    details={"error": str(e)},
                )
                db.add(log_entry)
                db.commit()

    except Exception as e:
        logger.error(f"Email fetch job failed: {e}")
    finally:
        db.close()
