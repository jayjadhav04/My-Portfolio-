from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Project(BaseModel):
    id: Optional[str] = Field(alias="_id")
    title: str
    description: str
    icon: str
    tags: List[str]
    features: List[str]
    workflow: str
    challenges: str
    improvements: str
    color: str = "#6366f1"
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Skill(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    icon: str
    category: str
    proficiency: str

class Certification(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    issuer: str
    icon: str
    category: str

class ContactMessage(BaseModel):
    id: Optional[str] = Field(alias="_id")
    name: str
    email: str
    subject: Optional[str] = ""
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdminLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
