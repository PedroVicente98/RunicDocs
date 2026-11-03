---
title: "Where each thing lives"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Where each thing lives"
created: "2026-10-26"
modified: "2026-10-30"
---

Mobs, stats and definitions are not database rows. The database holds only what must survive a restart and cannot be recomputed.

| Thing | Content (cooked data) | Simulation (memory) | Database |
| :---- | :---- | :---- | :---- |
| Creatures and mobs | Definitions, stats, AI trees, loot tables, spawn areas and routines | Every live mob: HP, threat, position, AI memory | No row per mob. Only world bosses, bestiary knowledge, routine exceptions and kill-based lockouts |
| Character stats | Formulas and base values per race, class, level and gear | Resolved attributes: level, gear, build and buffs together | Never stored; rebuilt on load. Only effects that outlive a session (character\_effects) |
| Characters | Races, classes, skill definitions | Position, health, statuses, cooldowns, combat state | Character row, build, checkpoint, progression, durable cooldowns |
| Items | Item definitions, grades, recipes | A mirror of equipped items and their modifiers ([[GPL-4\|GPL-4]]) | Every item instance in the ledger: owner, slot, payload |
| Skills | Skills, trees, timelines | Timelines, cooldowns, input queue | Points spent, milestone choices, skill bars |
| Quests and story | Quest and chapter definitions | Quest runtime: objectives advance in the same tick | Progress, completions, rewards, branches taken |
| World | Regions, volumes, node borders and connections, spawn areas, routes, water | Loaded cells, spawned resources, routine positions | Node state, castles, houses, crops, animals, [[Trade packs and routes\|trade packs]], events, rifts |
| Currency | Currency definitions | Nothing; the simulation only requests changes | Wallets with double-entry history |
| Map knowledge | The cell grid from the cook | Cells crossed since the last batch | Bitsets per Lineage, map, layer and kind |
| Soundtrack and client settings | Albums shipped with the game | Nothing | Nothing: playlists stay on the player's machine (local profile) |

---

↑ [[Database Layout|Database Layout]] · ← [[Conventions Proposal|Conventions (Proposal)]] · [[Connections|Connections]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Where each thing lives · exported 2026-11-03
