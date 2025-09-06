import asyncio
import sys
import mcp.types as types

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

                if not read_result.content or not isinstance(read_result.content[0], types.TextContent):
                    raise TypeError("Expected TextContent from read_file tool")
                file_content = read_result.content[0].text
                print("File read successfully.")

                # Step 2: Summarize the content.
                print("Summarizing content...")
                summary_result = await session.call_tool("summarize_content", {"content": file_content})
                
                if not summary_result.content or not isinstance(summary_result.content[0], types.TextContent):
                    raise TypeError("Expected TextContent from summarize_content tool")
                summary = summary_result.content[0].text
                print("Content summarized.")

                # Step 3: Write the summary to a new file.
                print("Writing summary...")
                write_result = await session.call_tool("write_summary", {"path": "summary.txt", "summary": summary})

                if not write_result.content or not isinstance(write_result.content[0], types.TextContent):
                    raise TypeError("Expected TextContent from write_summary tool")
                final_message = write_result.content[0].text

                print(f"\n--- Success! ---")
                print(f"Server says: {final_message}")

    except Exception as e:
        print(f"\n--- Error ---", file=sys.stderr)
        print(f"Could not connect to the server. Please ensure server.py is running.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())