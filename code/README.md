# Hackathon — Pydantic AI agent

A minimal, runnable agent in ~80 lines. Slides explaining the ideas live one folder up at `01-agents-with-pydantic-ai.md`.

## Setup

With `uv` (recommended):

```bash
cd courses/hackathon/code
uv sync
export OPENAI_API_KEY=sk-...
uv run python agent.py "What files are here? Pick a Python file and summarize it."
```

With plain `pip`:

```bash
pip install pydantic-ai
export OPENAI_API_KEY=sk-...
python agent.py "What files are here? Pick a Python file and summarize it."
```

Run with no arguments for an interactive REPL.

## What's inside

- `agent.py` — the agent itself. `Agent("openai:gpt-4o-mini", ...)`, three tools (`list_files`, `read_file`, `edit_file`), and a `run()` helper that prints every tool call so you can watch the loop.
- `serve_cli.py` — exposes the same agent as an interactive terminal REPL via `agent.to_cli_sync()`.
- `serve_web.py` — exposes the same agent over HTTP via `agent.to_a2a()` (agent-to-agent) and `agent.to_ag_ui()` (web chat UIs).

The behaviour lives in `agent.py`. The serve scripts are one-liners that pick who can talk to it. Don't fork the agent to add a new interface.

## Talking to the agent three ways

```bash
# 1. One-shot from the command line
python agent.py "What files are here?"

# 2. Interactive REPL (multi-turn, history carries across turns)
pip install "pydantic-ai[cli]"
python serve_cli.py

# 3. Over HTTP — A2A endpoint for other agents
pip install "pydantic-ai[a2a]" uvicorn
uvicorn serve_web:a2a_app --reload --port 8000
curl -s http://localhost:8000/.well-known/agent-card.json | jq

# 4. Over HTTP — AG-UI endpoint for browser chat frontends (CopilotKit etc.)
pip install "pydantic-ai[ag-ui]" uvicorn
uvicorn serve_web:ag_ui_app --reload --port 8001
```

## Other model providers

Pydantic AI is provider-agnostic. Swap the model string and the env var:

```python
agent = Agent("anthropic:claude-haiku-4-5", instructions=...)
# export ANTHROPIC_API_KEY=...

agent = Agent("google-gla:gemini-2.0-flash", instructions=...)
# export GEMINI_API_KEY=...
```

For local models via Ollama, see the Pydantic AI docs.

## Exercise

1. **Run it.** Confirm the example prompt works end-to-end.
2. **Add a tool.** Pick one and add it to `agent.py`:
   - `word_count(path: str) -> int`
   - `find_files(pattern: str) -> list[str]` (e.g. `"*.py"`)
   - `run_python(code: str) -> str` — be careful, this executes code.
3. **Use it.** Write a prompt that *requires* your new tool. Watch the trace to confirm the model called it.

Stretch: change `MODEL` to a different provider, or add `output_type=SomeBaseModel` to get typed structured output.

## Reading the trace

Lines starting with `→` are tool calls the model made. Lines starting with `←` are the values your function returned (truncated). The final block after the divider is the model's answer to the user.

If the model isn't calling a tool you expect, the docstring is almost always the reason. Make it clearer about *when* the tool should be used.
