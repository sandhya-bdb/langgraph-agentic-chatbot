# Auto-generated from chatbot_agent_mocktool.ipynb.

import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"

from typing import List
from pydantic import BaseModel, ConfigDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_openai import ChatOpenAI
from langchain.tools import tool

from dotenv import load_dotenv
load_dotenv()

from typing import List, Annotated
from pydantic import BaseModel, ConfigDict
from langgraph.graph.message import add_messages

class State(BaseModel):
    messages: Annotated[List, add_messages]

    model_config = ConfigDict(arbitrary_types_allowed=True)

@tool
def get_stock_price(symbol: str) -> float:
    """
    Return the current price of a stock given the stock symbol.
    """
    return {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 87.6
    }.get(symbol.upper(), 0.0)


tools = [get_stock_price]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    response = llm_with_tools.invoke(state.messages)
    return {"messages": [response]}

builder = StateGraph(State)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")

graph = builder.compile()


from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))

state = graph.invoke(
    {
        "messages": [
            {"role": "user", "content": "What is the price of AAPL stock right now?"}
        ]
    }
)

print(state["messages"][-1].content)

state = graph.invoke(
    {
        "messages": [
            {"role": "user", "content": "Who invented theory of relativity? Print person name only"}
        ]
    }
)

print(state["messages"][-1].content)
