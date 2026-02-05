![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-green)
![LangSmith](https://img.shields.io/badge/LangSmith-Tracing-orange)
![Human-in-the-Loop](https://img.shields.io/badge/HITL-Enabled-purple)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o--mini-black)
![Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue)
![Build Status](https://img.shields.io/badge/Status-Completed-success)

# AI Chatbot System using LangGraph, LangChain, and OpenAI

This project is an end-to-end exploration of **agentic AI systems** built using LangGraph and LangChain, with a strong emphasis on **observability, debugging, and real-world execution challenges** rather than just happy-path demos.

The repository progresses step by step — from a simple chatbot to **tool-augmented, memory-enabled, and Human-in-the-Loop (HITL) agents** — while addressing practical issues related to **environment management, tracing, persistence, and infrastructure**.

All experiments were developed and tested locally and in **GitHub Codespaces**, using **uv** for dependency and Python version management.

---

## 🚀 What This Project Demonstrates

This repository shows how to design, debug, and scale **production-style AI agents**, including:

- **State-based agent workflows** using LangGraph  
- **Tool calling and agent-style decision-making** (mock & real APIs)  
- **Persistent memory and checkpointing using SQLite** (thread-based conversations)  
- **Human-in-the-Loop (HITL)** execution with interrupt & resume  
- **LangSmith tracing** for full observability (LLM calls, tools, latency, cost)  
- **Clean Git + Codespaces workflow**, including environment pinning and reproducibility

## 🧩 Project Evolution (Step-by-Step)

The project was intentionally built incrementally:

1. Simple chatbot  
2. Chatbot with tools  
3. Agent-style chatbot (tool routing & decision-making)  
4. Chatbot with **persistent memory (SQLite + thread-based checkpoints)**  
5. LangSmith tracing & observability  
6. Human-in-the-Loop (HITL) workflows  
7. HITL fully traced in LangSmith  

---

## 🛠️ Technologies Used

- Python  
- LangGraph  
- LangChain  
- LangSmith  
- OpenAI (ChatOpenAI)  
- SQLite (persistent memory & checkpoints)  
- uv (dependency & Python version management)  
- GitHub Codespaces  

   

### 📂 Project Structure
```
.
├── chatbot.ipynb                     # Simple chatbot
├── chatbot_agent_tool.ipynb          # Original agent with tools
├── chatbot_agent_mocktool.ipynb      # Agent with mock stock tool
├── chatbot_agent_tool_real_api.ipynb # Agent with real stock API
├── chatbot_langsmith.ipynb           # LangSmith tracing experiments
├── chatbot_with_memory.ipynb         # LangGraph chatbot with persistent SQLite memory (thread-based)                         
├── pyproject.toml                    # uv dependency config
├── uv.lock                           # Locked dependencies
├── README.md
└── .gitignore

```
###  Human-in-the-Loop Example

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

##  Persistent Memory with SQLite (LangGraph)

The chatbot now supports **persistent conversational memory** using **LangGraph’s SQLite checkpointer**.

- Memory is stored in a local SQLite database (`memory.db`)
- Conversations are isolated using `thread_id`
- Memory persists across multiple invocations and sessions
- Database files are intentionally excluded from version control via `.gitignore`

This enables realistic multi-turn conversations while keeping the repository clean and production-ready.


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
###  Author

Sandhya Banti Dutta Borah
Built as a hands-on LangGraph + Agent Systems learning project.












