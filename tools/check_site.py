#!/usr/bin/env python3
"""
Open the built site the way GitHub Pages serves it, under a subpath (/RunicDocs/),
and check that the graph, the explorer and search get their data and link inside
the site:

- the local graph is drawn around the page itself, with its neighbours (not one unknown dot),
  and the full graph holds every page;
- no plugin remembers a page under the base path ("RunicDocs/Vision/Combat");
- every link on the checked pages and in the search results opens a page (no 404, such as
  /RunicDocs/RunicDocs/);
- embedded notes (![[Note]]) are filled in and shown in a scroll box.

    python3 tools/check_site.py PUBLIC_DIR BASE_PATH      e.g.  .quartz/public RunicDocs

Needs Python Playwright (pip install playwright) and Chrome, or Playwright's own
Chromium. Exits with status 1 when a check fails.
"""
import http.server
import subprocess
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

PUBLIC = Path(sys.argv[1]).resolve()
BASE = "/" + sys.argv[2].strip("/")
PAGES = ["/", "/Vision/Combat", "/Ideias/NAV-01-Naval-Raid", "/Ideias/RunicGame-—-Ideias"]
EMBED_PAGE = "/Ideias/RunicGame-—-Ideias"  # the Ideias list embeds every idea

# The graph plugin loads d3 from a CDN as window.d3. Wrap d3.forceSimulation to record the node ids
# of each graph it lays out, so the check can see which nodes the local and the full graph hold.
RECORD_GRAPHS = """
(() => {
  const sims = (window.__graphSims = []);
  let d3;
  const wrap = (v) => {
    if (v && typeof v.forceSimulation === "function" && !v.__checkWrapped) {
      const real = v.forceSimulation;
      v.forceSimulation = function (nodes) {
        sims.push((nodes || []).map((n) => n.id));
        return real.apply(this, arguments);
      };
      v.__checkWrapped = true;
    }
    return v;
  };
  Object.defineProperty(window, "d3", {
    configurable: true,
    get() { return wrap(d3); },
    set(v) { d3 = v; },
  });
})();
"""

REMEMBERED_SLUGS = """
(() => {
  const read = (store, key) => { try { return JSON.parse(store.getItem(key) || "null"); } catch (e) { return null; } };
  const tabs = (read(sessionStorage, "stacked-pages-state") || {}).tabs || [];
  return {
    "graph visited pages": read(localStorage, "graph-visited") || [],
    "stacked-pages tabs": tabs.map((t) => t.slug),
  };
})()
"""


def page_id(path: str) -> str:
    """The id the graph gives a page: its slug, with the home page as "/"."""
    return path.strip("/") or "/"


def status(url: str) -> int:
    try:
        with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(url) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


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
        page.add_init_script(RECORD_GRAPHS)
        errors, missing = [], []
        links = {}  # absolute URL -> the page it was found on
        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("response", lambda r: missing.append(r.url) if r.status >= 400 else None)

        for path in PAGES:
            url = root + BASE + urllib.parse.quote(path)
            errors.clear()
            missing.clear()
            page.goto(url, wait_until="networkidle")
            try:
                page.wait_for_function("window.__graphSims.length > 0", timeout=15000)
            except Exception:
                pass
            page.wait_for_timeout(1000)
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

            # the local graph: drawn around this page, with its neighbours
            here = page_id(path)
            sims = page.evaluate("window.__graphSims")
            local = sims[-1] if sims else []
            print(f"{path}: local graph nodes={len(local)}, has {here!r}={here in local}")
            if not sims:
                failures.append(f"{path}: the local graph laid out no nodes")
            elif here not in local:
                failures.append(f"{path}: the local graph is not drawn around {here!r}; its nodes: {local[:5]}")
            elif len(local) < 2:
                failures.append(f"{path}: the local graph shows only {local}")

            # the full graph: every page
            try:
                before = len(sims)
                page.locator(".global-graph-icon").first.click()
                page.wait_for_function(f"window.__graphSims.length > {before}", timeout=15000)
                full = page.evaluate("window.__graphSims")[-1]
                print(f"{path}: full graph nodes={len(full)}")
                if len(full) < 100 or here not in full:
                    failures.append(f"{path}: the full graph has {len(full)} nodes, {'with' if here in full else 'without'} {here!r}")
                page.keyboard.press("Escape")
            except Exception as e:
                failures.append(f"{path}: the full graph could not be checked: {str(e).splitlines()[0][:200]}")

            # pages that plugins remember must be slugs, not paths under the base
            base_slug = BASE.strip("/")
            for what, slugs in page.evaluate(REMEMBERED_SLUGS).items():
                bad = [s for s in slugs if s == base_slug or s.startswith(base_slug + "/")]
                if bad:
                    failures.append(f"{path}: {what} include the base path: {bad[:5]}")

            # embedded notes: filled in (no "Transclude of ..." placeholder left) and in a scroll box
            embeds = page.evaluate("""() => [...document.querySelectorAll("article .transclude")].map(e => {
                const st = getComputedStyle(e);
                return { filled: !e.querySelector(":scope > a.transclude-inner"), overflow: st.overflowY, maxHeight: st.maxHeight };
            })""")
            if embeds:
                unfilled = sum(not e["filled"] for e in embeds)
                unboxed = sum(e["overflow"] != "auto" or e["maxHeight"] == "none" for e in embeds)
                print(f"{path}: embedded notes={len(embeds)}, not filled in={unfilled}, without a scroll box={unboxed}")
                if unfilled:
                    failures.append(f"{path}: {unfilled} embedded notes were not filled in")
                if unboxed:
                    failures.append(f"{path}: {unboxed} embedded notes have no scroll box (quartz-styles/custom.scss not applied?)")
            if path == EMBED_PAGE and len(embeds) < 100:
                failures.append(f"{path}: expected about 100 embedded ideas, found {len(embeds)}")

            for h in page.eval_on_selector_all("a[href]", "els => els.map(e => e.href)"):
                if h.startswith(root):
                    links.setdefault(h.split("#", 1)[0], path)
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
            for h in page.eval_on_selector_all(".result-card:not(.no-match)", "els => els.map(e => e.href)"):
                if h.startswith(root):
                    links.setdefault(h.split("#", 1)[0], "search 'Combat'")
            print(f"search 'Combat': {len(results)} results, first: {results[:3]}")
            if not results:
                failures.append("search returned no results for 'Combat'")
            bad = [h for h in results if h and h.startswith("/") and not h.startswith(BASE + "/")]
            if bad:
                failures.append(f"search results leave the site: {bad[:5]}")
        except Exception as e:  # the search UI's selectors differ from what this check expects
            failures.append(f"search could not be checked: {str(e).splitlines()[0][:200]}")
        browser.close()

    # every link found above must open a page
    broken = [(u, where) for u, where in sorted(links.items()) if status(u) >= 400]
    print(f"links opened: {len(links)}, broken: {len(broken)}")
    for u, where in broken[:20]:
        failures.append(f"{where}: link to a missing page: {urllib.parse.unquote(u[len(root):])}")
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
