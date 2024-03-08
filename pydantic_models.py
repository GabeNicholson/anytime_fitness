# models/pydantic_models.py
from pydantic import BaseModel

class ClickEvent(BaseModel):
    action: str