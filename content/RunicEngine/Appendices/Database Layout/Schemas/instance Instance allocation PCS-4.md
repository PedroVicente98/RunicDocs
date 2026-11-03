---
title: "instance — Instance allocation (PCS-4)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › instance — Instance allocation (PCS-4)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · shard database · Built on decisions.* Instances allocated from Agones fleets: dungeons, raids, naval raids, the [[Inventory equipment and the Market Isle#Market Isle (working name)|Market Isle]], rifts, arenas.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| instances | instance\_id bigint PK; map\_id int ⇢ coordinator.maps; kind text; simulation\_id bigint ⇢ coordinator.simulations null; owner\_group\_id bigint ⇢ social.parties null; state text; created\_at timestamptz; closes\_at timestamptz null | One row per allocated copy of a map. — instance\_id: InstanceId; kind: dungeon, raid, naval\_raid, shop\_island, rift, battleground, arena; state: allocating, ready, running, closing, closed |
| instance\_members | instance\_id bigint PK → instances; entity\_id bigint PK; joined\_at timestamptz; left\_at timestamptz null | Who entered. PK (instance\_id, entity\_id). — entity\_id: a character's GlobalEntityId |

---

↑ [[Schemas|Schemas]] · ← [[coordinator World Coordinator PCS-2 PCS-7|coordinator — World Coordinator (PCS-2, PCS-7)]] · [[directive World directives PCS-3|directive — World directives (PCS-3)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › instance — Instance allocation (PCS-4) · exported 2026-11-03
