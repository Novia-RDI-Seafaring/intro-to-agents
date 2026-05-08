---
marp: true
theme: default
paginate: true
header: 'Hackathon · Serving Agents'
footer: 'Christoffer Björkskog · Novia UAS · 2026'
style: |
  section {
    font-family: -apple-system, 'Inter', 'Helvetica Neue', Helvetica, sans-serif;
    padding: 60px;
    font-size: 26px;
    color: #222;
  }
  h1 { color: #1a4789; font-weight: 700; }
  h2 { color: #1a4789; font-weight: 600; }
  h3 { color: #444; font-weight: 500; }
  code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-size: 0.85em; }
  pre { background: #f6f8fb; color: #2b2b2b; padding: 20px; border-radius: 6px; font-size: 0.62em; line-height: 1.4; border: 1px solid #dde3ea; }
  pre code { background: transparent; color: inherit; padding: 0; }
  .hljs-keyword, .hljs-selector-tag { color: #1a4789; font-weight: 600; }
  .hljs-string, .hljs-attr { color: #22863a; }
  .hljs-comment { color: #6a737d; font-style: italic; }
  .hljs-number, .hljs-literal { color: #b35900; }
  .hljs-title, .hljs-function { color: #6f42c1; }
  .hljs-built_in { color: #005cc5; }
  blockquote {
    border-left: 4px solid #1a4789;
    padding: 8px 18px;
    color: #444;
    background: #f6f8fb;
    font-style: italic;
    font-size: 0.9em;
  }
  table { font-size: 0.8em; border-collapse: collapse; margin: 10px 0; }
  th, td { padding: 6px 12px; border: 1px solid #ccc; text-align: left; }
  th { background: #1a4789; color: white; }
  section.title {
    background: #1a4789;
    color: white;
    justify-content: center;
    text-align: center;
  }
  section.title h1 { color: white; font-size: 2.8em; margin-bottom: 0; }
  section.title h2 { color: #a6c8ff; font-weight: 300; margin-top: 0.2em; }
  section.divider {
    background: #f0f4f8;
    justify-content: center;
    text-align: center;
  }
  section.divider h1 { font-size: 2.5em; color: #1a4789; }
  section.divider h2 { color: #666; font-weight: 300; }
  .highlight {
    background: #fff8dc;
    padding: 14px 18px;
    border-left: 4px solid #d4a017;
    border-radius: 4px;
    margin: 10px 0;
  }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
  .caption { color: #777; font-size: 0.8em; font-style: italic; }
---

<!-- _class: title -->

# Serving your agent

## From `agent.run_sync(...)` to something humans and other agents can talk to

**Hackathon · Part 2**
Novia UAS · 2026

---

## The problem

You have an agent. You can call `agent.run_sync("...")` from a Python script.

But:

- A demo to a teammate needs a **chat-style REPL**, not a one-shot prompt.
- A web frontend needs an **HTTP endpoint** with streaming.
- Another agent needs a **machine-readable interface** so it can call yours.

Pydantic AI gives you a one-liner for each.

---

## Three adapters, one agent

```python
from agent import agent   # your existing Agent(...) object

agent.to_cli_sync()        # interactive terminal REPL
a2a_app   = agent.to_a2a()    # ASGI app: A2A protocol (agent ↔ agent)
ag_ui_app = agent.to_ag_ui()  # ASGI app: AG-UI protocol (web chat UI)
```

| Adapter        | For…                                | Transport                |
|----------------|-------------------------------------|--------------------------|
| `to_cli_sync`  | You, in a terminal                  | stdin/stdout + `rich`    |
| `to_a2a`       | Another agent or backend service    | HTTP / JSON-RPC + SSE    |
| `to_ag_ui`     | A browser frontend (CopilotKit etc.)| HTTP + SSE streaming     |

Same agent, three audiences.

---

<!-- _class: divider -->

# Adapter 1

## `to_cli_sync` — a REPL in your terminal

---

## The whole thing

```python
# serve_cli.py
from agent import agent

if __name__ == "__main__":
    agent.to_cli_sync()
```

Run it:

```bash
pip install "pydantic-ai[cli]"
python serve_cli.py
```

You get a multi-turn chat in the terminal: colored output, tool-call traces, conversation history carried across turns. Ctrl-C exits.

---

## When you'd reach for it

- **Demos.** Faster than building a UI, more interactive than a script.
- **Manual testing.** Hand-test prompts before automating them.
- **Exploration.** Poke at a new agent's behaviour.

Limits: it's local-only and single-user. For anything multi-user or remote, you want HTTP.

---

<!-- _class: divider -->

# Adapter 2

## `to_a2a` — agent-to-agent over HTTP

---

## What A2A is

**A2A** is a protocol for *agents calling other agents*. Think of it as "REST for agents":

- A discovery endpoint (`/.well-known/agent-card.json`) describes what your agent can do.
- A JSON-RPC endpoint accepts tasks.
- Streaming progress comes back over Server-Sent Events.

If you've ever exposed a Python function as a REST endpoint so another service could call it — A2A is the same idea, lifted to agents.

---

## The whole thing

```python
# serve_web.py
from agent import agent

a2a_app = agent.to_a2a()
```

Run it:

```bash
pip install "pydantic-ai[a2a]" uvicorn
uvicorn serve_web:a2a_app --reload --port 8000
```

Discover what the agent can do:

```bash
curl -s http://localhost:8000/.well-known/agent-card.json | jq
```

Now any A2A-speaking client — including other Pydantic AI agents — can call this one as a tool.

---

## When you'd reach for it

- **Multi-agent systems.** A planner agent calls a research agent calls a coder agent.
- **Service boundaries.** One team ships an agent; another team's backend calls it.
- **Language interop.** Your agent is in Python; the caller is in TypeScript or Go.

You're treating the agent the same way you'd treat any other backend microservice — with a standard contract.

---

<!-- _class: divider -->

# Adapter 3

## `to_ag_ui` — streaming chat for the browser

---

## What AG-UI is

**AG-UI** is a protocol designed for *frontends that render agent chats*. It defines:

- Streaming message events (token-by-token text).
- Tool-call events the UI can render as cards.
- State events for things like progress bars and intermediate steps.

Frontend libraries like **CopilotKit** speak AG-UI. Point them at your endpoint, and you get a chat UI with tool rendering for free — no protocol glue on your side.

---

## The whole thing

```python
# serve_web.py
from agent import agent

ag_ui_app = agent.to_ag_ui()
```

Run it:

```bash
pip install "pydantic-ai[ag-ui]" uvicorn
uvicorn serve_web:ag_ui_app --reload --port 8001
```

Then point an AG-UI compatible frontend at `http://localhost:8001`. The frontend handles the streaming, the tool rendering, the chat scrollback.

---

## When you'd reach for it

- **You want a real chat UI in a browser**, but you don't want to write the streaming code, the tool-call rendering, the message history widgets.
- **You're integrating with an existing CopilotKit app.**
- **You want a polished demo** that works on any laptop, not just yours.

If you're building from scratch and need full control of the UI, you can also wrap the agent in your own FastAPI route — `to_ag_ui()` is just the convenient default.

---

<!-- _class: divider -->

# Putting it together

---

## One agent file, three entry points

```
courses/hackathon/code/
├── agent.py          ← Agent(...) + tools, the actual logic
├── serve_cli.py      ← agent.to_cli_sync()
└── serve_web.py      ← agent.to_a2a()  +  agent.to_ag_ui()
```

The agent's *behaviour* lives in one place. The *interface* is a one-liner that picks who can talk to it.

This is the deployment story for a Pydantic AI agent in a single picture.

---

## Pick the right one

| Situation                                       | Use                |
|-------------------------------------------------|--------------------|
| You're hacking, want to talk to it now          | `to_cli_sync()`    |
| Another agent / a backend needs to call it      | `to_a2a()`         |
| A web chat UI needs to render against it        | `to_ag_ui()`       |
| You're testing in a script / Jupyter            | `agent.run_sync()` |

All four are the *same agent object* underneath. Don't fork the logic to add a new interface — just pick another adapter.

---

<!-- _class: divider -->

# Mini-exercise

---

## 10 minutes, two terminals

1. **Terminal 1.** Run `python serve_cli.py`. Have a 3-turn conversation with your agent. Notice the history carries across turns.
2. **Terminal 2.** Run `uvicorn serve_web:a2a_app --port 8000`. In a third shell, `curl http://localhost:8000/.well-known/agent-card.json` and read what your agent advertises about itself.
3. **Stretch.** Add a new tool to `agent.py`, restart both servers, and check that the agent card now lists it. (It should — without you touching `serve_cli.py` or `serve_web.py`.)

That last point is the win: **interface is decoupled from behaviour**.

---

<!-- _class: title -->

# Now ship it

## Code in `courses/hackathon/code/`
