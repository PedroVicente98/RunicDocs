---
title: "behavior — Behavior scoring service (GSVC-11)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › behavior — Behavior scoring service (GSVC-11)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Per-minute behavior summaries, scores, flags and ban waves. Features and thresholds stay secret and server-side.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| minute\_summaries | character\_id bigint PK ⇢ character.characters; minute timestamptz PK; summary bytea | About 128 bytes per player per minute; about 1.8 GB a day at 10,000 players. 14-day retention. PK (character\_id, minute). Partitioned daily. |
| scores | character\_id bigint PK ⇢ character.characters; model\_version int PK; score real; features jsonb; updated\_at timestamptz | PK (character\_id, model\_version). |
| flags | flag\_id bigint PK; character\_id bigint ⇢ character.characters; score real; reason text; reviewed\_by bigint null; outcome text null; created\_at timestamptz | Automation only flags; a person reviews before any permanent ban. |
| ban\_waves | wave\_id bigint PK; scheduled\_at timestamptz; executed\_at timestamptz null | Detect now, ban later in batches. |
| wave\_members | wave\_id bigint PK → ban\_waves; account\_id bigint PK ⇢ account.accounts; flag\_id bigint → flags | PK (wave\_id, account\_id). |

---

↑ [[Schemas|Schemas]] · ← [[moderation Moderation service GSVC-12 GSRV-9|moderation — Moderation service (GSVC-12, GSRV-9)]] · [[content Deploy pipeline read-only for services|content — Deploy pipeline (read-only for services)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › behavior — Behavior scoring service (GSVC-11) · exported 2026-11-03
