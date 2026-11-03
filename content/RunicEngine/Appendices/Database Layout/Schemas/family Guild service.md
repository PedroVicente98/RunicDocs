---
title: "family — Guild service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › family — Guild service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Family (ArcheAge-style mini guild per character, may mix factions) and marriage, which is per character, between different Lineages.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| families | family\_id bigint PK; name citext UQ; leader\_id bigint ⇢ character.characters; created\_at timestamptz; disbanded\_at timestamptz null | One family. |
| family\_members | character\_id bigint PK ⇢ character.characters; family\_id bigint → families; role text; joined\_at timestamptz | One family per character. |
| marriages | marriage\_id bigint PK; character\_a bigint ⇢ character.characters; character\_b bigint ⇢ character.characters; family\_name text null; altar\_id text; officiant\_id bigint null; state text; divorce\_by bigint null; divorce\_requested\_at timestamptz null; divorce\_effective\_at timestamptz null; remarry\_lock\_until timestamptz null; ceremony\_at timestamptz | Ceremony at an [[Real exploration#Altars, death, respawn and teleports\|Altar]]; unilateral divorce takes about 48 h, together it is instant. One active marriage per character (partial unique index). — family\_name: optional couple name, the account name is unchanged; officiant\_id: null \= NPC priest; state: active, divorce\_pending, divorced |
| marriage\_guests | marriage\_id bigint PK → marriages; character\_id bigint PK ⇢ character.characters; buff\_until timestamptz | Guests get a small buff for a few hours. PK (marriage\_id, character\_id). |

---

↑ [[Schemas|Schemas]] · ← [[guild Guild service|guild — Guild service]] · [[access Housing service|access — Housing service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › family — Guild service · exported 2026-11-03
