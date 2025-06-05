from fastapi import FastAPI, Request, Depends, HTTPException
# from fastapi.responses import RedirectResponse, HTMLResponse
# from fastapi.security import OAuth2AuthorizationCodeBearer
# from jose import jwt
# from httpx import AsyncClient
# import secrets

app = FastAPI()


@app.head("/")
@app.get("/")
async def index():
    return {"message": "Hello, world!"}

@app.get("/test")
async def test():
    return {"message": "test"}
'''
# Конфигурация Google OAuth
GOOGLE_CLIENT_ID = "ваш_client_id"
GOOGLE_CLIENT_SECRET = "ваш_client_secret"
GOOGLE_REDIRECT_URI = "http://localhost:8000/auth/google/callback"
GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# Для защиты от CSRF
sessions = {}

@app.get("/login/google")
async def login_google(request: Request):
    # Генерируем случайный state (защита от CSRF)
    state = secrets.token_urlsafe(16)
    sessions[state] = True

    # Формируем URL для авторизации Google
    auth_url = (
        f"{GOOGLE_AUTHORIZATION_URL}?"
        f"client_id={GOOGLE_CLIENT_ID}&"
        f"response_type=code&"
        f"scope=openid%20email%20profile&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"state={state}"
    )
    return RedirectResponse(auth_url)

@app.get("/auth/google/callback")
async def auth_google_callback(code: str, state: str):
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
    return {
        "email": user_data["email"],
        "name": user_data.get("name"),
        "picture": user_data.get("picture"),
    }

@app.get("/")
async def home():
    return HTMLResponse("""
        <html>
            <body>
                <a href="/login/google">Login with Google</a>
            </body>
        </html>
    """)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    '''