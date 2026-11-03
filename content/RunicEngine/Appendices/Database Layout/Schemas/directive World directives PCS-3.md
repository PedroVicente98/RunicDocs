---
title: "directive — World directives (PCS-3)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › directive — World directives (PCS-3)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · shard database · Built on decisions.* Time-boxed world-wide overrides (weather, wind, current) with an effective world time and a duration.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| directives | directive\_id bigint PK; kind text; target jsonb; payload jsonb; effective\_world\_ms bigint; duration\_ms bigint; source text; created\_by bigint null; created\_at timestamptz; cancelled\_at timestamptz null | Delivered to every simulation through NATS; applied at the same world time everywhere. — kind: weather, wind, current, custom; target: region, node or area; effective\_world\_ms: world time, not wall time; source: the Game service or operator panel that asked |

---

↑ [[Schemas|Schemas]] · ← [[instance Instance allocation PCS-4|instance — Instance allocation (PCS-4)]] · [[social Chat and party groups PCS-5|social — Chat and party groups (PCS-5)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › directive — World directives (PCS-3) · exported 2026-11-03
