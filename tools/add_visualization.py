#!/usr/bin/env python3
"""
Add an interactive page (for example one made in a Claude chat) to content/Visualizations/.

    python3 tools/add_visualization.py SOURCE.html NAME [--title "Note title" --description "One line."]

NAME is the page's file name without its extension, in lowercase words joined by hyphens (latency-feel-lab). The page
is written to content/Visualizations/NAME.htm, ready to be served on its own by the site. The extension is .htm because
Quartz drops .html from the files it copies, and the site would then send the page as a download. On the way:

- a page saved without its <!doctype html><head> (as Claude writes an artifact) gets a minimal document around it;
- a page that draws Mermaid with the claude.ai runtime (/_runtime/mermaid-*.min.js) loads Mermaid from jsDelivr
  instead, and a page with <pre class="mermaid"> blocks and no Mermaid at all gets a loader;
- the RunicDocs embed helper (tools/templates/embed-helper.html) is added, so inside a note the page follows the
  site's light/dark toggle.

With --title, the script also creates the note content/Visualizations/TITLE.md that shows the page in a frame and
links to it, unless that note exists. Add the new note to the list in "RunicGame — Visualizations" yourself.

Running it again on the same source rewrites the page; the note is never overwritten.
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "Visualizations"
HELPER = ROOT / "tools" / "templates" / "embed-helper.html"
HELPER_MARK = "RunicDocs embed helper"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.min.js"

SKELETON = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light}body{margin:0;font:14px system-ui,-apple-system,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
"""

MERMAID_LOADER = f"""<script src="{MERMAID}"></script>
<script>
(function () {{
  var t = document.documentElement.getAttribute("data-theme");
  var dark = t === "dark" || (t !== "light" && window.matchMedia("(prefers-color-scheme: dark)").matches);
  mermaid.initialize({{ startOnLoad: false, securityLevel: "strict", theme: dark ? "dark" : "default" }});
  mermaid.run({{ querySelector: "pre.mermaid" }});
}})();
</script>"""

NOTE = """---
title: {title_yaml}
tags:
  - "visualization"
created: "{today}"
modified: "{today}"
---

{description}

<iframe class="runic-viz" src="{file}" title="{title_attr}" loading="lazy"></iframe>

<a href="{file}" target="_blank" rel="noopener" data-router-ignore data-no-popover="true">Open {title} on its own page</a>
"""


def standalone(html: str) -> str:
    if not re.match(r"\s*<!doctype html", html, re.I):
        html = SKELETON + html.strip() + "\n</body>\n</html>\n"
    html = re.sub(r'src="/_runtime/mermaid-[\d.]+\.min\.js"', f'src="{MERMAID}"', html)
    additions = []
    if 'class="mermaid"' in html and "mermaid" not in "".join(re.findall(r"<script[^>]*src=\"[^\"]*\"", html)):
        additions.append(MERMAID_LOADER)
    if HELPER_MARK not in html:
        additions.insert(0, HELPER.read_text(encoding="utf-8").strip())
    if additions:
        block = "\n".join(additions) + "\n"
        i = html.lower().rfind("</body>")
        html = html[:i] + block + html[i:] if i >= 0 else html + "\n" + block
    return html


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", type=Path)
    ap.add_argument("name", help="file name without extension, e.g. latency-feel-lab")
    ap.add_argument("--title", help="also create the note with this title")
    ap.add_argument("--description", default="", help="the note's opening line")
    args = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.name):
        sys.exit("NAME must be lowercase words joined by hyphens, e.g. latency-feel-lab")
    OUT.mkdir(parents=True, exist_ok=True)
    page = OUT / f"{args.name}.htm"
    page.write_text(standalone(args.source.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"Wrote {page.relative_to(ROOT)}")
    if args.title:
        note = OUT / (re.sub(r'[*"\\/<>:|?#^\[\]]', "", args.title) + ".md")
        if note.exists():
            print(f"{note.relative_to(ROOT)} exists; left as it is")
        else:
            note.write_text(NOTE.format(title_yaml=f'"{args.title}"', today=date.today().isoformat(),
                                        description=args.description or f"{args.title}.", file=page.name,
                                        title_attr=args.title.replace('"', "&quot;"), title=args.title),
                            encoding="utf-8")
            print(f"Wrote {note.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
