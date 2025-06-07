from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

# Импортируем вашу логику
from main import *  
from graph import * 

# Хранилище состояний для нескольких сессий
# В продакшене можно заменить на Redis, БД и т.п.
conversations: dict[str, State] = {}

app = FastAPI(
    title="Multi-Agent Chat API",
    version="1.0"
)

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    user_input: str

class ChatResponse(BaseModel):
    conversation_id: str
    assistant_response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    # Определяем ID диалога
    conv_id = request.conversation_id or str(uuid.uuid4())

    # Если диалога нет — инициализируем состояние
    if conv_id not in conversations:
        conversations[conv_id] = {
            "messages": [],
            "message_type": None,
            "access": "NO",
            "web_search_context": None,
            "nl2sql_context": None
        }
    state = conversations[conv_id]

    # Добавляем сообщение пользователя
    state["messages"].append({"role": "user", "content": request.user_input})

    # Запускаем мультиагентную логику
    state = graph.invoke(state)

    # Ищем последний ответ ассистента
    assistant_msgs = [m for m in state.get("messages", []) if m.get("role") == "assistant"]
    if not assistant_msgs:
        raise HTTPException(status_code=500, detail="No assistant response generated.")
    response_content = assistant_msgs[-1]["content"]

    # Сохраняем обновлённое состояние
    conversations[conv_id] = state

    return ChatResponse(
        conversation_id=conv_id,
        assistant_response=response_content
    )

# Запуск через: uvicorn app:app --host 0.0.0.0 --port 8000 --reload
