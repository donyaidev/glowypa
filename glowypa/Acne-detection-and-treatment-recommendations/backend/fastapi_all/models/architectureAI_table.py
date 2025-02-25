from pydantic import BaseModel

class ArchitectureAiTable(BaseModel):
    ai_name: str
    ai_description: str

class ArchitectureAiFormat(BaseModel):
    id_architecture: str
    ai_name: str
    ai_description: str
