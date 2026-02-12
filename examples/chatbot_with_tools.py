

import os

os.environ["LANGCHAIN_TRACING_V2"] = "false"

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain.tools import tool

from dotenv import load_dotenv
load_dotenv()

class State(TypedDict):
   
    messages: Annotated[list, add_messages]

@tool
def get_stock_price(symbol: str) -> float:
    '''Return the current price of a stock given the stock symbol
    :param symbol: stock symbol
    :return: current price of the stock
    '''
    return {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 87.6
    }.get(symbol, 0.0)

tools = [get_stock_price]


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State) -> State:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}



builder = StateGraph(State)

builder.add_node(chatbot)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)

graph = builder.compile()

from IPython.display import Image, display

display(Image(graph.get_graph().draw_mermaid_png()))

state = graph.invoke({"messages": [{"role": "user", "content": "What is the price of AAPL stock right now?"}]})
print(state["messages"][-1].content)

from pprint import pprint

state = graph.invoke({
    "messages": [{"role": "user", "content": "What is the price of AAPL stock right now?"}]
})

pprint(state)

state = graph.invoke({"messages": [{"role": "user", "content": "Who invented theory of relativity? print person name only"}]})
print(state["messages"][-1].content)

from pprint import pprint

state = graph.invoke({
    "messages": [{"role": "user", "content": "Who invented theory of relativity? print person name only?"}]
})

pprint(state)

msg = "I want to buy 20 AMZN stocks using current price. Then 15 MSFT. What will be the total cost?"

state = graph.invoke({"messages": [{"role": "user", "content": msg}]})
print(state["messages"][-1].content)

from pprint import pprint

state = graph.invoke({
    "messages": [{"role": "user", "content": "I want to buy 20 AMZN stocks using current price. Then 15 MSFT. What will be the total cost?"}]
})

pprint(state)
