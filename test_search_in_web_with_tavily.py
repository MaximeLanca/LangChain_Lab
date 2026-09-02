from dotenv import load_dotenv
from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient

load_dotenv("lca-lc-foundations/.env")
tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict [str, Any]:
    """Search the web for information"""

    return tavily_client.search(query)

result = web_search.invoke("Who is the current mayor of San Francisco?")
print(result)