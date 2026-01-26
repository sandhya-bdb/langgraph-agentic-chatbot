![Python](https://img.shields.io/badge/Python-3.12-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-green)
![LangSmith](https://img.shields.io/badge/LangSmith-Tracing-orange)
![Human-in-the-Loop](https://img.shields.io/badge/HITL-Enabled-purple)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o--mini-black)
![Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue)
![Build Status](https://img.shields.io/badge/Status-Completed-success)

### 🧠 Agentic AI with LangGraph, LangSmith & Human-in-the-Loop

- This project is an end-to-end exploration of agentic AI systems built using LangGraph and LangSmith, focusing not just on functionality, but on observability, debugging, and real-world execution challenges.
- The project progresses step by step—from a simple chatbot to a fully traced, Human-in-the-Loop (HITL) agent—while solving practical issues related to environments, tracing, and infrastructure.
- This repository contains a progressively built AI chatbot system using LangGraph, LangChain, and OpenAI, developed and tested inside GitHub Codespaces using uv for dependency management.

The project demonstrates:

- Tool-augmented agents (mock & real APIs)
- Pydantic-based state management
- LangSmith tracing for observability
- Gradio UI for interactive chatting
- Clean Git & Codespaces workflow

### 🚀 What This Project Demonstrates

This repository shows how to build and debug production-style AI agents, including:

1. State-based agent workflows using LangGraph

2. Tool calling and agent-style decision-making

3. Memory and checkpointing

4. Human-in-the-Loop (interrupt & resume)

5. Full LangSmith tracing (LLM calls, tools, HITL, cost, latency)
   
### 🧩 Project Evolution (Step-by-Step)

The project was intentionally built incrementally:

- Simple Chatbot
- Chatbot with Tools
- Agent-Style Chatbot
- Chatbot with Memory
- LangSmith Tracing
- Human-in-the-Loop (HITL)
- HITL Traced in LangSmith


### 🛠️ Technologies Used

- Python
- LangGraph
- LangChain
- LangSmith
- OpenAI (ChatOpenAI)
- uv (dependency management)
- GitHub Codespaces
  
### 📂 Project Structure
```
.
├── chatbot.ipynb                     # Simple chatbot
├── chatbot_agent_tool.ipynb          # Original agent with tools
├── chatbot_agent_mocktool.ipynb      # Agent with mock stock tool
├── chatbot_agent_tool_real_api.ipynb # Agent with real stock API
├── chatbot_langsmith.ipynb           # LangSmith tracing experiments
├── chatbot_with_memory.ipynb         # Memory-enabled chatbot                          
├── pyproject.toml                    # uv dependency config
├── uv.lock                           # Locked dependencies
├── README.md
└── .gitignore

```
### 🧠 Human-in-the-Loop Example

The HITL agent pauses execution before performing a sensitive action (e.g., buying stocks):

1. AI proposes an action

2. Execution interrupts

3. Human approves or declines

4. Execution resumes safely

This workflow is fully traced in LangSmith, including:

1. Interrupt point

2. Human decision

3. Resume path

4. Final outcome
   
### 🔍 LangSmith Tracing & Debugging

LangSmith was used to trace:

1. LangGraph execution

2. LLM calls

3. Tool usage

4. Human interruptions & resumes

5. Token usage

6. Latency and cost

Key Challenge Faced

1. LangSmith tracing did not work reliably in the local environment due to:

2. DNS-level network blocking on local Wi-Fi

3. Kernel and environment inconsistencies

4. Credential and billing mismatches

#### Solution

👉 Moved execution to GitHub Codespaces

Codespaces provided:

1. A clean, reproducible environment

2. No DNS or firewall restrictions

3. Correct credential loading

4. Immediate and reliable LangSmith tracing

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

- Observability is critical
- Environment and infrastructure matter as much as code
- Human-in-the-Loop workflows require:
- Memory
- Checkpointing
- Careful control flow
- LangSmith makes invisible agent behavior visible
- GitHub Codespaces can solve real-world debugging blockers

### 🚀 Future Improvements

- UI-based Human-in-the-Loop approval
- Multi-agent graphs
- Persistent long-term memory
- Automated evaluations in LangSmith
- API deployment

### 📌 Final Note

This project was as much about debugging and understanding systems as it was about writing code.
It represents a practical, real-world approach to building traceable, controllable, and production-ready AI agents.
Debugging environment and network-level issues

Using GitHub Codespaces to overcome local DNS and tracing problems
### 🧠 Author

Sandhya Banti Dutta Borah
Built as a hands-on LangGraph + Agent Systems learning project.





