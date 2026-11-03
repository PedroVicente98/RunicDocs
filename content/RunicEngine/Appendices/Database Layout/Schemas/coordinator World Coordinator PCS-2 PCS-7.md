---
title: "coordinator — World Coordinator (PCS-2, PCS-7)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › coordinator — World Coordinator (PCS-2, PCS-7)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · shard database · Built on decisions.* Maps, regions, neighbors, live simulations and who owns what. Operational state the Coordinator must recover after its own restart.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| maps | map\_id int PK; content\_id text; kind text; world\_epoch\_ms bigint | The Engine's WorldId: the main world, the sky world, instance maps. — map\_id: WorldId; content\_id: game:map/...; kind: main, persistent, instance\_template; world\_epoch\_ms: start of world time for the Environment clock |
| regions | region\_id int PK; map\_id int → maps; content\_id text; origin\_x double; origin\_y double; origin\_z double; boundary jsonb; content\_build text | Cooked regions with their 64-bit origin. — origin\_x: WorldPosition, 64-bit; boundary: polygon from the cook; content\_build: cook build that produced it |
| region\_neighbors | region\_id int PK → regions; neighbor\_id int PK → regions; border\_kind text | Neighbor topology for [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] candidates. PK (region\_id, neighbor\_id). — border\_kind: land, sea, sky |
| simulations | simulation\_id bigint PK; pod\_name text; node\_name text; state text; vcpus smallint; started\_at timestamptz; heartbeat\_at timestamptz | Running GameServer pods. — simulation\_id: SimulationId; state: starting, ready, draining, shutdown |
| authority\_assignments | assignment\_id bigint PK; region\_id int → regions; partition\_bounds jsonb null; simulation\_id bigint → simulations; epoch bigint; assigned\_at timestamptz; released\_at timestamptz null | Which simulation owns a region or an authority partition, with its epoch. — partition\_bounds: null \= the whole region; never cuts an indivisible volume; epoch: AuthorityEpoch |
| placement\_moves | move\_id bigint PK; simulation\_id bigint → simulations; from\_node text; to\_node text; reason text; started\_at timestamptz; finished\_at timestamptz null | Move-by-handoff history (load, traffic, resize). — reason: load, traffic, resize |

---

↑ [[Schemas|Schemas]] · ← [[directory Accounts and Admission services PCS-1 PCS-6|directory — Accounts and Admission services (PCS-1, PCS-6)]] · [[instance Instance allocation PCS-4|instance — Instance allocation (PCS-4)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › coordinator — World Coordinator (PCS-2, PCS-7) · exported 2026-11-03
