#!/usr/bin/env python3
"""Write _site/index.html linking to every deck Marp produced.

Called from .github/workflows/pages.yml after marp has populated _site/.
Standalone Python: stdlib only.
"""

from __future__ import annotations

import html
import pathlib
import sys

site = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "_site")
decks = sorted(p for p in site.glob("*.html") if p.name != "index.html")

items = "\n".join(
    f'      <li><a href="{p.name}">{html.escape(p.stem)}</a></li>'
    for p in decks
)

PAGE = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>intro-to-agents — slides</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root {{ color-scheme: light dark; }}
    body {{
      font-family: -apple-system, 'Inter', 'Helvetica Neue', sans-serif;
      max-width: 720px;
      margin: 4rem auto;
      padding: 0 1.5rem;
      line-height: 1.5;
    }}
    h1 {{ color: #1a4789; margin-bottom: 0.2em; }}
    .sub {{ color: #666; margin-top: 0; }}
    ul {{ padding-left: 1.2em; }}
    li {{ margin: 0.4em 0; }}
    a {{ color: #1a4789; text-decoration: none; border-bottom: 1px solid transparent; }}
    a:hover {{ border-bottom-color: #1a4789; }}
    footer {{ margin-top: 3rem; color: #888; font-size: 0.85em; }}
  </style>
</head>
<body>
  <h1>intro-to-agents</h1>
  <p class="sub">Hackathon slides — what an agent is, and how to build one with Pydantic AI.</p>
  <ul>
{items}
  </ul>
  <footer>
    Source: <a href="https://github.com/Novia-RDI-Seafaring/intro-to-agents">github.com/Novia-RDI-Seafaring/intro-to-agents</a>
  </footer>
</body>
</html>
"""

(site / "index.html").write_text(PAGE)
print(f"Generated {site / 'index.html'} with {len(decks)} deck(s).")
