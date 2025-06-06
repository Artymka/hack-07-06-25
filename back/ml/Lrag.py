import sys
from pathlib import Path 
sys.path.append(str(Path(__file__).parent.parent))  

from main import *
from agents.RAG import *

wikipedia_retriever = WikipediaRetriever(
        lang="ru", 
        top_k_results=4
    )


def rag_agent(state: State):
    
    query = state['messages'][-1]['content']
    
    context = rag_sys(query)
    
    prompt = f"""
    Ты — ассистент по вопросам муниципалитетов России и статистики. 
    Ответь на вопрос пользователя, основываясь только на контексте ниже.
    Если исходя из на вопрос ответить невозможно, ответь "данные отсутствуют"
    
    Контекст: {context}

    """

    result = llm.invoke([
        SystemMessage(content=prompt),
        HumanMessage(content=query)
    ])

    return {'web_search_context':result.content}







