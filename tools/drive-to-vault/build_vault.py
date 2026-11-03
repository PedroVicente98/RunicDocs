#!/usr/bin/env python3
"""
Build the RunicDocs Obsidian vault (Quartz-ready) from Markdown exports of the
RunicMMOEngine Google Drive documents.

    python3 build_vault.py <source_dir> <content_dir>

<source_dir> holds one Markdown export per document (Google Docs:
File > Download > Markdown), named as in DOCS below. Images may stay embedded
as data URIs; they are extracted to <content_dir>/attachments.

<content_dir> is rebuilt from scratch (its .obsidian folder is kept).

What it produces
- One folder per document, split along the document's own outline. The
  document's main note has the folder's name (Vision/Vision.md), every
  top-level section becomes a note, and very long sections become a folder
  with a main note of the same name that lists their subsections.
- Every file name in the vault is unique (only the home page is index.md), so
  links are short ([[Combat]]). A title used twice gets its parent in
  parentheses: "Ownership (Water system)".
- Documents that live in another repository (Lore, Quest Design) keep their
  folder with a single note that links there.
- RunicGame — Ideias becomes one note per idea ID, with status tags and a link
  to the Vision section that holds it.
- The Architecture's work-package tables become one note per package (with
  links to the packages it needs and the slice that first needs it), and the
  vertical-slice roadmap becomes one note per slice.
- Cross-links everywhere: idea IDs, package IDs, slice numbers, document
  names, Google Docs URLs of the folder's documents and a curated list of game
  and engine terms all become wikilinks.
"""
from __future__ import annotations

import base64
import json
from collections import Counter
import re
import shutil
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

SNAPSHOT = "2026-11-03"
SPLIT_CHARS = 14000  # sections longer than this (with subsections) become folders
MAX_DEPTH = 3

DRIVE_FOLDER = "https://drive.google.com/drive/folders/1hSflbWXn8Y2Ox-3QPFpXjrVkMo5warhv"
RUNICGAME_REPO = "https://github.com/PedroVicente98/RunicGame"
RUNICWORLD_URL = RUNICGAME_REPO + "/tree/main/docs/RunicWorld"

DOCS = [
    dict(key="vision", file="RunicGame_Complete_MMORPG_Vision.md",
         title="RunicGame — Complete MMORPG Vision", short="Vision",
         folder="RunicGame/Vision", drive="1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk",
         created="2026-10-13", modified="2026-10-30", tags=["runicgame", "vision"]),
    # Lore and Quest Design live in the RunicGame repository (docs/RunicWorld); here they keep
    # their folder with one note that points there.
    dict(key="lore", file=None, title="RunicGame — Lore", short="Lore",
         folder="RunicGame/Lore", drive="1WfyE78jlRm-So9YndQvtplTwua3p8bWY26uIqMAwjYE",
         created="2026-10-27", modified="2026-10-30", tags=["runicgame", "lore"], kind="redirect"),
    dict(key="quests", file=None, title="RunicGame — Quest Design",
         short="Quest Design", folder="RunicGame/Quest Design",
         drive="11UTu2AtZl00OAmg6sMzjS8xcUDvXXoU9PAlhPsbOwJk",
         created="2026-10-27", modified="2026-10-30", tags=["runicgame", "quest-design"], kind="redirect"),
    dict(key="ideias", file="RunicGame_Ideias.md", title="RunicGame — Ideias", short="Ideias",
         folder="RunicGame/Ideias", drive="17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow",
         created="2026-10-17", modified="2026-11-03", tags=["runicgame", "ideias"], kind="ideas"),
    dict(key="nodes", file="RunicGame_Appendix_Nodes_Economy_and_Exploration.md",
         title="RunicGame — Appendix: Nodes, Economy and Exploration",
         short="Nodes, Economy and Exploration",
         folder="RunicGame/Appendices/Nodes Economy and Exploration",
         drive="1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA",
         created="2026-10-19", modified="2026-10-30", tags=["runicgame", "appendix"]),
    dict(key="pipeline", file="RunicGame_Appendix_Content_Pipeline_and_Art_Direction.md",
         title="RunicGame — Appendix: Content Pipeline and Art Direction",
         short="Content Pipeline and Art Direction",
         folder="RunicGame/Appendices/Content Pipeline and Art Direction",
         drive="1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ",
         created="2026-10-26", modified="2026-10-30", tags=["runicgame", "appendix"]),
    dict(key="ping", file="RunicGame_Appendix_Ping_Resolution.md",
         title="RunicGame — Appendix: Ping Resolution", short="Ping Resolution",
         folder="RunicGame/Appendices/Ping Resolution",
         drive="1iYe10T523upQnBfv91Pk3dL1FC6TuyF7hmdGg6ZG5Ys",
         created="2026-10-21", modified="2026-10-21", tags=["runicgame", "appendix"]),
    dict(key="arch", file="RunicEngine_Technical_Architecture_v4.md",
         title="RunicEngine — Technical Architecture v4", short="Technical Architecture v4",
         folder="RunicEngine/Architecture", drive="1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA",
         created="2026-10-14", modified="2026-10-30", tags=["runicengine", "architecture"]),
    dict(key="security", file="RunicEngine_Appendix_Security.md",
         title="RunicEngine — Appendix: Security", short="Security",
         folder="RunicEngine/Appendices/Security", drive="1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ",
         created="2026-10-22", modified="2026-10-22", tags=["runicengine", "appendix"]),
    dict(key="db", file="RunicEngine_Appendix_Database_Layout.md",
         title="RunicEngine — Appendix: Database Layout", short="Database Layout",
         folder="RunicEngine/Appendices/Database Layout",
         drive="1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8",
         created="2026-10-26", modified="2026-10-30", tags=["runicengine", "appendix"]),
]
DOC = {d["key"]: d for d in DOCS}
CTX = {"nodes": "Nodes and Economy", "pipeline": "Content Pipeline"}
for d in DOCS:
    d["url"] = f"https://docs.google.com/document/d/{d['drive']}/edit"
    d["hub"] = d["folder"].rsplit("/", 1)[-1]          # the document's main note: Vision/Vision.md
    d["ctx"] = CTX.get(d["key"], d["hub"])             # short name used in "(…)" to tell clashing titles apart
    d["hub_path"] = f"{d['folder']}/{d['hub']}"

PACKAGES_FOLDER = "RunicEngine/Packages"
ROADMAP_FOLDER = "RunicEngine/Roadmap"
PACKAGES_HUB = f"{PACKAGES_FOLDER}/Packages"
ROADMAP_HUB = f"{ROADMAP_FOLDER}/Roadmap"

# Text fixes for known glitches in the source documents.
FIXES = {
    # Google Docs turned "$1 WHERE grant_id=$" into an equation in this SQL line.
    "db": [(r"ledger_op=\$1WHEREgran\{t\}_\{i\}d=\$1", "ledger_op=$1 WHERE grant_id=$1")],
    "ping": [
        # Two amounts in the AWS cost line are Google Docs equation objects; the
        # API returns them empty and the Markdown export runs their words together.
        (r"US\$?0\.025perhourperacceleratorplusUS\$?0\.007", "US$0.025 per hour per accelerator plus US$0.007"),
        (r"US\$?0\.035perGB,1,000concurrentplayersaddaboutUS\$?3\.50", "US$0.035 per GB, 1,000 concurrent players add about US$3.50"),
        (r"(?<![\w$])US(?=0\.007 to 0\.105)", "US$0.025 per hour per accelerator plus US$"),
        (r"player-hour and US(?=3\.50 per hour)", "player-hour and US$0.035 per GB, 1,000 concurrent players add about US$"),
    ],
}

# Curated term links: (regex, doc key, heading path). First occurrence per note.
TERMS = [
    # Vision
    (r"\bDisciplines?\b", "vision", ["Weapon Class System", "Disciplines"]),
    (r"\bloadouts?\b", "vision", ["Weapon Class System", "Loadouts"]),
    (r"\bnamed class(?:es)?\b", "vision", ["Weapon Class System", "Named classes"]),
    (r"\bResolve\b", "vision", ["Combat", "Resolve: hard and light CC"]),
    (r"\bTolerance\b", "vision", ["Combat", "Conditions, build-up and Tolerance"]),
    (r"\bEvasion\b", "vision", ["Defense: Evasion, Guard and armor", "Evasion"]),
    (r"\bGuard\b", "vision", ["Defense: Evasion, Guard and armor", "Guard"]),
    (r"\bAltars?\b", "vision", ["Real exploration", "Altars, death, respawn and teleports"]),
    (r"\bExploration XP\b", "vision", ["Real exploration", "Exploration XP"]),
    (r"\bMarket Isle\b", "vision", ["Inventory, equipment and the Market Isle", "Market Isle (working name)"]),
    (r"\bOutlaws?\b", "vision", ["Factions, PvP and crime", "Outlaw and Infamy"]),
    (r"\bInfamy\b", "vision", ["Factions, PvP and crime", "Outlaw and Infamy"]),
    (r"\bJurisdiction\b", "vision", ["Factions, PvP and crime", "Jurisdiction"]),
    (r"\bRunes\b", "vision", ["Runes"]),
    (r"\bpower budget\b", "vision", ["Item progression and infinite progression", "Power budget"]),
    (r"\binfinite progression\b", "vision", ["Item progression and infinite progression", "Infinite progression"]),
    (r"\bsubscription\b", "vision", ["Business model, launch, visuals and audio", "Subscription"]),
    (r"\bcontext kit\b", "vision", ["Weapon Class System", "Context kit: mount, glider and wing"]),
    # Appendix: Nodes, Economy and Exploration
    (r"\blabor reserve\b", "nodes", ["Labor", "Labor reserve"]),
    (r"\b[Ll]abor\b", "nodes", ["Labor"]),
    (r"\btrade packs?\b", "nodes", ["Trade packs and routes"]),
    (r"\b[Pp]rosperity\b", "nodes", ["Regional economy", "Prosperity and node missions"]),
    (r"\bnode missions?\b", "nodes", ["Regional economy", "Prosperity and node missions"]),
    (r"\b[Ss]urveying\b", "nodes", ["Maps and cartography", "Surveying"]),
    (r"\b[Tt]riangulation\b", "nodes", ["Maps and cartography", "Triangulation (base chart on land)"]),
    (r"\b[Ss]tamina\b", "nodes", ["Stamina and climbing", "Stamina"]),
    (r"\bnodes?\b(?= (?:volume|ecology|type|prosperity|mission))", "nodes", ["Nodes", "What a node is"]),
    # Technical Architecture v4
    (r"\bFlecs\b", "arch", ["Simulation core: Flecs and Jolt (Engine)", "Flecs rules"]),
    (r"\bJolt\b", "arch", ["Simulation core: Flecs and Jolt (Engine)", "Jolt rules"]),
    (r"\bLayerStack\b", "arch", ["Application and LayerStack (Engine)"]),
    (r"\bGameNetworkingSockets\b", "arch", ["Networking: stack, sessions and responsiveness", "Stack (decided)"]),
    (r"\bRunicEditor\b", "arch", ["Tools (Engine)", "RunicEditor"]),
    (r"\b(?:the |Runic )?Cooker\b", "arch", ["World authoring and cooking (Engine, Game)", "Cooker"]),
    (r"\bRunicBot\b", "arch", ["Tools (Engine)", "Testing at scale"]),
    (r"\bGodotBridge\b", "arch", ["Godot integration (Engine)", "How the Engine uses Godot"]),
    (r"\bRenderFrame\b", "arch", ["Render data, extraction and world UI (Engine, Game)", "RenderData in Core"]),
    (r"\bRenderData\b", "arch", ["Render data, extraction and world UI (Engine, Game)", "RenderData in Core"]),
    (r"\bWorld Coordinator\b", "arch", ["Platform and operations", "Simulation placement"]),
    (r"\bAgones\b", "arch", ["Platform and operations", "Simulation placement"]),
    (r"\bGameplayFlow\b", "arch", ["Engine gameplay APIs (Engine)", "Scripted sequences (GameplayFlow) and restrictions"]),
    (r"\bWaterSystem\b", "arch", ["Water system (Engine)", "Core model: water reports facts"]),
    (r"\bbehavior trees?\b", "arch", ["AI architecture (Engine, Game)", "Behavior-tree runtime"]),
    (r"\bactivation volumes?\b", "arch", ["World space: coordinates, cells and activation (Engine)", "Activation volumes"]),
    (r"\b64-bit coordinates\b", "arch", ["World space: coordinates, cells and activation (Engine)", "64-bit coordinates (decided)"]),
    (r"\bmulti-rate (?:fixed-step )?scheduler\b", "arch", ["Simulation core: clock and threads (Engine)", "Multi-rate fixed-step scheduler"]),
    (r"\binterest set\b", "arch", ["Networking: replication, interest and handoff (Engine)", "Interest and visibility tiers (decided)"]),
    (r"\bhandoff\b", "arch", ["Networking: replication, interest and handoff (Engine)", "Simulations, handoff and ghosts"]),
    (r"\bdebug draw(?:ing)?\b", "arch", ["Debug drawing (Engine)"]),
    # Appendix: Ping Resolution
    (r"\b[Dd]efender grace\b", "ping", ["Part 1. Locked: ping resolution", "3. Defender grace (all defense)"]),
    (r"\b[Cc]apped rewind\b", "ping", ["Part 1. Locked: ping resolution", "5. Capped rewind"]),
    (r"\b[Tt]elegraph fast-forward\b", "ping", ["Part 1. Locked: ping resolution", "2. Telegraph fast-forward"]),
    (r"\b[Rr]elay routing\b", "ping", ["Part 1. Locked: ping resolution", "10. Relay routing"]),
    (r"\bLatency Feel Lab\b", "ping", []),
    # Appendix: Security
    (r"\b[Aa]nti-cheat\b", "security", ["The client"]),
    (r"\bDDoS\b", "security", ["DDoS"]),
    (r"\b[Ss]upply chain\b", "security", ["Supply chain and releases"]),
    # Appendix: Database Layout
    (r"\bPostgreSQL\b", "db", ["Physical layout (Proposal)"]),
    # Appendix: Content Pipeline
    (r"\bMPFB2?\b", "pipeline", ["Characters"]),
    (r"\bQuaternius\b", "pipeline", ["Animation"]),
    (r"\bdye masks?\b", "pipeline", ["Characters"]),
    (r"\b[Aa]rt direction\b", "pipeline", ["Art direction"]),
]

# Mentions of whole documents. Target is the document's index note.
DOC_MENTIONS = [
    (r"RunicGame — Visão Completa do MMORPG", "vision"),
    (r"RunicGame — Complete MMORPG Vision", "vision"),
    (r"RunicEngine — Technical Architecture v\d", "arch"),
    (r"Technical Architecture v4", "arch"),
    (r"Architecture v4", "arch"),
    (r"RunicGame — Ideias", "ideias"),
    (r"\bIdeias\b", "ideias"),
    (r"RunicGame — Lore", "lore"),
    (r"RunicGame — Quest Design", "quests"),
    (r"\bQuest Design\b", "quests"),
    (r"(?:RunicGame — )?(?:Appendix: )?Nodes, Economy and Exploration", "nodes"),
    (r"(?:RunicGame — )?(?:Appendix: )?Content Pipeline and Art Direction", "pipeline"),
    (r"(?:RunicGame — )?(?:Appendix: )?Ping Resolution", "ping"),
    (r"(?:RunicEngine — )?Appendix: Security", "security"),
    (r"(?:RunicEngine — )?(?:Appendix: )?Database Layout", "db"),
    (r"\bthe Vision\b", "vision"),
    (r"\bthe game vision\b", "vision"),
]


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


# --------------------------------------------------------------------------- notes

class Note:
    def __init__(self, path: str, title: str, body: str, fm: dict, doc: dict | None = None,
                 node: Node | None = None, self_ids: set | None = None):
        self.path = path
        self.title = title
        self.body = body
        self.fm = fm
        self.doc = doc
        self.node = node
        self.self_ids = self_ids or set()
        self.footer: list[str] = []

    def render(self) -> str:
        fm = OrderedDict()
        fm["title"] = self.title
        for k, v in self.fm.items():
            fm[k] = v
        # Quartz reads dates from frontmatter first; generated notes get the build date
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
        body = self.body.rstrip() + "\n"
        if self.footer:
            body += "\n---\n\n" + "  \n".join(self.footer) + "\n"
        return "\n".join(out) + "\n\n" + body


NOTES: "OrderedDict[str, Note]" = OrderedDict()


def add_note(n: Note):
    if n.path in NOTES:
        raise SystemExit(f"duplicate note path {n.path}")
    NOTES[n.path] = n


def wl(path: str, text: str | None = None, anchor: str | None = None, table: bool = False) -> str:
    """Wikilink by file name only: every name in the vault is unique, so Obsidian and Quartz
    ("shortest" resolution) find it wherever it lives."""
    target = path.rsplit("/", 1)[-1] + (f"#{anchor_text(anchor)}" if anchor else "")
    if text is None:
        return f"[[{target}]]"
    text = text.replace("[", "(").replace("]", ")").replace("|", "/")
    sep = "\\|" if table else "|"
    return f"[[{target}{sep}{text}]]"


def doc_fm(doc: dict, extra_tags=(), section: str | None = None) -> dict:
    return OrderedDict(
        tags=list(dict.fromkeys(doc["tags"] + list(extra_tags))),
        source=doc["title"],
        source_url=doc["url"],
        section=section,
        created=doc["created"],
        modified=doc["modified"],
    )


OWNER_RE = re.compile(r"\s*\(((?:Engine|Game|Platform)(?:, (?:Engine|Game|Platform))*)\)\s*$")


def owner_tags(title: str) -> list[str]:
    m = OWNER_RE.search(title)
    if not m:
        return []
    return [f"repo/{x.strip().lower()}" for x in m.group(1).split(",")]


PLANNED: list[Node] = []  # every outline node that becomes a note


def plan_node(node: Node, depth: int, ctx: str):
    node.base = safe_name(OWNER_RE.sub("", node.title))
    node.ctx = ctx
    node.is_folder = bool(node.children) and node.size() > SPLIT_CHARS and depth < MAX_DEPTH
    PLANNED.append(node)
    if node.is_folder:
        for ch in node.children:
            plan_node(ch, depth + 1, node.base)


def plan_doc(doc: dict, md: str):
    """Parse a document and decide which sections become notes or folders (names come later)."""
    root = parse_tree(md, doc)
    doc["root"] = root
    root.is_folder = True
    root.base = doc["hub"]
    root.ctx = doc["ctx"]
    PLANNED.append(root)
    for ch in root.children:
        plan_node(ch, 1, doc["ctx"])


def resolve_names(reserved: set[str]):
    """Give every planned note a file name that is unique in the whole vault (case-insensitive).
    A name used more than once gets its parent in parentheses: 'Ownership (Water system)'."""
    counts = Counter(n.base.lower() for n in PLANNED)
    taken = set(reserved)
    for n in PLANNED:
        name = n.base
        if counts[name.lower()] > 1 or name.lower() in reserved:
            name = f"{n.base} ({n.ctx})"
        if name.lower() in taken:
            name = f"{n.base} ({n.ctx}, {n.doc['ctx']})"
        k = 2
        while name.lower() in taken:
            name = f"{n.base} ({n.ctx}) {k}"
            k += 1
        taken.add(name.lower())
        n.name = name


def assign_node(node: Node, folder: str):
    if node.is_folder:
        sub = folder if node.parent is None else f"{folder}/{node.name}"
        node.path = f"{sub}/{node.name}"  # folder note: same name as its folder
        node.container = node
        for ch in node.children:
            assign_node(ch, sub)
    else:
        node.path = f"{folder}/{node.name}"
        for d in node.walk():
            d.container = node


def build_doc(doc: dict):
    root = doc["root"]
    assign_node(root, doc["folder"])
    doc["hub_path"] = root.path
    # create notes
    for n in root.walk():
        if n.container is not n:
            continue
        section = " › ".join(n.heading_path()) or None
        tags = []
        for h in n.heading_path():
            tags += owner_tags(h)
        if n.is_folder:
            body = trim(n.lines)
            contents = []
            for ch in n.children:
                contents.append(f"- {wl(ch.path, ch.title)}")
                if not ch.is_folder:
                    for g in ch.children:
                        contents.append(f"  - {wl(ch.path, g.title, anchor=g.title)}")
            if contents:
                if body:
                    body += [""]
                body += ["## Contents", ""] + contents
            title = doc["title"] if n.parent is None else (n.title if n.name == n.base else n.name)
            fm = doc_fm(doc, tags, section)
            if n.parent is None and doc["short"] != doc["hub"]:
                fm["aliases"] = [doc["short"]]
            add_note(Note(n.path, title, "\n".join(body), fm, doc, n))
        else:
            body = render_subtree(n, n.level)
            title = n.title if n.name == n.base else n.name
            add_note(Note(n.path, title, "\n".join(body), doc_fm(doc, tags, section), doc, n))


def find_node(key: str, hpath: list[str]) -> Node | None:
    node = DOC[key]["root"]
    for h in hpath:
        want = norm_key(h)
        nxt = None
        for ch in node.children:
            if norm_key(ch.title) == want:
                nxt = ch
                break
        if nxt is None:
            for ch in node.children:
                if norm_key(ch.title).startswith(want) or want.startswith(norm_key(ch.title)):
                    nxt = ch
                    break
        if nxt is None:
            # the path may skip a parent: search the whole subtree for this title
            nxt = next((x for x in node.walk() if x is not node and norm_key(x.title) == want), None)
        if nxt is None:
            return None
        node = nxt
    return node


def node_target(node: Node) -> tuple[str, str | None]:
    """(note path, anchor) for a node."""
    c = node.container
    if c is node:
        return node.path, None
    return c.path, node.title


# --------------------------------------------------------------------------- ideas

ID_LINE_RE = re.compile(r"^\*\*ID:\*\*\s*([A-Z]+-\d+)\s*·\s*\*\*Status:\*\*\s*(.+?)(?:\s*·\s*\*\*Game vision:\*\*\s*(.+?))?\s*$")
IDEAS: "OrderedDict[str, dict]" = OrderedDict()
ARCHIVED_IDS: dict[str, dict] = {}


def build_ideas(doc: dict, md: str):
    lines = md.split("\n")
    heads = [(i, len(m.group(1)), m.group(2).strip()) for i, l in enumerate(lines)
             for m in [re.match(r"^(#{1,6}) (.*)$", l)] if m]
    folder = doc["folder"]
    title_idx = heads[0][0]
    pre_end = heads[1][0]
    preamble = trim(lines[title_idx + 1:pre_end])
    groups = []
    stack = []  # (level, idea id)
    archived_lines = []
    for n, (i, lvl, title) in enumerate(heads[1:], 1):
        end = heads[n + 1][0] if n + 1 < len(heads) else len(lines)
        block = lines[i + 1:end]
        first = next((l for l in block if l.strip()), "")
        m = ID_LINE_RE.match(first)
        while stack and stack[-1][0] >= lvl:
            stack.pop()
        if m:
            iid, status, vision = m.group(1), m.group(2).strip(), (m.group(3) or "").strip()
            rest = list(block)
            rest.remove(first)
            parent = stack[-1][1] if stack else None
            IDEAS[iid] = dict(id=iid, title=title, status=status, vision=vision, body=trim(rest),
                              parent=parent, children=[], group=None)
            if parent and parent in IDEAS:
                IDEAS[parent]["children"].append(iid)
            elif parent and parent.startswith("group:"):
                IDEAS[iid]["group"] = parent[6:]
            stack.append((lvl, iid))
        elif norm_key(title).startswith("archived"):
            archived_lines = trim(block)
            stack.append((lvl, "archived"))
        else:
            groups.append(dict(title=title, intro=trim(block), ideas=[]))
            stack.append((lvl, "group:" + title))
    for g in groups:
        g["ideas"] = [k for k, v in IDEAS.items() if v["group"] == g["title"]]
    for l in archived_lines:
        m = re.match(r"^\|\s*([A-Z]+-\d+)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|", l)
        if m:
            ARCHIVED_IDS[m.group(1)] = dict(title=m.group(2), status=m.group(3))
    for iid, idea in IDEAS.items():
        idea["path"] = f"{folder}/{iid} {safe_name(idea['title'], False)}"
    doc["archived_path"] = f"{folder}/Archived and Discarded ideas"
    doc["hub_path"] = f"{folder}/{doc['hub']}"
    doc["ideas_preamble"] = preamble
    doc["ideas_groups"] = groups
    doc["archived_lines"] = archived_lines


def status_tag(status: str) -> str:
    s = status.lower()
    for key, tag in (("in game vision", "status/in-game-vision"), ("partial", "status/partial"),
                     ("being", "status/being-designed"), ("open", "status/open"),
                     ("archived", "status/archived"), ("discarded", "status/discarded")):
        if s.startswith(key):
            return tag
    return "status/" + slugify(s)


def vision_links(field: str, table=False) -> str:
    """'Combat › Resolve: hard and light CC (effect gates); PvE' -> links."""
    parts = [p.strip() for p in field.split(";") if p.strip()]
    out = []
    for p in parts:
        m = re.match(r"^(.*?)\s*(\(.*\))?$", p)
        main, paren = m.group(1).strip(), (m.group(2) or "")
        hp = [x.strip() for x in main.split("›")]
        node = find_node("vision", hp)
        if node is None and len(hp) > 1:
            node = find_node("vision", hp[:1])
        if node is None:
            UNRESOLVED.append(("vision-field", field))
            out.append(p)
            continue
        path, anchor = node_target(node)
        out.append(wl(path, main, anchor, table) + (f" {paren}" if paren else ""))
    return "; ".join(out)


def make_idea_notes(doc: dict):
    for iid, idea in IDEAS.items():
        idea_line = f"**ID:** {iid} · **Status:** {idea['status']}"
        if idea["vision"]:
            idea_line += f" · **Game vision:** {vision_links(idea['vision'])}"
        body = [idea_line, ""] + idea["body"]
        fm = OrderedDict(aliases=[iid, idea["title"]],
                         tags=["runicgame", "idea", status_tag(idea["status"])],
                         id=iid, status=idea["status"], game_vision=idea["vision"] or None,
                         source=doc["title"], source_url=doc["url"],
                         created=doc["created"], modified=doc["modified"])
        note = Note(idea["path"], f"{iid} · {idea['title']}", "\n".join(body), fm, doc, self_ids={iid})
        if idea["parent"] and idea["parent"] in IDEAS:
            p = IDEAS[idea["parent"]]
            note.footer.append(f"Part of {wl(p['path'], p['id'] + ' · ' + p['title'])}")
        if idea["children"]:
            note.footer.append("Includes " + ", ".join(wl(IDEAS[c]["path"], c + ' · ' + IDEAS[c]["title"]) for c in idea["children"]))
        if idea["group"]:
            note.footer.append(f"Group: {wl(doc['hub_path'], idea['group'], anchor=idea['group'] + ' ideas')}")
        add_note(note)
    # archived table
    fm = OrderedDict(tags=["runicgame", "ideias", "status/archived", "status/discarded"],
                     source=doc["title"], source_url=doc["url"], created=doc["created"], modified=doc["modified"])
    add_note(Note(doc["archived_path"], "Archived and Discarded ideas", "\n".join(doc["archived_lines"]), fm, doc,
                  self_ids=set(ARCHIVED_IDS)))
    # index
    body = list(doc["ideas_preamble"]) + [""]
    order = ["Open", "Partial", "Being designed", "In game vision"]
    by_status = defaultdict(list)
    for iid, idea in IDEAS.items():
        st = next((o for o in order if idea["status"].lower().startswith(o.lower())), idea["status"])
        by_status[st].append(idea)
    body += ["## Ideas by status", ""]
    body += [f"{len(IDEAS)} ideas with an ID, plus {len(ARCHIVED_IDS)} archived or discarded ones in "
             f"{wl(doc['archived_path'], 'Archived and Discarded')}.", ""]
    for st in order + [s for s in by_status if s not in order]:
        if not by_status.get(st):
            continue
        body += [f"### {st} ({len(by_status[st])})", "", "| ID | Idea | Game vision |", "| :---- | :---- | :---- |"]
        for idea in by_status[st]:
            vis = vision_links(idea["vision"], table=True) if idea["vision"] else "—"
            body.append(f"| {wl(idea['path'], idea['id'], table=True)} | {idea['title']} | {vis} |")
        body.append("")
    for g in doc["ideas_groups"]:
        body += [f"## {g['title']} ideas", ""] + g["intro"] + [""]
        body += [f"- {wl(IDEAS[i]['path'], i + ' · ' + IDEAS[i]['title'])}" for i in g["ideas"]] + [""]
    fm = OrderedDict(aliases=["Ideas inbox"], tags=["runicgame", "ideias"], source=doc["title"],
                     source_url=doc["url"], created=doc["created"], modified=doc["modified"])
    add_note(Note(doc["hub_path"], doc["title"], "\n".join(body), fm, doc))


# --------------------------------------------------------------------------- packages and slices

PACKAGES: "OrderedDict[str, dict]" = OrderedDict()
SLICES: "OrderedDict[str, dict]" = OrderedDict()
PREFIXES: dict[str, tuple[str, str]] = {}  # prefix -> (module name, repo)


def split_row(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", s)]


def parse_tables(doc: dict):
    """Yield (heading node, header cells, rows) for every table in a document."""
    for n in doc["root"].walk():
        lines = n.lines
        i = 0
        while i < len(lines):
            if lines[i].startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*:?-{3,}", lines[i + 1]):
                header = split_row(lines[i])
                rows = []
                j = i + 2
                while j < len(lines) and lines[j].startswith("|"):
                    rows.append(split_row(lines[j]))
                    j += 1
                yield n, header, rows
                i = j
            else:
                i += 1


def slice_id_from_cell(cell: str):
    s = unescape_md(cell).strip()
    m = re.match(r"^(\d+)([a-z]?)(\+)?\.\s*(.*)$", s)
    if not m:
        return None
    return m.group(1), m.group(2), bool(m.group(3)), m.group(4).strip()


def build_slices_and_packages():
    arch = DOC["arch"]
    # prefix legend
    for n in arch["root"].walk():
        for l in n.lines:
            if l.startswith("**Prefixes.**"):
                text = unescape_md(l.replace("**Prefixes.**", "")).strip()
                for repo, items in re.findall(r"(Engine|Platform|Game):\s*(.*?)(?=(?:Engine|Platform|Game):|$)", text):
                    for item in items.strip().rstrip(".").split(","):
                        item = item.strip()
                        if not item:
                            continue
                        parts = item.split(" ", 1)
                        name = parts[1] if len(parts) > 1 else parts[0]
                        PREFIXES[parts[0]] = (name[0].upper() + name[1:], repo)
    # roadmap slices
    for node, header, rows in parse_tables(arch):
        if header and header[0] == "Slice" and "Runnable result" in header:
            for r in rows:
                sid = slice_id_from_cell(r[0])
                if not sid:
                    continue
                num, letter, plus, name = sid
                key = f"{num}{letter}{'+' if plus else ''}"
                fields = OrderedDict((header[k], r[k] if k < len(r) else "") for k in range(1, len(header)))
                SLICES[key] = dict(key=key, num=int(num), letter=letter, plus=plus, name=name, fields=fields,
                                   path=f"{ROADMAP_FOLDER}/Slice {int(num):02d}{letter} {safe_name(name, False)}",
                                   packages_first=[], node=node)
            break
    # packages (Architecture tables first, then any other doc that defines new ones)
    for key in ["arch", "security", "db", "pipeline", "ping", "nodes", "vision"]:
        doc = DOC[key]
        for node, header, rows in parse_tables(doc):
            if not header or header[0] != "ID" or len(header) < 2 or header[1] != "Package":
                continue
            group = node.title
            for r in rows:
                pid = unescape_md(r[0]).strip()
                if not re.match(r"^[A-Z]+-\d+[a-z]?$", pid):
                    continue
                fields = OrderedDict((header[k], r[k] if k < len(r) else "") for k in range(1, len(header)))
                if pid in PACKAGES:
                    for k, v in fields.items():
                        if k not in PACKAGES[pid]["fields"] and v:
                            PACKAGES[pid]["fields"][k] = v
                    PACKAGES[pid]["also"].append((doc, node))
                    continue
                prefix = pid.split("-")[0]
                mod, repo = PREFIXES.get(prefix, (prefix, "Other"))
                PACKAGES[pid] = dict(id=pid, prefix=prefix, module=mod, repo=repo, fields=fields,
                                     group=group, doc=doc, node=node, also=[])
    for pid, p in PACKAGES.items():
        mod_dir = p["prefix"] if p["module"] == p["prefix"] else f"{p['prefix']} {safe_name(p['module'], False)}"
        folder = f"{PACKAGES_FOLDER}/{p['repo']}/{mod_dir}"
        p["folder"] = folder
        p["module_note"] = f"{folder}/{mod_dir}"
        p["path"] = f"{folder}/{pid}"
        desc = unescape_md(p["fields"].get("Package", ""))
        short = re.split(r":|\s\(|;|\.\s", desc, maxsplit=1)[0].strip()
        if len(short) > 64:
            short = short[:64].rsplit(" ", 1)[0] + "…"
        p["short"] = short
        sl = unescape_md(p["fields"].get("Slice", "")).strip()
        p["slice"] = sl
        sk = slice_key(sl)
        if sk:
            SLICES[sk]["packages_first"].append(pid)


def slice_key(token: str) -> str | None:
    t = unescape_md(token).strip().rstrip(".")
    if t in SLICES:
        return t
    m = re.match(r"^(\d+)([a-z]?)(\+)?$", t)
    if not m:
        return None
    for k in (f"{m.group(1)}{m.group(2)}{m.group(3) or ''}", f"{m.group(1)}{m.group(2)}", f"{m.group(1)}+"):
        if k in SLICES:
            return k
    return None


def make_package_and_slice_notes():
    arch = DOC["arch"]
    for pid, p in PACKAGES.items():
        f = p["fields"]
        lines = []
        for k, v in f.items():
            if not v or v in ("—", "-"):
                v = "—"
            if k == "Slice":
                sk = slice_key(v)
                v = wl(SLICES[sk]["path"], f"Slice {sk} · {SLICES[sk]['name']}") if sk else v
            lines.append(f"**{k}:** {v}")
            lines.append("")
        mod_index = p["module_note"]
        mname = p["prefix"] if p["module"] == p["prefix"] else p["prefix"] + " · " + p["module"]
        lines.append(f"**Module:** {wl(mod_index, mname)} ({p['repo']})")
        lines.append("")
        dpath, danchor = node_target(p["node"])
        lines.append(f"**Defined in:** {wl(dpath, p['doc']['short'] + ' › ' + p['group'], danchor)}")
        for d, nd in p["also"]:
            ap, aa = node_target(nd)
            lines.append("")
            lines.append(f"**Also in:** {wl(ap, d['short'] + ' › ' + nd.title, aa)}")
        fm = OrderedDict(aliases=[pid], tags=["runicengine", "package", f"repo/{p['repo'].lower()}"],
                         id=pid, module=f"{p['prefix']} {p['module']}", slice=p["slice"] or None,
                         source=p["doc"]["title"], source_url=p["doc"]["url"],
                         created=p["doc"]["created"], modified=p["doc"]["modified"])
        add_note(Note(p["path"], f"{pid} · {p['short']}", "\n".join(lines), fm, p["doc"], self_ids={pid}))
    # module, repo and package indexes
    repos = OrderedDict()
    for p in PACKAGES.values():
        repos.setdefault(p["repo"], OrderedDict()).setdefault(p["prefix"], []).append(p)
    wp_node = find_node("arch", ["Modules, work packages and the implementation contract (Engine, Platform, Game)", "Work packages"])
    wp_path, wp_anchor = node_target(wp_node) if wp_node else (DOC["arch"]["root"].path, None)
    top = [f"Every work package of the {wl(arch['root'].path, 'Technical Architecture v4')} as its own note, "
           f"grouped by repository and module. The tables these notes come from are in "
           f"{wl(wp_path, 'Work packages', wp_anchor)}; a package's **Needs** links form the dependency graph, "
           f"and its **Slice** links to the {wl(ROADMAP_HUB, 'roadmap')} slice that first needs it.", ""]
    for repo, mods in repos.items():
        top += [f"## {repo}", ""]
        for prefix, plist in mods.items():
            mpath = plist[0]["module_note"]
            mtitle = prefix if plist[0]["module"] == prefix else f"{prefix} · {plist[0]['module']}"
            top.append(f"- {wl(mpath, mtitle)} — {', '.join(wl(x['path'], x['id']) for x in plist)}")
            mb = [f"Module **{prefix}** ({plist[0]['module']}) in {repo}.", "",
                  "| ID | Package | Needs | Slice |", "| :---- | :---- | :---- | :---- |"]
            for x in plist:
                sk = slice_key(x["slice"])
                sl = wl(SLICES[sk]["path"], sk, table=True) if sk else (x["slice"] or "—")
                needs = x["fields"].get("Needs", "") or "—"
                mb.append(f"| {wl(x['path'], x['id'], table=True)} | {x['short']} | {needs} | {sl} |")
            add_note(Note(mpath, mtitle, "\n".join(mb), OrderedDict(tags=["runicengine", "package", f"repo/{repo.lower()}"]), arch))
        top.append("")
    add_note(Note(PACKAGES_HUB, "Work Packages", "\n".join(top),
                  OrderedDict(aliases=["Packages"], tags=["runicengine", "package"]), arch))
    # slices
    keys = list(SLICES)
    rm_node = find_node("arch", ["Vertical-slice roadmap"])
    rm_path, rm_anchor = node_target(rm_node) if rm_node else (arch["root"].path, None)
    for i, k in enumerate(keys):
        s = SLICES[k]
        lines = []
        for fk, fv in s["fields"].items():
            lines += [f"**{fk}:** {fv or '—'}", ""]
        if s["packages_first"]:
            lines += ["**Packages first needed here:** " + ", ".join(wl(PACKAGES[p]["path"], p) for p in s["packages_first"]), ""]
        if rm_node:
            for para in rm_node.lines:
                m = re.match(r"^\*\*[^*]*\(slice (\d+[a-z]?)\)[^*]*\*\*", para)
                if m and slice_key(m.group(1)) == k:
                    lines += [para, ""]
        lines.append(f"**Defined in:** {wl(rm_path, 'Technical Architecture v4 › Vertical-slice roadmap', rm_anchor)}")
        owners = [o.strip().lower() for o in unescape_md(s["fields"].get("Owner", "")).split(",") if o.strip()]
        fm = OrderedDict(aliases=[f"Slice {k}"], tags=["runicengine", "slice"] + [f"repo/{o}" for o in owners],
                         slice=k, source=arch["title"], source_url=arch["url"],
                         created=arch["created"], modified=arch["modified"])
        note = Note(s["path"], f"Slice {k} · {s['name']}", "\n".join(lines), fm, arch)
        nav = [f"↑ {wl(ROADMAP_HUB, 'Roadmap')}"]
        if i > 0:
            p = SLICES[keys[i - 1]]
            nav.append(f"← {wl(p['path'], 'Slice ' + p['key'] + ' · ' + p['name'])}")
        if i + 1 < len(keys):
            nx = SLICES[keys[i + 1]]
            nav.append(f"{wl(nx['path'], 'Slice ' + nx['key'] + ' · ' + nx['name'])} →")
        note.footer.append(" · ".join(nav))
        add_note(note)
    rb = [f"The vertical slices of the {wl(rm_path, 'roadmap', rm_anchor)}, one note per slice. Each slice is small, "
          "ends in something runnable and testable, and adds one piece of the architecture.", "",
          "| Slice | Runnable result | Owner |", "| :---- | :---- | :---- |"]
    for k in keys:
        s = SLICES[k]
        rr = s["fields"].get("Runnable result", "")
        if len(rr) > 160:
            rr = rr[:160].rsplit(" ", 1)[0] + "…"
        rb.append(f"| {wl(s['path'], k + '. ' + s['name'], table=True)} | {rr} | {s['fields'].get('Owner', '')} |")
    add_note(Note(ROADMAP_HUB, "Vertical-slice roadmap", "\n".join(rb),
                  OrderedDict(aliases=["Slices"], tags=["runicengine", "slice"],
                              source=arch["title"], source_url=arch["url"]), arch))


# --------------------------------------------------------------------------- navigation

def add_navigation():
    for d in DOCS:
        if d.get("kind") in ("ideas", "redirect"):
            continue
        for n in d["root"].walk():
            if n.container is not n or n.parent is None:
                continue
            note = NOTES[n.path]
            sibs = [c for c in n.parent.children]
            i = sibs.index(n)
            label = lambda x: x.title if x.name == x.base else x.name
            nav = [f"↑ {wl(n.parent.path, label(n.parent) if n.parent.parent else d['short'])}"]
            if i > 0:
                nav.append(f"← {wl(sibs[i - 1].path, label(sibs[i - 1]))}")
            if i + 1 < len(sibs):
                nav.append(f"{wl(sibs[i + 1].path, label(sibs[i + 1]))} →")
            note.footer.append(" · ".join(nav))
    # up-links for document main notes and generated notes, so every note hangs from the tree
    up = {PACKAGES_HUB: (HOME, "RunicDocs"), ROADMAP_HUB: (HOME, "RunicDocs")}
    for d in DOCS:
        up[d["hub_path"]] = (HOME, "RunicDocs")
    ideias = DOC["ideias"]
    for idea in IDEAS.values():
        up[idea["path"]] = (ideias["hub_path"], "Ideias")
    up[ideias["archived_path"]] = (ideias["hub_path"], "Ideias")
    for p in PACKAGES.values():
        up[p["module_note"]] = (PACKAGES_HUB, "Work Packages")
    for path, (parent, label) in up.items():
        if path in NOTES and parent in NOTES:
            NOTES[path].footer.insert(0, f"↑ {wl(parent, label)}")

    for note in NOTES.values():
        if note.doc and note.fm.get("source_url"):
            sec = note.fm.get("section")
            src = f"Source: [{note.doc['title']}]({note.doc['url']})" + (f" › {sec}" if sec else "")
            note.footer.append(f"{src} · exported {SNAPSHOT}")


# --------------------------------------------------------------------------- link injection

HOME = "index"
PROTECT_RE = re.compile(r"(!?\[\[[^\]]*\]\]|!?\[[^\]]*\]\([^)]*\)|`[^`]*`|https?://[^\s)>|]+|<[^>]+>)")
UNRESOLVED: list = []
STATS = defaultdict(int)


def map_segments(line: str, fn):
    parts = PROTECT_RE.split(line)
    for k in range(0, len(parts), 2):
        if parts[k]:
            parts[k] = fn(parts[k])
    return "".join(parts)


def linkify(note: Note, id_targets: dict, slice_targets: dict, term_targets: list, doc_targets: list):
    out = []
    in_code = False
    used_terms = set()
    used_docs = set()
    table_header = None
    lines = note.body.split("\n")
    for li, line in enumerate(lines):
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code or re.match(r"^#{1,6} ", line):
            out.append(line)
            continue
        in_table = line.startswith("|")
        if in_table and li + 1 < len(lines) and re.match(r"^\|\s*:?-{3,}", lines[li + 1]):
            table_header = [h.lower() for h in split_row(line)]
        elif not in_table:
            table_header = None

        # Google Docs URLs of folder documents -> wikilinks
        def gdoc(m):
            text, did = m.group(1), m.group(2)
            for d in DOCS:
                if d["drive"] == did and d["hub_path"] != note.path:
                    STATS["gdoc-url"] += 1
                    return wl(d["hub_path"], text, table=in_table)
            return m.group(0)
        line = re.sub(r"\[([^\]]+)\]\(https://docs\.google\.com/document/d/([\w-]+)[^)]*\)", gdoc, line)

        def ids(seg):
            def r(m):
                t = m.group(0)
                if t in note.self_ids or t not in id_targets:
                    return t
                STATS["id"] += 1
                path = id_targets[t]
                if path == note.path:
                    return t
                return wl(path, t, table=in_table)
            return ID_RE.sub(r, seg)
        line = map_segments(line, ids)

        def slices(seg):
            def r(m):
                word, sp, toks = m.group(1), m.group(2), m.group(3)
                def tok(mm):
                    k = slice_key(mm.group(0))
                    if not k or slice_targets[k] == note.path:
                        return mm.group(0)
                    STATS["slice"] += 1
                    return wl(slice_targets[k], unescape_md(mm.group(0)), table=in_table)
                return word + sp + re.sub(r"\d+[a-z]?(?:\\?\+)?", tok, toks)
            return SLICE_RE.sub(r, seg)
        line = map_segments(line, slices)

        if in_table and table_header and not re.match(r"^\|\s*:?-{3,}", line):
            cells = split_row(line)
            changed = False
            for ci, h in enumerate(table_header):
                if ci >= len(cells) or "[[" in cells[ci]:
                    continue
                if h == "slice" and ci == 0 and slice_id_from_cell(cells[0]):
                    sid = slice_id_from_cell(cells[0])
                    k = slice_key(f"{sid[0]}{sid[1]}{'+' if sid[2] else ''}")
                    if k and slice_targets[k] != note.path:
                        cells[0] = wl(slice_targets[k], unescape_md(cells[0]), table=True)
                        changed = True
                elif h in ("slice", "slices"):
                    def tok(mm):
                        k = slice_key(mm.group(0))
                        if not k:
                            return mm.group(0)
                        STATS["slice-cell"] += 1
                        return wl(slice_targets[k], unescape_md(mm.group(0)), table=True)
                    new = re.sub(r"(?<![\w-])\d+[a-z]?(?:\\?\+)?(?![\w-])", tok, cells[ci])
                    if new != cells[ci]:
                        cells[ci] = new
                        changed = True
            if changed:
                line = "| " + " | ".join(cells) + " |"

        def docs(seg):
            for rx, key, target in doc_targets:
                if key in used_docs or target == note.path or (note.doc and note.doc["key"] == key):
                    continue
                m = rx.search(seg)
                if m:
                    used_docs.add(key)
                    STATS["doc"] += 1
                    return docs(seg[:m.start()]) + wl(target, m.group(0), table=in_table) + docs(seg[m.end():])
            return seg
        line = map_segments(line, docs)

        def terms(seg):
            for rx, tpath, anchor, tkey in term_targets:
                if tkey in used_terms:
                    continue
                if tpath == note.path:
                    continue
                m = rx.search(seg)
                if m:
                    used_terms.add(tkey)
                    STATS["term"] += 1
                    return seg[:m.start()] + wl(tpath, m.group(0), anchor, table=in_table) + terms(seg[m.end():])
            return seg
        line = map_segments(line, terms)
        out.append(line)
    note.body = "\n".join(out)


ID_RE = re.compile(r"$^")
SLICE_RE = re.compile(r"\b([Ss]lices?)(\s+)((?:\d+[a-z]?(?:\\?\+)?)(?:(?:,\s*|\s+and\s+|\s+to\s+|\s+or\s+|\s*/\s*)\d+[a-z]?(?:\\?\+)?)*)")


def inject_links():
    global ID_RE
    id_targets = {}
    for iid, idea in IDEAS.items():
        id_targets[iid] = idea["path"]
    for aid in ARCHIVED_IDS:
        id_targets[aid] = DOC["ideias"]["archived_path"]
    for pid, p in PACKAGES.items():
        id_targets[pid] = p["path"]
    ids_sorted = sorted(id_targets, key=len, reverse=True)
    ID_RE = re.compile(r"(?<![\w\-/#\[|])(?:" + "|".join(re.escape(x) for x in ids_sorted) + r")(?![\w-])")
    slice_targets = {k: s["path"] for k, s in SLICES.items()}
    term_targets = []
    for i, (rx, key, hp) in enumerate(TERMS):
        node = find_node(key, hp) if hp else DOC[key]["root"]
        if node is None:
            UNRESOLVED.append(("term", rx, key, hp))
            continue
        path, anchor = node_target(node)
        term_targets.append((re.compile(rx), path, anchor, f"t{i}"))
    doc_targets = [(re.compile(rx), key, DOC[key]["hub_path"]) for rx, key in DOC_MENTIONS]
    for note in NOTES.values():
        linkify(note, id_targets, slice_targets, term_targets, doc_targets)


# --------------------------------------------------------------------------- hubs

def write_hubs():
    g = lambda k: DOC[k]["hub_path"]
    home = f"""This site is the RunicGame and RunicEngine design documentation, compiled from the documents in the
[RunicMMOEngine Drive folder]({DRIVE_FOLDER}) on {SNAPSHOT}. Every note says which document and section it comes from.

## RunicGame — the game

- {wl(g('vision'), 'Complete MMORPG Vision')}: how the game should work, and every recorded decision.
- {wl(g('ideias'), 'Ideias')}: the ideas inbox, one note per idea ID with its status.
- {wl(g('lore'), 'Lore')} and {wl(g('quests'), 'Quest Design')}: they live in the RunicGame repository, in the
  [RunicWorld vault]({RUNICWORLD_URL}).
- Appendices, until they are merged into the Vision: {wl(g('nodes'), 'Nodes, Economy and Exploration')},
  {wl(g('pipeline'), 'Content Pipeline and Art Direction')}, {wl(g('ping'), 'Ping Resolution')}.

## RunicEngine — the technology

![[runicengine-layered-architecture.png]]
*RunicEngine layered architecture*

- {wl(g('arch'), 'Technical Architecture v4')}: how the Engine, the Platform and the Game are built.
- {wl(ROADMAP_HUB, 'Vertical-slice roadmap')}: one note per slice, with its packages.
- {wl(PACKAGES_HUB, 'Work Packages')}: one note per package, linked to what it needs.
- Appendices, until they are merged into the Architecture: {wl(g('security'), 'Security')}, {wl(g('db'), 'Database Layout')}.

## How to read it

- **Hierarchy.** Each document is a folder whose main note has the folder's name and lists its sections in order.
  Sections are notes, and long sections are folders of their own. Every note links up to its parent and to the
  previous and next section.
- **Graph.** Links carry the connections between documents: idea IDs (like NAV-01), package IDs (like PCS-1), slice
  numbers, document names and key terms (Disciplines, Labor, Flecs, Jolt…) all link to where they are defined.
  The graph on the right shows a note's neighbourhood; open it full-screen to see the whole map.
- **Labels.** The documents mark items as Decided (or Decision), Proposal and Open. Numbers are examples that show the
  shape; final values come from development and playtests.
- **Tags.** `vision`, `architecture`, `ideias`, `appendix`, `idea` with `status/…`, `package` and `slice` with
  `repo/engine`, `repo/platform` and `repo/game`.
"""
    add_note(Note(HOME, "RunicDocs", home, OrderedDict(aliases=["Home"], tags=["home"])))
    # documents that live in another repository keep their folder with one note pointing there
    where = {
        "lore": "The world's story, gods, peoples, factions and the main story.",
        "quests": "Quests, the Chronicle journal, the Codex, knowledge tags and secrets.",
    }
    for d in DOCS:
        if d.get("kind") != "redirect":
            continue
        body = f"""{where[d['key']]}

This document lives in the **RunicGame** repository, in the RunicWorld vault:
**[RunicGame › docs/RunicWorld]({RUNICWORLD_URL})**

Until its text moves there, the current version is the Google Doc [{d['title']}]({d['url']}).

↑ {wl(HOME, 'RunicDocs')}
"""
        fm = OrderedDict(aliases=[d["title"]], tags=d["tags"] + ["redirect"], source=d["title"],
                         source_url=d["url"], moved_to=RUNICWORLD_URL)
        add_note(Note(d["hub_path"], d["hub"], body, fm))


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
    extra_png = src / "RunicEngine_Layered_Architecture.png"
    if extra_png.exists():
        attach.mkdir(parents=True, exist_ok=True)
        shutil.copy(extra_png, attach / "runicengine-layered-architecture.png")

    for d in DOCS:
        if d.get("kind") == "redirect":
            continue
        md = normalize((src / d["file"]).read_text(encoding="utf-8"), d["key"], attach)
        if d.get("kind") == "ideas":
            build_ideas(d, md)
        else:
            plan_doc(d, md)
    build_slices_and_packages()
    # names that generated notes already use; section notes must not take them
    reserved = {HOME}
    reserved |= {i["path"].rsplit("/", 1)[-1] for i in IDEAS.values()}
    reserved |= {DOC["ideias"]["hub"], DOC["ideias"]["archived_path"].rsplit("/", 1)[-1]}
    reserved |= {p["id"] for p in PACKAGES.values()} | {p["module_note"].rsplit("/", 1)[-1] for p in PACKAGES.values()}
    reserved |= {s_["path"].rsplit("/", 1)[-1] for s_ in SLICES.values()}
    reserved |= {PACKAGES_HUB.rsplit("/", 1)[-1], ROADMAP_HUB.rsplit("/", 1)[-1]}
    reserved |= {d["hub"] for d in DOCS if d.get("kind") in ("redirect", "ideas")}
    resolve_names({r.lower() for r in reserved})
    for d in DOCS:
        if d.get("kind") not in ("ideas", "redirect"):
            build_doc(d)
    make_idea_notes(DOC["ideias"])
    make_package_and_slice_notes()
    write_hubs()
    add_navigation()
    inject_links()

    names = Counter(path.rsplit("/", 1)[-1].lower() for path in NOTES)
    dupes = [n for n, c in names.items() if c > 1]
    if dupes:
        raise SystemExit(f"duplicate note names: {dupes}")

    for note in NOTES.values():
        p = out / (note.path + ".md")
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(note.render(), encoding="utf-8")

    report = dict(notes=len(NOTES), ideas=len(IDEAS), archived=len(ARCHIVED_IDS), packages=len(PACKAGES),
                  slices=len(SLICES), links=dict(STATS), unresolved=UNRESOLVED)
    print(json.dumps(report, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
