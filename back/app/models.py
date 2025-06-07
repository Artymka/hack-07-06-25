from pydantic import BaseModel
from datetime import datetime
from typing import List

# -----------------------------
# 3) Схемы (Pydantic-модели)
# -----------------------------
class HistCreate(BaseModel):
    title: str

class Question(BaseModel):
    text: str


class RegisterRequest(BaseModel):
    username: str
    password: str
 
 
class LoginResponse(BaseModel):
    detail: str
 
 
class SessionCreateResponse(BaseModel):
    session_id: int
    created_at: datetime
 
 
class MessageRead(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime
 
    class Config:
        orm_mode = True
 
 
class HistoryResponse(BaseModel):
    session_id: int
    messages: List[MessageRead]
 
 

'''
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey, Integer
import enum
from pydantic import EmailStr


class Question(BaseModel):
    text: str


class UserRequest(BaseModel):
    email: EmailStr
    password: str

class HistRequest(BaseModel):
    email: EmailStr
 
 class HistCreateRequest(BaseModel):
    email: EmailStr
    title: str
# -----------------------------
# 3) Схемы (Pydantic-модели)
# -----------------------------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
 
class LoginResponse(BaseModel):
    detail: str
 
class SessionCreateResponse(BaseModel):
    session_id: int
    created_at: datetime
 
 
class MessageRead(BaseModel):
    id: int
    role: str
    content: str
    timestamp: datetime
 
    class Config:
        orm_mode = True
 
 
class HistoryResponse(BaseModel):
    session_id: int
    messages: List[MessageRead]
'''