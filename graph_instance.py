#graph_instance.py
from graph import build_graph
from llm import get_llm
from mcp_client.mcp_client import get_tools

# Create singletons ONCE
_llm = get_llm()
_tools = get_tools()

graph = build_graph(_llm, _tools)
