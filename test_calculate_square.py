from dotenv import load_dotenv
from langchain.tools import tool
load_dotenv("lca-lc-foundations/.env")

@tool
def square_root(x:float) -> float:
    """Calculate the square root of a number"""
    return x ** 0.5

@tool("square_root")
def tool1 (x:float) -> float:
    """Calculate the square root of a number"""
    return x ** 0.5

print(square_root.name)
print(square_root.invoke({"x": 16}))