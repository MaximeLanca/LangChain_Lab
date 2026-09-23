"""
Serveur MCP local exposant :
  - un tool `search_web` (recherche web via Tavily)
  - une resource `github_file` (lecture d'un fichier distant sur GitHub)
  - un prompt `prompt` (system prompt de l'agent)

Ce fichier tourne comme un PROCESS SÉPARÉ : c'est lui que
`MultiServerMCPClient` lance en sous-processus (transport "stdio")
depuis le script client (voir client_agent.py).
Il ne doit PAS être importé ni exécuté depuis le notebook/le client :
il est lancé automatiquement par la lib au moment du `get_tools()`.
"""

from pathlib import Path
from typing import Dict, Any

from dotenv import load_dotenv
from requests import get
from tavily import TavilyClient

from mcp.server.fastmcp import FastMCP


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / "lca-lc-foundations" / ".env")

tavily_client = TavilyClient()
mcp = FastMCP("mcp_server")


@mcp.tool()
def search_web(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    result = tavily_client.search(query)
    return result


@mcp.resource("github://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def github_file():
    """Resource for accessing langchain-ai/langchain-mcp-adapters/README.md file"""
    url = "https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/main/README.md"
    try:
        resp = get(url)
        return resp.text
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.prompt()
def prompt():
    """Analyse data from a langchain-ai repo file with comprehensive insights"""
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