from pathlib import Path
from dotenv import load_dotenv
from tavily import TavilyClient
from mcp.server.fastmcp import FastMCP
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / "lca-lc-foundations" / ".env")
tavily_client = TavilyClient()
mcp = FastMCP("mcp_server")

@mcp.tool()
def search_web(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    result = tavily_client.search(query)
    return result

@mcp.prompt()
def prompt():
    """Analayse data from a langchain-ai repo file with comprehensive insights"""
    return """
        You are a helpful assistant that answers user questions about LangChain, LangGraph and LangSmith.
        You can use the following tools/resources to answer user questions:
        -search_web: Search the web for information
        -github_file: Access the Langchain-ai repo files
    
        If the user asks a question that is not related to LangChain, LangGraph and LangSmith, you should say "I'm sorry, i can't answer at you question"
        You may try multiple tool and resource calls to answer the user's question.
        You may also ask clarifying questions to the user to better understand their question."""

if __name__ == "__main__":
    mcp.run(transport="stdio")