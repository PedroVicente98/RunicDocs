#!/usr/bin/env python3
"""
Build content/Visualizations/slice-map.htm, the interactive dependency graph of the vertical-slice roadmap.

    python3 tools/build_slice_map.py

What comes from where:
- slices and their packages: Architecture/Vertical-slice roadmap.md (read with sync_development.read_slices)
- package needs: the work-package tables in the Architecture (sync_development.read_packages)
- done packages, package names and issue links: the generated notes in content/Development/ (run
  tools/sync_development.py first to refresh them from GitHub). Without those notes the map still builds, with
  nothing done and no links.

Slice A depends on slice B when a package of A needs a package of B. The page draws the transitive reduction of
those dependencies (no edge that is a shortcut through another slice) and lays the slices out in levels, the
level being the longest chain of slices before it. The deploy workflow runs this before every build, so the site
never shows a stale map; run it yourself to see the result in the vault.

Only content/Visualizations/slice-map.htm is written, and only when its content changes. Its extension is .htm because
Quartz drops .html from the files it copies, and the site would then send the page as a download.
"""
import json
import re
import sys
from functools import lru_cache
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_development import ROADMAP, read_packages, read_slices  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEV = ROOT / "content" / "Development"
TEMPLATE = ROOT / "tools" / "templates" / "slice-map.html"
HELPER = ROOT / "tools" / "templates" / "embed-helper.html"
OUT = ROOT / "content" / "Visualizations" / "slice-map.htm"
SWEEPS = 12  # barycenter sweeps for the order of slices inside a level


def read_status():
    """Slice issue links, package names, issue links and done flags from the generated Development notes."""
    slice_issue, pkg = {}, {}
    for path in DEV.glob("Slice *.md"):
        text = path.read_text(encoding="utf-8")
        m = re.search(r'^slice: "([^"]+)"', text, re.M)
        if not m:
            continue
        i = re.search(r'^issue: "([^"]+)"', text, re.M)
        slice_issue[m.group(1)] = i.group(1) if i else ""
        for p in re.finditer(r"^- \[([ x])\] \*\*([A-Z]+-\d+)\*\* · (.+?) · (?:\[([^\]]+)\]\(([^)]+)\)|[^·]+) · ", text, re.M):
            pkg[p.group(2)] = dict(done=p.group(1) == "x", short=p.group(3).strip(),
                                   issue=[p.group(4) or "", p.group(5) or ""])
    return slice_issue, pkg


def build_graph(slices, packages):
    ids = [s["id"] for s in slices]
    order = {s: i for i, s in enumerate(ids)}
    owner = {p: s["id"] for s in slices for p in s["packages"]}
    unknown = sorted({p for s in slices for p in s["packages"] if p not in packages})
    if unknown:
        sys.exit(f"Packages in the roadmap with no row in the package tables: {', '.join(unknown)}")
    deps = {s: set() for s in ids}
    for s in slices:
        for p in s["packages"]:
            for n in packages[p]["needs"]:
                if n not in owner:
                    sys.exit(f"{p} needs {n}, which no slice lists")
                if owner[n] != s["id"]:
                    deps[s["id"]].add(owner[n])

    @lru_cache(None)
    def ancestors(s):
        out = set()
        for t in deps[s]:
            out |= {t} | ancestors(t)
        return frozenset(out)

    for s in ids:
        if s in ancestors(s):
            sys.exit(f"Slice {s} depends on itself through its packages' needs")

    @lru_cache(None)
    def level(s):
        return 0 if not deps[s] else 1 + max(level(t) for t in deps[s])

    reduced = {s: sorted((t for t in deps[s] if not any(t in ancestors(u) for u in deps[s] if u != t)), key=order.get)
               for s in ids}
    return ids, order, owner, deps, reduced, {s: level(s) for s in ids}


def lay_out(ids, order, reduced, level):
    """Horizontal slot of each slice: barycenter ordering inside each level, then shifted to start at 0."""
    kids = {s: [] for s in ids}
    for s, ts in reduced.items():
        for t in ts:
            kids[t].append(s)
    rows = [[s for s in ids if level[s] == lv] for lv in range(max(level.values()) + 1)]
    slots = max(len(r) for r in rows) + 1
    x = {}

    def place(row, desired):
        items = sorted(row, key=lambda s: (desired[s], order[s]))
        xs = [desired[s] for s in items]
        for _ in range(2):
            for i in range(len(xs)):
                xs[i] = max(xs[i], 0 if i == 0 else xs[i - 1] + 1)
            for i in range(len(xs) - 1, -1, -1):
                xs[i] = min(xs[i], slots - 1 if i == len(xs) - 1 else xs[i + 1] - 1)
        for s, v in zip(items, xs):
            x[s] = v

    for r in rows:
        off = (slots - len(r)) / 2
        for i, s in enumerate(r):
            x[s] = off + i
    for _ in range(SWEEPS):
        for r in rows[1:]:
            place(r, {s: sum(x[t] for t in reduced[s]) / len(reduced[s]) if reduced[s] else x[s] for s in r})
        for r in reversed(rows[:-1]):
            place(r, {s: 0.5 * x[s] + 0.5 * sum(x[c] for c in kids[s]) / len(kids[s]) if kids[s] else x[s] for s in r})
    low = min(x.values())
    x = {s: round(v - low, 3) for s, v in x.items()}
    return x, int(max(x.values())) + 1


def main():
    slices, packages = read_slices(), read_packages()
    ids, order, owner, deps, reduced, level = build_graph(slices, packages)
    x, slots = lay_out(ids, order, reduced, level)
    slice_issue, status = read_status()
    m = re.search(r'^modified: "([^"]+)"', ROADMAP.read_text(encoding="utf-8"), re.M)
    data = dict(
        roadmapModified=m.group(1) if m else "",
        slots=slots,
        slices=[dict(id=s["id"], name=s["name"], result=s["runnable"], owner=s["owners"], pkgs=s["packages"],
                     issue=slice_issue.get(s["id"], ""), lvl=level[s["id"]], x=x[s["id"]],
                     needs=sorted(deps[s["id"]], key=order.get), red=reduced[s["id"]]) for s in slices],
        pkgs={p: dict(n=status.get(p, {}).get("short") or packages[p]["what"], needs=packages[p]["needs"], s=owner[p],
                      iss=status.get(p, {}).get("issue", ["", ""]), done=status.get(p, {}).get("done", False))
              for s in slices for p in s["packages"]},
    )
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = TEMPLATE.read_text(encoding="utf-8").replace("/*DATA*/", payload, 1)
    page = page.replace("<!--EMBED-HELPER-->", HELPER.read_text(encoding="utf-8").strip(), 1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists() and OUT.read_text(encoding="utf-8") == page:
        print(f"{OUT.relative_to(ROOT)} is up to date")
    else:
        OUT.write_text(page, encoding="utf-8")
        print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"{len(ids)} slices, {len(data['pkgs'])} packages, {sum(len(v) for v in deps.values())} dependencies, "
          f"{max(level.values()) + 1} levels, {sum(1 for p in data['pkgs'].values() if p['done'])} packages done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
