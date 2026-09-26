from pathlib import Path
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR.parent / "lca-lc-foundations" / ".env")

client = MultiServerMCPClient(
    {
        "local_server": {
                "transport": "stdio",
                "command": "python",
                "args": [str(BASE_DIR/"2.1_mcp_server.py")],
            }
        "time": {
            "transport" : "stdio",
            "command": "uvx",
            "args": ["mcp-server-time", "--local-timezone=Europe/Paris"]
        }
    }
    
)