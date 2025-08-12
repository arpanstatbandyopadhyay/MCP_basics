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
# It runs "uv run calculator_server.py", which should start your MCP FastMCP server
# `env=None` uses the current environment variables
params = StdioServerParameters(
    command="uv", 
    args=["run", "mcp\\calculator_server.py"], 
    env=None
)

# -------------------- List Available Tools from the Calculator Server --------------------

async def list_calculator_tools():
    """
    Connect to the calculator MCP server and retrieve the list of available tools.

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

# -------------------- Invoke a Specific Calculator Tool --------------------

async def call_calculator_tool(tool_name, tool_args):
    """
    Call a specific calculator tool by name with given arguments.

    Args:
        tool_name (str): The name of the tool (e.g., "add", "multiply").
        tool_args (dict): Arguments for the tool.

    Returns:
        The result returned by the tool.
    """
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, tool_args)  # Invoke tool
            return result

# -------------------- Convert Calculator Tools into OpenAI-compatible Tool Wrappers --------------------

async def get_calculator_tools_openai():
    """
    Wrap all available calculator tools as FunctionTool instances
    so they can be used in OpenAI agent/tool interfaces.

    Returns:
        List of FunctionTool objects.
    """
    openai_tools = []

    for tool in await list_calculator_tools():
        # Use the tool's input schema directly, disallowing extra properties
        schema = {
            **tool.inputSchema, 
            "additionalProperties": False
        }

        # Create a FunctionTool that will convert OpenAI-style input to MCP calls
        openai_tool = FunctionTool(
            name=tool.name,                    # Tool name (e.g., "add")
            description=tool.description,      # Tool description from server
            params_json_schema=schema,         # JSON schema for tool inputs
            # Lambda used to actually call the MCP tool when invoked from the agent
            on_invoke_tool=lambda ctx, args, toolname=tool.name: 
                call_calculator_tool(toolname, json.loads(args))
        )

        openai_tools.append(openai_tool)

    return openai_tools
