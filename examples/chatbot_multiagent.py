

import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"

from typing import List, Dict, Optional, Literal
from pydantic import BaseModel, ConfigDict

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain.tools import tool

class State(BaseModel):
    messages: list[dict]
    route: str | None = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

@tool
def get_stock_price(symbol: str) -> float:
    """
    Return the current price of a stock given the stock symbol.
    """
    prices = {
        "AAPL": 100.4,
        "MSFT": 200.3,
        "AMZN": 150.0,
    }
    return prices.get(symbol.upper(), 0.0)

tools = [get_stock_price]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)

def router_agent(state: State):
    user_text = state.messages[-1]["content"].lower()

    if "price" in user_text or "stock" in user_text:
        return {"route": "stock"}
    else:
        return {"route": "knowledge"}

def stock_agent(state: State):
    response = llm_with_tools.invoke(state.messages)

    messages = list(state.messages)

    # Convert AIMessage → dict
    messages.append({
        "role": "assistant",
        "content": response.content or ""
    })

    if response.tool_calls:
        symbol = response.tool_calls[0]["args"]["symbol"]
        price = get_stock_price.invoke({"symbol": symbol})

        messages.append({
            "role": "assistant",
            "content": f"The current price of {symbol} stock is ${price}."
        })

    return {"messages": messages}

def knowledge_agent(state: State) -> dict:
    messages = state.messages

    response = llm.invoke(messages)

    messages.append({
        "role": "assistant",
        "content": response.content
    })

    return {
        "messages": messages
    }

builder = StateGraph(State)

builder.add_node("router", router_agent)
builder.add_node("stock", stock_agent)
builder.add_node("knowledge", knowledge_agent)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    lambda s: s.route,
    {
        "stock": "stock",
        "knowledge": "knowledge",
    }
)

builder.add_conditional_edges("stock", tools_condition)
builder.add_edge("tools", "stock")

builder.add_edge("stock", END)
builder.add_edge("knowledge", END)

graph = builder.compile()

from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))

result = graph.invoke(
    State(messages=[{"role": "user", "content": "What is the price of AAPL stock?"}])
)


for msg in reversed(result["messages"]):
    if msg["role"] == "assistant" and msg["content"]:
        print(msg["content"])
        break

result = graph.invoke(
    State(messages=[
        {"role": "user", "content": "Explain what LangGraph is in simple terms"}
    ])
)

for msg in reversed(result["messages"]):
    if msg["role"] == "assistant" and msg["content"]:
        print(msg["content"])
        break
