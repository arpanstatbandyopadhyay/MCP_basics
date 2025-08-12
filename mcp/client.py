# ---------------------- IMPORTS ----------------------

import asyncio  # Built-in Python library for writing concurrent code using async/await syntax.
                # It allows asynchronous execution of I/O-bound tasks without blocking.

from dotenv import load_dotenv  # Loads environment variables from a .env file into os.environ.
from langchain_openai import ChatOpenAI  # LangChain wrapper for OpenAI chat models.

from mcp_use import MCPAgent, MCPClient  # Custom classes for working with MCP servers and agents.
import os  # Standard library for interacting with environment variables, file paths, etc.

# ---------------------- MAIN ASYNC FUNCTION ----------------------

async def calculator_chat():
    """
    Run an interactive chat session with an MCP agent that has built-in conversation memory.
    The conversation memory lets the agent remember previous interactions within the same session.
    """
    
    # Load environment variables from .env (API keys, config values, etc.)
    load_dotenv(override=True)
    
    # Explicitly set the OpenAI API key in the environment
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    # Path to the MCP client configuration file (points to your MCP server setup)
    config_file = "mcp/calculator_server.json"

    print("Initializing chat...")

    # Create an MCP client from the config file
    client = MCPClient.from_config_file(config_file)

    # Create the LLM (Large Language Model) interface
    # Here, we’re using OpenAI's GPT-4o-mini through LangChain
    llm = ChatOpenAI(model="gpt-4o-mini")

    # Create the MCP agent with memory enabled
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,          # Maximum steps for tool calls per request
        memory_enabled=True,   # Enables built-in conversation memory tracking
    )

    # Chat instructions for the user
    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")

    try:
        # ---------------------- MAIN CHAT LOOP ----------------------
        while True:
            # Get user input from the console
            user_input = input("\nYou: ")

            # Handle exit commands
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Handle clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Display assistant's response without line break
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the given user input.
                # Memory is automatically updated between turns.
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Ensure MCP client sessions are closed to avoid dangling connections
        if client and client.sessions:
            await client.close_all_sessions()

# ---------------------- SCRIPT ENTRY POINT ----------------------

if __name__ == "__main__":
    # asyncio.run() is used to execute the async function run_memory_chat()
    asyncio.run(calculator_chat())
