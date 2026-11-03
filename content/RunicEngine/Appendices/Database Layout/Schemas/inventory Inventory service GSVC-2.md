---
title: "inventory — Inventory service (GSVC-2)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › inventory — Inventory service (GSVC-2)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Game meaning over the Platform ledger: which container is whose bag, equipment, profession kit or global storage; loot grants; supply alerts.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| owner\_containers | owner\_kind text PK; owner\_id bigint PK; role text PK; scope text PK; container\_id bigint UQ ⇢ ledger.containers; created\_at timestamptz | Maps a game role to a ledger container. PK (owner\_kind, owner\_id, role, scope). — owner\_kind: character, lineage, guild, house, ship; role: bag, equipment, profession\_kit:mining, storage, guild\_bank, house\_chest, library...; scope: bank location for the guild bank, '-' otherwise (personal storage is one global chest) |
| loot\_grants | grant\_id uuid PK; character\_id bigint ⇢ character.characters; source text; status text; ledger\_op uuid ⇢ ledger.operations null; created\_at timestamptz | A loot grant is applied once across reconnects. — grant\_id: the kill fact's stable ID; source: kill, chest, quest, event, coin\_purse; status: pending, committed, rejected |
| supply\_alerts | alert\_id bigint PK; template\_id text; period date; threshold bigint; observed bigint; raised\_at timestamptz; acknowledged\_by bigint null | Daily supply alerts from the ledger counters. |

---

↑ [[Schemas|Schemas]] · ← [[justice Character service|justice — Character service]] · [[vehicle Inventory service|vehicle — Inventory service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › inventory — Inventory service (GSVC-2) · exported 2026-11-03
