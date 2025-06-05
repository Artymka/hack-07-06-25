from fastapi import FastAPI, Request, Depends, HTTPException, Cookie, Response
from fastapi.responses import StreamingResponse
from asyncio import sleep as asleep
from app.models import Question
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from httpx import AsyncClient
import secrets
from os import environ
import jwt
from datetime import datetime, timedelta, timezone


app = FastAPI()
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


# Конфигурация Google OAuth
GOOGLE_CLIENT_ID = environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = environ["GOOGLE_CLIENT_SECRET"]
GOOGLE_REDIRECT_URI = environ["GOOGLE_REDIRECT_URI"]
GOOGLE_AUTHORIZATION_URL = environ["GOOGLE_AUTHORIZATION_URL"]
GOOGLE_TOKEN_URL = environ["GOOGLE_TOKEN_URL"]
GOOGLE_USER_INFO_URL = environ["GOOGLE_USER_INFO_URL"]
SECRET_KEY = environ["SECRET_KEY"]
ALGORITHM = "HS256"

@app.get("/login/google")
async def login_google(request: Request):
    """Редиректит на страницу google для выбора пользователя."""
    # Генерируем случайный state (защита от CSRF)
    state = secrets.token_urlsafe(16)
    sessions[state] = True

    # Формируем URL для авторизации Google
    auth_url = (
        f"{GOOGLE_AUTHORIZATION_URL}?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"response_type=code&"
        f"scope=email%20profile&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"state={state}"
    )
    return RedirectResponse(auth_url)

@app.get("/auth/google/callback")
async def auth_google_callback(code: str, state: str, response: Response):
    """Получает данные пользователя по коду, который вернул google, устанавливает jwt."""
    # Проверяем state (CSRF-защита)
    if state not in sessions:
        raise HTTPException(status_code=400, detail="Invalid state")
    del sessions[state]

    # Обмениваем код на токен
    async with AsyncClient() as client:
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )

    token_data = token_response.json()
    access_token = token_data["access_token"]
    id_token = token_data.get("id_token")

    # Получаем данные пользователя
    async with AsyncClient() as client:
        user_info = await client.get(
            GOOGLE_USER_INFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )

    user_data = user_info.json()

    token_data = {
        "sub": user_data["email"],  # Уникальный идентификатор
        "name": user_data.get("name"),
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),  # Срок действия
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Устанавливаем токен в куки (HTTP-only для защиты от XSS)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=3600,  # 1 час
        secure=True,    # Только HTTPS (в продакшене)
        samesite="lax",
    )

    return {
        "email": user_data["email"],
        "name": user_data["name"],
        "picture": user_data["picture"],
    }

async def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Не авторизован")
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")
