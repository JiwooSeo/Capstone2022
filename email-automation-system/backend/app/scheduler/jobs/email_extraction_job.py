from app.database import SessionLocal
from app.models import Email, ExtractedEvent, ProcessingLog
from app.services.openai_service import EmailParsingService
from app.models.processing_log import ProcessingLogStatus, ProcessingLogType
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def process_unprocessed_emails():
    """Background job to extract events from unprocessed emails."""
    db = SessionLocal()
    try:
        unprocessed_emails = db.query(Email).filter(
            Email.processed_at == None,
            Email.is_deleted == False,
        ).limit(20).all()

        logger.info(f"Processing {len(unprocessed_emails)} unprocessed emails")

        for email in unprocessed_emails:
            try:
                if not email.subject or not email.body:
                    logger.warning(f"Email {email.id} missing subject or body")
                    email.processed_at = datetime.utcnow()
                    db.commit()
                    continue

                extracted_events = EmailParsingService.extract_events(
                    subject=email.subject,
                    body=email.body,
                )

                for event_data in extracted_events:
                    validated_event = EmailParsingService.validate_and_normalize_event(
                        event_data
                    )
                    if validated_event:
                        event = ExtractedEvent(
                            email_id=email.id,
                            user_id=email.user_id,
                            event_type=validated_event["event_type"],
                            title=validated_event["title"],
                            description=validated_event["description"],
                            extracted_date=validated_event["extracted_date"],
                            extracted_time=validated_event["extracted_time"],
                            confidence_score=validated_event["confidence_score"],
                            raw_text=validated_event["raw_text"],
                        )
                        db.add(event)

                email.processed_at = datetime.utcnow()
                db.commit()

                log_entry = ProcessingLog(
                    user_id=email.user_id,
                    email_id=email.id,
                    log_type=ProcessingLogType.EMAIL_EXTRACTION,
                    status=ProcessingLogStatus.SUCCESS,
                    message=f"Extracted {len(extracted_events)} events",
                    details={"event_count": len(extracted_events)},
                )
                db.add(log_entry)
                db.commit()
                logger.info(f"Processed email {email.id}: {len(extracted_events)} events")

            except Exception as e:
                logger.error(f"Failed to process email {email.id}: {e}")

                log_entry = ProcessingLog(
                    user_id=email.user_id,
                    email_id=email.id,
                    log_type=ProcessingLogType.EMAIL_EXTRACTION,
                    status=ProcessingLogStatus.FAILED,
                    message=f"Extraction failed: {str(e)}",
                    details={"error": str(e)},
                )
                db.add(log_entry)
                db.commit()

    except Exception as e:
        logger.error(f"Email extraction job failed: {e}")
    finally:
        db.close()
