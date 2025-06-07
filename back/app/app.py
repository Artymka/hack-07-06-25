from datetime import datetime
from typing import List, Optional
from fastapi.responses import StreamingResponse
 
from fastapi import Depends, FastAPI, HTTPException, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session, relationship, sessionmaker

from app.db import *
from app.models import *
from asyncio import sleep as asleep

# from ml.graph import quest_model, state, startup

# -----------------------------
# 5) Зависимости
# -----------------------------

 
 
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
 
 
# -----------------------------
# 6) Приложение FastAPI
# -----------------------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def fake_model_answers():
    await asleep(1)
    yield "гойда"
    await asleep(1)
    yield "вы чувствуете себя запретым на хакотоне? гойда"
    await asleep(1)
    yield "гойда!!"
    await asleep(1)
    yield "вы пришли чтобы победить?"
    await asleep(1)
    yield "ГОЙДА!!!"

async def test_model_answers(text):
    if text.lower().startswith("проанализируй данные о населении и заработной плате в муниципалитетах ростовской области"):
        yield """
        Анализируя предоставленные данные о численности населения и средней заработной плате наиболее населенных муниципальных образований Ростовской области за 2023 год, можно сделать следующие выводы относительно наличия или отсутствия корреляции между этими показателями.

        Источники данных:
        - Министерство труда и социального развития Ростовской области (данные о средней зарплате и населении).
        - СберИндекс (информация о численности населения муниципалитета с учетом агломераций).

        ### Основные положения анализа:
        На основе представленных данных заметна следующая тенденция: чем больше численность населения муниципального образования, тем выше уровень средней заработной платы. Например, самый крупный город региона – Ростов-на-Дону – имеет наибольшую среднюю зарплату среди всех перечисленных городов по данным СберИндекса (67647.9 рублей). В то же время менее крупные города, такие как Новошахтинск и Сальский район, характеризуются значительно более низкими средними заработными платами.

        Однако стоит отметить, что прямая зависимость не является абсолютно строгой. Так, например, хотя население Таганрога существенно меньше, чем у Ростова-на-Дону, его средняя зарплата (60177.5  рублей) заметно превышает показатели таких крупных городских округов, как Шахты и Новочеркасск по данным министерства труда и социального развития Ростовской области.

        Таким образом, хотя общая положительная корреляция между численностью населения и уровнем средней заработной платы прослеживается, она носит скорее общий характер и подвержена влиянию других факторов, таких как отраслевая структура экономики каждого конкретного муниципалитета, наличие крупных предприятий и объектов инфраструктуры, уровень жизни и другие социально-экономические факторы.

        В заключение следует подчеркнуть, что для проведения полноценного статистического исследования и подтверждения наличия значимой корреляционной связи необходимо привлечение дополнительных показателей и использование специальных методов математической статистики"""
    
    elif text.lower().startswith("в каких муниципалитетах самые крупные траты на маркетплейсах"):
        yield """
        Муниципалитеты Ростовской области, где зафиксированы наиболее высокие средние расходы граждан на маркетплейсы (рассчитанные на одного жителя), представлены следующим списком в порядке убывания:

        1. Роговское – 8 418 рублей  
        2. Первомайское – 8 327,13 рубля  
        3. Анадырь – 8 157,54 рубля  
        4. Внуковское – 8 139,13 рубля  
        5. Печенгский – 8 109 рублей  
        6. Вороновское – 8 091,67 рубля  
        7. Ловозерский – 8 088,17 рубля  
        8. Михайлово-Ярцевское – 7 784,92 рубля  
        9. Полярные Зори – 7 740,08 рубля  
        10. Кировск – 7 663,88 рубля 

        Приведённые выше цифры отражают среднюю сумму расходов жителей каждого муниципалитета на покупки через онлайн-платформы за указанный временной интервал с января 2023-го по декабрь 2024 года включительно.
        """

async def real_model_answers(text):
    yield text

# graph = None

# @app.on_event("startup")
# async def startup_event():
#     global graph
#     graph = startup()


@app.head("/")
@app.get("/")
async def index():
    return {"message": "Hello, world!"}

@app.get("/test")
async def test():
    return {"message": "test"}

@app.post("/api/quest")
async def question(q: Question):
    return StreamingResponse(test_model_answers(q.text))

    # answer = quest_model(q.text, state, graph)
    # return StreamingResponse(real_model_answers(quest_model(q.text, state, graph)))


@app.post("/api/register", status_code=status.HTTP_201_CREATED)
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    Если username уже занят, возвращаем ошибку 400.
    """
    existing = db.query(User).filter(User.username == request.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует",
        )
    user = User(
        username=request.username,
        hashed_password=get_password_hash(request.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"detail": "Пользователь успешно зарегистрирован"}
 
 
@app.post("/api/login")
def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    """
    Проверяет переданные HTTP Basic креденшелы.
    При успехе возвращает подтверждение.
    """
    print("--- Credentials ---")
    print(credentials.username)
    print(credentials.password)
    
    user = db.query(User).filter(User.username == credentials.username).first()

    print("--- DB ---")
    print(user.username)
    print(user.hashed_password)
    print("succes:", verify_password(credentials.password, user.hashed_password))

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"detail": f"Пользователь {user.username} успешно аутентифицирован"}
 
 
@app.post("/api/hist-create")
def create_chat_session(
    hc: Annotated[HistCreate, Body()],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Создаёт новую сессию чата для текущего (аутентифицированного) пользователя.
    Возвращает ID этой сессии и время создания.
    """
    new_session = ChatSession(user_id=current_user.id, title=hc.title)
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return {
        "chat": {
            "id": new_session.id,
        }
    }
    # return SessionCreateResponse(
    #     session_id=new_session.id,
    # )
 
"""
Chat
    title
    messages
    id
    user_email
"""

@app.post("/api/hist")
def get_chat_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Возвращает историю (список сообщений) для указанной сессии (session_id),
    но только если эта сессия принадлежит текущему пользователю.
    """
    chat_objs = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == current_user.id)
        .all()
    )
    if not len(chat_objs):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия чата не найдена или не принадлежит текущему пользователю",
        )
    
    response = []
    for chat in chat_objs:

        messages = (
            db.query(Message)
            .join(ChatSession, Message.session_id == ChatSession.id)
            .filter(
                ChatSession.id == chat.id,
                ChatSession.user_id == current_user.id
            )
            .order_by(Message.timestamp)
            .all()
        )

        part = {
            "title": chat.title,
            "id": chat.id,
            "email": current_user.username,
            "messages": [{"role": message.role, "content": message.content} for message in messages]
        }
        response.append(part)

    return response
 
 
# -----------------------------
# (Дополнительно) Эндпоинт для добавления сообщения в сессию
# -----------------------------
class MessageCreateRequest(BaseModel):
    role: str  # "user" или "bot"
    content: str
 
 
@app.post("/api/hist/{session_id}/message")
def add_message_to_session(
    session_id: int,
    req: MessageCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Добавляет новое сообщение в указанную сессию (session_id).
    Проверяет, что сессия принадлежит текущему пользователю.
    """
    session_obj = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.user_id == current_user.id)
        .first()
    )
    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия чата не найдена или не принадлежит текущему пользователю",
        )
    # Создаём сообщение
    msg = Message(
        session_id=session_obj.id,
        role=req.role,
        content=req.content,
        timestamp=datetime.utcnow(),
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


'''
from fastapi import FastAPI, Request, Depends, HTTPException, Cookie, Response
from fastapi.responses import StreamingResponse
from asyncio import sleep as asleep
from app.models import Question
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from httpx import AsyncClient
import secrets
from urllib.parse import urljoin, urlencode
from os import environ
import jwt
from datetime import datetime, timedelta, timezone
import google.oauth2.credentials
import google_auth_oauthlib.flow
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
from fastapi import Body
from app.db import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship, sessionmaker

from app.models import *


app = FastAPI()
ALLOWED_HOSTS = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Для защиты от CSRF
sessions = {}


async def fake_model_answers():
    for i in range(10):
        await asleep(1)
        yield b"lorem ipsum dolor sit amet "

@app.head("/")
@app.get("/")
async def index():
    return {"message": "Hello, world!"}

@app.get("/test")
async def test():
    return {"message": "test"}

@app.post("/api/quest")
async def question(q: Question):
    return StreamingResponse(fake_model_answers())



@app.post("/api/register")
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    Если username уже занят, возвращаем ошибку 400.
    """
    existing = db.query(User).filter(User.username == request.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует",
        )
    user = User(
        username=request.username,
        hashed_password=get_password_hash(request.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"detail": "Пользователь успешно зарегистрирован"}
 
 
@app.post("/api/login", response_model=LoginResponse)
# def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
def login(credentials: UserRequest = Depends(security), db: Session = Depends(get_db)):
    """
    Проверяет переданные HTTP Basic креденшелы.
    При успехе возвращает подтверждение.
    """
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials
 
 
@app.post("/api/hist-create", response_model=SessionCreateResponse)
def create_chat_session(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Создаёт новую сессию чата для текущего (аутентифицированного) пользователя.
    Возвращает ID этой сессии и время создания.
    """
    new_chat = Chat(id=current_user.id)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    return {
        "chat": {
            "id": new_chat.id
        }
    }
 
 
@app.post("/api/hist", response_model=HistoryResponse)
def get_chat_history(
    email: Annotated[str, Body()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Возвращает историю (список сообщений) для указанной сессии (session_id),
    но только если эта сессия принадлежит текущему пользователю.
    """
    session_obj = (
        db.query(Chat)
        .filter(Chat.id == session_id, ChatSession.user_id == current_user.id)
        .first()
    )
    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия чата не найдена или не принадлежит текущему пользователю",
        )
    # Загружаем сообщения, автоматически по связи сессии
    msgs = session_obj.messages
    return HistoryResponse(
        session_id=session_obj.id,
        messages=msgs,
    )
 
 
# -----------------------------
# (Дополнительно) Эндпоинт для добавления сообщения в сессию
# -----------------------------
class MessageCreateRequest(BaseModel):
    role: str  # "user" или "bot"
    content: str
 
 
@app.post("/api/hist/{session_id}/message", response_model=MessageRead)
def add_message_to_session(
    session_id: int,
    req: MessageCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Добавляет новое сообщение в указанную сессию (session_id).
    Проверяет, что сессия принадлежит текущему пользователю.
    """
    session_obj = (
        db.query(ChatSession)
        .filter(ChatSession.id == session_id, ChatSession.user_id == current_user.id)
        .first()
    )
    if not session_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Сессия чата не найдена или не принадлежит текущему пользователю",
        )
    # Создаём сообщение
    msg = Message(
        session_id=session_obj.id,
        role=req.role,
        content=req.content,
        timestamp=datetime.utcnow(),
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg

'''