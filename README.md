# Web Research Agent

An AI agent that researches any topic on the web and returns a top 10 list.

## How it works

1. You give it a topic
2. Agent searches the web using DuckDuckGo
3. Agent reads the most relevant pages
4. LLM synthesizes everything into a top 10 list

The agent decides on its own which pages to search and read — 
no hardcoded steps.

## Tech Stack

- Python
- Groq API (LLaMA 3.3 70B)
- DuckDuckGo Search (ddgs)
- httpx
- OpenAI-compatible client

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv .venv`
3. Activate: `source .venv/bin/activate`
4. Install dependencies: `pip install openai httpx ddgs python-dotenv`
5. Create `.env` file: `GROQ_API_KEY=your-key-here`
6. Run: `python searching.py`

## Example

Input:
    "top AI agent frameworks in Python"

Output:
    1. LangChain — most popular framework for building LLM apps
    2. CrewAI — multi-agent orchestration
    3. AutoGen — Microsoft's agent framework
    ...

## What I learned

- Multi-step agent reasoning (ReAct loop)
- Dynamic tool routing with tool_map
- Web search + page fetching as agent tools
- How agents use message history as memory
