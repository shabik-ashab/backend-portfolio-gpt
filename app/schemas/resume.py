from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

# Resume Input Schema (for creating resumes)
class ResumeCreate(BaseModel):
    file_name: str
    raw_text: str
    uploaded_at: Optional[str] = None

    class Config:
        orm_mode = True  # For working with SQLAlchemy models


# Resume Output Schema (for reading resumes)
class ResumeOut(BaseModel):
    id: UUID
    file_name: str
    raw_text: str
    uploaded_at: datetime
    parsed_at: Optional[datetime] = None

    class Config:
        orm_mode = True  # For working with SQLAlchemy models