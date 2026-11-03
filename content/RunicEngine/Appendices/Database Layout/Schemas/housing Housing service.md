---
title: "housing — Housing service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › housing — Housing service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Open-world land: zones, plots, properties built from designs, construction stages, furniture, crops and animals.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| land\_zones | zone\_id text PK; region\_id int; node\_id text ⇢ territory.nodes null; kind text; open bool | Where housing and farms may be built. — zone\_id: ContentId; kind: housing, farm, mixed; open: new areas open over time |
| plots | plot\_id bigint PK; zone\_id text → land\_zones; grid\_x int; grid\_z int; size text | Grid slots. UNIQUE (zone\_id, grid\_x, grid\_z). |
| properties | property\_id bigint PK; plot\_id bigint UQ → plots; owner\_lineage\_id bigint ⇢ character.lineages; owner\_character\_id bigint ⇢ character.characters; design\_template\_id text; state text; built\_at timestamptz null; upkeep\_due\_at timestamptz; frozen\_at timestamptz null; version int | A house or farm; the count per Lineage is limited by content rules. — state: constructing, complete, frozen, demolished |
| construction\_progress | property\_id bigint PK → properties; stage smallint PK; required jsonb; delivered jsonb | Materials per construction stage. PK (property\_id, stage). |
| furniture | furniture\_id bigint PK; property\_id bigint → properties; item\_id bigint ⇢ ledger.items; local\_x real; local\_y real; local\_z real; yaw real | Placed furniture, local to the property. — local\_x: 32-bit: local offset, not a world position |
| crops | crop\_id bigint PK; property\_id bigint → properties null; planter\_id bigint ⇢ character.characters; seed\_template text; pos\_x double; pos\_y double; pos\_z double; state text; planted\_at timestamptz; ready\_at timestamptz; tended\_at timestamptz null | Planted crops, on a plot or in the open world. — crop\_id: GlobalEntityId; state: growing, ready, withered, harvested |
| animals | animal\_id bigint PK; property\_id bigint → properties; species\_template text; state text; born\_at timestamptz; last\_cared\_at timestamptz; sick\_since timestamptz null | Neglected animals get sick but never die; only slaughter removes them. — state: young, adult, sick, slaughtered |

---

↑ [[Schemas|Schemas]] · ← [[access Housing service|access — Housing service]] · [[world World events and World routines services GWTH-1 GSVC-9|world — World events and World routines services (GWTH-1, GSVC-9)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › housing — Housing service · exported 2026-11-03
