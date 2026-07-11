# app/schemas.py
from pydantic import BaseModel
from datetime import datetime

class EventIn(BaseModel):
    api_key: str
    event_type: str
    page: str
    properties: dict = {}
    timestamp: datetime | None = None