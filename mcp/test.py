import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio
from calculator_client import get_calculator_tools_openai, list_calculator_tools

# Load environment variables
load_dotenv(override=True)

instructions = (
    "You are an expert calculator tool. "
    "You can interpret and solve arithmetic expressions accurately. "
    "Use the available tools to perform operations like addition, subtraction, multiplication, division, and exponentiation. "
    "Always return the precise numerical result."
)

request = "Calculate  2+2"
model = "gpt-4o-mini"


async def main():
    # List tools from MCP server
    mcp_tools = await list_calculator_tools()
    print("MCP Tools:", mcp_tools)

    # Get OpenAI-compatible tools
    openai_tools = await get_calculator_tools_openai()
    print("OpenAI Tools:", openai_tools)

    # Run the agent
    with trace("calculator_mcp_client"):
        agent = Agent(name="calculator_manager", instructions=instructions, model=model, tools=openai_tools)
        result = await Runner.run(agent, request)

    # Print output instead of Jupyter display
    print("\nFinal Output:\n", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())