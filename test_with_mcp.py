from dotenv import load_dotenv
from tavily import TavilyClient
from typing import Dict, Any
from requests import get

from mcp.server.fastmcp import FastMCP


load_dotenv("lca-lc-foundations/.env")
tavily_client = TavilyClient()
mcp = FastMCP[any]("mcp_server")

# Tool for searching the web
@mcp.tool()
def search_web(query:str) -> Dict[str, Any]:
    """Search the web for information"""

    result = tavily_client.search(query)
    return result

#Resources - provide access to langchain-ai repo file
@mcp.resource("github://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def github_file():
    """Resource for accessing langchain-ai/langchain-mcp-adapters/README.md file"""

    url=f"https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/blob/main/README.md"
    try:
        resp = get(url)
        return resp.text
    except Exception as e:
        return f"Error: {str(e)}"

#Prompt template
@mcp.prompt()
def prompt():
    """Analyse data from a langchain-ai repo file with comprehensive insights"""
    return """
    You are a helpful assistant tha answers user questions about LangChain, LangGraph and LangSmith.
    You can use the following tools/resources to answer user questions:
    -search_web: Search the web for information
    -github_file: Access the Langchain-ai repo files
    
    If the user asks a question that is not related to LangChain, LangGraph and LangSmith, you should say "I'm sorry, i can't answer at you question
    You may try multiple tool and resource calls to answer the user's question.
    You may also ask clarifying questions to the user to better understand their question."""

if __name__ == "__main__":
    mcp.run(transport="stdio")
