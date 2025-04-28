import uuid
from sqlalchemy import Column, Text, ForeignKey, TIMESTAMP, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class ResumeSection(Base):
    __tablename__ = "resume_sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    section_type = Column(Text, nullable=False)
    content = Column(Text, nullable=True)
    extracted_data = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    resume = relationship("Resume", back_populates="sections")
