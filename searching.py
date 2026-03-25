import json
import os
import httpx
from ddgs import DDGS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "fetch_page",
            "description": "Fetches the content of a web page",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "URL of the page to fetch"}
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Searches the web for a query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "search query string"}
                },
                "required": ["query"]
            }
        }
    }
]

def search_web(query: str) -> list:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
    return results

def fetch_page(url: str) -> str:
    return httpx.get(url).text[:3000]

tool_map = {
    "search_web": search_web,
    "fetch_page": fetch_page,
}

def research_agent(topic: str):
    messages = [
        {
            "role": "system",
            "content": "You are a research assistant. You have two tools: search_web to search the internet, and fetch_page to read a webpage. Always use search_web first, then fetch_page to read results. Never use any other tools."
        },
        {
            "role": "user", 
            "content": f"Research this topic and give me a top 10 list: {topic}"
        }
    ]
    while True:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":
            tool_call = message.tool_calls[0]
            print(f"🔧 Agent calling: {tool_call.function.name}({tool_call.function.arguments})")
            args = json.loads(tool_call.function.arguments)
            result = tool_map[tool_call.function.name](**args)

            messages.append(message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })
        else:
            return message.content

if __name__ == "__main__":
    print(research_agent("Dostoevsky best books"))