# intro-to-agents

Hackathon slides + runnable code: **what an agent is, and how to build one with Pydantic AI**.

Source of truth lives in `docs/` (Marp markdown). HTML for browser viewing is built by CI and published to GitHub Pages.

## Layout

```
docs/                              # Marp source — the truth.
  01-agents-with-pydantic-ai.md    # Deck 1: agent = LLM + loop + tools, MCP.
  02-serving-agents.md             # Deck 2: to_cli_sync, to_a2a, to_ag_ui.
code/                              # Runnable Python (uv project).
  agent.py                         # Minimal Pydantic AI agent.
  serve_cli.py                     # agent.to_cli_sync()
  serve_web.py                     # agent.to_a2a() + agent.to_ag_ui()
.github/workflows/pages.yml        # Builds slides → Pages on every push to main.
```

## View the slides

Published at **https://novia-rdi-seafaring.github.io/intro-to-agents/** (after the first successful Pages deploy — see *Setup* below).

## Build locally

Slides:

```bash
npm install                # one-time, pulls marp-cli
npm run build              # docs/*.md → _site/*.html
npm run watch              # live-reload on edit, serves on http://localhost:8080
```

Code:

```bash
cd code
uv sync
export OPENAI_API_KEY=sk-...
uv run python agent.py "What files are here?"
```

## Setup (one-time, after cloning a fresh repo)

In the repo's GitHub settings → **Pages** → **Source: GitHub Actions**.

That's it — `.github/workflows/pages.yml` does the rest on every push to `main`.

## Editing the slides

The Marp frontmatter is shared between decks; copy it from an existing deck when starting a new one. New decks dropped into `docs/` are picked up automatically by the workflow and listed on the Pages index.
