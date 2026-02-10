# Auto-generated from chatbot.ipynb.

import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"

from typing import Annotated
from dotenv import load_dotenv
load_dotenv()

from typing_extensions import TypedDict
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)



class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State) -> State:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(State)
builder.add_node("chatbot_node", chatbot)
builder.add_edge(START, "chatbot_node")
builder.add_edge("chatbot_node", END)

graph = builder.compile()

from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))

message = {
    "role": "user",
    "content": "Who walked on the moon for the first time? Print only the name."
}

response = graph.invoke({"messages": [message]})
print(response["messages"][-1].content)

state = None

while True:
    in_message = input("You: ")
    if in_message.lower() in {"quit", "exit"}:
        break

    if state is None:
        state = {
            "messages": [{"role": "user", "content": in_message}]
        }
    else:
        state["messages"].append(
            {"role": "user", "content": in_message}
        )

    state = graph.invoke(state)
    print("Bot:", state["messages"][-1].content)
