from dotenv import load_dotenv
load_dotenv()

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)


class State(TypedDict):
    messages: Annotated[list, add_messages]



@tool
def get_stock_price(symbol: str) -> float:
    """Return the current price of a stock."""
    prices = {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 87.6,
    }
    return prices.get(symbol, 0.0)


@tool
def prepare_buy(symbol: str, quantity: int, total_price: float) -> str:
    """
    Prepare a buy request.
    Human approval will be handled by a graph node.
    """
    return f"REQUEST_BUY::{symbol}::{quantity}::{total_price}"


tools = [get_stock_price, prepare_buy]


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)


def chatbot_node(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def approval_node(state: State):
    """
    Human-in-the-loop approval node.
    Interrupts are ONLY allowed here.
    """
    last_message = state["messages"][-1]

    if isinstance(last_message, ToolMessage) and last_message.content.startswith("REQUEST_BUY::"):
        _, symbol, quantity, total_price = last_message.content.split("::")

        decision = interrupt(
            f"Approve buying {quantity} {symbol} stocks for ${float(total_price):.2f}?"
        )

        if decision == "yes":
            return {
                "messages": [
                    AIMessage(
                        content=f"✅ Approved: Bought {quantity} shares of {symbol} for ${total_price}"
                    )
                ]
            }
        else:
            return {
                "messages": [
                    AIMessage(content="❌ Trade declined by human.")
                ]
            }

    return {}



memory = MemorySaver()
builder = StateGraph(State)

builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", ToolNode(tools))
builder.add_node("approval", approval_node)

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "approval")
builder.add_edge("approval", END)

graph = builder.compile(checkpointer=memory)


config = {"configurable": {"thread_id": "buy_thread"}}

# Step 1: Ask price
graph.invoke(
    {
        "messages": [
            HumanMessage(content="What is the current price of 10 MSFT stocks?")
        ]
    },
    config=config,
)

# Step 2: Ask to buy (will pause for HITL)
state = graph.invoke(
    {
        "messages": [
            HumanMessage(content="Buy 10 MSFT stocks at current price.")
        ]
    },
    config=config,
)

# Resume after interrupt
decision = input("Approve (yes/no): ").strip().lower()
state = graph.invoke(Command(resume=decision), config=config)

print(state["messages"][-1].content)

@tool
def get_stock_price(symbol: str) -> float:
    """Return the current price of a stock given the stock symbol"""
    return {
        "MSFT": 200.3,
        "AAPL": 100.4,
        "AMZN": 150.0,
        "RIL": 87.6
    }.get(symbol, 0.0)


@tool
def buy_stocks(symbol: str, quantity: int, total_price: float) -> str:
    """Buy stocks given the stock symbol and quantity"""
    decision = interrupt(
        f"Approve buying {quantity} {symbol} stocks for ${total_price:.2f}?"
    )

    if decision == "yes":
        return f"You bought {quantity} shares of {symbol} for a total price of ${total_price:.2f}"
    else:
        return "Buying declined."


tools = [get_stock_price, buy_stocks]



llm = ChatOpenAI(
    model="gpt-4o-mini",   
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)



def chatbot_node(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}



memory = MemorySaver()

builder = StateGraph(State)

builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", tools_condition)
builder.add_edge("tools", "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile(checkpointer=memory)



config = {"configurable": {"thread_id": "buy_thread"}}

# Step 1: ask price
state = graph.invoke(
    {"messages": [{"role": "user", "content": "What is the current price of 10 MSFT stocks?"}]},
    config=config
)
print(state["messages"][-1].content)


# Step 2: ask to buy
state = graph.invoke(
    {"messages": [{"role": "user", "content": "Buy 10 MSFT stocks at current price."}]},
    config=config
)

# HITL interrupt
print(state.get("__interrupt__"))

decision = input("Approve (yes/no): ")

# Resume execution
state = graph.invoke(Command(resume=decision), config=config)
print(state["messages"][-1].content)

