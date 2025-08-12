# Import the FastMCP server framework
from mcp.server.fastmcp import FastMCP

# Import the Calculator class that provides arithmetic methods
from calculator import Calculator

# Initialize an MCP server instance with the identifier "calculator_server"
# This name is used to identify the toolset when consumed by agentic frameworks
mcp = FastMCP("calculator_server")

# ---------------------- TOOL DEFINITIONS ----------------------

@mcp.tool()
async def add(a: float, b: float) -> float:
    """
    Asynchronous MCP tool that adds two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The sum of a and b.
    """
    return Calculator().add(a, b)

@mcp.tool()
async def subtract(a: float, b: float) -> float:
    """
    Asynchronous MCP tool that subtracts the second number from the first.

    Args:
        a (float): The number to subtract from.
        b (float): The number to subtract.

    Returns:
        float: The result of a - b.
    """
    return Calculator().subtract(a, b)

@mcp.tool()
async def multiply(a: float, b: float) -> float:
    """
    Asynchronous MCP tool that multiplies two numbers.

    Args:
        a (float): The first number.
        b (float): The second number.

    Returns:
        float: The product of a and b.
    """
    return Calculator().multiply(a, b)

@mcp.tool()
async def divide(a: float, b: float) -> float:
    """
    Asynchronous MCP tool that divides the first number by the second.

    Args:
        a (float): The numerator.
        b (float): The denominator.

    Returns:
        float: The result of a / b.

    Raises:
        ValueError: If b is zero (handled inside Calculator).
    """
    return Calculator().divide(a, b)

@mcp.tool()
async def power(a: float, b: float) -> float:
    """
    Asynchronous MCP tool that raises a to the power of b.

    Args:
        a (float): The base.
        b (float): The exponent.

    Returns:
        float: The result of a ** b.
    """
    return Calculator().power(a, b)


#In MCP (Model Context Protocol), a resource is a piece of data that the client can request directly via a URI-like address.
# If a client requests calculator://square/3, it will call your function with number=9.0. Tool call not required
@mcp.resource("calculator://square/{number}")
async def get_square(number: float) -> float:
    """
    Example MCP resource that calculates the square of a number.
    Clients can fetch this by requesting:
    calculator://square/5
    """
    return number * number

# ---------------------- SERVER ENTRY POINT ----------------------

if __name__ == "__main__":
    # Start the MCP server using default transport ('stdio')
    mcp.run()
