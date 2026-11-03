---
title: "social — Chat and party groups (PCS-5)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › social — Chat and party groups (PCS-5)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · shard database · Built on decisions.* Parties and raid groups, friends and blocks, chat channels and a short chat log for moderation.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| parties | party\_id bigint PK; kind text; leader\_entity\_id bigint; loot\_rule jsonb; created\_at timestamptz; disbanded\_at timestamptz null | Parties and raid groups (up to 40). — kind: party, raid |
| party\_members | party\_id bigint PK → parties; entity\_id bigint PK; subgroup smallint; joined\_at timestamptz | PK (party\_id, entity\_id). — subgroup: raid groups of five |
| relations | subject\_entity\_id bigint PK; object\_entity\_id bigint PK; kind text PK; created\_at timestamptz | Friends and blocks. PK (subject, object, kind). — kind: friend, block |
| chat\_channels | channel\_id bigint PK; kind text; scope\_ref bigint null; created\_at timestamptz | Say, party, guild, faction, region, whisper, custom. — scope\_ref: guild, party or region the channel belongs to |
| chat\_log | message\_id bigint PK; channel\_id bigint → chat\_channels; sender\_entity\_id bigint; body text; flags int; sent\_at timestamptz | Kept 30 days (example) as moderation evidence. Partitioned daily. — flags: filtered, reported |

---

↑ [[Schemas|Schemas]] · ← [[directive World directives PCS-3|directive — World directives (PCS-3)]] · [[ledger Item ledger PBB-1|ledger — Item ledger (PBB-1)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › social — Chat and party groups (PCS-5) · exported 2026-11-03
