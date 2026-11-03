---
title: "cartography — Character service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › cartography — Character service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Chart editions, survey jobs and the [[Maps and cartography#Triangulation (base chart on land)|triangulation]] tools placed in the world, and perishable information.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| chart\_editions | edition\_id bigint PK; chart\_kind text; region\_id int; node\_id text null; season text null; coverage bytea; created\_at timestamptz | A chart's content: kind, area, season. Chart items point to an edition in their payload. — chart\_kind: land, nautical, mobs, resources, events...; coverage: cells this edition covers |
| survey\_jobs | job\_id bigint PK; character\_id bigint ⇢ character.characters; node\_id text ⇢ territory.nodes; chart\_kind text; state text; score real null; result\_edition\_id bigint → chart\_editions null; started\_at timestamptz | A survey in progress at one node; scored by geometry only. — state: placing, measuring, done, failed, abandoned |
| survey\_markers | marker\_id bigint PK; job\_id bigint → survey\_jobs; item\_id bigint ⇢ ledger.items; pos\_x double; pos\_y double; pos\_z double; state text; destroyed\_by bigint null; placed\_at timestamptz | The three tools placed in the world; others can destroy them. — marker\_id: GlobalEntityId of the placed tool; item\_id: the tool item, recovered or lost; state: placed, recovered, destroyed |
| perishable\_reports | report\_id bigint PK; kind text; node\_id text ⇢ territory.nodes; data jsonb; item\_id bigint ⇢ ledger.items null; expires\_at timestamptz | Rotating resource richness and event timers that expire. — kind: resource\_richness, event\_timer |

---

↑ [[Schemas|Schemas]] · ← [[character Character service GSVC-1 5 7 10|character — Character service (GSVC-1, 5, 7, 10)]] · [[justice Character service|justice — Character service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › cartography — Character service · exported 2026-11-03
