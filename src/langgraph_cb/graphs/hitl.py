from __future__ import annotations

from typing import Annotated
from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI

from langgraph_cb.config import load_env
from langgraph_cb.tools.stocks import get_stock_price, prepare_buy


class State(TypedDict):
    messages: Annotated[list, add_messages]


def build_graph():
    load_env()

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
        last_message = state["messages"][-1]

        if isinstance(last_message, ToolMessage) and last_message.content.startswith(
            "REQUEST_BUY::"
        ):
            _, symbol, quantity, total_price = last_message.content.split("::")

            decision = interrupt(
                f"Approve buying {quantity} {symbol} stocks for ${float(total_price):.2f}?"
            )

            if decision == "yes":
                return {
                    "messages": [
                        AIMessage(
                            content=(
                                f"Approved: Bought {quantity} shares of {symbol} "
                                f"for ${total_price}"
                            )
                        )
                    ]
                }

            return {"messages": [AIMessage(content="Trade declined by human.")]}

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

    return builder.compile(checkpointer=memory)


def run_demo() -> None:
    graph = build_graph()
    config = {"configurable": {"thread_id": "buy_thread"}}

    graph.invoke(
        {"messages": [HumanMessage(content="What is the current price of 10 MSFT stocks?")]},
        config=config,
    )

    graph.invoke(
        {"messages": [HumanMessage(content="Buy 10 MSFT stocks at current price.")]},
        config=config,
    )

    decision = input("Approve (yes/no): ").strip().lower()
    state = graph.invoke(Command(resume=decision), config=config)

    print(state["messages"][-1].content)
