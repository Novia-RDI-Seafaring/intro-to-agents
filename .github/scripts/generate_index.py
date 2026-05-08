#!/usr/bin/env python3
"""Write _site/index.html linking to every Marp deck.

Pulls each deck's title (first H1) and subtitle (first H2) out of the
markdown so the cards on the landing page show what each deck is about
without hard-coding it here.

Stdlib only. Called from .github/workflows/pages.yml after marp runs.
"""

from __future__ import annotations

import html
import pathlib
import re
import sys


def parse_meta(md_path: pathlib.Path) -> tuple[str, str]:
    """Return (title, subtitle) from the first H1 / H2 in a marp markdown file."""
    text = md_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        # Strip frontmatter.
        m = re.search(r"\n---\s*\n", text)
        if m:
            text = text[m.end():]

    title = subtitle = ""
    for line in text.splitlines():
        line = line.strip()
        if not title and line.startswith("# "):
            title = line[2:].strip()
        elif title and not subtitle and line.startswith("## "):
            subtitle = line[3:].strip()
            break
    return title or md_path.stem, subtitle


def part_label(stem: str) -> str:
    """'01-agents-with-pydantic-ai' -> 'Part 1'. Falls back to ''."""
    m = re.match(r"^(\d+)[-_]", stem)
    return f"Part {int(m.group(1))}" if m else ""


def main() -> None:
    site = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
    docs = pathlib.Path("docs")
    decks = sorted(p for p in site.glob("*.html") if p.name != "index.html")

    def render_inline(s: str) -> str:
        """Escape, then render `…` as <code>…</code>."""
        escaped = html.escape(s)
        return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)

    cards = []
    for deck in decks:
        md = docs / f"{deck.stem}.md"
        title, subtitle = parse_meta(md) if md.exists() else (deck.stem, "")
        prefix = part_label(deck.stem)
        heading = f"{prefix} — {title}" if prefix else title
        desc = subtitle or "&nbsp;"
        cards.append(
            f'    <a class="deck" href="{html.escape(deck.name)}">\n'
            f'      <h2>{render_inline(heading)}</h2>\n'
            f'      <p>{render_inline(desc)}</p>\n'
            f'    </a>'
        )

    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>intro-to-agents</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{
      font-family: -apple-system, 'Inter', 'Helvetica Neue', sans-serif;
      max-width: 640px;
      margin: 5rem auto 6rem;
      padding: 0 1.5rem;
      line-height: 1.55;
      color: #222;
      background: #fafafa;
    }}
    h1 {{
      color: #1a4789;
      font-size: 2.1rem;
      font-weight: 700;
      margin: 0 0 0.2em;
    }}
    .sub {{
      color: #555;
      margin: 0 0 2.5rem;
    }}
    .deck {{
      display: block;
      padding: 1rem 1.25rem;
      margin: 0.7rem 0;
      border: 1px solid #dde3ea;
      border-radius: 6px;
      background: #fff;
      text-decoration: none;
      color: inherit;
      transition: border-color 0.12s ease;
    }}
    .deck:hover {{
      border-color: #1a4789;
    }}
    .deck h2 {{
      color: #1a4789;
      font-size: 1.05rem;
      font-weight: 600;
      margin: 0 0 0.2em;
    }}
    .deck p {{
      color: #555;
      margin: 0;
      font-size: 0.95rem;
    }}
    .deck code {{
      background: #f4f4f4;
      padding: 1px 5px;
      border-radius: 3px;
      font-size: 0.9em;
    }}
    footer {{
      margin-top: 3rem;
      color: #888;
      font-size: 0.85rem;
    }}
    footer a {{ color: #1a4789; text-decoration: none; }}
    footer a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
  <h1>intro-to-agents</h1>
  <p class="sub">Slides on building agents with Pydantic AI. Novia UAS, 2026.</p>

{chr(10).join(cards)}

  <footer>
    Source: <a href="https://github.com/Novia-RDI-Seafaring/intro-to-agents">github.com/Novia-RDI-Seafaring/intro-to-agents</a>
  </footer>
</body>
</html>
"""

    out = site / "index.html"
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out} ({len(decks)} decks).")


if __name__ == "__main__":
    main()
