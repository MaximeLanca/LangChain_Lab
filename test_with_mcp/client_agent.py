"""
Script client : lance un agent LangChain qui utilise les tools/resources/prompt
exposés par le serveur MCP local (resource/2.1_mcp_server.py).
"""

import asyncio
from pprint import pprint
from pathlib import Path

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.messages import HumanMessage


BASE_DIR = Path(__file__).resolve().parent


load_dotenv(BASE_DIR.parent / "lca-lc-foundations" / ".env")

client = MultiServerMCPClient(
    {
        "local_server": {
            "transport": "stdio",
            "command": "python",
            "args": [str(BASE_DIR/"2.1_mcp_server.py")],
        }
    }
)
""" 
For example
    client = MultiServerMCPClient(
    {
        "time": {
            "transport": "stdio",
            "command": "uvx",
            "args": ["mcp-server-time", "--local-timezone=Europe/Paris"],
        },
        "fetch": {
            "transport": "stdio",
            "command": "uvx",
            "args": ["mcp-server-fetch"],
        },
        "filesystem": {
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "/chemin/autorise"],
        },
        "mon_api": {
            "transport": "streamable_http",   # serveur distant, pas de command/args
            "url": "http://localhost:8000/mcp",
        },
    }
) """


async def main() -> None:
    # 1. Récupère les tools exposés par le serveur MCP local
    tools = await client.get_tools()

    # 2. Récupère les resources exposées par ce même serveur
    resources = await client.get_resources("local_server")

    # 3. Récupère le prompt nommé "prompt" et prend son contenu texte
    prompt_messages = await client.get_prompt("local_server", "prompt")
    system_prompt = prompt_messages[0].content

    # 4. Construit l'agent avec les tools récupérés + le system prompt
    agent = create_agent(
        model="gpt-5-nano",
        tools=tools,
        system_prompt=system_prompt,
    )

    # 5. Invoque l'agent
    config = {"configurable": {"thread_id": "1"}}
    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="Tell me about the langchain-mcp-adapters library")]},
        config=config,
    )

    pprint(response)


if __name__ == "__main__":
    asyncio.run(main())