import sys
from pathlib import Path 
sys.path.append(str(Path(__file__).parent.parent))  # Добавляет /workspace/ML в пути

from ml.main import *

def responder(state: State):
    query = state["messages"][-1]["content"]
    style = state.get("message_type", "formal")
    web_ctx = state.get("web_search_context", "")
    sql_ctx = state.get("nl2sql_context", "")

    prompt = f"""
        Ты — ассистент по муниципальной статистике России. Дай развёрнутый ответ на вопрос пользователя.
        
        Используй информацию из двух источников:

        1) Официальные интернет-ресурсы:
        {web_ctx}

        2) Данные СберИндекса:
        {sql_ctx}

        Если данные СберИндекса по населению сильно отличаются, тогда используй только данные веб-поиска, 
        если данные веб-поиска позволяют ответить на вопрос.
        
        Если данные в двух источниках не позволяют точно ответить на вопрос, 
        попробуй ответить самостоятельно, но будь точен, перепроверь информацию, прежде чем дать ответ.

        Не говори пользователю, если данных в одном из источников нет. Отвечай только по делу.

        Оформи ответ в стиле: {style}.
    """
    result = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=query)
    ])

    # Добавляем готовый ответ в историю сообщений
    return {"messages": [{"role": "assistant", "content": result.content}]}