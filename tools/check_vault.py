#!/usr/bin/env python3
"""
Check the RunicDocs vault: every wikilink resolves to a note or an attachment,
every #anchor matches a heading in its target note, every frontmatter block
parses as YAML, no two notes share a file name (ignoring case and folder), so
short links like [[Combat]] always point to one note, and the vault's folders
exist (Lore/ and Quest Design/ are never removed, even when empty).

    python3 tools/check_vault.py [content_dir]

Link resolution follows Obsidian and Quartz ("shortest" mode): a link with a
path is taken from the vault root; a bare name must match exactly one file.
Anchors are compared with the GitHub slug rules Quartz uses for headings.
Exits with status 1 when something is broken.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # the YAML check is skipped without PyYAML
    yaml = None

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "content")
LINK_RE = re.compile(r"(!?)\[\[([^\]]+?)\]\]")
REQUIRED_FOLDERS = ["Vision", "Architecture", "Ideias", "Archive", "Lore", "Quest Design"]


def slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def headings(md: str) -> set:
    out, in_code = set(), False
    for line in md.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
        elif not in_code:
            m = re.match(r"^#{1,6} (.*)$", line)
            if m:
                out.add(slug(m.group(1).strip()))
    return out


def main() -> int:
    notes = {p.relative_to(ROOT).with_suffix("").as_posix(): p for p in ROOT.rglob("*.md") if ".obsidian" not in p.parts}
    files = {p.name for p in ROOT.rglob("*") if p.is_file() and ".obsidian" not in p.parts}
    by_name = defaultdict(list)
    for key in notes:
        by_name[key.split("/")[-1]].append(key)
    heads = {}
    broken, bad_anchor, bad_yaml, total = [], [], [], 0
    lower = defaultdict(list)
    for key in notes:
        lower[key.split("/")[-1].lower()].append(key)
    dupes = [(name, ", ".join(keys)) for name, keys in lower.items() if len(keys) > 1]
    missing = [(f, "folder missing") for f in REQUIRED_FOLDERS if not (ROOT / f).is_dir()]
    for key, path in notes.items():
        text = path.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            end = text.find("\n---\n", 4)
            if end < 0:
                bad_yaml.append((key, "unterminated frontmatter"))
            elif yaml:
                try:
                    yaml.safe_load(text[4:end])
                except yaml.YAMLError as e:
                    bad_yaml.append((key, str(e).split("\n")[0]))
        in_code = False
        for line in text.split("\n"):
            if line.startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for m in LINK_RE.finditer(line):
                total += 1
                embed, inner = m.group(1), m.group(2)
                target = re.split(r"\\?\|", inner, maxsplit=1)[0]
                target, _, anchor = target.partition("#")
                target = target.strip()
                if embed and not target.endswith(".md") and "." in target.split("/")[-1]:
                    if target.split("/")[-1] not in files:
                        broken.append((key, inner))
                    continue
                if not target:
                    resolved = key
                elif target in notes:
                    resolved = target
                elif "/" not in target and len(by_name.get(target, [])) == 1:
                    resolved = by_name[target][0]
                elif target.endswith("/") and target + "index" in notes:
                    resolved = target + "index"
                else:
                    broken.append((key, inner))
                    continue
                if anchor and not anchor.startswith("^"):
                    if resolved not in heads:
                        heads[resolved] = headings(notes[resolved].read_text(encoding="utf-8"))
                    if slug(anchor.strip()) not in heads[resolved]:
                        bad_anchor.append((key, inner))
    print(f"{len(notes)} notes, {total} links checked")
    for title, items in (("Broken links", broken), ("Anchors with no matching heading", bad_anchor),
                         ("Frontmatter that does not parse", bad_yaml), ("Note names used more than once", dupes),
                         ("Required folders missing", missing)):
        print(f"{title}: {len(items)}")
        for k, v in items[:40]:
            print(f"  {k}  ->  {v}")
    return 1 if (broken or bad_anchor or bad_yaml or dupes or missing) else 0


if __name__ == "__main__":
    sys.exit(main())
