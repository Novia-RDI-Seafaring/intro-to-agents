"""Expose the agent over HTTP — two flavours.

Pydantic AI gives you two one-liner web adapters:

  * `agent.to_a2a()`    → an ASGI app speaking the A2A (Agent-to-Agent)
                          protocol. Use this when another *agent* or
                          backend service needs to call your agent.
  * `agent.to_ag_ui()`  → an ASGI app speaking AG-UI, the streaming
                          chat-UI protocol used by tools like CopilotKit.
                          Use this when a *web frontend* needs to render
                          a chat against your agent.

Both return a Starlette ASGI app, so you serve them with uvicorn.

Run (pick one):
    pip install "pydantic-ai[a2a]" uvicorn
    export OPENAI_API_KEY=sk-...
    uvicorn serve_web:a2a_app   --reload --port 8000   # A2A endpoint
    uvicorn serve_web:ag_ui_app --reload --port 8001   # AG-UI endpoint

Smoke test the A2A endpoint:
    curl -s http://localhost:8000/.well-known/agent-card.json | jq
"""

from agent import agent

# A2A: agent-to-agent / backend-to-agent. JSON-RPC over HTTP, streaming
# via SSE. Other agents discover capabilities at /.well-known/agent-card.json.
a2a_app = agent.to_a2a()

# AG-UI: streaming chat protocol for browser frontends. A React app
# speaking AG-UI can connect to this endpoint and render a full chat UI
# with tool-call rendering, no glue code on your side.
ag_ui_app = agent.to_ag_ui()
