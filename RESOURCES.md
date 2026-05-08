# Good resources

Stuff I'd actually point a student at. Curated, not exhaustive.

## Read first

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — Anthropic, Schluntz & Ingargiola. The clearest short essay on workflow vs. agent and why most production "agentic" systems are just workflows. Read this before anything else.
- [How to think about agents](https://simonwillison.net/2025/Mar/11/agents/) — Simon Willison's running notes. Short, opinionated, kept current.
- [Anthropic Cookbook — Tool use & agents](https://github.com/anthropics/anthropic-cookbook/tree/main/tool_use) — runnable, low-magic. Good after you've built one yourself.

## Frameworks

- [Pydantic AI docs](https://ai.pydantic.dev/) — what Part 1 of the slides is built on. The "Tools" and "Multi-agent" pages are the high-leverage ones.
- [Pydantic AI source](https://github.com/pydantic/pydantic-ai) — small enough to read. Skim `agent.py` once.
- [LangGraph](https://langchain-ai.github.io/langgraph/) — graph/state-machine framing for multi-step agents. Heavier than Pydantic AI; pull it out when you actually need explicit state.
- [smolagents](https://github.com/huggingface/smolagents) — Hugging Face's minimal agent framework, code-execution focused.
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — the OpenAI-native option, recently renamed from Swarm.

## Protocols

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) — the "USB-C for tools" spec. Read [the architecture page](https://modelcontextprotocol.io/docs/concepts/architecture) and the [Python SDK](https://github.com/modelcontextprotocol/python-sdk).
- [A2A — Agent-to-Agent](https://a2aproject.github.io/A2A/) — Google's spec for agents calling agents over HTTP. Picked up by Pydantic AI, LangGraph, and others.
- [AG-UI](https://docs.ag-ui.com/) — chat-UI streaming protocol. The thing CopilotKit speaks.

## Production / harness engineering

- [Boris Cherny — Claude Code talks](https://www.youtube.com/results?search_query=boris+cherny+claude+code) — best public window into how a real agent harness is built.
- [Claude Code best practices](https://www.anthropic.com/engineering/claude-code-best-practices) — Anthropic's own writeup.
- [Effective harnesses for long-running agents](https://applied-llms.org/) — applied-llms.org. Practical, not hypey.
- [Karpathy — LLM OS](https://www.youtube.com/watch?v=zjkBMFhNj_g) — the framing that makes "tools + memory + loop" feel obvious in retrospect.

## Models, providers, and the basement

- [Anthropic API docs](https://docs.anthropic.com/) — start with the [tool use page](https://docs.anthropic.com/en/docs/build-with-claude/tool-use).
- [OpenAI structured outputs](https://platform.openai.com/docs/guides/structured-outputs) — when you want JSON, not paragraphs.
- [Ollama](https://ollama.com/) — for running local models. Useful when you want to see what a smaller model gets wrong.

## People worth following

- [Simon Willison](https://simonwillison.net/) — independent, fast, no hype.
- [Hamel Husain](https://hamel.dev/) — evals, RAG, what-actually-works writing.
- [Anthropic engineering blog](https://www.anthropic.com/engineering) — when they post, read it.
- [Eugene Yan](https://eugeneyan.com/) — long-form on applied LLM systems.

## SysML / systems-modelling specific

(For the [agentic-sysml-hackathon](https://github.com/Novia-RDI-Seafaring/agentic-sysml-hackathon) project.)

- [SysML v2 API Services](https://github.com/Systems-Modeling/SysML-v2-API-Services) — the reference REST/HTTP service.
- [SysML v2 API Cookbook](https://github.com/Systems-Modeling/SysML-v2-API-Cookbook) — usage examples.
- [SysML v2 release](https://github.com/Systems-Modeling/SysML-v2-Release) — the spec and pilot impl.
