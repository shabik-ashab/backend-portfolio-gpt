import uuid
import enum
from sqlalchemy import Column, Text, ForeignKey, TIMESTAMP, Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class TaskStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    file_name = Column(Text, nullable=True)
    raw_text = Column(Text, nullable=True)
    uploaded_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    parsed_at = Column(TIMESTAMP(timezone=True), nullable=True)

    task_status = Column(
        SqlEnum(TaskStatusEnum, name="taskstatusenum"),
        nullable=False,
        server_default=TaskStatusEnum.PENDING.value
    )

    user = relationship("User", back_populates="resumes")
    sections = relationship("ResumeSection", back_populates="resume", cascade="all, delete-orphan")
    skills = relationship("ResumeSkills", back_populates="resume", cascade="all, delete-orphan")
    insights = relationship("ResumeInsight", back_populates="resume", cascade="all, delete-orphan")
