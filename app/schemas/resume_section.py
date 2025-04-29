from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Resume Section Input Schema (for creating resume sections)
class ResumeSectionCreate(BaseModel):
    section_type: str
    content: str
    extracted_data: Optional[dict] = None

    class Config:
        orm_mode = True  # For working with SQLAlchemy models


# Resume Section Output Schema (for reading resume sections)
class ResumeSectionOut(BaseModel):
    id: UUID
    section_type: str
    content: str
    extracted_data: Optional[dict] = None
    created_at: datetime

    class Config:
        orm_mode = True  # For working with SQLAlchemy models