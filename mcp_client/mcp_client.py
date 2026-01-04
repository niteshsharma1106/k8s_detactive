import asyncio
from typing import Dict, Any

# Correct imports for the current MCP SDK
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPTools:
    """
    Synchronous wrapper around async MCP ClientSession.
    """
    def __init__(self, server_params: StdioServerParameters):
        self.server_params = server_params

    async def _call_async(self, tool_name: str, args: Dict[str, Any]):
        # Spawns the server as a subprocess
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                # call_tool returns a CallToolResult
                result = await session.call_tool(tool_name, args)
                
                # result.content is a list of content blocks (TextContent, etc.)
                # We extract the text from the first block
                if result.content and hasattr(result.content[0], 'text'):
                    return result.content[0].text
                return result.content

    def _call(self, tool_name: str, args: Dict[str, Any]):
        return asyncio.run(self._call_async(tool_name, args))

    # ===== Explicit tool methods =====

    def get_pod(self, cluster: str, namespace: str, pod: str):
        return self._call("get_pod", {"cluster": cluster, "namespace": namespace, "pod": pod})

    def get_events(self, cluster: str, namespace: str):
        return self._call("get_events", {"cluster": cluster, "namespace": namespace})

    def get_scc_for_pod(self, cluster: str, namespace: str, pod: str):
        return self._call("get_scc_for_pod", {"cluster": cluster, "namespace": namespace, "pod": pod})

def get_tools():
    """
    Factory returning MCPTools using stdio transport.
    Make sure the path to server.py is correct relative to where you run the script.
    """
    params = StdioServerParameters(
        command="python",
        args=["mcp_server/server.py"] 
    )
    return MCPTools(params)