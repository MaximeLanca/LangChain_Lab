from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.messages import HumanMessage

load_dotenv("lca-lc-foundations/.env")

agent = create_agent(model = "gpt-5-nano")
question = HumanMessage(content =  "What is the capital of France ?")
response = agent.invoke(
    {"messages": [question]}
)

print(response['messages'][-1].content)