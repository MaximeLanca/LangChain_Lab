from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage
from langchain.agents import create_agent

load_dotenv("lca-lc-foundations/.env")
agent = create_agent("gpt-5", checkpointer=InMemorySaver(),)

question = HumanMessage(content="Hello my name is Sean and my favorite coulour is green")
config = {"configurable" : {"thread_id" : "1"}}

response = agent.invoke({"messages" : [question]}, config,)

print(response)