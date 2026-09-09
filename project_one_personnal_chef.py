from dotenv import load_dotenv
from langchain.tools import tool
from typing import Dict, Any
from tavily import TavilyClient
from ipywidgets import FileUpload
from IPython.display import display
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import base64

load_dotenv("lca-lc-foundations/.env")
tavily_client = TavilyClient()

@tool
def web_search(query:str)-> Dict [str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

agent = create_agent(model = "gpt-5-nano", tools=[web_search])
question = HumanMessage(content = "What is a banana?")
response = agent.invoke({"messages":[question]})
print(response['messages'][-1].content)