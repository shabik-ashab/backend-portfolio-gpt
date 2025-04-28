import uuid
from sqlalchemy import Column, String, Text, JSON, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    linkedin_url = Column(Text, nullable=True)
    github_url = Column(Text, nullable=True)
    portfolio_url = Column(Text, nullable=True)
    blog_url = Column(Text, nullable=True)
    x_twitter_url = Column(Text, nullable=True)
    facebook_url = Column(Text, nullable=True)
    other_links = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    resumes = relationship("Resume", back_populates="user", cascade="all, delete-orphan")
