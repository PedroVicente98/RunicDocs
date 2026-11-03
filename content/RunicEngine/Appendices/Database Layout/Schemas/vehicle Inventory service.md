---
title: "vehicle — Inventory service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › vehicle — Inventory service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Proposal.* State that belongs to summon items: ships with their stations, mounts, and ship construction sites.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| ships | ship\_id bigint PK; summon\_item\_id bigint UQ ⇢ ledger.items; owner\_id bigint ⇢ character.characters; template\_id text; name text null; hull\_hp int; state text; permission\_level text; last\_pos\_x double null; last\_pos\_y double null; last\_pos\_z double null; summoned\_at timestamptz null; version int | A ship lives as a summon item; this row holds its state between summons. — ship\_id: GlobalEntityId while summoned; template\_id: clipper, brigantine, galleon...; state: stored, summoned, sinking, sunk, destroyed; permission\_level: crew, party, guild, anyone |
| ship\_stations | ship\_id bigint PK → ships; station\_key text PK; hp int; state text; ammo int null | Each station is destroyed and repaired separately. PK (ship\_id, station\_key). — station\_key: cannon\_port\_1, sail\_main, repair, arcane, archer...; state: ok, destroyed |
| mounts | mount\_id bigint PK; summon\_item\_id bigint UQ ⇢ ledger.items; owner\_id bigint ⇢ character.characters; template\_id text; name text null; level smallint; xp bigint; state text; revive\_at timestamptz null; kit\_mods jsonb | Mount state between summons. — state: stabled, summoned, downed; kit\_mods: skill changes the mount brings |
| construction\_sites | site\_id bigint PK; owner\_id bigint ⇢ character.characters; design\_template\_id text; port\_node\_id text ⇢ territory.nodes; pos\_x double; pos\_y double; pos\_z double; delivered jsonb; state text; created\_at timestamptz; expires\_at timestamptz | Ship platform from a [[Inventory equipment and the Market Isle#Market Isle (working name)\|Market Isle]] design; returns the design if unfinished in about 4 h. — site\_id: GlobalEntityId of the platform; delivered: packs delivered so far; state: building, completed, expired |

---

↑ [[Schemas|Schemas]] · ← [[inventory Inventory service GSVC-2|inventory — Inventory service (GSVC-2)]] · [[quest Quest service GSVC-3|quest — Quest service (GSVC-3)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › vehicle — Inventory service · exported 2026-11-03
