

import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"

from typing import List
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

from typing import Annotated, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, ConfigDict

class State(BaseModel):
    messages: Annotated[List[BaseMessage], add_messages]

    model_config = ConfigDict(arbitrary_types_allowed=True)

from langchain.tools import tool
import os, requests

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

@tool
def get_stock_price(symbol: str) -> float:
    """Get the latest stock price for a symbol."""
    if not ALPHAVANTAGE_API_KEY:
        raise ValueError("Alpha Vantage API key not set")

    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": ALPHAVANTAGE_API_KEY,
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    quote = data.get("Global Quote", {})
    price = quote.get("05. price")

    if not price:
        raise ValueError(f"No price found for {symbol}")

    return float(price)

def chatbot(state: State):
    response = llm_with_tools.invoke(state.messages)
    return {"messages": [response]}

tools = [get_stock_price]

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)

builder = StateGraph(State)

builder.add_node("chatbot", chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")

graph = builder.compile()

from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))

state = graph.invoke({
    "messages": [
        {"role": "user", "content": "What is the price of AAPL stock right now?"}
    ]
})

print(state["messages"][-1].content)

from langsmith import traceable

@traceable(name="agent_tools_run")
def run_agent(user_input: str):
    return graph.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

state = graph.invoke({"messages": [{"role": "user", "content": "What is the price of MSFT stock right now?"}]})
print(state["messages"][-1].content)

from pprint import pprint

state = graph.invoke({
    "messages": [{"role": "user", "content": "What is the price of AAPL stock right now?"}]
})

pprint(state)

state = graph.invoke({"messages": [{"role": "user", "content": "Who invented theory of relativity? print person name only"}]})
print(state["messages"][-1].content)



state = graph.invoke({
    "messages": [{"role": "user", "content": "Who invented theory of relativity? print person name only?"}]
})

pprint(state)
