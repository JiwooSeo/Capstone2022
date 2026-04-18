from openai import OpenAI
from app.config import get_settings
from app.models.event import EventType
from app.utils.errors import OpenAIException
import json
import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)
settings = get_settings()

client = OpenAI(api_key=settings.openai_api_key)


class EmailParsingService:
    """Service for parsing email content with OpenAI GPT."""

    EXTRACTION_PROMPT = """
You are an email content analyzer. Extract scheduling information from the following email.

Email Subject: {subject}
Email Body:
{body}

Return a JSON array of extracted events. For each event, extract:
- type: one of "meeting", "deadline", "action_item" (required)
- title: brief title (required)
- description: optional details
- date: extracted date in YYYY-MM-DD format (optional)
- time: extracted time in HH:MM format (optional)
- confidence: confidence score 0-1

Return ONLY valid JSON array, no other text.
Example format:
[
  {"type": "meeting", "title": "Team standup", "date": "2024-01-15", "time": "10:00", "confidence": 0.95},
  {"type": "deadline", "title": "Project submission", "date": "2024-01-20", "confidence": 0.85}
]
"""

    @staticmethod
    def extract_events(subject: str, body: str) -> list:
        """Extract events from email using OpenAI."""
        if not body or not body.strip():
            logger.warning(f"Empty email body for subject: {subject}")
            return []

        try:
            prompt = EmailParsingService.EXTRACTION_PROMPT.format(
                subject=subject[:200],
                body=body[:2000],
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000,
            )

            content = response.choices[0].message.content.strip()

            try:
                events = json.loads(content)
                if not isinstance(events, list):
                    events = [events]
                return events
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse GPT response as JSON: {e}")
                logger.debug(f"GPT response: {content}")
                return []

        except Exception as e:
            logger.error(f"Failed to extract events from email: {e}")
            raise OpenAIException(f"Email parsing failed: {e}")

    @staticmethod
    def validate_and_normalize_event(event: dict) -> Optional[dict]:
        """Validate and normalize extracted event."""
        try:
            event_type = event.get("type", "").lower()
            if event_type not in [e.value for e in EventType]:
                event_type = "other"

            return {
                "event_type": event_type,
                "title": event.get("title", "")[:200],
                "description": event.get("description", "")[:500],
                "extracted_date": EmailParsingService._parse_date(event.get("date")),
                "extracted_time": EmailParsingService._parse_time(event.get("time")),
                "confidence_score": float(event.get("confidence", 0.5)),
                "raw_text": json.dumps(event),
            }
        except Exception as e:
            logger.error(f"Failed to validate event: {e}")
            return None

    @staticmethod
    def _parse_date(date_str: str) -> Optional[str]:
        """Parse date string in YYYY-MM-DD format."""
        if not date_str:
            return None
        try:
            from datetime import datetime
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except Exception:
            logger.warning(f"Failed to parse date: {date_str}")
            return None

    @staticmethod
    def _parse_time(time_str: str) -> Optional[str]:
        """Parse time string in HH:MM format."""
        if not time_str:
            return None
        try:
            from datetime import datetime
            datetime.strptime(time_str, "%H:%M")
            return time_str
        except Exception:
            logger.warning(f"Failed to parse time: {time_str}")
            return None
