"""
Custom provider for testing tool calls.

Calls the Anthropic Messages API with tools enabled, captures which tools
were called, and returns both the final text output and a trace so that
trajectory:tool-used / trajectory:tool-sequence assertions can work.
"""

import json
import os
import sys

import anthropic

# ---------------------------------------------------------------------------
# Tool definitions exposed to the model
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "name": "web_search",
        "description": "Search the web for up-to-date information.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"],
        },
    },
    {
        "name": "read_file",
        "description": "Read the contents of a local file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path to read"}
            },
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a local file.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "File path"},
                "content": {"type": "string", "description": "Content to write"},
            },
            "required": ["path", "content"],
        },
    },
]

# ---------------------------------------------------------------------------
# Fake tool executor (returns stub results so the model can finish)
# ---------------------------------------------------------------------------

def _execute_tool(name: str, tool_input: dict) -> str:
    if name == "web_search":
        return json.dumps({"results": [f"Search result for: {tool_input.get('query')}"]})
    if name == "read_file":
        return f"(stub) contents of {tool_input.get('path')}"
    if name == "write_file":
        return f"(stub) wrote {len(tool_input.get('content', ''))} bytes to {tool_input.get('path')}"
    return "(stub) unknown tool"


# ---------------------------------------------------------------------------
# Main provider entry point
# ---------------------------------------------------------------------------

def call_api(prompt: str, options: dict, context: dict) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    base_url = os.environ.get("ANTHROPIC_BASE_URL", "")
    model = os.environ.get("MODEL", "claude-sonnet-4-6")

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url
    client = anthropic.Anthropic(**client_kwargs)

    messages = [{"role": "user", "content": prompt}]
    trace = []          # list of {"type": "tool_call", "name": ...}
    final_text = ""

    # Agentic loop: keep going until the model stops using tools
    for _ in range(10):
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        # Collect any tool calls from this turn
        tool_uses = [b for b in response.content if b.type == "tool_use"]
        text_blocks = [b for b in response.content if b.type == "text"]

        if text_blocks:
            final_text = text_blocks[-1].text

        if response.stop_reason == "end_turn" or not tool_uses:
            break

        # Record tool calls in trace
        for tu in tool_uses:
            trace.append({"type": "tool_call", "name": tu.name})

        # Build assistant message (all content blocks)
        messages.append({"role": "assistant", "content": response.content})

        # Execute each tool and feed results back
        tool_results = []
        for tu in tool_uses:
            result_content = _execute_tool(tu.name, tu.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tu.id,
                "content": result_content,
            })
        messages.append({"role": "user", "content": tool_results})

    tool_names = [t["name"] for t in trace]

    return {
        # Primary output shown in promptfoo results table
        "output": final_text or f"(no text; tools called: {tool_names})",
        # Metadata carries the trace for trajectory:* assertions
        "metadata": {
            "trace": trace,
            # Convenience fields for javascript assertions
            "tools_called": tool_names,
        },
    }
