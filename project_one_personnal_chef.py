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
from typing import Optional

load_dotenv("lca-lc-foundations/.env")
tavily_client = TavilyClient()

def upload_png():
    uploader = FileUpload(accept='.png', multiple=False)
    display(uploader)
    print(uploader.value)
    return uploader

def load_image_b64(path:str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
@tool
def web_search(query:str)-> Dict [str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

agent = create_agent(model = "gpt-5-nano", tools=[web_search], checkpointer=InMemorySaver(),)

def ask_agent(image_path: Optional[str]=None, question:str="Tell me about this capital"):

    content = [{"type":"text", "text":question}]

    if image_path:
        img_b64 = load_image_b64(image_path)
        content.append({"type":"image", "base64":img_b64, "mime_type":"image/png"})

    message = HumanMessage(content=content)
    response = agent.invoke(
        {"messages" : [message]},
        config={"configurable": {"thread_id": "conversation-1"}},)
    
    print(response['messages'][-1].content)

if __name__ == "__main__":
    ask_agent("/Users/maxime/Desktop/img.png")