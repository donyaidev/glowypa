from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class recommendMessage(BaseModel):
    user_id: str
    message: str
    role: str
    messageUser: str
    rag: bool = Field(default=True)
    db: bool = Field(default=True)
    history_chat: Optional[list] = Field(default=[])

# Model cho mỗi bước trong routine
class RoutineStep(BaseModel):
    _id: Optional[str]
    step: str
    product: str
    usage: str
    link: str
    image: str
    like: int = Field(default=0)

# Model cho daily routine (sáng và tối)
class DailyRoutine(BaseModel):
    morning: List[RoutineStep]
    evening: List[RoutineStep]

# Model cho microneedling
# class Microneedling(BaseModel):
#     description: str

# Model chính
class SkincareRoutine(BaseModel):
    _id: Optional[str]
    context: str = Field(default="")
    acne_treatment: str
    daily_routine: DailyRoutine
    # microneedling: Microneedling
    # notes: List[str]
    
    
class LikeRequest(BaseModel):
    routine_id: str
    product_name: str