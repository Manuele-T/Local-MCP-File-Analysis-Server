import asyncio
import sys
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

async def main():
    """Connects to the server, runs the file analysis, and prints the result."""
    server_url = "http://localhost:8000/sse"
    print(f"Attempting to connect to server at {server_url}...")

    try:
        # Use the sse_client function to connect to the server's SSE endpoint.
        async with sse_client(url=server_url) as (reader, writer):
            # A session is created to manage the connection.
            session = ClientSession(reader, writer)
            await session.initialize()
            print("Connection successful.")

            # Step 1: Read the file from the server.
            print("Reading input.txt...")
            read_result = await session.call_tool("read_file", {"path": "input.txt"})
            file_content = read_result.content

            # Step 2: Send the content to the server for summarization.
            print("Summarizing content...")
            summary_result = await session.call_tool("summarize_content", {"content": file_content})
            summary = summary_result.content

            # Step 3: Tell the server to write the summary to a new file.
            print("Writing summary...")
            write_result = await session.call_tool("write_summary", {"path": "summary.txt", "summary": summary})

            print(f"\nSuccess! Server says: {write_result.content}")

    except Exception as e:
        print(f"\nError: Could not connect to the server.", file=sys.stderr)
        print(f"Please make sure server.py is running in another terminal.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
