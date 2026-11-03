# RunicDocs

The RunicGame and RunicEngine design documentation as an Obsidian vault, published as a website with
[Quartz](https://quartz.jzhao.xyz) (folder explorer, backlinks and the note graph).

It was compiled on 2026-11-03 from the documents in the
[RunicMMOEngine Drive folder](https://drive.google.com/drive/folders/1hSflbWXn8Y2Ox-3QPFpXjrVkMo5warhv).
Every note ends with a link to the Google Doc and section it came from.

## What is inside

| Area | Notes | From |
| :--- | ---: | :--- |
| `RunicGame/Vision` | 28 | RunicGame — Complete MMORPG Vision |
| `RunicGame/Ideias` | 99 | RunicGame — Ideias: one note per idea ID, plus the archived and discarded table |
| `RunicGame/Lore` | 1 | A note pointing to the RunicGame repository, where the Lore lives |
| `RunicGame/Quest Design` | 1 | A note pointing to the RunicGame repository, where the Quest Design lives |
| `RunicGame/Appendices` | 43 | Nodes, Economy and Exploration · Content Pipeline and Art Direction · Ping Resolution |
| `RunicEngine/Architecture` | 147 | RunicEngine — Technical Architecture v4 |
| `RunicEngine/Roadmap` | 53 | The vertical-slice roadmap table, one note per slice |
| `RunicEngine/Packages` | 249 | The work-package tables, one note per package, grouped by repository and module |
| `RunicEngine/Appendices` | 58 | Security · Database Layout |

680 notes and about 6,700 links. Nothing was rewritten: the text is the documents' own, checked word by word against
the exports.

**Appendices** stay here until their content is merged into the Vision or the Architecture. On 2026-11-03 most of it
wasn't yet: Security, Ping Resolution, Database Layout and Content Pipeline were 89–98% absent from both documents,
and Nodes, Economy and Exploration about half. After a merge, delete the appendix folder (or rebuild without it).

```
content/                          ← the Obsidian vault (open this folder in Obsidian)
├── index.md                      home page (the only index.md)
├── RunicGame/
│   ├── Vision/
│   │   ├── Vision.md             the document's main note: intro and contents, in document order
│   │   ├── Combat.md             one note per section
│   │   └── Recorded decisions and next steps/   a long section becomes a folder with a main note of the same name
│   ├── Ideias/                   Ideias.md, NAV-01 Naval Raid.md, LAND-01 Land Ownership.md, …
│   ├── Lore/Lore.md              → RunicGame repository
│   ├── Quest Design/Quest Design.md   → RunicGame repository
│   └── Appendices/
├── RunicEngine/
│   ├── Architecture/             Architecture.md and its sections
│   ├── Roadmap/                  Roadmap.md, Slice 00 Build skeleton.md … Slice 44 Expansion.md
│   ├── Packages/                 Packages.md, Engine/CMB Combat/CMB Combat.md, Engine/CMB Combat/CMB-3.md, …
│   └── Appendices/
└── attachments/                  the diagrams embedded in the documents
quartz.config.yaml                site configuration (Quartz 5)
.github/workflows/deploy.yml      builds and publishes the site on every push to main
scripts/preview.sh|.ps1           build and serve the site on your machine
tools/                            the converter that built the vault, and a vault checker
```

## Names and links

- **Every file name is unique** in the vault, ignoring case and folder, so links are short: `[[Combat]]`,
  `[[PCS-1]]`, `[[Weapon Class System#Loadouts|loadout]]`. Obsidian is set to write new links the same way, and
  Quartz resolves them by name.
- **Main notes** have their folder's name (`Vision/Vision.md`), the convention of Obsidian's Folder Notes plugin.
- **Sections** use their heading as the file name, without numbers. When two headings are the same, each gets its
  parent in parentheses: `Ownership (Water system)`, `Open (Security)`, `About this document (Vision)`.
- **Order.** File explorers sort alphabetically. The document's order is in each main note's contents list and in the
  previous/next links at the bottom of every section.

## How the notes connect

- **Hierarchy.** Every note links up to its parent (the main note of its folder, or the home page) and to the previous
  and next section.
- **Idea IDs** (`NAV-01`, `QUEST-02`…) link to the idea's note wherever they appear. Each idea note links to the Vision
  section named in its *Game vision* field and is tagged with its status (`status/open`, `status/partial`,
  `status/being-designed`, `status/in-game-vision`, `status/discarded`).
- **Package IDs** (`PCS-1`, `SIM-6`, `GSVC-11`…) link to the package's note. A package note links to the packages it
  needs, so the notes form the dependency graph, and to the slice that first needs it.
- **Slices** ("slice 44", the roadmap table, the *Slice* columns) link to the slice notes, which list their packages.
- **Documents and terms.** Document names, the documents' Google Docs links and about 65 key terms (Disciplines, Labor,
  Market Isle, Flecs, Jolt, GameNetworkingSockets, defender grace…) link to where they are defined, once per note.
  Mentions of the Lore and the Quest Design link to their notes here, which point on to the RunicGame repository.
- **Tags.** `vision`, `ideias`, `appendix`, `architecture`, `idea`, `package`, `slice`, `redirect`, and `repo/engine`,
  `repo/platform`, `repo/game` for the Architecture sections, packages and slices that name an owner.

## Publish with GitHub Pages

1. Push this repository to GitHub.
2. In the repository, open **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Every push to `main` runs `.github/workflows/deploy.yml`: it downloads Quartz 5.0.0, copies `content/` and
   `quartz.config.yaml` into it, builds, and publishes. The site appears at
   `https://pedrovicente98.github.io/runicdocs/`.

The site is public even if the repository is private (on plans that allow Pages for private repositories). Each note's
footer links to its Google Doc, and the Lore and Quest Design notes link to the RunicGame repository; people without
access to those can't open the links.

If the site lives at another address, change `baseUrl` in `quartz.config.yaml`.

## Preview on your machine

Needs Node 22 or newer and git.

```
./scripts/preview.sh          # macOS / Linux
.\scripts\preview.ps1         # Windows PowerShell
```

The first run downloads Quartz into `.quartz/` (ignored by git). Then open http://localhost:8080. Re-run after editing
notes.

## Editing

Open `content/` as a vault in Obsidian and edit as usual. After moving or renaming notes, run the checker:

```
python3 tools/check_vault.py
```

It reports broken links, anchors that no longer match a heading, frontmatter that does not parse, and note names used
more than once.

## Rebuilding from the Drive documents

While the Google Docs are still the source of truth, the vault can be regenerated from fresh exports. This rebuilds
`content/` from scratch (keeping `content/.obsidian`), so don't use it once you start editing the vault directly.

1. Export each document with **File → Download → Markdown (.md)** into one folder, with these names:
   `RunicGame_Complete_MMORPG_Vision.md`, `RunicGame_Ideias.md`, `RunicEngine_Technical_Architecture_v4.md`,
   `RunicGame_Appendix_Nodes_Economy_and_Exploration.md`, `RunicGame_Appendix_Content_Pipeline_and_Art_Direction.md`,
   `RunicGame_Appendix_Ping_Resolution.md`, `RunicEngine_Appendix_Security.md`,
   `RunicEngine_Appendix_Database_Layout.md`, and optionally `RunicEngine_Layered_Architecture.png`.
2. Run `python3 tools/drive-to-vault/build_vault.py <export folder> content`, then `python3 tools/check_vault.py`.

The script's header explains what it produces. Its `DOCS` list says which documents are included (remove an appendix
there once it is merged), and its `TERMS` list holds the curated term links; add a term there to link it across the
vault. `tools/drive-to-vault/docsjson2md.py` converts a Google Docs API JSON export (`documents.get`) to Markdown, for
documents whose Markdown export isn't available.

## Notes on the conversion

- **Code samples.** Google's Markdown export writes the Architecture's code as plain paragraphs. The converter rebuilt
  them as fenced blocks with a language (C++, GDScript, Go, YAML, JSON, XML, CMake or plain text).
- **Formulas.** The three formulas in the Architecture are kept as LaTeX (`$$…$$`); every other dollar sign is escaped.
- **Equation glitches in the Google Docs.** Google Docs turned two pieces of text into equation objects, which export
  badly. The vault has them repaired; the Docs still need the fix:
  - *Ping Resolution*, relay routing cost: "US\$0.025 per hour per accelerator plus US\$0.007 to 0.105 per GB… US\$0.035
    per GB, 1,000 concurrent players add about US\$3.50 per hour".
  - *Database Layout*, the Go example: `ledger_op=$1 WHERE grant_id=$1`.
