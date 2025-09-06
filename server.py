# --- IMPORTS ---
# Import necessary libraries.
import os  # Used to access environment variables like the API key.
from dotenv import load_dotenv  # Used to load environment variables from a .env file.
from openai import OpenAI  # The official OpenAI library for interacting with the API.
from fastmcp import FastMCP  # The library for creating the MCP tool server.

# --- INITIALIZATION ---
# Load environment variables from a .env file into the script's environment.
# This is how the script gets the OPENAI_API_KEY without hardcoding it.
load_dotenv()

# Initialize the FastMCP server instance.
# This 'mcp' object will be used to register our functions as tools.
# log_level="DEBUG" provides detailed output for easier troubleshooting.
mcp = FastMCP(log_level="DEBUG")

# --- TOOL DEFINITIONS ---
# The @mcp.tool decorator is crucial. It tells the FastMCP server
# that this Python function should be exposed as a remote tool that agents can call.

@mcp.tool
def read_file(path: str) -> str:
    """Reads the full content of a specified text file."""
    # This tool uses standard Python I/O to open and read a file.
    # It takes a file path as input and returns the file's content as a string.
    with open(path, 'r') as f:
        return f.read()

@mcp.tool
def summarize_content(content: str) -> str:
    """Takes text content and uses the OpenAI API to return a concise, AI-generated summary."""
    # This tool encapsulates the logic for calling an external AI service.
    # 1. Initialize the OpenAI client, securely getting the API key from the environment.
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # 2. Call the OpenAI Chat Completions API.
    response = client.chat.completions.create(
        model="gpt-4.1-nano",  # Specifies which AI model to use.
        messages=[
            # The system message sets the context for the AI's behavior.
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            # The user message provides the actual content to be summarized.
            {"role": "user", "content": content},
        ],
    )
    
    # 3. Extract the summary text from the API's response structure.
    summary = response.choices[0].message.content
    
    # 4. Return the summary, ensuring it's not None to prevent errors.
    return summary if summary is not None else ""

@mcp.tool
def write_summary(path: str, summary: str) -> str:
    """Writes the final summary string to a new file."""
    # This tool handles writing data to the local file system.
    # It takes a file path and the summary string as input.
    with open(path, 'w') as f:
        f.write(summary)
    # It returns a confirmation message to the agent.
    return f"Summary successfully written to {path}"

# --- SERVER EXECUTION ---
# This standard Python construct ensures the code inside only runs
# when the script is executed directly (e.g., `python server.py`).
if __name__ == "__main__":
    # This command starts the MCP server.
    # It will begin listening for incoming connections from agents.
    # transport="sse" specifies that it should use Server-Sent Events for communication.
    mcp.run(transport="sse")