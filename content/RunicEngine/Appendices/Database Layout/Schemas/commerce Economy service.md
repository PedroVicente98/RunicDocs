---
title: "commerce — Economy service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › commerce — Economy service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Trade packs: world entities, not inventory items, with their origin node and the route a Go service records; pack demand per region and the black market's stock.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| trade\_packs | pack\_id bigint PK; template\_id text; origin\_node\_id text ⇢ territory.nodes; crafted\_by bigint ⇢ character.characters; state text; holder\_entity\_id bigint null; map\_id int null; pos\_x double null; pos\_y double null; pos\_z double null; delivery\_node\_id text ⇢ territory.nodes null; payout bigint null; crafted\_at timestamptz; delivered\_at timestamptz null; version int | A pack's durable state; floating packs stay until a hard reset. — pack\_id: GlobalEntityId; state: carried, cargo, dropped, floating, delivered, destroyed; holder\_entity\_id: carrier or vehicle |
| pack\_route | pack\_id bigint PK → trade\_packs; seq smallint PK; node\_id text ⇢ territory.nodes; danger smallint; entered\_at timestamptz | Nodes passed; repeats and loops are ignored when pricing. PK (pack\_id, seq). — danger: danger level when passed |

---

↑ [[Schemas|Schemas]] · ← [[economy Economy service GSVC-4|economy — Economy service (GSVC-4)]] · [[trade Trade service GSVC-4|trade — Trade service (GSVC-4)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › commerce — Economy service · exported 2026-11-03
