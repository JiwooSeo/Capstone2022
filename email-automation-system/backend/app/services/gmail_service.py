from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.api_python_client import build
from app.config import get_settings
from app.utils.errors import GmailAPIException
import logging
from typing import Optional, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
settings = get_settings()


class GmailService:
    """Wrapper around Gmail API for email operations."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self, access_token: str, refresh_token: Optional[str] = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=settings.gmail_client_id,
            client_secret=settings.gmail_client_secret,
        )
        self.service = build("gmail", "v1", credentials=self.credentials)

    def refresh_credentials(self) -> bool:
        """Refresh access token using refresh token."""
        try:
            request = Request()
            self.credentials.refresh(request)
            self.access_token = self.credentials.token
            return True
        except RefreshError as e:
            logger.error(f"Failed to refresh Gmail credentials: {e}")
            return False

    def get_messages(
        self,
        query: str = "",
        max_results: int = 10,
        page_token: Optional[str] = None,
    ) -> dict:
        """Get list of messages matching query."""
        try:
            result = self.service.users().messages().list(
                userId="me",
                q=query,
                maxResults=max_results,
                pageToken=page_token,
            ).execute()
            return result
        except Exception as e:
            logger.error(f"Failed to get Gmail messages: {e}")
            raise GmailAPIException(f"Failed to fetch messages: {e}")

    def get_message(self, message_id: str, format: str = "full") -> dict:
        """Get full message content."""
        try:
            message = self.service.users().messages().get(
                userId="me",
                id=message_id,
                format=format,
            ).execute()
            return message
        except Exception as e:
            logger.error(f"Failed to get Gmail message {message_id}: {e}")
            raise GmailAPIException(f"Failed to fetch message: {e}")

    def parse_message(self, message: dict) -> dict:
        """Parse Gmail message into structured format."""
        try:
            headers = message.get("payload", {}).get("headers", [])
            header_dict = {h["name"]: h["value"] for h in headers}

            subject = header_dict.get("Subject", "No Subject")
            sender = header_dict.get("From", "Unknown")
            date_str = header_dict.get("Date", "")

            body = self._get_message_body(message.get("payload", {}))

            return {
                "gmail_message_id": message.get("id"),
                "subject": subject,
                "sender": sender,
                "body": body,
                "received_at": self._parse_date(date_str),
                "raw_payload": message,
            }
        except Exception as e:
            logger.error(f"Failed to parse message: {e}")
            raise

    def _get_message_body(self, payload: dict) -> str:
        """Extract body from message payload."""
        if "parts" in payload:
            for part in payload["parts"]:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data", "")
                    if data:
                        return self._decode_body(data)
            for part in payload["parts"]:
                if part.get("mimeType") == "text/html":
                    data = part.get("body", {}).get("data", "")
                    if data:
                        return self._decode_body(data)
        else:
            data = payload.get("body", {}).get("data", "")
            if data:
                return self._decode_body(data)
        return ""

    @staticmethod
    def _decode_body(data: str) -> str:
        """Decode base64url encoded body."""
        import base64
        try:
            return base64.urlsafe_b64decode(data + "==").decode("utf-8")
        except Exception as e:
            logger.warning(f"Failed to decode body: {e}")
            return data

    @staticmethod
    def _parse_date(date_str: str) -> datetime:
        """Parse RFC 2822 date string from Gmail."""
        from email.utils import parsedate_to_datetime
        try:
            return parsedate_to_datetime(date_str)
        except Exception as e:
            logger.warning(f"Failed to parse date: {e}")
            return datetime.utcnow()

    def get_unread_messages(
        self,
        max_results: int = 10,
        page_token: Optional[str] = None,
    ) -> dict:
        """Get unread messages."""
        return self.get_messages(
            query="is:unread",
            max_results=max_results,
            page_token=page_token,
        )

    def get_messages_since(
        self,
        since: datetime,
        max_results: int = 10,
    ) -> dict:
        """Get messages since a specific datetime."""
        rfc_date = since.strftime("%Y/%m/%d")
        return self.get_messages(
            query=f"after:{rfc_date}",
            max_results=max_results,
        )

    @staticmethod
    def get_oauth_flow():
        """Get OAuth 2.0 flow for Gmail authentication."""
        from google_auth_oauthlib.flow import Flow

        flow = Flow.from_client_secrets_file(
            "client_secret.json",
            scopes=GmailService.SCOPES,
            redirect_uri=settings.gmail_redirect_uri,
        )
        return flow
