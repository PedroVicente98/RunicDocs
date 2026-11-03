#!/usr/bin/env python3
"""
Regenerate content/Development/ from the Architecture and the GitHub issues.

    python3 tools/sync_development.py                 # fetch the issues with gh (needs access to the three repos)
    python3 tools/sync_development.py --issues DIR    # use saved issues: DIR/RunicEngine.jsonl, ... (one issue per line)

What comes from where:
- slices (name, runnable result, what they prove, owners, Godot) and their order: Architecture/Vertical-slice roadmap.md
- packages (what, done when, needs, slice): the tables in Architecture/Modules, work packages and the implementation
  contract (Engine, Platform, Game).md
- status and links: the GitHub issues of RunicEngine, RunicPlatform and RunicGame. A package is done when its issue is
  closed; "ready" is the status:ready label. A slice is done when its issue is closed, in progress when one of its
  packages is done.

Only content/Development/ is written. A note whose text didn't change keeps its dates.
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCH = ROOT / "content" / "Architecture"
OUT = ROOT / "content" / "Development"
ROADMAP = ARCH / "Vertical-slice roadmap.md"
PACKAGES = ARCH / "Modules, work packages and the implementation contract (Engine, Platform, Game).md"
OWNER = "PedroVicente98"
REPOS = ["RunicEngine", "RunicPlatform", "RunicGame"]
PROJECT = "https://github.com/users/PedroVicente98/projects/7"
DOC_NOTE = "RunicGame — Development"
OVERVIEW = "Development overview"
TODAY = date.today().isoformat()


def plain(s: str) -> str:
    """Cell text without the escapes the Google Docs export added."""
    s = re.sub(r"\\([.+_=\-#*])", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def table_rows(text: str):
    for line in text.splitlines():
        if line.startswith("|") and not line.startswith("| :"):
            yield [c.strip() for c in line.strip().strip("|").split("|")]


def read_slices():
    slices = []
    for c in table_rows(ROADMAP.read_text()):
        if len(c) < 6 or c[0] == "Slice":
            continue
        m = re.match(r"^(\d+[a-z]?\+?)\.?\s+(.*)$", plain(c[0]))
        if not m:
            continue
        slices.append(dict(id=m.group(1), name=m.group(2), runnable=plain(c[1]), proves=plain(c[2]),
                           packages=[p.strip() for p in plain(c[3]).split(",") if p.strip()],
                           owners=plain(c[4]), godot=plain(c[5])))
    return slices


def read_packages():
    packages, section = {}, None
    for line in PACKAGES.read_text().splitlines():
        if line.startswith("#### "):
            section = line[5:].strip()
        elif line.startswith("| ") and section and not line.startswith("| :"):
            c = [x.strip() for x in line.strip().strip("|").split("|")]
            if len(c) < 5 or c[0] == "ID":
                continue
            needs = [n.strip() for n in plain(c[3]).split(",") if n.strip() and n.strip() not in ("None", "—", "-")]
            packages[c[0]] = dict(id=c[0], section=section, what=plain(c[1]), done=plain(c[2]), needs=needs,
                                  slice=plain(c[4]))
    return packages


def fetch_issues(saved: Path | None):
    issues = []
    for repo in REPOS:
        if saved:
            lines = (saved / f"{repo}.jsonl").read_text().splitlines()
        else:
            lines = []
            for page in range(1, 20):  # page by page: the session proxy can't follow gh's --paginate links
                out = subprocess.run(["gh", "api", "-X", "GET", f"repos/{OWNER}/{repo}/issues", "-f", "state=all",
                                      "-f", "per_page=100", "-f", f"page={page}", "--jq", ".[]"],
                                     capture_output=True, text=True, check=True).stdout.splitlines()
                lines += out
                if len(out) < 100:
                    break
        for line in lines:
            i = json.loads(line)
            if "pull_request" in i:
                continue
            i["_repo"] = repo
            issues.append(i)
    return issues


def index_issues(issues):
    slices, packages = {}, {}
    for i in issues:
        labels = {l["name"] for l in i["labels"]}
        info = dict(repo=i["_repo"], number=i["number"], url=i["html_url"], closed=i["state"] == "closed",
                    ready="status:ready" in labels)
        if "type:slice" in labels:
            m = re.match(r"Slice (\S+) · ", i["title"])
            if m:
                slices[m.group(1)] = info
        elif "type:package" in labels:
            m = re.match(r"([A-Z]+-\d+) · (.*)", i["title"])
            if m:
                info["short"] = m.group(2).strip()
                packages[m.group(1)] = info
    return slices, packages


def note_name(s):
    return f"Slice {s['id']} · {s['name']}"


def file_name(name):
    return re.sub(r'[*"\\/<>:|?#^\[\]]', "", name) + ".md"


def issue_link(info):
    return f"[{info['repo']}#{info['number']}]({info['url']})"


def render(frontmatter_lines, created, modified, body):
    return ("---\n" + "\n".join(frontmatter_lines + [f'created: "{created}"', f'modified: "{modified}"'])
            + "\n---\n" + body)


def write_note(name, frontmatter_lines, body):
    """Write a note; keep its dates when the text is unchanged, and always keep its created date."""
    path = OUT / file_name(name)
    created = modified = TODAY
    if path.exists():
        old = path.read_text()
        c = re.search(r'^created: "([^"]+)"', old, re.M)
        m = re.search(r'^modified: "([^"]+)"', old, re.M)
        if c:
            created = c.group(1)
        if m and render(frontmatter_lines, created, m.group(1), body) == old:
            modified = m.group(1)
    path.write_text(render(frontmatter_lines, created, modified, body))
    return path


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--issues", type=Path, help="folder with saved issues (RunicEngine.jsonl, ...) instead of gh")
    args = ap.parse_args()

    slices, packages = read_slices(), read_packages()
    slice_issues, package_issues = index_issues(fetch_issues(args.issues))
    slice_of = {pid: s for s in slices for pid in s["packages"]}

    problems = []
    for s in slices:
        for pid in s["packages"]:
            if pid not in packages:
                problems.append(f"slice {s['id']} lists {pid}, which has no row in the work-package tables")
            if pid not in package_issues:
                problems.append(f"{pid} has no GitHub issue")
        if s["id"] not in slice_issues:
            problems.append(f"slice {s['id']} has no GitHub issue")
    for pid in package_issues:
        if pid not in packages:
            problems.append(f"issue for {pid} has no row in the work-package tables")

    OUT.mkdir(parents=True, exist_ok=True)
    written = set()
    summary = []
    for n, s in enumerate(slices):
        name = note_name(s)
        sinfo = slice_issues.get(s["id"])
        pinfos = [package_issues.get(pid) for pid in s["packages"]]
        done = sum(1 for p in pinfos if p and p["closed"])
        total = len(s["packages"])
        if sinfo and sinfo["closed"]:
            status = "Done"
        elif done:
            status = "In progress"
        else:
            status = "Not started"
        summary.append((s, name, status, done, total))

        prev_link = f"← [[{note_name(slices[n - 1])}]]" if n > 0 else ""
        next_link = f"[[{note_name(slices[n + 1])}]] →" if n + 1 < len(slices) else ""
        nav = " · ".join(x for x in (prev_link, f"[[{DOC_NOTE}|All slices]]", next_link) if x)

        lines = []
        head = [f"**Slice:** {s['id']}", f"**Status:** {status}", f"**Packages done:** {done} of {total}",
                f"**Owners:** {s['owners']}"]
        if sinfo:
            head.append(f"**Issue:** {issue_link(sinfo)}")
        lines += [" · ".join(head), "", nav, ""]
        lines += [f"**Runnable result:** {s['runnable']}", "", f"**Proves:** {s['proves']}", ""]
        if s["godot"] and s["godot"] != "—":
            lines += [f"**Godot:** {s['godot']}", ""]
        lines += ["### Packages", ""]
        for pid, pinfo in zip(s["packages"], pinfos):
            p = packages.get(pid, {})
            box = "x" if pinfo and pinfo["closed"] else " "
            label = pinfo["short"] if pinfo else p.get("what", "")
            state = "done" if pinfo and pinfo["closed"] else ("ready to start" if pinfo and pinfo["ready"] else "not started")
            link = f" · {issue_link(pinfo)}" if pinfo else " · no issue"
            lines.append(f"- [{box}] **{pid}** · {label}{link} · {state}")
            if p.get("what"):
                lines.append(f"    - {p['what']}")
            if p.get("done"):
                lines.append(f"    - **Done when:** {p['done']}")
            needs = []
            for nid in p.get("needs", []):
                ns = slice_of.get(nid)
                needs.append(nid if ns is None or ns is s else f"[[{note_name(ns)}|{nid}]]")
            lines.append(f"    - **Needs:** {', '.join(needs) if needs else 'nothing'}")
        lines += ["", f"*Generated by `tools/sync_development.py` from the [[Vertical-slice roadmap]], the work packages "
                      f"and the GitHub issues. Change those, then run it again.*", ""]
        fm = [f"title: {yaml_str(name)}", "aliases:", f"  - {yaml_str('Slice ' + s['id'])}", "tags:",
              '  - "development"', '  - "slice"', f'  - "progress/{status.lower().replace(" ", "-")}"',
              f"slice: {yaml_str(s['id'])}", f"status: {yaml_str(status)}", f"owners: {yaml_str(s['owners'])}"]
        if sinfo:
            fm.append(f"issue: {yaml_str(sinfo['url'])}")
        written.add(write_note(name, fm, "\n" + "\n".join(lines)).name)

    # the document's note: progress and the checklist of slices
    all_pids = [pid for s in slices for pid in s["packages"]]
    by_repo = {}
    for pid in all_pids:
        info = package_issues.get(pid)
        repo = info["repo"] if info else "no issue"
        d, t = by_repo.get(repo, (0, 0))
        by_repo[repo] = (d + (1 if info and info["closed"] else 0), t + 1)
    slices_done = sum(1 for x in summary if x[2] == "Done")
    pk_done = sum(d for d, _ in by_repo.values())
    ready = [pid for pid in all_pids if package_issues.get(pid, {}).get("ready") and not package_issues[pid]["closed"]]
    repos_line = ", ".join(f"{r.replace('Runic', '')} {d} of {t}" for r, (d, t) in by_repo.items())
    lines = [
        "",
        "The development plan: the slices of the [[Vertical-slice roadmap]] and the packages of "
        "[[Modules, work packages and the implementation contract (Engine, Platform, Game)|Modules and work packages]], "
        f"with their status from the GitHub issues of RunicEngine, RunicPlatform and RunicGame ([GitHub Project]({PROJECT})). "
        "A slice is small, ends in something runnable and testable, and is done when its packages are merged and its "
        "result passes. Each slice note lists its packages; [[Development overview]] shows them all on one page.",
        "",
        f"**Progress:** {slices_done} of {len(slices)} slices done · {pk_done} of {len(all_pids)} packages done "
        f"({repos_line}) · {len(ready)} packages ready to start: {', '.join(ready) if ready else 'none'}.",
        "",
        "**Slices**",
        "",
    ]
    for s, name, status, done, total in summary:
        box = "x" if status == "Done" else " "
        extra = " · in progress" if status == "In progress" else ""
        lines.append(f"- [{box}] [[{name}]] · {done}/{total} packages · {s['owners']}{extra}")
    lines += ["", "*Generated by `tools/sync_development.py`: a package is done when its issue is closed, a slice when "
                  "its issue is closed. Close the issues on GitHub, then run the script again.*", ""]
    fm = [f"title: {yaml_str(DOC_NOTE)}", "tags:", '  - "development"']
    written.add(write_note(DOC_NOTE, fm, "\n".join(lines)).name)

    lines = ["", f"Every slice of [[{DOC_NOTE}]], shown in full in its own box, in roadmap order.", ""]
    for _, name, *_ in summary:
        lines += [f"![[{name}]]", ""]
    fm = [f"title: {yaml_str(OVERVIEW)}", "tags:", '  - "development"']
    written.add(write_note(OVERVIEW, fm, "\n".join(lines)).name)

    stale = [p for p in OUT.glob("*.md") if p.name not in written]
    for p in stale:
        p.unlink()
    print(f"{len(slices)} slices, {len(all_pids)} packages; {slices_done} slices and {pk_done} packages done; "
          f"wrote {len(written)} notes, removed {len(stale)}")
    for p in problems:
        print("warning:", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
