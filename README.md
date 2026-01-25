![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-green)
![LangSmith](https://img.shields.io/badge/LangSmith-Tracing-orange)
![Human-in-the-Loop](https://img.shields.io/badge/HITL-Enabled-purple)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o--mini-black)
![Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue)
![Build Status](https://img.shields.io/badge/Status-Completed-success)

### 🧠 Agentic AI with LangGraph, LangSmith & Human-in-the-Loop

This project is an end-to-end exploration of agentic AI systems built using LangGraph and LangSmith, focusing not just on functionality, but on observability, debugging, and real-world execution challenges.

The project progresses step by step—from a simple chatbot to a fully traced, Human-in-the-Loop (HITL) agent—while solving practical issues related to environments, tracing, and infrastructure.

### 🚀 What This Project Demonstrates

This repository shows how to build and debug production-style AI agents, including:

State-based agent workflows using LangGraph

Tool calling and agent-style decision-making

Memory and checkpointing

Human-in-the-Loop (interrupt & resume)

Full LangSmith tracing (LLM calls, tools, HITL, cost, latency)
### 🧩 Project Evolution (Step-by-Step)

The project was intentionally built incrementally:

Simple Chatbot

Basic LangGraph setup

State, nodes, and edges

Chatbot with Tools

Tool definitions

Conditional routing based on tool usage

Agent-Style Chatbot

Model decides when to call tools

ToolNode + tools_condition

Chatbot with Memory

Persistent state using checkpoints

Thread-based execution

LangSmith Tracing

Observing graph execution

Tool calls, tokens, latency, and cost

Human-in-the-Loop (HITL)

Interrupting execution for human approval

Resuming execution safely

HITL Traced in LangSmith

Full visibility into pauses, resumes, and decisions

### 🛠️ Technologies Used

Python

LangGraph

LangChain

LangSmith

OpenAI (ChatOpenAI)

uv (dependency management)

GitHub Codespaces
### 📂 Project Structure
```
├── basic_chatbot.ipynb
├── chatbot_with_tools.ipynb
├── agent_chatbot.ipynb
├── chatbot_with_memory.ipynb
├── langsmith_tracing.ipynb
├── chatbot_hitl.py
├── pyproject.toml
├── uv.lock
└── README.md
```
### 🧠 Human-in-the-Loop Example

The HITL agent pauses execution before performing a sensitive action (e.g., buying stocks):

AI proposes an action

Execution interrupts

Human approves or declines

Execution resumes safely

This workflow is fully traced in LangSmith, including:

Interrupt point

Human decision

Resume path

Final outcome
### 🔍 LangSmith Tracing & Debugging

LangSmith was used to trace:

LangGraph execution

LLM calls

Tool usage

Human interruptions & resumes

Token usage

Latency and cost

Key Challenge Faced

LangSmith tracing did not work reliably in the local environment due to:

DNS-level network blocking on local Wi-Fi

Kernel and environment inconsistencies

Credential and billing mismatches

Solution

👉 Moved execution to GitHub Codespaces

Codespaces provided:

A clean, reproducible environment

No DNS or firewall restrictions

Correct credential loading

Immediate and reliable LangSmith tracing

This was a major learning outcome of the project.

### ▶️ How to Run the Project
#### Option 1: GitHub Codespaces (Recommended)

Open the repository in GitHub Codespaces

Sync dependencies:
```
uv sync
```
Run the HITL agent:
```
python chatbot_hitl.py
```
Follow the approval prompt in the terminal

View traces in LangSmith → Tracing
#### Option 2: Local Setup

Create a .env file:
```
OPENAI_API_KEY=your_openai_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=langgraph_cb
```

Sync dependencies:
```
uv sync
```

Run:
```
python chatbot_hitl.py
```

Note: Local LangSmith tracing may fail due to network or DNS restrictions.
### 📘 Key Learnings

Agentic AI is not just about prompts or logic

Observability is critical

Environment and infrastructure matter as much as code

Human-in-the-Loop workflows require:

Memory

Checkpointing

Careful control flow

LangSmith makes invisible agent behavior visible

GitHub Codespaces can solve real-world debugging blockers

### 🚀 Future Improvements

UI-based Human-in-the-Loop approval

Multi-agent graphs

Persistent long-term memory

Automated evaluations in LangSmith

API deployment

### 📌 Final Note

This project was as much about debugging and understanding systems as it was about writing code.
It represents a practical, real-world approach to building traceable, controllable, and production-ready AI agents.
Debugging environment and network-level issues

Using GitHub Codespaces to overcome local DNS and tracing problems

