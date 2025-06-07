import sys
from pathlib import Path 
sys.path.append(str(Path(__file__).parent.parent))  # Добавляет /workspace/ML в пути


from main import *
from agents.nl2sql import qwen

def clarify(state: State):
    query = state['messages'][-1]['content']

    prompt=f"""
        Твоя задача - одобрить запрос пользователя.
        Если запрос пользователя связан с муниципалитетами, субъектами России, территориями, статистиками
        и прочей аналитически-деловой областью, то верни "YES".

        В ином случае верни "NO".

        {parser_clarify.get_format_instructions()}

    """

    result = qwen.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=query)
    ])

    parsed = parser_clarify.parse(result.content)
    print(parsed)
    prompt = """
            Ты помощник по вопросам статистики, городов, областей и других субъектов РФ. 
            Пользователь интересуется у тебя вопросом,
            не связанным с твоей доменной областью. Вежливо объясни ему, 
            что ты консультируешь по вопросам муниципальных образований.
                    
        """
    if parsed.message_type == 'NO':
        result = llm.invoke([
            SystemMessage(content=prompt),
            HumanMessage(content=query)
        ])
        print(result.content)
    

    return  {'access':parsed.message_type}


def classify(state: State):
    query = state["messages"][-1]["content"]
    prompt = f"""
        Твоя задача — определить стиль ответа: официальный (formal) или неофициальный (informal).
        Если запрос пользователя носит официальный деловой характер (запрос статистики, аналитика, формальные формулировки), 
        верни "formal". Если запрос скорее непринужденный, разговорный, шуточный или личный — верни "informal".

        {parser_classify.get_format_instructions()}
    """
    result = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=query)
    ])
    parsed = parser_classify.parse(result.content)
    return {"message_type": parsed.message_type}