import asyncio
import sys

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

async def main():
    """Connects to the server, runs the file analysis, and prints the result."""
    server_url = "http://localhost:8000/sse"
    print(f"--- MCP Agent ---")
    print(f"Connecting to server at {server_url}...")

    try:
        # Connect to the server's SSE endpoint.
        async with sse_client(url=server_url) as (reader, writer):
            # Create and run the client session within a context block.
            async with ClientSession(reader, writer) as session:
                print("Connection successful. Initializing session...")
                await session.initialize()
                print("Session initialized.")

                # Step 1: Read the input file.
                print("Reading input.txt...")
                read_result = await session.call_tool("read_file", {"path": "input.txt"})
                file_content = read_result.content
                print("File read successfully.")

                # Step 2: Summarize the content.
                print("Summarizing content...")
                summary_result = await session.call_tool("summarize_content", {"content": file_content})
                summary = summary_result.content
                print("Content summarized.")

                # Step 3: Write the summary to a new file.
                print("Writing summary...")
                write_result = await session.call_tool("write_summary", {"path": "summary.txt", "summary": summary})

                print(f"\n--- Success! ---")
                print(f"Server says: {write_result.content}")

    except Exception as e:
        print(f"\n--- Error ---", file=sys.stderr)
        print(f"Could not connect to the server. Please ensure server.py is running.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
