from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# Resume Insight Input Schema (for creating resume insights)
class ResumeInsightCreate(BaseModel):
    insight_type: str
    content: str

    class Config:
        orm_mode = True  # For working with SQLAlchemy models


# Resume Insight Output Schema (for reading resume insights)
class ResumeInsightOut(BaseModel):
    id: UUID
    insight_type: str
    content: str
    created_at: datetime

    class Config:
        orm_mode = True  # For working with SQLAlchemy models