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
│   ├── NAV-01 Naval Raid.md                  one note per idea ID, text unchanged; the ID is its alias
│   └── Archived and Discarded ideas.md
├── Archive/                                  the original appendices, unchanged, even after they are merged
├── Lore/                                     one note linking to the RunicGame repository — never delete this folder
├── Quest Design/                             one note linking to the RunicGame repository — never delete this folder
└── attachments/                              images
quartz.config.yaml                            site configuration (Quartz 5)
.github/workflows/deploy.yml                  builds and publishes the site on every push to main
scripts/preview.sh|.ps1                       build and serve the site on your machine
tools/                                        the split script, the move tool and the vault checker
```

| Folder | Notes |
| :--- | ---: |
| `Vision/` | 22 |
| `Architecture/` | 28 |
| `Ideias/` | 99 |
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
plugins looked for their data and built their links at the root, so the graph came up empty. Two files fix it until a
Quartz release includes the fixes:

- `quartz-patches/body-basepath.patch` backports a change from Quartz's main branch: each page's `<body>` gets
  `data-basepath="/RunicDocs"`.
- `quartz.lock.json` is Quartz 5.0.0's plugin lockfile with those four plugins moved to their 22 March 2026 commits,
  which read that attribute ("resolve links correctly on subdirectory deployments").

After the build, `tools/check_site.py` opens the site under `/RunicDocs/` in Chrome and fails the deploy if the graph
draws nothing, the explorer has no links, search finds nothing, or a link leaves the site.

## Preview on your machine

Needs Node 22 or newer and git.

```
./scripts/preview.sh          # macOS / Linux
.\scripts\preview.ps1         # Windows PowerShell
```

The first run downloads Quartz into `.quartz/` (ignored by git). Then open http://localhost:8080.
