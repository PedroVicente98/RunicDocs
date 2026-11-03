"""Convert a Google Docs API JSON export (documents.get) into Markdown.

Usage: python3 -I docsjson2md.py <json_file> <out_md>
Handles headings, bullets (nested, ordered/unordered), bold/italic/strike,
links, and tables. Output style matches the cleaned Google markdown export.
"""
import json
import sys

ORDERED_GLYPHS = {"DECIMAL", "ZERO_DECIMAL", "UPPER_ALPHA", "ALPHA", "UPPER_ROMAN", "ROMAN"}


def run_text(el):
    tr = el.get("textRun")
    if not tr:
        return ""
    text = tr.get("content", "")
    st = tr.get("textStyle", {})
    if text.strip() == "":
        return text
    core = text.rstrip("\n")
    trail = text[len(core):]
    # keep leading/trailing spaces outside the markers
    lead_ws = core[: len(core) - len(core.lstrip())]
    tail_ws = core[len(core.rstrip()):]
    body = core.strip()
    if not body:
        return text
    link = st.get("link", {}).get("url")
    if st.get("bold") and st.get("italic"):
        body = f"***{body}***"
    elif st.get("bold"):
        body = f"**{body}**"
    elif st.get("italic"):
        body = f"*{body}*"
    if st.get("strikethrough"):
        body = f"~~{body}~~"
    if link:
        body = f"[{body}]({link})"
    return lead_ws + body + tail_ws + trail


def para_text(p):
    out = "".join(run_text(e) for e in p.get("elements", []))
    # merge adjacent identical markers like **a****b** -> **ab**
    out = out.replace("****", "").replace("~~~~", "")
    return out.rstrip("\n")


def is_ordered(lists, list_id, level):
    try:
        lv = lists[list_id]["listProperties"]["nestingLevels"][level]
    except (KeyError, IndexError):
        return False
    return lv.get("glyphType") in ORDERED_GLYPHS


def cell_text(cell, lists):
    parts = []
    for el in cell.get("content", []):
        if "paragraph" in el:
            t = para_text(el["paragraph"]).strip()
            if t:
                parts.append(t)
    return "<br>".join(parts).replace("|", "\\|")


def convert(doc):
    content = doc["content"] if "content" in doc else doc
    tab = content["tabs"][0]["documentTab"]
    lists = tab.get("lists", {})
    lines = []
    counters = {}
    prev_was_list = False
    for el in tab["body"]["content"]:
        if "paragraph" in el:
            p = el["paragraph"]
            style = p.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
            text = para_text(p)
            if "bullet" in p:
                b = p["bullet"]
                lid = b.get("listId")
                lvl = b.get("nestingLevel", 0)
                indent = "  " * lvl
                if is_ordered(lists, lid, lvl):
                    key = (lid, lvl)
                    counters[key] = counters.get(key, 0) + 1
                    # reset deeper levels
                    for k in list(counters):
                        if k[0] == lid and k[1] > lvl:
                            del counters[k]
                    marker = f"{counters[key]}."
                else:
                    marker = "*"
                lines.append(f"{indent}{marker} {text.strip()}")
                prev_was_list = True
                continue
            if prev_was_list:
                lines.append("")
                prev_was_list = False
            if not text.strip():
                if lines and lines[-1] != "":
                    lines.append("")
                continue
            if style == "TITLE":
                lines += [f"# {text.strip().strip('*')}", ""]
            elif style.startswith("HEADING_"):
                n = int(style.split("_")[1])
                h = text.strip().replace("**", "")
                lines += [f"{'#' * n} {h}", ""]
            else:
                lines += [text, ""]
        elif "table" in el:
            if prev_was_list:
                lines.append("")
                prev_was_list = False
            rows = el["table"].get("tableRows", [])
            grid = [[cell_text(c, lists) for c in r.get("tableCells", [])] for r in rows]
            if not grid:
                continue
            ncol = max(len(r) for r in grid)
            grid = [r + [""] * (ncol - len(r)) for r in grid]
            lines.append("| " + " | ".join(grid[0]) + " |")
            lines.append("| " + " | ".join([":----"] * ncol) + " |")
            for r in grid[1:]:
                lines.append("| " + " | ".join(r) + " |")
            lines.append("")
    # collapse multiple blank lines
    out, blank = [], False
    for ln in lines:
        if ln.strip() == "":
            if not blank:
                out.append("")
            blank = True
        else:
            out.append(ln)
            blank = False
    return content.get("title", ""), "\n".join(out).strip() + "\n"


if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    title, md = convert(data)
    open(sys.argv[2], "w").write(md)
    print(title, len(md))
