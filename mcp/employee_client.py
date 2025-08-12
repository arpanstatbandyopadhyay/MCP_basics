# Import the MCP framework
import mcp

# Import the stdio-based client for interacting with MCP servers via subprocess/stdin/stdout
from mcp.client.stdio import stdio_client

# Parameters to define how to launch the calculator server process
from mcp import StdioServerParameters

# FunctionTool is a wrapper class that allows MCP tools to be compatible with OpenAI-style tool use
from agents import FunctionTool

# JSON is used for parsing arguments into proper dictionaries
import json

# -------------------- MCP Server Launch Parameters --------------------

# Define the server process launch configuration
# It runs "uv run employee_server.py", which should start your MCP FastMCP server
# `env=None` uses the current environment variables
params = StdioServerParameters(
    command="uv", 
    args=["run", "mcp\\employee_server.py"], 
    env=None
)

# -------------------- List Available Tools from the employee Server --------------------

async def list_employee_tools():
    """
    Connect to the employee MCP server and retrieve the list of available tools.

    Returns:
        List of Tool objects describing each callable operation.
    """
    # Open connection to subprocess using stdio
    async with stdio_client(params) as streams:
        # Create an MCP client session using those streams
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()              # Initialize handshake with server
            tools_result = await session.list_tools()  # Fetch the available tools
            return tools_result.tools                # Return the list of Tool objects

