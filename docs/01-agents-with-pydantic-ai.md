---
marp: true
theme: default
paginate: true
header: 'Agents with Pydantic AI · Part 1'
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

# Agents with Pydantic AI

## What an agent is, and how to build one in ~80 lines

**Part 1**
Novia UAS · 2026

---

## What you walk out with

1. A working mental model: **agent = LLM + loop + tools**.
2. A running Python agent on your laptop, less than 100 lines of your own code.
3. The skill to add a new tool to that agent in two minutes.
4. Enough vocabulary to read the Pydantic AI docs without getting lost.

---

<!-- _class: divider -->

# Part 1

## What is an agent?

---

## A normal LLM call

You send text in. You get text out. That's it.

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What's in /tmp on my laptop?"}],
)
print(response.choices[0].message.content)
```

The model has **no idea** what's in `/tmp`. It's never seen your laptop. It will guess, hedge, or apologise.

---

## What's missing

The model can't *do* anything. It can only produce text.

To answer "what's in `/tmp`?", *something* has to:

1. Run `ls /tmp` on your machine.
2. Feed the output back to the model.
3. Let the model use that output to answer.

That something is **the loop**, and the things it can run are **tools**.

---

## The shape of an agent

> An agent is an LLM running in a loop with access to tools.

```
        ┌──────────────────────────────────────┐
        │                                      │
        ▼                                      │
   ┌────────┐    tool call    ┌────────────┐   │
   │  LLM   │ ───────────────▶│   tool     │   │
   │        │                 │  (Python)  │   │
   │        │◀─── result ─────│            │   │
   └────────┘                 └────────────┘   │
        │                                      │
        │ "I'm done, here's the answer" ───────┘
        ▼
     final text to user
```

Loop until the model says it's done.

---

## What a "tool" actually is

A tool is **a Python function with a name, a description, and typed arguments**.

The model doesn't run the function. The model decides:

- *which* tool to call,
- *with what arguments*,

and your code runs the function and hands the return value back.

```python
def list_files(directory: str) -> list[str]:
    """List files in a directory on the local filesystem."""
    return os.listdir(directory)
```

That's a tool.

---

## Why frameworks exist

If you do this from scratch you have to:

- Write a JSON schema for every tool.
- Maintain a name → function dispatch table.
- Hand-write the loop and the stop condition.
- Wrap each tool result in the right message format.
- Parse structured output yourself.

It's about 200 lines of plumbing before you write any *interesting* code.

**Pydantic AI** is the framework that makes this go away.

---

<!-- _class: divider -->

# Part 2

## Building one with Pydantic AI

---

## The pitch

You write **functions with type hints and docstrings**.

Pydantic AI:

- Generates the JSON schemas from the type hints.
- Reads the docstrings as tool descriptions.
- Drives the loop until the model stops calling tools.
- Hands you a typed result at the end.

Your code stays at the level of *what the agent does*, not the plumbing under it.

---

## Install

```bash
pip install pydantic-ai
# or, with uv:
uv add pydantic-ai
```

You also need an API key. For OpenAI:

```bash
export OPENAI_API_KEY=sk-...
```

Pydantic AI also speaks Anthropic, Google, Ollama, Mistral, and more — same code, different model string.

---

## Step 1 — create the agent

```python
from pydantic_ai import Agent

agent = Agent(
    "openai:gpt-4o-mini",
    instructions=(
        "You are a helpful coding assistant. "
        "Use the tools to inspect the filesystem. "
        "When you finish, summarize what you did."
    ),
)
```

Two arguments: *which model* and *what the system prompt is*.

That's the whole agent declaration. Tools come next.

---

## Step 2 — add a tool

```python
from pathlib import Path

@agent.tool_plain
def read_file(path: str) -> str:
    """Read the contents of a file and return it as text.

    Args:
        path: The file path, e.g. 'notes.md'.
    """
    return Path(path).read_text()
```

A decorator, a function, type hints, a docstring.

The model now knows it has a `read_file` tool, what it does, and what argument to pass.

---

## Step 3 — run it

```python
result = agent.run_sync("Read notes.md and summarize it.")
print(result.output)
```

Behind the scenes Pydantic AI:

1. Sends your prompt + the tool schemas to the model.
2. Receives back: "call `read_file('notes.md')`".
3. Runs the function, captures the return value.
4. Feeds it back to the model.
5. Receives back the final summary.
6. Gives you `result.output`.

Six lines for you. Zero lines of loop boilerplate.

---

## The whole thing

```python
from pathlib import Path
from pydantic_ai import Agent

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a helpful filesystem assistant.",
)

@agent.tool_plain
def list_files(directory: str = ".") -> list[str]:
    """List non-hidden entries in a directory."""
    return [p.name for p in Path(directory).iterdir() if not p.name.startswith(".")]

@agent.tool_plain
def read_file(path: str) -> str:
    """Read the text contents of a file."""
    return Path(path).read_text()

result = agent.run_sync("What Python files are in this directory? Pick one and summarize it.")
print(result.output)
```

That is a real, working agent. Run it.

---

## Watching it think

By default `run_sync` only returns the final answer. To *see* the tool calls, walk the message history:

```python
from pydantic_ai.messages import ToolCallPart, ToolReturnPart

result = agent.run_sync("Find a python file and summarize it.")
for msg in result.all_messages():
    for part in msg.parts:
        if isinstance(part, ToolCallPart):
            print(f"→ {part.tool_name}({part.args_as_json_str()})")
        elif isinstance(part, ToolReturnPart):
            print(f"← {part.content[:80]}")
print(f"\nFinal: {result.output}")
```

This is your debugging window. Every weird agent behaviour starts here.

---

## Typed structured output

Sometimes you don't want a paragraph. You want JSON you can use.

```python
from pydantic import BaseModel

class FileSummary(BaseModel):
    path: str
    line_count: int
    one_line_description: str

typed_agent = Agent(
    "openai:gpt-4o-mini",
    instructions="Summarize the file the user names.",
    output_type=FileSummary,
)

result = typed_agent.run_sync("Summarize hello.py")
print(result.output.line_count)        # int
print(result.output.one_line_description)  # str
```

The model is *forced* to produce something that validates against your type.

---

## When tools fail

Tools throw exceptions. Files don't exist. APIs return 500s.

The pattern is to **catch and return a string** so the model sees the error and can recover:

```python
@agent.tool_plain
def read_file(path: str) -> str:
    """Read the text contents of a file."""
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return f"Error: file not found: {path}"
    except Exception as e:
        return f"Error reading {path}: {e}"
```

The model often retries with a corrected argument. That's the loop earning its keep.

---

## Tools you didn't write — MCP

So far you've written tools as Python functions. The other source of tools is **MCP** (Model Context Protocol): a standard way for *external processes* to expose tools.

There's already an ecosystem: filesystems, GitHub, Slack, Postgres, Playwright, Notion. Each is a server you point your agent at. No glue code per tool.

Pydantic AI speaks MCP natively. You attach a server when you create the agent, and every tool that server exposes appears as if you'd decorated it yourself.

---

## Adding an MCP server

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio, MCPServerStreamableHTTP

# (a) Local server, launched as a subprocess over stdio
fs_server = MCPServerStdio(
    "npx",
    args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
)

# (b) Remote server, reached over HTTP
remote = MCPServerStreamableHTTP(url="http://localhost:3001/mcp")

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You can read and write files via the filesystem MCP server.",
    toolsets=[fs_server, remote],   # mix and match
)

async with agent:                   # MCP servers need a lifecycle
    result = await agent.run("List the files in /tmp and summarise the largest.")
    print(result.output)
```

Your `@agent.tool_plain` tools and the MCP-provided tools live side by side — the model picks whichever fits.

---

<!-- _class: divider -->

# Part 3

## Exercise

---

## Build a project assistant

Start from [`code/agent.py`](https://github.com/Novia-RDI-Seafaring/intro-to-agents/blob/main/code/agent.py) in the repo. It has three tools: `list_files`, `read_file`, `edit_file`.

**Your job, in three steps:**

1. **Run it.** Confirm the example prompt works end-to-end.
2. **Add a tool.** Pick one:
   - `word_count(path) -> int`
   - `find_files(pattern) -> list[str]` (e.g. `"*.py"`)
   - `run_python(code) -> str` (use `subprocess`, watch out for safety)
3. **Use it.** Write a prompt that *forces* the agent to use your new tool, and verify it does (check the trace).

Stretch: swap the model to `"anthropic:claude-haiku-4-5"` or `"openai:gpt-4o"` and compare.

---

## What to look for while you hack

- **Tool name + docstring quality matters more than you think.** If the model isn't picking your tool, the description is usually too vague.
- **Argument types tell the model what's legal.** `path: str` is fine; `path: Path` will confuse it.
- **One tool, one verb.** `read_file` good. `read_or_edit_file` bad.
- **Return strings the model can read.** Errors as strings, not exceptions. Long output → truncate or summarize.

---

## Why this is the whole game

Everything else in agentic systems — multi-step planning, RAG, multi-agent setups, long-running jobs — is built on this one primitive:

> **A model that can call functions you wrote, in a loop, until it's done.**

Get fluent with this. The rest is variations on the theme.

---

<!-- _class: title -->

# Now go build

## [github.com/Novia-RDI-Seafaring/intro-to-agents](https://github.com/Novia-RDI-Seafaring/intro-to-agents)

Questions → ask. Bugs → grep first, ask second.
