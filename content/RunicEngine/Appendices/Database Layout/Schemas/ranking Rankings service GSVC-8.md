---
title: "ranking — Rankings service (GSVC-8)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › ranking — Rankings service (GSVC-8)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Seasons, ranked arena ratings, match history, world boss contributions and leaderboards.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| seasons | season\_id bigint PK; kind text; starts\_at timestamptz; ends\_at timestamptz | PvP and other ranked seasons. — kind: pvp, boss, honor |
| pvp\_ratings | character\_id bigint PK ⇢ character.characters; bracket text PK; season\_id bigint PK → seasons; rating int; wins int; losses int | PK (character\_id, bracket, season\_id). — bracket: 1v1, 2v2, 3v3, 5v5 |
| pvp\_matches | match\_id bigint PK; kind text; bracket text null; instance\_id bigint ⇢ instance.instances; started\_at timestamptz; ended\_at timestamptz null | Arenas and battlegrounds. — kind: arena, battleground |
| match\_participants | match\_id bigint PK → pvp\_matches; character\_id bigint PK ⇢ character.characters; team smallint; result text; rating\_before int null; rating\_after int null; kills int; deaths int | PK (match\_id, character\_id). |
| boss\_contributions | kill\_id bigint PK ⇢ world.boss\_kills; character\_id bigint PK ⇢ character.characters; contribution int | PK (kill\_id, character\_id). |
| leaderboards | board\_id text PK; season\_id bigint PK → seasons; subject\_id bigint PK; score bigint; rank int; updated\_at timestamptz | Computed boards. PK (board\_id, season\_id, subject\_id). — subject\_id: character or guild |

---

↑ [[Schemas|Schemas]] · ← [[world World events and World routines services GWTH-1 GSVC-9|world — World events and World routines services (GWTH-1, GSVC-9)]] · [[production Character service GSRV-7 GSVC-7|production — Character service (GSRV-7, GSVC-7)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › ranking — Rankings service (GSVC-8) · exported 2026-11-03
