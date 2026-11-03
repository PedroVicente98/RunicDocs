---
title: "RunicDocs"
aliases:
  - "Home"
tags:
  - "home"
created: "2026-11-03"
modified: "2026-11-03"
---

This site is the RunicGame and RunicEngine design documentation, compiled from the documents in the
[RunicMMOEngine Drive folder](https://drive.google.com/drive/folders/1hSflbWXn8Y2Ox-3QPFpXjrVkMo5warhv) on 2026-11-03. Every note says which document and section it comes from.

## RunicGame — the game

- [[Vision|Complete MMORPG Vision]]: how the game should work, and every recorded decision.
- [[Ideias|Ideias]]: the ideas inbox, one note per idea ID with its status.
- [[Lore|Lore]] and [[Quest Design|Quest Design]]: they live in the RunicGame repository, in the
  [RunicWorld vault](https://github.com/PedroVicente98/RunicGame/tree/main/docs/RunicWorld).
- Appendices, until they are merged into [[Vision|the Vision]]: [[Nodes Economy and Exploration|Nodes, Economy and Exploration]],
  [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]], [[Ping Resolution|Ping Resolution]].

## RunicEngine — the technology

![[runicengine-layered-architecture.png]]
*RunicEngine layered architecture*

- [[Architecture|Technical Architecture v4]]: how the Engine, the Platform and the Game are built.
- [[Roadmap|Vertical-slice roadmap]]: one note per slice, with its packages.
- [[Packages|Work Packages]]: one note per package, linked to what it needs.
- Appendices, until they are merged into the Architecture: [[Security|Security]], [[Database Layout|Database Layout]].

## How to read it

- **Hierarchy.** Each document is a folder whose main note has the folder's name and lists its sections in order.
  Sections are notes, and long sections are folders of their own. Every note links up to its parent and to the
  previous and next section.
- **Graph.** Links carry the connections between documents: idea IDs (like [[NAV-01 Naval Raid|NAV-01]]), package IDs (like [[PCS-1|PCS-1]]), slice
  numbers, document names and key terms ([[Weapon Class System#Disciplines|Disciplines]], [[Labor|Labor]], [[Simulation core Flecs and Jolt#Flecs rules|Flecs]], [[Simulation core Flecs and Jolt#Jolt rules|Jolt]]…) all link to where they are defined.
  The graph on the right shows a note's neighbourhood; open it full-screen to see the whole map.
- **Labels.** The documents mark items as Decided (or Decision), Proposal and Open. Numbers are examples that show the
  shape; final values come from development and playtests.
- **Tags.** `vision`, `architecture`, `ideias`, `appendix`, `idea` with `status/…`, `package` and `slice` with
  `repo/engine`, `repo/platform` and `repo/game`.
