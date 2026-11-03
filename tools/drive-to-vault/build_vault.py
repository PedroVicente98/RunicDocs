#!/usr/bin/env python3
"""
Split the RunicGame and RunicEngine Drive documents into the RunicDocs vault.

    python3 build_vault.py <export_dir> <content_dir>

<export_dir> holds each Google Doc exported as text/markdown (File > Download >
Markdown), named as in DOCS below. <content_dir> is rebuilt from scratch; its
.obsidian folder is kept.

The text is moved, not rewritten: every section is cut out of its document by
its heading and written into a note. The only text changes are listed in
H2_RENAMES and TEXT_EDITS (each with the number of matches it must have), the
Markdown cleanup in normalize() and the links added by inject_links().

Vault layout
- Vision/, Architecture/: H1 = folder, H2 = note, H3 and below stay inside the
  note with their original level. Each folder has a note named after the
  document with its introduction and its sections in order.
- Ideias/: one note per idea ID with the text unchanged (the ID is the note's
  alias), the archived and discarded table, and the document's own note.
- Archive/: the original appendices, one note each, text unchanged.
- Lore/, Quest Design/: one note linking to the RunicGame repository.
Every note name is unique in the vault, so [[Combat]] always finds one note.

Links added: "Section › Subsection" references, "(see X)" references to a
heading, idea IDs, document names and Google Docs links of these documents.
"""
from __future__ import annotations

import base64
import json
import re
import shutil
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

SNAPSHOT = "2026-11-03"
DRIVE_FOLDER = "https://drive.google.com/drive/folders/1hSflbWXn8Y2Ox-3QPFpXjrVkMo5warhv"
RUNICGAME_DOCS = "https://github.com/PedroVicente98/RunicGame/tree/main/docs/RunicWorld"
REQUIRED_FOLDERS = ["Vision", "Architecture", "Ideias", "Archive", "Lore", "Quest Design"]

DOCS = [
    dict(key="vision", kind="split", file="RunicGame_Complete_MMORPG_Vision.md",
         title="RunicGame — Complete MMORPG Vision", folder="Vision", tags=["vision"],
         drive="1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk", created="2026-10-13", modified="2026-10-30"),
    dict(key="arch", kind="split", file="RunicEngine_Technical_Architecture_v4.md",
         title="RunicEngine — Technical Architecture", folder="Architecture", tags=["architecture"],
         drive="1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA", created="2026-10-14", modified="2026-10-30"),
    dict(key="ideias", kind="ideas", file="RunicGame_Ideias.md",
         title="RunicGame — Ideias", folder="Ideias", tags=["ideias"],
         drive="17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow", created="2026-10-17", modified="2026-11-03"),
    dict(key="nodes", kind="archive", file="RunicGame_Appendix_Nodes_Economy_and_Exploration.md",
         title="RunicGame — Appendix: Nodes, Economy and Exploration", folder="Archive", tags=["archive"],
         drive="1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA", created="2026-10-19", modified="2026-10-30"),
    dict(key="pipeline", kind="archive", file="RunicGame_Appendix_Content_Pipeline_and_Art_Direction.md",
         title="RunicGame — Appendix: Content Pipeline and Art Direction", folder="Archive", tags=["archive"],
         drive="1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ", created="2026-10-26", modified="2026-10-30"),
    dict(key="ping", kind="archive", file="RunicGame_Appendix_Ping_Resolution.md",
         title="RunicGame — Appendix: Ping Resolution", folder="Archive", tags=["archive"],
         drive="1iYe10T523upQnBfv91Pk3dL1FC6TuyF7hmdGg6ZG5Ys", created="2026-10-21", modified="2026-10-21"),
    dict(key="security", kind="archive", file="RunicEngine_Appendix_Security.md",
         title="RunicEngine — Appendix: Security", folder="Archive", tags=["archive"],
         drive="1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ", created="2026-10-22", modified="2026-10-22"),
    dict(key="db", kind="archive", file="RunicEngine_Appendix_Database_Layout.md",
         title="RunicEngine — Appendix: Database Layout", folder="Archive", tags=["archive"],
         drive="1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8", created="2026-10-26", modified="2026-10-30"),
    dict(key="lore", kind="redirect", title="RunicGame — Lore", folder="Lore", tags=["lore"],
         drive="1WfyE78jlRm-So9YndQvtplTwua3p8bWY26uIqMAwjYE", created="2026-10-27", modified="2026-10-30"),
    dict(key="quests", kind="redirect", title="RunicGame — Quest Design", folder="Quest Design", tags=["quest-design"],
         drive="11UTu2AtZl00OAmg6sMzjS8xcUDvXXoU9PAlhPsbOwJk", created="2026-10-27", modified="2026-10-30"),
]

# H2s must be unique in the vault; these are the only renamed headings.
H2_RENAMES = {
    "vision": {"About this document": "About the Vision"},
    "arch": {"About this document": "About the Architecture"},
}

# The only wording changes (English throughout; no "v4" in titles). (pattern, replacement, expected matches)
TEXT_EDITS = {
    "vision": [
        (r"\| War \(Guerra\) \|", "| War |", 1),
        (r"\| Defense \(Vigília\) \|", "| Defense |", 1),
        (r"\| Vitality \(Restauração\) \|", "| Vitality |", 1),
        (r"\| Arcane \(Arcano\) \|", "| Arcane |", 1),
        (r"\| Occultism \(Ocultismo\) \|", "| Occultism |", 1),
        (r"Canção(?= doesn)", "Song", 1),
        (r"Elementalismo(?= merged)", "Elementalism", 1),
        (r"Sombra(?=['’]s stealth)", "Shadow", 1),
        (r"Caça(?= \(marks and traps\))", "Hunt", 1),
        (r"\| Canção, Elementalismo and Sombra as Disciplines \|", "| Song, Elementalism and Shadow as Disciplines |", 1),
        (r"RunicEngine — Technical Architecture v4", "RunicEngine — Technical Architecture", 1),
        (r"\bex\.:", "e.g.", 21),
        (r"\bEx\.:", "E.g.", 8),
    ],
    "arch": [
        (r"Espada \\\+ Escudo, Lança 2H and Varinha \\\+ Foco Arcano", r"Sword \\+ Shield, Spear and Wand \\+ Focus", 1),
        (r"\bex\.:", "e.g.", 2),
    ],
}

# The Vision's two diagrams were images with Portuguese text; they are redrawn in English as Mermaid.
DIAGRAMS = {
    "resolvedor de skills · 5 fontes, 2 checagens": """```mermaid
flowchart TB
  subgraph sources["Rule sources (same format)"]
    S1["Skill and tree choices"]
    S2["Class role passive"]
    S3["Class signature"]
    S4["Item effect (or extracted)"]
    S5["Mount, glider or wing"]
  end
  subgraph server["Execution on the server"]
    A1["1 · Activation — checks the caster<br/>Conditions: previous skill, resources, buffs, position<br/>Changes cost, casting or variant (e.g. Grab with no cast time)"]
    A2["2 · Timeline in ticks (30 Hz)<br/>Startup, active and recovery, scaled by the weapon's profile<br/>Shape and reach create the hit volume or the projectile"]
    A3["3 · Hit — checks the target<br/>Target conditions: Stagger becomes Trip, Frozen is consumed<br/>Damage per component against resistances; Resolve decides the CC"]
    A4["4 · Authoritative events<br/>Damage, effects and new states become conditions for the next skills"]
  end
  sources --> A1
  sources --> A3
  A1 --> A2 --> A3 --> A4
```

*Skill resolver · 5 sources, 2 checks: rules from five sources are checked at two moments, activation and hit.*""",
    "fluxo de recursos · 4 atividades, 1 destino": """```mermaid
flowchart TB
  PVE["PvE — dungeons and raids<br/>raid-exclusive materials, drops and equipment"]
  PVP["Faction PvP<br/>gold, honor, special resources and contribution theft"]
  CRAFT["Endgame crafting<br/>raid mats + regional and special resources become<br/>weapons and armor used in raids and wars"]
  OW["Open world and housing<br/>gathering, farms, rare mobs, gold and regional resources"]
  TP["Trade packs<br/>carry production between regions;<br/>pay gold and special resources"]
  PVE --> CRAFT
  PVP --> CRAFT
  OW --> CRAFT
  TP --> CRAFT
  OW -- "production becomes cargo" --> TP
  TP -- "the cargo draws PvP" --> PVP
```

*Resource flow · 4 activities, 1 destination: PvE, PvP, the open world and trade packs converge in endgame crafting.*""",
}

# Mentions of a document by name link to its note (first mention per note).
DOC_MENTIONS = [
    (r"RunicGame — Visão Completa do MMORPG", "vision"),
    (r"RunicGame — Complete MMORPG Vision", "vision"),
    (r"RunicEngine — Technical Architecture(?: v\d)?", "arch"),
    (r"(?:Technical )?Architecture v4", "arch"),
    (r"RunicGame — Ideias", "ideias"),
    (r"\bIdeias\b", "ideias"),
    (r"RunicGame — Lore", "lore"),
    (r"(?:RunicGame — )?Quest Design", "quests"),
    (r"(?:RunicGame — )?(?:Appendix: )?Nodes, Economy and Exploration", "nodes"),
    (r"(?:RunicGame — )?(?:Appendix: )?Content Pipeline and Art Direction", "pipeline"),
    (r"(?:RunicGame — )?(?:Appendix: )?Ping Resolution", "ping"),
    (r"(?:RunicEngine — )?Appendix: Security", "security"),
    (r"(?:RunicEngine — )?(?:Appendix: )?Database Layout", "db"),
    (r"\bthe game vision\b", "vision"),
    (r"\bthe Vision\b", "vision"),
]

# Text fixes for known glitches in the exports (equation objects that export badly).
FIXES = {
    "db": [(r"ledger_op=\$1WHEREgran\{t\}_\{i\}d=\$1", "ledger_op=$1 WHERE grant_id=$1")],
    "ping": [
        (r"(?<![\w$])US(?=0\.007 to 0\.105)", "US$0.025 per hour per accelerator plus US$"),
        (r"player-hour and US(?=3\.50 per hour)", "player-hour and US$0.035 per GB, 1,000 concurrent players add about US$"),
    ],
}

# --------------------------------------------------------------------------- helpers

def yaml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def safe_name(title: str, strip_number: bool = True, maxlen: int = 70) -> str:
    t = title
    if strip_number:
        t = re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", t)
    t = t.replace("&", " and ").replace("—", " ").replace("–", " ").replace("’", "").replace("'", "")
    t = "".join(ch if (ch.isalnum() or ch in " -") else " " for ch in t)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > maxlen:
        t = t[:maxlen].rsplit(" ", 1)[0]
    return t


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s


def clean_heading(t: str) -> str:
    t = t.strip()
    t = t.replace("**", "")
    t = re.sub(r"^\*(.*)\*$", r"\1", t)
    t = re.sub(r"\\([\\.+\-_#()\[\]!*$<>=|~`{}])", r"\1", t)
    return re.sub(r"\s+", " ", t).strip()


def anchor_text(heading: str) -> str:
    """Heading text usable after '#' in a wikilink (Obsidian and Quartz)."""
    a = heading.replace(":", " ").replace("#", " ").replace("|", " ").replace("[", " ").replace("]", " ").replace("^", " ")
    return re.sub(r"\s+", " ", a).strip()


def norm_key(s: str) -> str:
    s = clean_heading(s).lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return s.strip()


UNESCAPE_RE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!<>=|~$&:;,/\"'])")


def unescape_md(s: str) -> str:
    return UNESCAPE_RE.sub(r"\1", s)


# --------------------------------------------------------------------------- normalization

def extract_images(md: str, key: str, out_attach: Path) -> str:
    defs = {}
    for m in re.finditer(r"^\[(image\d+)\]:\s*<data:image/(\w+);base64,([^>]+)>\s*$", md, re.M):
        defs[m.group(1)] = (m.group(2), m.group(3))
    md = re.sub(r"^\[(image\d+)\]:\s*<data:image/\w+;base64,[^>]+>\s*$\n?", "", md, flags=re.M)

    def repl(m):
        alt, ref = m.group(1), m.group(2)
        if ref not in defs:
            return m.group(0)
        if alt in DIAGRAMS:
            return DIAGRAMS[alt]
        ext, data = defs[ref]
        name = f"{key}-{slugify(alt)[:50].strip('-') or ref}.{ 'png' if ext == 'png' else ext }"
        out_attach.mkdir(parents=True, exist_ok=True)
        (out_attach / name).write_bytes(base64.b64decode(data))
        caption = unescape_md(alt)
        return f"![[{name}]]\n*{caption}*"

    return re.sub(r"!\[([^\]]*)\]\[(image\d+)\]", repl, md)


CODE_LINE_RE = re.compile(
    r"(;\s*$|\{\s*$|^\s*\}|^\s*//|::|->|^\s{2,}\S|\)\s*(const\s*)?\{|^\s*#include|^\s*</?\w[\w.]*[ >/]"
    r"|^\s*(func|extends|class|void|struct|enum|using|return|if|for|var|const|constexpr|auto|template|static|inline|virtual|namespace|BT::|std::)\b"
    r"|^\s*\w[\w:<>*&]*\s+[\w:~]+\(.*\)\s*[;{]?\s*$|:=)"
)
LIST_START_RE = re.compile(r"^\s*([*+\-]|\d+\.)\s")


def is_code_line(s: str) -> bool:
    return bool(CODE_LINE_RE.search(unescape_md(s)))


TICK_RE = re.compile(r"^(\s*)(`+)(.*?)\2\s*$")


def is_tick_line(s: str) -> bool:
    return bool(TICK_RE.match(s.rstrip()))


def untick(s: str) -> str:
    m = TICK_RE.match(s.rstrip())
    if not m:
        return s.rstrip()
    inner = m.group(3)
    if len(m.group(2)) > 1 and inner.startswith(" ") and inner.endswith(" "):
        inner = inner[1:-1]
    return m.group(1) + inner


def guess_lang(lines: list[str]) -> str:
    nb = [l for l in lines if l.strip()]
    if not nb:
        return "text"
    text = "\n".join(nb)
    semi = sum(1 for l in nb if re.search(r"[;{]\s*(//.*)?$", l) or re.match(r"^\s*[}\])]+\s*[;,]?\s*(//.*)?$", l))
    if nb[0].lstrip().startswith(("{", "[")) and re.search(r'"[\w.\-]+"\s*:', text):
        return "json"
    if re.search(r"^\s*(if|elseif|else|endif)\s*\(|target_compile_options|target_link_libraries|add_library\(|runic_add_module\(", text, re.M) \
            and not re.search(r";\s*(//.*)?$", text, re.M):
        return "cmake"
    if re.search(r"^\s*(@tool|extends\s|func\s+\w+\(.*\)\s*(->\s*[\w\[\]]+)?\s*:|var\s+\w+\s*:?=)", text, re.M) and "{" not in text:
        return "gdscript"
    if re.search(r"^\s*func\s*\(|context\.Context|\berr != nil\b", text, re.M):
        return "go"
    if re.match(r"^\s*<\w", nb[0]) and not semi:
        return "xml"
    keyish = sum(1 for l in nb if re.match(r"^\s*(-\s+)?[\w\-.]+:(\s|$)", l) or l.strip() == "---" or l.lstrip().startswith("# "))
    if semi == 0 and keyish * 10 >= len(nb) * 6:
        return "yaml"
    if semi > 0 or re.search(r"^\s*//", text, re.M):
        return "cpp"
    return "text"


COMPATIBLE = {"text"}


def fence_code(md: str) -> str:
    """Turn the code samples Google exports as plain paragraphs into fenced blocks."""
    lines = md.split("\n")
    paras = []  # (start, end) inclusive, non-blank runs
    i = 0
    while i < len(lines):
        if lines[i].strip():
            j = i
            while j + 1 < len(lines) and lines[j + 1].strip():
                j += 1
            # whole-line backtick code directly followed by prose: split it off
            if is_tick_line(lines[i]):
                t = i
                while t <= j and is_tick_line(lines[t]):
                    t += 1
                if i + 1 < t <= j:
                    paras.append((i, t - 1))
                    lines.insert(t, "")
                    i = t + 1
                    continue
            paras.append((i, j))
            i = j + 1
        else:
            i += 1

    def kind(p):
        a, b = p
        block = lines[a:b + 1]
        first = block[0]
        if first.startswith(("#", "|", "![[", ">", "$$")) or first.startswith("```"):
            return None
        if all(is_tick_line(l) for l in block) and (len(block) >= 2 or re.search(r"[;{}]\s*`\s*$", first)):
            return "tick"
        if LIST_START_RE.match(first):
            return None
        soft = len(block) >= 2 and all(l.endswith("  ") for l in block[:-1])
        codey = sum(1 for l in block if is_code_line(l))
        if soft and codey * 2 >= len(block):
            return "code"
        if len(block) == 1:
            s = unescape_md(first.rstrip())
            if re.match(r"^\s*(//.*|[}\])]+;?|.*[;{]|\w[\w:.<>]*\(.*\);?)\s*$", s) and len(s) < 200 and not re.search(r"\w\.\s*$", s):
                return "code1"
        if soft and len(block) >= 3:
            if sum(1 for l in block if re.match(r"^\s{2,}\S", l)) * 2 >= len(block):
                return "code"
        return None

    def body_of(p, tick):
        a, b = p
        return [untick(l) if tick or is_tick_line(l) else unescape_md(l.rstrip()) for l in lines[a:b + 1]]

    kinds = [kind(p) for p in paras]
    plang = [guess_lang(body_of(p, k == "tick")) if k else None for p, k in zip(paras, kinds)]
    groups = []
    cur = []
    for idx, k in enumerate(kinds):
        if k in ("code", "tick", "code1"):
            gap_ok = cur and paras[idx][0] - paras[cur[-1]][1] <= 2
            same_kind = cur and (k == "tick") == (kinds[cur[0]] == "tick")
            langs = {plang[x] for x in cur} - COMPATIBLE
            lang_ok = cur and (plang[idx] in COMPATIBLE or not langs or plang[idx] in langs or kinds[idx] == "code1")
            if cur and gap_ok and same_kind and lang_ok:
                cur.append(idx)
            else:
                if cur:
                    groups.append(cur)
                cur = [idx]
        else:
            if cur:
                groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    groups = [g for g in groups if any(kinds[i] in ("code", "tick") for i in g)]

    out = list(lines)
    for g in reversed(groups):
        a = paras[g[0]][0]
        b = paras[g[-1]][1]
        tick = kinds[g[0]] == "tick"
        body = []
        for ln in lines[a:b + 1]:
            if not ln.strip():
                body.append("")
            else:
                body.append(untick(ln) if (tick or is_tick_line(ln)) else unescape_md(ln.rstrip()))
        out[a:b + 1] = [f"```{guess_lang(body)}"] + body + ["```"]
    return "\n".join(out)


def normalize(md: str, key: str, attach: Path) -> str:
    md = md.replace("\r\n", "\n")
    for pat, rep in FIXES.get(key, []):
        md = re.sub(pat, rep.replace("\\", "\\\\"), md)
    md = extract_images(md, key, attach)
    out = []
    for ln in md.split("\n"):
        m = re.match(r"^(#{1,6})\s+(.*)$", ln)
        if m:
            out.append(f"{m.group(1)} {clean_heading(m.group(2))}")
            continue
        # Google exports indented lists as blockquotes: "> * item"
        m = re.match(r"^>\s?(\s*(?:[*+\-]|\d+\.)\s.*|\s*)$", ln)
        if m:
            ln = m.group(1)
        out.append(ln)
    md = "\n".join(out)
    if key not in ("ideias", "lore", "quests"):
        md = fence_code(md)
    # escape bare dollar signs (LaTeX in Obsidian and Quartz), outside code fences
    res, in_code = [], False
    for ln in md.split("\n"):
        if ln.startswith("```"):
            in_code = not in_code
        elif re.match(r"^\$\$.*\$\$\s*$", ln):
            # display math: Google exports thin and four-per-em spaces, which KaTeX can't typeset
            ln = ln.replace("\u2009", "\\,").replace("\u2005", "\\,")
        elif not in_code:
            ln = re.sub(r"(?<!\\)\$", r"\\$", ln)
            ln = re.sub(r"(^|\s)#(\d)", r"\1\\#\2", ln) if not ln.startswith("#") else ln
            ln = ln.replace("%%", "%​%")
        res.append(ln)
    return "\n".join(res).strip() + "\n"


# --------------------------------------------------------------------------- outline tree

class Node:
    def __init__(self, level: int, title: str):
        self.level = level
        self.title = title
        self.lines: list[str] = []
        self.children: list[Node] = []
        self.parent: Node | None = None
        self.doc: dict | None = None
        self.path: str | None = None  # vault path without .md
        self.is_folder = False
        self.container: Node | None = None  # node whose note holds this node
        self.base = ""   # file name before de-duplication
        self.ctx = ""    # parent name used to de-duplicate
        self.name = ""   # final, unique file name

    def size(self) -> int:
        return sum(len(l) + 1 for l in self.lines) + sum(c.size() for c in self.children)

    def walk(self):
        yield self
        for c in self.children:
            yield from c.walk()

    def heading_path(self) -> list[str]:
        p, n = [], self
        while n and n.parent is not None:
            p.append(n.title)
            n = n.parent
        return list(reversed(p))


def parse_tree(md: str, doc: dict) -> Node:
    lines = md.split("\n")
    heads = []
    in_code = False
    for i, l in enumerate(lines):
        if l.startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            m = re.match(r"^(#{1,6}) (.*)$", l)
            if m:
                heads.append((i, len(m.group(1)), m.group(2).strip()))
    root = Node(0, doc["title"])
    root.doc = doc
    start = 0
    if heads and heads[0][0] == next((k for k, l in enumerate(lines) if l.strip()), 0) and heads[0][1] == 1:
        start = heads[0][0] + 1  # document title line
        heads = heads[1:]
    first = heads[0][0] if heads else len(lines)
    root.lines = lines[start:first]
    base = min((h[1] for h in heads), default=1)
    stack = [root]
    for n, (i, lvl, title) in enumerate(heads):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        node = Node(lvl - base + 1, title)
        node.doc = doc
        node.lines = lines[i + 1:end]
        while stack[-1].level >= node.level:
            stack.pop()
        node.parent = stack[-1]
        stack[-1].children.append(node)
        stack.append(node)
    return root


def trim(lines: list[str]) -> list[str]:
    a, b = 0, len(lines)
    while a < b and not lines[a].strip():
        a += 1
    while b > a and not lines[b - 1].strip():
        b -= 1
    return lines[a:b]


def render_subtree(node: Node, base_level: int) -> list[str]:
    out = trim(node.lines)
    for ch in node.children:
        lvl = min(6, ch.level - base_level + 1)
        out += ["", f"{'#' * lvl} {ch.title}", ""]
        out += render_subtree(ch, base_level)
    return out



# --------------------------------------------------------------------------- file names and links

FORBIDDEN = '*"\\/<>:|?#^[]'


def file_name(title: str) -> str:
    """A heading as a file name: drop only the characters Obsidian or Windows reject (in practice ':')."""
    t = "".join(" " if ch in FORBIDDEN else ch for ch in clean_heading(title))
    return re.sub(r"\s+", " ", t).strip()


def wl(path: str, text: str | None = None, anchor: str | None = None, table: bool = False) -> str:
    """Wikilink by file name (unique in the vault). `path` may be a full vault path or a name."""
    name = path.rsplit("/", 1)[-1]
    target = name + (f"#{anchor_text(anchor)}" if anchor else "")
    if text is None or (text == name and not anchor):
        return f"[[{target}]]"
    text = text.replace("[", "(").replace("]", ")").replace("|", "/")
    return f"[[{target}{chr(92) + '|' if table else '|'}{text}]]"


for d in DOCS:
    d["url"] = f"https://docs.google.com/document/d/{d['drive']}/edit"
    d["note"] = f"{d['folder']}/{file_name(d['title'])}"
DOC = {d["key"]: d for d in DOCS}


# --------------------------------------------------------------------------- notes

class Note:
    def __init__(self, path, title, body, fm, kind, doc=None, self_ids=()):
        self.path, self.title, self.body, self.fm, self.kind, self.doc = path, title, body, fm, kind, doc
        self.self_ids = set(self_ids)

    def render(self) -> str:
        fm = OrderedDict([("title", self.title)])
        fm.update(self.fm)
        fm.setdefault("created", SNAPSHOT)
        fm.setdefault("modified", SNAPSHOT)
        out = ["---"]
        for k, v in fm.items():
            if v is None or v == [] or v == "":
                continue
            if isinstance(v, list):
                out.append(f"{k}:")
                out += [f"  - {yaml_str(str(x))}" for x in v]
            else:
                out.append(f"{k}: {yaml_str(str(v))}")
        out.append("---")
        return "\n".join(out) + "\n\n" + self.body.strip() + "\n"


NOTES: "OrderedDict[str, Note]" = OrderedDict()


def add_note(n: Note):
    name = n.path.rsplit("/", 1)[-1].lower()
    clash = [p for p in NOTES if p.rsplit("/", 1)[-1].lower() == name]
    if clash:
        raise SystemExit(f"note name used twice: {n.path} and {clash[0]}")
    NOTES[n.path] = n


def doc_fm(doc: dict, tags=()) -> OrderedDict:
    return OrderedDict(tags=list(dict.fromkeys(doc["tags"] + list(tags))), source=doc["title"],
                       source_url=doc["url"], created=doc["created"], modified=doc["modified"])


OWNER_RE = re.compile(r"\s*\(((?:Engine|Game|Platform)(?:, (?:Engine|Game|Platform)| on (?:Engine|Game|Platform))*)\)\s*$")


def owner_tags(title: str) -> list[str]:
    m = OWNER_RE.search(title)
    if not m:
        return []
    return [f"repo/{x.strip().lower()}" for x in re.split(r",| on ", m.group(1)) if x.strip()]


def apply_edits(md: str, key: str) -> str:
    for pat, rep, count in TEXT_EDITS.get(key, []):
        md, n = re.subn(pat, rep, md)
        if n != count:
            raise SystemExit(f"{key}: edit {pat!r} matched {n} times, expected {count}")
    return md


# --------------------------------------------------------------------------- Vision and Architecture: H1 = folder, H2 = note

def render_children(node: Node, offset: int) -> list[str]:
    """The node's own text, then every subsection with its original heading level."""
    out = trim(node.lines)
    for ch in node.children:
        out += ["", f"{'#' * min(6, ch.level + offset)} {ch.title}", ""]
        out += render_children(ch, offset)
    return out


def build_split(doc: dict, md: str):
    root = parse_tree(md, doc)
    levels, in_code = [], False
    for l in md.split("\n"):
        if l.startswith("```"):
            in_code = not in_code
        elif not in_code and re.match(r"^#{1,6} ", l):
            levels.append(len(l) - len(l.lstrip("#")))
    offset = min(levels[1:]) - 1  # the first heading is the document title; H2 -> level 1
    doc["root"], doc["offset"] = root, offset
    renames = H2_RENAMES.get(doc["key"], {})
    root.path, root.container = doc["note"], root
    for ch in root.children:
        ch.title = renames.get(ch.title, ch.title)
        ch.path = f"{doc['folder']}/{file_name(ch.title)}"
        for d in ch.walk():
            d.container = ch
    contents = []
    for ch in root.children:
        contents.append(f"- {wl(ch.path, ch.title)}")
        for g in ch.children:
            contents.append(f"  - {wl(ch.path, g.title, anchor=g.title)}")
        tags = owner_tags(ch.title)
        add_note(Note(ch.path, ch.title, "\n".join(render_children(ch, offset)), doc_fm(doc, tags), "section", doc))
    body = trim(root.lines) + ["", "**Contents**", ""] + contents
    fm = doc_fm(doc)
    add_note(Note(root.path, doc["title"], "\n".join(body), fm, "doc", doc))


def find_heading(key: str, title: str, within: Node | None = None):
    """Nodes of a document whose heading is `title`, or starts with it followed by ':', ',' or ' ('."""
    want = norm_key(title)
    base = within or DOC[key]["root"]
    exact, prefix = [], []
    for n in base.walk():
        if n is base and within is None:
            continue
        t = clean_heading(n.title)
        k = norm_key(t)
        if k == want:
            exact.append(n)
        elif t.lower().startswith(title.lower()) and t[len(title):len(title) + 2] in (": ", ", ", " (") :
            prefix.append(n)
    return exact or prefix


def target(node: Node):
    """(note path, anchor) of a heading node."""
    c = node.container
    return (c.path, None) if c is node else (c.path, node.title)


def resolve_path(parts: list[str], key="vision"):
    """'Combat › Resolve: hard and light CC' -> node, walking down the outline."""
    node = DOC[key]["root"]
    for p in parts:
        found = [c for c in node.children if norm_key(c.title) == norm_key(p)] or find_heading(key, p, node)
        if not found:
            return None
        node = found[0]
    return node


# --------------------------------------------------------------------------- Ideias: one note per ID, text unchanged

ID_LINE_RE = re.compile(r"^\*\*ID:\*\*\s*([A-Z]+-\d+)\s*·\s*\*\*Status:\*\*\s*(.+?)(?:\s*·\s*\*\*Game vision:\*\*\s*(.+?))?\s*$")
IDEAS: "OrderedDict[str, dict]" = OrderedDict()
ARCHIVED: "OrderedDict[str, str]" = OrderedDict()


def status_tag(status: str) -> str:
    s = status.lower()
    for k, tag in (("in game vision", "in-game-vision"), ("partial", "partial"), ("being", "being-designed"),
                   ("open", "open"), ("archived", "archived"), ("discarded", "discarded")):
        if s.startswith(k):
            return "status/" + tag
    return "status/" + re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def build_ideas(doc: dict, md: str):
    lines = md.split("\n")
    heads = [(i, len(m.group(1)), m.group(2).strip()) for i, l in enumerate(lines)
             for m in [re.match(r"^(#{1,6}) (.*)$", l)] if m]
    preamble = trim(lines[heads[0][0] + 1:heads[1][0]])
    outline = []  # ("idea", id, depth) | ("group", title, depth, intro) | ("archived",)
    stack = []
    archived_lines = []
    for n, (i, lvl, title) in enumerate(heads[1:], 1):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        block = lines[i + 1:end]
        first = next((l for l in block if l.strip()), "")
        while stack and stack[-1][0] >= lvl:
            stack.pop()
        depth = sum(1 for _, kind in stack if kind == "idea")  # list nesting: only ideas inside ideas
        m = ID_LINE_RE.match(first)
        if m:
            iid = m.group(1)
            rest = list(block)
            rest.remove(first)
            IDEAS[iid] = dict(id=iid, title=title, status=m.group(2).strip(), vision=(m.group(3) or "").strip(),
                              id_line=first, body=trim(rest),
                              path=f"{doc['folder']}/{iid} {file_name(title)}")
            outline.append(("idea", iid, depth))
            kind = "idea"
        elif norm_key(title).startswith("archived"):
            archived_lines = trim(block)
            outline.append(("archived", title, depth))
            kind = "archived"
        else:
            outline.append(("group", title, depth, trim(block)))
            kind = "group"
        stack.append((lvl, kind))
    for l in archived_lines:
        m = re.match(r"^\|\s*([A-Z]+-\d+)\s*\|\s*([^|]*?)\s*\|", l)
        if m:
            ARCHIVED[m.group(1)] = m.group(2)
    archived_path = f"{doc['folder']}/Archived and Discarded ideas"
    doc["archived_path"] = archived_path

    for iid, idea in IDEAS.items():
        fm = OrderedDict(aliases=[iid], tags=["ideias", "idea", status_tag(idea["status"])], id=iid,
                         status=idea["status"], game_vision=idea["vision"] or None, source=doc["title"],
                         source_url=doc["url"], created=doc["created"], modified=doc["modified"])
        body = [vision_field_links(idea["id_line"], idea["vision"]), ""] + idea["body"]
        add_note(Note(idea["path"], f"{iid} · {idea['title']}", "\n".join(body), fm, "idea", doc, {iid}))
    fm = OrderedDict(aliases=list(ARCHIVED), tags=["ideias", "status/archived", "status/discarded"],
                     source=doc["title"], source_url=doc["url"], created=doc["created"], modified=doc["modified"])
    add_note(Note(archived_path, "Archived and Discarded ideas", "\n".join(archived_lines), fm, "idea", doc,
                  set(ARCHIVED)))
    # the document's own note: its preamble, then every entry in document order
    body = preamble + ["", "**Contents**", ""]
    for item in outline:
        if item[0] == "idea":
            idea = IDEAS[item[1]]
            body.append(f"{'  ' * item[2]}- {wl(idea['path'], idea['id'] + ' · ' + idea['title'])}")
        elif item[0] == "archived":
            body.append(f"{'  ' * item[2]}- {wl(archived_path, item[1])}")
        else:
            body += ["", f"**{item[1]}**", ""] + item[3] + [""]
    add_note(Note(doc["note"], doc["title"], "\n".join(body), doc_fm(doc), "doc", doc))


def vision_field_links(id_line: str, field: str) -> str:
    """The idea's 'Game vision:' field, each 'Section › Subsection' as a wikilink. The text stays the same."""
    if not field:
        return id_line
    out = []
    for part in [p.strip() for p in field.split(";")]:
        m = re.match(r"^(.*?)\s*(\(.*\))?$", part)
        main, paren = m.group(1).strip(), m.group(2) or ""
        steps = [x.strip() for x in main.split("›")]
        node = resolve_path(steps)
        while node is None and len(steps) > 1:  # a step that isn't a heading: link the closest one above it
            steps = steps[:-1]
            node = resolve_path(steps)
            STATS["› link to a parent heading"] += 1
        if node is None:
            UNRESOLVED.append(("game vision", part))
            out.append(part)
            continue
        path, anchor = target(node)
        out.append(wl(path, main, anchor) + (f" {paren}" if paren else ""))
    return id_line.replace(field, "; ".join(out))


# --------------------------------------------------------------------------- Archive, Lore and Quest Design

def build_archive(doc: dict, md: str):
    lines = md.split("\n")
    first = next(i for i, l in enumerate(lines) if l.strip())
    if lines[first].startswith("# "):
        lines = lines[first + 1:]
    fm = OrderedDict(tags=["archive", "appendix"], source=doc["title"], source_url=doc["url"],
                     created=doc["created"], modified=doc["modified"])
    add_note(Note(doc["note"], doc["title"], "\n".join(trim(lines)), fm, "archive", doc))


def build_redirect(doc: dict):
    body = f"""This document lives in the **RunicGame** repository: [RunicGame › docs/RunicWorld]({RUNICGAME_DOCS})."""
    fm = OrderedDict(tags=doc["tags"] + ["redirect"], moved_to=RUNICGAME_DOCS)
    add_note(Note(doc["note"], doc["title"], body, fm, "redirect", doc))


def build_home():
    g = lambda k: DOC[k]["note"]
    arch = [d for d in DOCS if d["kind"] == "archive"]
    body = f"""The RunicGame and RunicEngine design documentation, kept as Markdown. It started on {SNAPSHOT} as an export of
the documents in the [RunicMMOEngine Drive folder]({DRIVE_FOLDER}).

- {wl(g('vision'), 'RunicGame — Complete MMORPG Vision')}: how the game works. The Vision states the rules.
- {wl(g('arch'), 'RunicEngine — Technical Architecture')}: how the Engine, the Platform and the Game build them; it links to the Vision for the rules.
- {wl(g('ideias'), 'RunicGame — Ideias')}: the ideas inbox, one note per idea ID, kept whole as history.
- {wl(g('lore'), 'RunicGame — Lore')} and {wl(g('quests'), 'RunicGame — Quest Design')}: in the RunicGame repository.
- Archive: the original appendices, unchanged: {", ".join(wl(d['note'], d['title'].split(': ', 1)[-1]) for d in arch)}.

**How the vault is organized.** A folder is a document (its H1), a note is a section (an H2), and the headings inside a
note are its subsections (H3 and below). Every note name is unique, so a link like `[[Combat]]` always finds the same
note. Each document's main note lists its sections in order.
"""
    add_note(Note("index", "RunicDocs", body, OrderedDict(aliases=["Home"], tags=["home"]), "home"))


# --------------------------------------------------------------------------- links

PROTECT_RE = re.compile(r"(!?\[\[[^\]]*\]\]|!?\[[^\]]*\]\([^)]*\)|`[^`]*`|https?://[^\s)>|]+|<[^>]+>)")
UNRESOLVED: list = []
STATS = defaultdict(int)


def map_segments(line: str, fn):
    parts = PROTECT_RE.split(line)
    for k in range(0, len(parts), 2):
        if parts[k]:
            parts[k] = fn(parts[k])
    return "".join(parts)


def link_note(note: Note, id_re, id_targets, doc_targets):
    out, in_code = [], False
    used_docs = set()
    for line in note.body.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code or re.match(r"^#{1,6} ", line):
            out.append(line)
            continue
        tbl = line.startswith("|")

        def gdoc(m):
            for d in DOCS:
                if d["drive"] == m.group(2) and d["note"] != note.path:
                    STATS["google-doc link"] += 1
                    return wl(d["note"], m.group(1), table=tbl)
            return m.group(0)
        line = re.sub(r"\[([^\]]+)\]\(https://docs\.google\.com/document/d/([\w-]+)[^)]*\)", gdoc, line)

        def see(seg):
            def r(m):
                ref = m.group(2)
                key = note.doc["key"] if note.doc and note.doc["key"] in ("vision", "arch") else "vision"
                here = NOTES_NODE.get(note.path)
                cands = (find_heading(key, ref, here) if here else []) or find_heading(key, ref) or \
                    find_heading("arch" if key == "vision" else "vision", ref)
                uniq = {target(c) for c in cands}
                if len(uniq) != 1:
                    UNRESOLVED.append(("see", note.path, ref))
                    return m.group(0)
                path, anchor = uniq.pop()
                if path == note.path and anchor is None:
                    return m.group(0)
                STATS["see link"] += 1
                return f"{m.group(1)}{wl(path, ref, anchor, tbl)})"
            return re.sub(r"(\(see )([A-Z][\w ,'\-]*?)\)", r, seg)
        if note.kind in ("section", "doc"):
            line = map_segments(line, see)

        def arrows(seg):
            def r(m):
                parts = [p.strip() for p in m.group(0).split("›")]
                for key in ("vision", "arch"):
                    node = resolve_path(parts, key)
                    if node is not None and norm_key(parts[0]) in {norm_key(c.title) for c in DOC[key]["root"].children}:
                        path, anchor = target(node)
                        if path == note.path and anchor is None:
                            return m.group(0)
                        STATS["› link"] += 1
                        return wl(path, m.group(0), anchor, tbl)
                return m.group(0)
            return re.sub(r"[A-Z][\w ,:'()\-]*?(?: › [A-Z][\w ,:'()\-]*?)+(?=[.;)]|\s\(|$)", r, seg)
        line = map_segments(line, arrows)

        def ids(seg):
            def r(m):
                t = m.group(0)
                if t in note.self_ids or id_targets[t] == note.path:
                    return t
                STATS["idea ID link"] += 1
                return wl(id_targets[t], t, table=tbl)
            return id_re.sub(r, seg)
        line = map_segments(line, ids)

        def docs(seg):
            for rx, key in doc_targets:
                tgt = DOC[key]["note"]
                if key in used_docs or tgt == note.path or (note.doc and note.doc["key"] == key):
                    continue
                m = rx.search(seg)
                if m:
                    used_docs.add(key)
                    STATS["document link"] += 1
                    return docs(seg[:m.start()]) + wl(tgt, m.group(0), table=tbl) + docs(seg[m.end():])
            return seg
        line = map_segments(line, docs)
        out.append(line)
    note.body = "\n".join(out)


NOTES_NODE: dict = {}


def inject_links():
    id_targets = {i: d["path"] for i, d in IDEAS.items()}
    id_targets.update({a: DOC["ideias"]["archived_path"] for a in ARCHIVED})
    id_re = re.compile(r"(?<![\w\-/#\[|])(?:" + "|".join(sorted(map(re.escape, id_targets), key=len, reverse=True)) + r")(?![\w-])")
    doc_targets = [(re.compile(rx), key) for rx, key in DOC_MENTIONS]
    for key in ("vision", "arch"):
        for ch in DOC[key]["root"].children:
            NOTES_NODE[ch.path] = ch
    for note in NOTES.values():
        if note.kind in ("archive", "home", "redirect"):
            continue
        link_note(note, id_re, id_targets, doc_targets)


# --------------------------------------------------------------------------- main

def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    keep = None
    if (out / ".obsidian").exists():
        keep = out.parent / ".obsidian-keep"
        if keep.exists():
            shutil.rmtree(keep)
        shutil.copytree(out / ".obsidian", keep)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    if keep:
        shutil.copytree(keep, out / ".obsidian")
        shutil.rmtree(keep)
    attach = out / "attachments"

    for kind in ("split", "archive"):
        for d in DOCS:
            if d["kind"] == kind:
                md = apply_edits(normalize((src / d["file"]).read_text(encoding="utf-8"), d["key"], attach), d["key"])
                (build_split if kind == "split" else build_archive)(d, md)
    d = DOC["ideias"]
    build_ideas(d, normalize((src / d["file"]).read_text(encoding="utf-8"), d["key"], attach))
    for d in DOCS:
        if d["kind"] == "redirect":
            build_redirect(d)
    build_home()
    inject_links()

    for note in NOTES.values():
        p = out / (note.path + ".md")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(note.render(), encoding="utf-8")
    for folder in REQUIRED_FOLDERS:
        (out / folder).mkdir(parents=True, exist_ok=True)

    print(json.dumps(dict(notes=len(NOTES), ideas=len(IDEAS), archived_ids=len(ARCHIVED), links=dict(STATS),
                          unresolved=UNRESOLVED), indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
