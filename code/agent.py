"""Minimal Pydantic AI agent for the Novia hackathon.

An agent is an LLM in a loop with tools. This file is the smallest honest
example of that idea: a model, a system prompt, three tools, a runner that
prints what the model decided to do.

Run:
    python agent.py "What Python files are here? Summarize one."
    python agent.py                # interactive mode

Requires:
    pip install pydantic-ai
    export OPENAI_API_KEY=sk-...
"""

import sys
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.messages import ToolCallPart, ToolReturnPart

MODEL = "openai:gpt-5"
INSTRUCTIONS = (
    "You are a helpful coding assistant working in the user's project directory. "
    "Use the tools to inspect and edit files. Think one step at a time: list, "
    "read, then act. When finished, reply with a short natural-language summary."
)

agent = Agent(MODEL, instructions=INSTRUCTIONS)


# ── Tools ─────────────────────────────────────────────────────────────
# Type hints become the JSON schema. Docstrings teach the model when to
# call the tool. Keep both honest.

@agent.tool_plain
def list_files(directory: str = ".") -> list[str]:
    """List non-hidden files and directories.

    Directories are returned with a trailing slash so the model can tell them apart.

    Args:
        directory: Directory path. Defaults to '.' (current directory).
    """
    p = Path(directory)
    if not p.exists():
        return [f"Error: directory not found: {directory}"]
    if not p.is_dir():
        return [f"Error: not a directory: {directory}"]
    return [
        child.name + ("/" if child.is_dir() else "")
        for child in sorted(p.iterdir())
        if not child.name.startswith(".")
    ]


@agent.tool_plain
def read_file(path: str) -> str:
    """Read the text contents of a file.

    Args:
        path: Path to the file, e.g. 'README.md'.
    """
    try:
        return Path(path).read_text()
    except FileNotFoundError:
        return f"Error: file not found: {path}"
    except Exception as e:
        return f"Error reading {path}: {e}"


@agent.tool_plain
def edit_file(path: str, old_str: str, new_str: str) -> str:
    """Replace the first occurrence of old_str with new_str in the file at path.

    Special case: if old_str is empty and the file does not exist, create the
    file with new_str as its content. Use this for both editing and creation.

    Args:
        path: Path of the file to edit or create.
        old_str: Text to find. Use '' to create a new file.
        new_str: Replacement text, or the contents of the new file.
    """
    p = Path(path)
    if old_str == "" and not p.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(new_str)
        return f"Created {path} ({len(new_str)} chars)."
    if not p.exists():
        return f"Error: file not found: {path}"
    text = p.read_text()
    if old_str not in text:
        return f"Error: old_str not found in {path}."
    p.write_text(text.replace(old_str, new_str, 1))
    return f"Edited {path} (1 replacement)."


# ── Runner ────────────────────────────────────────────────────────────

def run(prompt: str) -> str:
    """Run the agent on a prompt and print every tool call along the way."""
    result = agent.run_sync(prompt)
    for msg in result.all_messages():
        for part in msg.parts:
            if isinstance(part, ToolCallPart):
                print(f"→ {part.tool_name}({part.args_as_json_str()})")
            elif isinstance(part, ToolReturnPart):
                preview = str(part.content).replace("\n", " ")[:120]
                print(f"← {preview}")
    print(f"\n{'─' * 60}\n{result.output}")
    return result.output


def main() -> None:
    if len(sys.argv) > 1:
        run(" ".join(sys.argv[1:]))
        return
    print("Pydantic AI agent. Type 'quit' to exit.\n")
    while True:
        try:
            prompt = input("you: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if prompt.lower() in {"quit", "exit", "q"}:
            break
        if prompt:
            run(prompt)
            print()


if __name__ == "__main__":
    main()
