from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker
from app.config import settings
from typing import Annotated
from datetime import datetime
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext


DATABASE_URL = settings.get_db_url()
 
# -----------------------------
# 1) Настройка SQLAlchemy
# -----------------------------
engine = create_engine(DATABASE_URL, echo=True)  # echo=True для вывода SQL-запросов в консоль
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()
 
 
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
 
 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
 
 
# -----------------------------
# 2) Модели (ORM)
# -----------------------------
class User(Base):
    __tablename__ = "users"
 
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
 
    sessions = relationship("ChatSession", back_populates="user")
 
 
class ChatSession(Base):
    __tablename__ = "chat_sessions"
 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete")
 
 
class Message(Base):
    __tablename__ = "messages"
 
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String(16), nullable=False)  # "user" или "bot"
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
 
    session = relationship("ChatSession", back_populates="messages")
 
 
# Выполняем создание таблиц (если не созданы)
Base.metadata.create_all(bind=engine)
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from os import environ
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, ForeignKey, Integer
import enum
from app.config import settings
from datetime import datetime
from typing import List, Optional
 
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        create_engine, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker
from config import settings


engine = create_async_engine(settings.get_db_url, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()
 
 
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
 
 
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
 
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(30))

class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

class SenderEnum(str, enum.Enum):
    USER = "user"
    BOT = "bot"
class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"))
    sender: Mapped[SenderEnum] = mapped_column()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 
 
def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """
    HTTP Basic авторизация: отвечает User из базы, если имя/пароль корректны.
    Иначе бросает HTTPException(401).
    """
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user

Base.metadata.create_all(engine)
'''