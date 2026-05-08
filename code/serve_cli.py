"""Expose the agent as an interactive terminal REPL.

Pydantic AI ships a `rich`-powered CLI for any agent. One method call,
multi-turn conversation, colored output, tool-call traces — for free.

Run:
    pip install "pydantic-ai[cli]"
    export OPENAI_API_KEY=sk-...
    python serve_cli.py

Then chat with the agent. Ctrl-C to quit.
"""

from agent import agent

if __name__ == "__main__":
    # Carries history across turns inside the session, unlike agent.py's
    # one-shot `run()` helper.
    agent.to_cli_sync()
