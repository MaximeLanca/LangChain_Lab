# utils.py
from pathlib import Path
from dotenv import load_dotenv
from langchain.messages import HumanMessage


def load_env(env_folder: str = "lca-lc-foundations") -> bool:
    env_path = Path(__file__).parent / env_folder / ".env"
    loaded = load_dotenv(env_path)
    if not loaded:
        print(f"⚠️  Aucun .env trouvé à : {env_path}")
    return loaded


def ask_agent(agent, question: str) -> str:
    response = agent.invoke({"messages": [HumanMessage(content=question)]})
    answer = response["messages"][-1].content
    print(answer)
    return answer