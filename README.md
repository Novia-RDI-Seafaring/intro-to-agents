# intro-to-agents

Slides and runnable code on building agents with Pydantic AI. Used for an Intelligent Systems session at Novia UAS, 2026.

Slides published at https://novia-rdi-seafaring.github.io/intro-to-agents/

A curated reading list lives in [RESOURCES.md](RESOURCES.md).

## Layout

```
docs/                              Marp markdown — the slides.
  01-agents-with-pydantic-ai.md    Agent = LLM + loop + tools, MCP.
  02-serving-agents.md             to_cli_sync, to_a2a, to_ag_ui.
code/                              Python (uv project).
  agent.py                         Minimal Pydantic AI agent.
  serve_cli.py                     agent.to_cli_sync()
  serve_web.py                     agent.to_a2a() + agent.to_ag_ui()
.github/workflows/pages.yml        Builds slides on push to main.
```

## Build slides locally

```bash
npm install
npm run build              # docs/*.md → _site/*.html
npm run watch              # live-reload on http://localhost:8080
```

## Run the code

```bash
cd code
uv sync
export OPENAI_API_KEY=sk-...
uv run python agent.py "What files are here?"
```

## First-time GitHub setup

Settings → Pages → Source: **GitHub Actions**. After that the workflow handles every push to `main`.
