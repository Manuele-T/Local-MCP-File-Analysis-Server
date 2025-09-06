# AI File Analysis Agent with MCP

![Cover Image](/screenshots/01.jpg)

## Overview

This project is a demonstration of the **Agent-Tool paradigm** using the **Machine-to-Machine Communication Protocol (MCP)**. It features a lightweight AI Agent that orchestrates a series of tasks by communicating with a local Tool Server. The agent's goal is to read a local text file, leverage  **OpenAI GPT-4.1-Nano API** for summarization, and write the resulting summary back to a local summary file.

The application's architecture separates the "brains" of the operation (the Agent) from the "hands" (the Tool). The Agent contains the high-level logic and plan, while the Server exposes specific, self-contained capabilities. Communication between these two components is handled MCP, abstracting away the complexities of network programming.

This project serves as a foundational blueprint for building more complex AI systems where autonomous agents can interact with a variety of digital and real-world tools.

![Image](/screenshots/02.jpg)

## Features

*   **AI-Powered Text Summarization:** Integrates the OpenAI API to provide context-aware text summaries.
*   **Local File System Interaction:** The Agent can read from and write to the local file system via the tools provided by the server.
*   **Decoupled Agent-Tool Architecture:** A clear separation between the agent's logic (`agent.py`) and the server's capabilities (`server.py`).
*   **Machine-to-Machine Communication:** Utilizes **MCP** for structured communication between the agent and the tool server.
*   **External API Abstraction:** The complexity of interacting with the OpenAI API is hidden from the agent, exposed as a simple `summarize_content` tool.
*   **Asynchronous Operations:** Built on Python's `asyncio` for high-performance execution.

## Tech Stack & Architecture

*   **Core Protocol:** **MCP (Machine-to-Machine Communication Protocol)**
    *   **Server Library:** `fastmcp` (from the `mcp` package)
    *   **Client Library:** `mcp.client` modules (from the `mcp` package)
    *   **Transport Layer:** SSE (Server-Sent Events)

*   **Agent (`agent.py`): The Orchestrator**
    *   Responsible for the high-level plan and sequencing of tool calls.
    *   Connects to the Tool Server using `ClientSession` and `sse_client`.
    *   Chains inputs and outputs between tools.

*   **Tool Server (`server.py`): The Capability Provider**
    *   Exposes functions as network-accessible tools using the `@mcp.tool` decorator.
    *   Handles file I/O operations (`read_file`, `write_summary`).
    *   Manages the integration with the external OpenAI API.

*   **AI Core & NLP:** **OpenAI API**
    *   **Model:** `gpt-4.1-nano` (or any other chat completion model)
    *   **Task:** Natural Language Summarization

*   **Language & Libraries:**
    *   **Language:** Python
    *   **Key Libraries:** `mcp`, `openai`, `python-dotenv`, `asyncio`

## How to Run This Project

### 1. Prerequisites

*   Python 3.8+
*   An OpenAI API Key (add it to a .env file)
*   an input.txt file in your project folder

### 2. Setup

**Clone the repository:**
```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

**Create and activate a virtual environment:**

* On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

* On Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Install the required packages:**

* With your virtual environment activated, install all dependencies from the requirements.txt file.

```bash
pip install -r requirements.txt
```