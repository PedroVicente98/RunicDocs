#!/usr/bin/env python3
"""
Open the built site the way GitHub Pages serves it, under a subpath (/RunicDocs/),
and check that the graph, the explorer and search get their data and link inside
the site.

    python3 tools/check_site.py PUBLIC_DIR BASE_PATH      e.g.  .quartz/public RunicDocs

Needs Python Playwright (pip install playwright) and Chrome, or Playwright's own
Chromium. Exits with status 1 when a check fails.
"""
import http.server
import subprocess
import sys
import threading
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

PUBLIC = Path(sys.argv[1]).resolve()
BASE = "/" + sys.argv[2].strip("/")
PAGES = ["/", "/Vision/Combat", "/Ideias/NAV-01-Naval-Raid"]


class Handler(http.server.SimpleHTTPRequestHandler):
    """Serve PUBLIC at BASE; like GitHub Pages, /a/b also finds a/b.html."""

    def translate_path(self, path):
        path = urllib.parse.unquote(path.split("?", 1)[0].split("#", 1)[0])
        if path != BASE and not path.startswith(BASE + "/"):
            return str(PUBLIC / "__outside_base__")
        p = PUBLIC / path[len(BASE):].lstrip("/")
        if p.is_dir():
            p = p / "index.html"
        elif not p.exists() and p.with_name(p.name + ".html").exists():
            p = p.with_name(p.name + ".html")
        return str(p)

    def log_message(self, *args):
        pass


def launch(pw):
    args = ["--enable-unsafe-swiftshader", "--use-angle=swiftshader"]  # software WebGL for the graph
    try:
        return pw.chromium.launch(channel="chrome", args=args)
    except Exception:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)
        return pw.chromium.launch(args=args)


def main() -> int:
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    root = f"http://127.0.0.1:{server.server_port}"
    failures = []

    with sync_playwright() as pw:
        browser = launch(pw)
        page = browser.new_page()
        errors, missing = [], []
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("response", lambda r: missing.append(r.url) if r.status >= 400 else None)

        for path in PAGES:
            url = root + BASE + urllib.parse.quote(path)
            errors.clear()
            missing.clear()
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(2000)
            basepath = page.evaluate("document.body.dataset.basepath")
            pages_in_index = page.evaluate("fetchData.then(d => Object.keys(d).length)")
            graph_canvases = page.locator(".graph-container canvas").count()
            explorer_links = page.eval_on_selector_all(".explorer-content a[href]", "els => els.map(e => e.getAttribute('href'))")
            outside = [h for h in page.eval_on_selector_all("a[href]", "els => els.map(e => e.getAttribute('href'))")
                       if h.startswith("/") and not h.startswith(BASE + "/") and h != BASE]
            print(f"{path}: basepath={basepath!r}, pages in contentIndex={pages_in_index}, graph canvases={graph_canvases}, "
                  f"explorer links={len(explorer_links)}, links outside {BASE}={len(outside)}")
            if basepath != BASE:
                failures.append(f"{path}: body data-basepath is {basepath!r}, expected {BASE!r}")
            if pages_in_index < 100:
                failures.append(f"{path}: contentIndex has only {pages_in_index} pages")
            if graph_canvases == 0:
                failures.append(f"{path}: the graph drew no canvas")
            if not explorer_links:
                failures.append(f"{path}: the explorer has no links")
            if outside:
                failures.append(f"{path}: links that leave the site: {outside[:5]}")
            for e in errors:
                failures.append(f"{path}: console error: {e[:200]}")
            for m in missing:
                failures.append(f"{path}: not found: {m}")

        # search: type a word and check where the results point
        page.goto(root + BASE + "/", wait_until="networkidle")
        try:
            page.locator(".search-button").first.click()
            page.locator(".search-bar").first.fill("Combat")
            page.wait_for_timeout(1500)
            results = page.eval_on_selector_all(".result-card:not(.no-match)", "els => els.map(e => e.getAttribute('href'))")
            print(f"search 'Combat': {len(results)} results, first: {results[:3]}")
            if not results:
                failures.append("search returned no results for 'Combat'")
            bad = [h for h in results if h and h.startswith("/") and not h.startswith(BASE + "/")]
            if bad:
                failures.append(f"search results leave the site: {bad[:5]}")
        except Exception as e:  # the search UI's selectors differ from what this check expects
            failures.append(f"search could not be checked: {str(e).splitlines()[0][:200]}")
        browser.close()
    server.shutdown()

    if failures:
        print("\nFAILED:")
        for f in failures:
            print(" -", f)
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
