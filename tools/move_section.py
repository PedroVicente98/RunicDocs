#!/usr/bin/env python3
"""
Move (cut and paste) or copy a section from one note to another, by its heading.
The text is never rewritten: only the heading levels can shift, and only when
--level asks for it.

    python3 tools/move_section.py SOURCE "HEADING" TARGET [options]

SOURCE and TARGET are note names ("Combat", "RunicEngine — Appendix: Security")
or paths inside content/ ("Architecture/Security.md"). A section is its heading
line plus everything up to the next heading of the same or a higher level.

Options
  --copy              leave the section in SOURCE (use this for Archive/, which stays intact)
  --level N           give the section's heading level N; its subheadings shift by the same amount
  --title "TEXT"      write the heading with a new text (only when a title must change, e.g. to stay unique)
  --after "HEADING"   paste after that section of TARGET (default: at the end of TARGET)
  --before "HEADING"  paste before that heading of TARGET
  --body-only         paste only the section's content, without its heading line
  --create            create TARGET if it doesn't exist (its title is its file name)
  --dry-run           show what would change and write nothing

Examples
  python3 tools/move_section.py "RunicEngine — Appendix: Security" "The client" "Security" --copy --level 3 --create
  python3 tools/move_section.py "RunicGame systems (Game)" "Castles" "Economy, housing and land" --level 3
"""
import argparse
import difflib
import re
import sys
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "content"
HEAD_RE = re.compile(r"^(#{1,6}) (.*?)\s*$")


def find_note(ref: str, must_exist: bool = True) -> Path:
    p = Path(ref)
    if p.suffix == ".md" or "/" in ref:
        p = CONTENT / (ref if ref.endswith(".md") else ref + ".md")
        if must_exist and not p.exists():
            sys.exit(f"no note at {p.relative_to(CONTENT)}")
        return p
    hits = [x for x in CONTENT.rglob("*.md") if x.stem.lower() == ref.lower() and ".obsidian" not in x.parts]
    if not hits and not must_exist:
        sys.exit(f"note '{ref}' doesn't exist; give TARGET as a path (Folder/Name.md) with --create")
    if len(hits) != 1:
        sys.exit(f"note '{ref}': {len(hits)} matches" + "".join(f"\n  {h.relative_to(CONTENT)}" for h in hits))
    return hits[0]


def split_frontmatter(text: str):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end > 0:
            return text[:end + 5], text[end + 5:]
    return "", text


def headings(lines):
    """(index, level, text) of every heading outside code blocks."""
    out, in_code = [], False
    for i, l in enumerate(lines):
        if l.startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            m = HEAD_RE.match(l)
            if m:
                out.append((i, len(m.group(1)), m.group(2)))
    return out


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("**", "")).strip().lower()


def section_range(lines, heading: str):
    hs = headings(lines)
    found = [h for h in hs if norm(h[2]) == norm(heading)]
    if not found:
        sys.exit(f"heading '{heading}' not found; headings here:" + "".join(f"\n  {'#' * l} {t}" for _, l, t in hs))
    if len(found) > 1:
        sys.exit(f"heading '{heading}' appears {len(found)} times; rename one first")
    start, level, _ = found[0]
    end = next((i for i, l, _ in hs if i > start and l <= level), len(lines))
    return start, end, level


def trim(block):
    while block and not block[0].strip():
        block = block[1:]
    while block and not block[-1].strip():
        block = block[:-1]
    return block


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[1], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source")
    ap.add_argument("heading")
    ap.add_argument("target")
    ap.add_argument("--copy", action="store_true")
    ap.add_argument("--level", type=int)
    ap.add_argument("--title")
    ap.add_argument("--after")
    ap.add_argument("--before")
    ap.add_argument("--body-only", action="store_true")
    ap.add_argument("--create", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    src = find_note(a.source)
    tgt = find_note(a.target, must_exist=not a.create)
    if src == tgt:
        sys.exit("source and target are the same note; use --after/--before on a copy instead")
    src_fm, src_body = split_frontmatter(src.read_text(encoding="utf-8"))
    s_lines = src_body.split("\n")
    start, end, level = section_range(s_lines, a.heading)
    block = trim(s_lines[start:end])

    shift = (a.level - level) if a.level else 0
    moved, in_code = [], False
    for k, l in enumerate(block):
        if l.startswith("```"):
            in_code = not in_code
        m = None if in_code else HEAD_RE.match(l)
        if m:
            new_level = len(m.group(1)) + shift
            if not 1 <= new_level <= 6:
                sys.exit(f"--level {a.level} would push '{m.group(2)}' to level {new_level}")
            text = a.title if (k == 0 and a.title) else m.group(2)
            l = f"{'#' * new_level} {text}"
        moved.append(l)
    if a.body_only:
        moved = trim(moved[1:])

    if tgt.exists():
        tgt_fm, tgt_body = split_frontmatter(tgt.read_text(encoding="utf-8"))
    else:
        tgt_fm, tgt_body = f'---\ntitle: "{tgt.stem}"\n---\n', "\n"
    t_lines = tgt_body.rstrip("\n").split("\n")
    if a.after:
        _, at, _ = section_range(t_lines, a.after)
    elif a.before:
        at, _, _ = section_range(t_lines, a.before)
    else:
        at = len(t_lines)
    before, after = trim(t_lines[:at]), trim(t_lines[at:])
    new_t = before + ([""] if before else []) + moved + ([""] + after if after else [])
    new_s = trim(s_lines[:start]) + ([""] if s_lines[end:] and trim(s_lines[:start]) else []) + trim(s_lines[end:])

    new_tgt_text = tgt_fm + ("\n" if tgt_fm else "") + "\n".join(new_t).strip() + "\n"
    new_src_text = src_fm + ("\n" if src_fm else "") + "\n".join(new_s).strip() + "\n"
    rel = lambda p: p.relative_to(CONTENT).as_posix()
    print(f"{'copy' if a.copy else 'move'}: '{a.heading}' ({len(block)} lines) {rel(src)} -> {rel(tgt)}"
          + (f", heading level {level} -> {level + shift}" if shift else ""))
    if a.dry_run:
        old_tgt = tgt.read_text(encoding="utf-8") if tgt.exists() else ""
        sys.stdout.writelines(difflib.unified_diff(old_tgt.splitlines(True), new_tgt_text.splitlines(True),
                                                   rel(tgt), rel(tgt) + " (new)", n=1))
        return
    tgt.parent.mkdir(parents=True, exist_ok=True)
    tgt.write_text(new_tgt_text, encoding="utf-8")
    if not a.copy:
        src.write_text(new_src_text, encoding="utf-8")


if __name__ == "__main__":
    main()
