from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Model for each step in the skincare routine
class RoutineStep(BaseModel):
    step: str
    product: str
    usage: str
    link: str
    image: str
    like: int = Field(default=0)

# Model for daily routines (morning and evening)
class DailyRoutine(BaseModel):
    morning: List[RoutineStep]
    evening: List[RoutineStep]

# Main model for the skincare routine
class SkincareRoutine(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # MongoDB ID
    context: Optional[str] = Field(default="")
    acne_treatment: Optional[str] = Field(default="")
    daily_routine: DailyRoutine
    cosine_score: Optional[float] = None


# Model for the recommendation message
class RecommendMessage(BaseModel):
    user_id: str
    message: str
    role: str
    type: str
    rag: bool = Field(default=True)
    db: bool = Field(default=True)
    history_chat: Optional[List[dict]] = Field(default=[])
    recommend: SkincareRoutine
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
