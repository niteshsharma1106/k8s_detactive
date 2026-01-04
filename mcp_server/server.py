# mcp_server/server.py
import logging
import sys
from mcp.server.fastmcp import FastMCP

from tools.k8s_pods import get_pod, get_pod_logs
from tools.k8s_events import get_events
from tools.k8s_nodes import get_node
from tools.k8s_scc import get_scc_for_pod

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr
)
logger = logging.getLogger("mcp-server")

mcp = FastMCP("k8s-openshift-investigation")

for tool in [get_pod, get_pod_logs, get_events, get_node, get_scc_for_pod]:
    logger.info(f"Registering tool: {tool.__name__}")
    mcp.add_tool(tool)

if __name__ == "__main__":
    logger.info("Starting MCP Server (stdio mode)")
    mcp.run()   # ← stdio ONLY
