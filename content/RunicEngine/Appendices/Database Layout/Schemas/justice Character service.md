---
title: "justice — Character service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › justice — Character service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Proposal.* ArcheAge-style trials with player jurors and judges. Still an idea in [[Vision|the Vision]]; tables shown so the shape is known.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| trials | trial\_id bigint PK; defendant\_id bigint ⇢ character.characters; infamy\_at\_trial int; judge\_id bigint ⇢ character.characters null; state text; verdict text null; sentence\_minutes int null; scheduled\_at timestamptz; decided\_at timestamptz null | A trial for a character with enough [[Factions PvP and crime#Outlaw and Infamy\|Infamy]]. — state: pending, in\_session, decided, expired |
| trial\_jurors | trial\_id bigint PK → trials; juror\_id bigint PK ⇢ character.characters; vote text null; voted\_at timestamptz null | PK (trial\_id, juror\_id). |
| jail\_sentences | sentence\_id bigint PK; character\_id bigint ⇢ character.characters; trial\_id bigint → trials null; starts\_at timestamptz; ends\_at timestamptz; served\_seconds int; released\_at timestamptz null | Time served, kept across logouts. |

---

↑ [[Schemas|Schemas]] · ← [[cartography Character service|cartography — Character service]] · [[inventory Inventory service GSVC-2|inventory — Inventory service (GSVC-2)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › justice — Character service · exported 2026-11-03
