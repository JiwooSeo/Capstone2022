from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class EmailResponse(BaseModel):
    id: str
    gmail_message_id: str
    subject: Optional[str]
    sender: Optional[str]
    received_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True
