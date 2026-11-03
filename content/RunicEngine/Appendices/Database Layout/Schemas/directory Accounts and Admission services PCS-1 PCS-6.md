---
title: "directory — Accounts and Admission services (PCS-1, PCS-6)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › directory — Accounts and Admission services (PCS-1, PCS-6)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · global cluster · Proposal.* The list of shards for server select, capacity, the login queue and an index of where each account has characters.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| shards | shard\_id int PK; name text UQ; datacenter text; status text; population\_band text; opened\_at timestamptz | A shard is what the docs call a world: one server copy of the game, with its own database. — datacenter: sa, na, eu; status: open, locked, maintenance, closed; population\_band: shown in server select |
| shard\_capacity | shard\_id int PK → shards; max\_concurrent int; queue\_enabled bool; updated\_at timestamptz | Per-shard capacity limits for the launch phases. |
| lineage\_index | account\_id bigint PK ⇢ account.accounts; shard\_id int PK → shards; lineage\_id bigint; character\_count smallint; last\_played\_at timestamptz null | Lets server select show the account's characters without querying every shard. PK (account\_id, shard\_id). — lineage\_id: id inside that shard's database |
| login\_queue | entry\_id bigint PK; shard\_id int → shards; account\_id bigint ⇢ account.accounts; cohort\_id text → admission\_cohorts null; enqueued\_at timestamptz; admitted\_at timestamptz null | Persisted queue so a restart keeps everyone's place. |
| admission\_cohorts | cohort\_id text PK; rule jsonb; opens\_at timestamptz | Waves by account cohort for the gradual free-to-play phase. |

---

↑ [[Schemas|Schemas]] · ← [[ticket Accounts service PCS-1|ticket — Accounts service (PCS-1)]] · [[coordinator World Coordinator PCS-2 PCS-7|coordinator — World Coordinator (PCS-2, PCS-7)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › directory — Accounts and Admission services (PCS-1, PCS-6) · exported 2026-11-03
