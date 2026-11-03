---
title: "ledger — Item ledger (PBB-1)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › ledger — Item ledger (PBB-1)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · shard database (same database as wallet) · Built on decisions.* Containers, slots and item instances with atomic transfers and operation IDs. Mechanisms only: the Game gives meaning to owner kinds, container kinds and the item payload.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| containers | container\_id bigint PK; owner\_kind text; owner\_id bigint; kind text; scope text null; capacity int; created\_at timestamptz; version int | Any place an item can be: bag, equipment, storage, guild bank, house chest, mail, escrow. — owner\_kind: opaque to the Platform: character, lineage, guild, house, ship, mail, escrow...; kind: game-defined: bag, equipment, storage, profession\_kit...; scope: game-defined location, e.g. a guild bank's city; capacity: expansions are ledger operations |
| items | item\_id bigint PK; template\_id text; quantity int; container\_id bigint → containers; slot int; payload jsonb; created\_op uuid → operations; created\_at timestamptz; version int | Every item instance. UNIQUE (container\_id, slot). — template\_id: ContentId of the item definition; payload: game-defined: grade, durability, binding, infusion, crafter, chart edition... |
| operations | op\_id uuid PK; kind text; requested\_by text; request\_hash bytea; status text; created\_at timestamptz; committed\_at timestamptz null | One row per durable item operation; the idempotency key of the ledger. — op\_id: SimulationId \+ sequence, or service-made; kind: grant, move, split, merge, consume, destroy, capacity; requested\_by: service name; status: committed, rejected, compensated |
| operation\_entries | entry\_id bigint PK; op\_id uuid → operations; item\_id bigint; template\_id text; from\_container bigint null; from\_slot int null; to\_container bigint null; to\_slot int null; quantity\_delta int; payload\_before jsonb null; payload\_after jsonb null | Audit history of every item movement. Never deleted. Partitioned monthly. — item\_id: not an FK: the item may be destroyed |
| supply\_counters | template\_id text PK; period\_start date PK; created bigint; destroyed bigint | Supply per item type and period (Security appendix). PK (template\_id, period\_start). |
| compensations | compensation\_id bigint PK; original\_op uuid → operations; compensating\_op uuid → operations; reason text; approved\_by bigint; at timestamptz | Rollback by a compensating operation, never by deleting history. |

---

↑ [[Schemas|Schemas]] · ← [[social Chat and party groups PCS-5|social — Chat and party groups (PCS-5)]] · [[wallet Currency wallets PBB-2 PBB-3|wallet — Currency wallets (PBB-2, PBB-3)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › ledger — Item ledger (PBB-1) · exported 2026-11-03
