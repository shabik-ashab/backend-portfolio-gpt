from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Resume Skill Input Schema (for creating resume skills)
class ResumeSkillCreate(BaseModel):
    skill: str
    category: str
    level: Optional[str] = None

    class Config:
        orm_mode = True  # For working with SQLAlchemy models


# Resume Skill Output Schema (for reading resume skills)
class ResumeSkillOut(BaseModel):
    id: UUID
    skill: str
    category: str
    level: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True  # For working with SQLAlchemy models
