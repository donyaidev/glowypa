from pydantic import BaseModel
from datetime import datetime
from typing import List

class Message(BaseModel):
    message_content: str
    roles: str
    date: datetime

class AcneTreatmentChatTable(BaseModel):
    user_id: str
    acne_treatment_id: str
    messages: List[Message]  
    date: datetime
