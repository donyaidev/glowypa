from typing import Optional
from pydantic import BaseModel, Field

from pydantic import BaseModel, Field

class ChatboxMessage(BaseModel):
    user_id: str
    message: str
    role: str
    rag: bool = Field(default=True)
    db: bool = Field(default=True)
    history_chat: Optional[list] = Field(default=[])

    
    