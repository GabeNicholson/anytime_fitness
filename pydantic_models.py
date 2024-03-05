# models/pydantic_models.py
from pydantic import BaseModel
from datetime import datetime

class ClickEvent(BaseModel):
    action: str
    timestamp: datetime