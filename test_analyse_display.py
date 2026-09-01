from dotenv import load_dotenv
from ipywidgets import FileUpload
from IPython.display import display
from langchain.messages import HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
import base64

load_dotenv("lca-lc-foundations/.env")
agent = create_agent("gpt-5", checkpointer=InMemorySaver(),)

def upload_png():
    uploader = FileUpload(accept='.png', multiple=False)
    display(uploader)
    print(uploader.value)
    return uploader

def load_image_b64(path:str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
def ask_agent(image_path:str, question:str="Tell me about this capital"):
    img_b64 = load_image_b64(image_path)

    multimodal_question = HumanMessage(content=[
            {"type": "text", "text": question},
            {"type": "image", "base64": img_b64, "mime_type": "image/png"},
        ])
    response = agent.invoke(
        {"messages" : [multimodal_question]},
        config={"configurable": {"thread_id": "conversation-1"}},)
    
    print(response['messages'][-1].content)

if __name__ == "__main__":
    ask_agent("/Users/maxime/Desktop/img.png")