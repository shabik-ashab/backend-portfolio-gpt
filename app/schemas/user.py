from pydantic import BaseModel, EmailStr, HttpUrl
from typing import Optional, List, Dict
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    linkedin_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    portfolio_url: Optional[HttpUrl] = None
    blog_url: Optional[HttpUrl] = None
    x_twitter_url: Optional[HttpUrl] = None
    facebook_url: Optional[HttpUrl] = None
    other_links: Optional[Dict[str, str]] = None


class UserOut(UserCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
