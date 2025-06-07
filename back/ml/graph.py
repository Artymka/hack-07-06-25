
from ml.main import *
from ml.agents.start import *
from ml.agents.RAG import * 
from ml.agents.nl2sql import * 
from ml.agents.responder import * 

state: State = {
    "messages": [],
    "message_type": None,
    "access": "NO",
    "web_search_context": None,
    "nl2sql_context": None
}

def startup():
    graph_builder = StateGraph(State)

    graph_builder.add_node("clarify", clarify)
    graph_builder.add_node("classifier", classify)
    graph_builder.add_node("rag_agent", rag_agent)
    graph_builder.add_node("nl2sql_agent", nl2sql_agent)
    graph_builder.add_node("responder", responder)
    graph_builder.add_edge(START, "clarify")
    graph_builder.add_conditional_edges(
        "clarify",
        lambda state: state.get("access"),
        {"YES": "classifier", "NO": "clarify"}
    )
    graph_builder.add_edge("classifier", "rag_agent")
    graph_builder.add_edge("classifier", "nl2sql_agent")
    graph_builder.add_edge("rag_agent", "responder")
    graph_builder.add_edge("nl2sql_agent", "responder")
    graph_builder.add_edge("responder", END)

    graph = graph_builder.compile()
    return graph

def quest_model(user_input: str, state, graph):
    if user_input.strip().lower() == "стоп":
            return "Assistant: Досвидания!"
        
    state["messages"].append({"role": "user", "content": user_input})

    state = graph.invoke(state)

    if state.get("messages"):
        last = state["messages"][-1]
        if last["role"] == "assistant":
            # print("Assistant:", last["content"])
            return last["content"]

'''
def run():
    

    while True:
        user_input = input("User: ")

        if user_input.strip().lower() == "стоп":
            return "Assistant: Досвидания!"
        
        state["messages"].append({"role": "user", "content": user_input})

        state = graph.invoke(state)

        if state.get("messages"):
            last = state["messages"][-1]
            if last["role"] == "assistant":
                print("Assistant:", last["content"])


if __name__ == "__main__":
    run()
'''