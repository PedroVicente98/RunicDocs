# RunicDocs

The RunicGame and RunicEngine design documentation, kept as Markdown: an Obsidian vault published as a website with
[Quartz](https://quartz.jzhao.xyz) at [pedrovicente98.github.io/RunicDocs](https://pedrovicente98.github.io/RunicDocs/).

The vault started on 2026-11-03 as an export of the documents in the
[RunicMMOEngine Drive folder](https://drive.google.com/drive/folders/1hSflbWXn8Y2Ox-3QPFpXjrVkMo5warhv). From then on the
documents are edited and merged here, in Markdown, not in Google Docs.

## Layout

```
content/                                      ← the Obsidian vault (open this folder in Obsidian)
├── index.md                                  home page (the only index.md; Quartz needs it)
├── Vision/                                   RunicGame — Complete MMORPG Vision: the rules
│   ├── RunicGame — Complete MMORPG Vision.md the document's note: introduction and sections in order
│   ├── Combat.md                             one note per H2
│   └── …
├── Architecture/                             RunicEngine — Technical Architecture: how they are built
│   ├── RunicEngine — Technical Architecture.md
│   └── …
├── Ideias/                                   RunicGame — Ideias, kept whole as history
│   ├── RunicGame — Ideias.md                 its introduction and every entry in order
│   ├── Ideias overview.md                    every idea embedded in full, in the same order
│   ├── NAV-01 Naval Raid.md                  one note per idea ID, text unchanged; the ID is its alias
│   └── Archived and Discarded ideas.md
├── Development/                              the slices checklist and one note per slice (generated, see below)
├── Visualizations/                           interactive pages, each shown in a note (see below)
├── Archive/                                  the original appendices, unchanged, even after they are merged
├── Lore/                                     one note linking to the RunicGame repository — never delete this folder
├── Quest Design/                             one note linking to the RunicGame repository — never delete this folder
└── attachments/                              images
quartz.config.yaml                            site configuration (Quartz 5)
quartz-styles/custom.scss                     site styles (the scroll box for embedded notes)
quartz-plugins/runic-graph/                   the site's graph, with the settings panel
.github/workflows/deploy.yml                  builds and publishes the site on every push to main
scripts/preview.sh|.ps1                       build and serve the site on your machine
tools/                                        the split script, the move tool, the vault checker and the visualization tools
```

| Folder | Notes |
| :--- | ---: |
| `Vision/` | 22 |
| `Architecture/` | 28 |
| `Ideias/` | 102 |
| `Development/` | 54 |
| `Visualizations/` | 4 |
| `Archive/` | 5 |
| `Lore/`, `Quest Design/` | 1 each |

## Rules

- **H1 = folder, H2 = note, H3 = section inside the note.** Headings keep the text and level they had in the documents.
  A document's own note (named after the document) holds its introduction and lists its sections in order.
- **H2s are unique in the whole vault**, so every note name is unique and links are short: `[[Combat]]`,
  `[[Weapon Class System#Loadouts|loadout]]`. A file name is the H2 without the characters Obsidian rejects (in
  practice `:`); the note's title keeps them.
- **Each fact lives in one place.** The Vision states the rule; the Architecture says how to implement it and links to
  the Vision.
- **Ideias stay whole**, as history: archived and decided entries are never removed. Each idea's ID is its alias.
- **The original appendices stay intact in `Archive/`**, also after they are merged. Merged notes get no "differences"
  or "conflicts" sections.
- **English throughout.** Titles carry no version ("RunicEngine — Technical Architecture").
- **Links.** "Section › Subsection" references, "(see X)" references, idea IDs and document names are wikilinks.

## Embedding notes

A note can show another note inside it, in a box with its own scrollbar, on the site and in Obsidian:

| Write | Shows |
| :--- | :--- |
| `![[NAV-01 Naval Raid]]` | the whole note, with its title |
| `![[Combat#Conditions, build-up and Tolerance]]` | one section, up to the next heading of the same level |
| `![[Combat#^naval-rule]]` | one paragraph, marked with ` ^naval-rule` at its end |

`Ideias overview` embeds every idea this way. The box comes from `quartz-styles/custom.scss` on the site and from the
`runicdocs-embeds` snippet in Obsidian: turn it on once in **Settings › Appearance › CSS snippets**.

## Development notes

`content/Development/` holds **RunicGame — Development** (progress and the checklist of slices), **Development
overview** (every slice embedded) and one note per slice with its packages as a checklist. They are generated; don't
edit them by hand:

```
python3 tools/sync_development.py
```

It reads the slices from the Architecture's Vertical-slice roadmap, the packages from its work-package tables, and the
status from the GitHub issues of RunicEngine, RunicPlatform and RunicGame (through `gh`, so it needs access to the three
repositories). A package is done when its issue is closed, and a slice when its issue is closed. To change a slice or a
package, change the Architecture (and its issue), then run the script; it warns when a package has no issue or an
issue has no package.

## Visualizations

`content/Visualizations/` holds interactive pages, each a single `.htm` file next to a note that shows it in a frame
(`<iframe class="runic-viz">`, styled in `quartz-styles/custom.scss`) and links to it on its own page. Quartz copies the
`.htm` files to the site as they are. The extension matters: Quartz drops `.html` from the files it copies, and the
site would then send the page as a download. Inside a note, a page follows the site's light and dark toggle through the
embed helper in `tools/templates/embed-helper.html`. In Obsidian the frames may stay empty; the link opens the page.

| Page | Made by |
| :--- | :--- |
| `slice-map.htm` (note: Slice map) | `python3 tools/build_slice_map.py`, from the roadmap, the package tables and the Development notes |
| `latency-feel-lab.htm`, `runic-database-map.htm` | pages made in Claude chats, added with `tools/add_visualization.py` |

**The slice map is generated; don't edit it by hand.** Its page comes from `tools/templates/slice-map.html`; the script
fills in the slices, the packages' needs and, from the Development notes, which packages are done and their issues.
The deploy workflow and the preview scripts run it before every build, so the site never shows a stale map. Run
`tools/sync_development.py` first when the issues changed.

**To add a page made in a Claude chat**, ask the chat to publish the visual as a page, save its HTML, then:

```
python3 tools/add_visualization.py SAVED.html page-name --title "Note title" --description "One line on what it shows."
```

It writes `content/Visualizations/page-name.htm` (with a document around it if the chat saved only the body, Mermaid
from jsDelivr instead of the claude.ai runtime, and the embed helper) and creates the note unless it exists. Add the
note to the list in **RunicGame — Visualizations**, then run `tools/check_vault.py`.

## Graph settings

The gear on the local graph and on the full graph opens a settings panel, like Obsidian's graph view:

- **Filters:** search highlights the matching notes (text, `path:Vision`, `tag:status/open`, `file:combat`); only
  matches, tags and orphans; the local graph's depth.
- **Groups:** colour the notes that match a query. The defaults are the folder colours of the Obsidian graph, set as
  `groups` in `quartz.config.yaml`.
- **Display:** arrows, text fade threshold, node size, link thickness, and Animate.
- **Forces:** center, repel, link force and link distance.

Changes apply at once and are kept in the browser's local storage, separately for the local and the full graph; the
search lasts until the page is reloaded. **Reset** goes back to the site's defaults. The site's defaults are the
`localGraph` and `globalGraph` options of the graph in `quartz.config.yaml`.

## Site navigation

- **Sidebar order:** in each folder the document's own note comes first, then its overview, then the other notes by
  name (the explorer's `sortFn` in `quartz.config.yaml`).
- **Home page:** `content/index.md` has `cssclasses: home-dashboard`, so its callouts show as a grid of cards, on the site
  (`quartz-styles/custom.scss`) and in Obsidian's reading view (the same `runicdocs-embeds` snippet).

## Moving text

Text that only changes place is moved with a script, never retyped:

```
python3 tools/move_section.py SOURCE "HEADING" TARGET [--copy] [--level N] [--after "HEADING" | --before "HEADING"] [--create] [--dry-run]
```

It cuts the section (its heading and everything up to the next heading of the same or a higher level) and pastes it
into the target note, changing nothing but the heading levels when `--level` asks for it. Use `--copy` when the source
is in `Archive/`, which stays intact. Run `--dry-run` first to see the change. `python3 tools/move_section.py -h` has
the full list of options.

After any change, run the checker:

```
python3 tools/check_vault.py
```

It reports broken links, anchors that no longer match a heading, frontmatter that does not parse, note names used more
than once, and missing required folders.

The dates the site shows come from each note's `created` and `modified` frontmatter; update `modified` when you change a
note.

## How the vault was made

`tools/drive-to-vault/build_vault.py` split each document by its headings into the notes above. The only wording
changes it made are listed in its `H2_RENAMES` and `TEXT_EDITS` (each must match an exact number of times):

- "About this document" became "About the Vision" and "About the Architecture", the only H2 used twice.
- The Architecture's title lost "v4", and so did the Vision's one mention of it.
- In the Vision, the Portuguese names of the Disciplines were dropped or translated (Song, Elementalism, Shadow, Hunt),
  and "ex.:" became "e.g.". In the Architecture, "ex.:" became "e.g." and GSH-6 names the loadouts in English.
- The Vision's two diagrams, images with Portuguese text, were redrawn in English as Mermaid.
- Two pieces of text that Google Docs had turned into equations were repaired (the relay cost in Ping Resolution and an
  SQL line in Database Layout).

The Ideias were left word for word, including the old Portuguese names they record. Every word of every document was
checked against the exports. The script is kept to document how the vault was made; running it again would overwrite
`content/` from the exports, so don't run it now that the vault is edited directly.

## Publish with GitHub Pages

Every push to `main` runs `.github/workflows/deploy.yml`: it downloads Quartz 5.0.0, copies `content/` and
`quartz.config.yaml` into it, builds, and publishes. The first build took about 15 minutes; the workflow caches
Quartz's plugins, so later builds are faster. GitHub Pages is set to **Source: GitHub Actions** in the repository
settings. If the site moves, change `baseUrl` in `quartz.config.yaml`.

### Quartz fixes for a subpath site

The site lives under `/RunicDocs/`, not at the domain root. Quartz 5.0.0's graph, explorer, search and stacked-pages
plugins looked for their data and built their links at the root, so the graph came up empty. These changes fix it
until a Quartz release includes the fixes:

- `quartz-patches/body-basepath.patch` backports a change from Quartz's main branch: each page's `<body>` gets
  `data-basepath="/RunicDocs"`.
- `quartz.lock.json` is Quartz 5.0.0's plugin lockfile with explorer, search and stacked-pages moved to their 22 March
  2026 commits, which read that attribute ("resolve links correctly on subdirectory deployments"). The graph is not in
  the lockfile: the site uses its own copy (below).
- **The graph** is `quartz-plugins/runic-graph`, a copy of the graph plugin (commit c54226d, which removes the base path
  when it works out the current page) with an Obsidian-style settings panel. It also decodes the page address, so a page
  with a non-ASCII character in its name (the "—" in "RunicGame — Ideias") finds itself instead of drawing a single
  unknown dot. The deploy and the preview scripts copy `quartz-plugins/` into Quartz, and `quartz.config.yaml` loads
  it from `./quartz-plugins/runic-graph`. Its `dist/` is committed; see its README to rebuild it after changing
  `src/`.
- `quartz.config.yaml` turns **stacked-pages off**. That plugin also works out the current page from the address and has
  no fix yet, so its tabs opened `/RunicDocs/RunicDocs/...`. Turn it back on when a newer commit removes the base path.

After the build, `tools/check_site.py` opens the site under `/RunicDocs/` in Chrome and fails the deploy if:

- the local graph isn't drawn around the page itself with its neighbours, or the full graph doesn't hold every page;
- a plugin remembers a page under the base path;
- the explorer has no links or search finds nothing;
- a link leaves the site or opens a missing page;
- an embedded note isn't filled in or has no scroll box.

## Preview on your machine

Needs Node 22 or newer and git.

```
./scripts/preview.sh          # macOS / Linux
.\scripts\preview.ps1         # Windows PowerShell
```

The first run downloads Quartz into `.quartz/` (ignored by git). Then open http://localhost:8080.
