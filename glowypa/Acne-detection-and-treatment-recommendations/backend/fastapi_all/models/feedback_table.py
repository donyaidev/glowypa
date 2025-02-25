from typing import Optional
from pydantic import BaseModel

class FeedbackTable(BaseModel):
    user_id: str
    image: Optional[str] = None  # Optional field
    feedback_content: str
    rate: int
    date: str
    
    
class FeedbackPost(BaseModel):
    user_id: str
    image: Optional[str] = None  # Optional field
    feedback_content: str
    rate: int
