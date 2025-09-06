
import os
from dotenv import load_dotenv
from openai import OpenAI
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP(log_level="DEBUG")

@mcp.tool
def read_file(path: str) -> str:
    """Reads the full content of a specified text file."""
    with open(path, 'r') as f:
        return f.read()

@mcp.tool
def summarize_content(content: str) -> str:
    """Takes text content and uses the OpenAI API to return a concise, AI-generated summary."""
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": content},
        ],
    )
    summary = response.choices[0].message.content
    return summary if summary is not None else ""

@mcp.tool
def write_summary(path: str, summary: str) -> str:
    """Writes the final summary string to a new file."""
    with open(path, 'w') as f:
        f.write(summary)
    return f"Summary successfully written to {path}"

if __name__ == "__main__":
    mcp.run(transport="sse")
