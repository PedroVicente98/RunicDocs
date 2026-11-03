---
title: "content — Deploy pipeline (read-only for services)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › content — Deploy pipeline (read-only for services)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Proposal.* Optional mirror of the cooked content catalog for admin panels and an armory site. Definitions themselves stay in the cooked Data files.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| builds | build\_id text PK; engine\_version text; published\_at timestamptz; notes text null | Each published content build. |
| entries | content\_id text PK; build\_id text PK → builds; kind text; name text; data\_hash bytea | One row per ContentId in a build. PK (content\_id, build\_id). — kind: item, skill, creature, quest, node, region, recipe, currency... |

---

↑ [[Schemas|Schemas]] · ← [[behavior Behavior scoring service GSVC-11|behavior — Behavior scoring service (GSVC-11)]] · [[std Go SDK PSDK-2 PSDK-3|_std — Go SDK (PSDK-2, PSDK-3)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › content — Deploy pipeline (read-only for services) · exported 2026-11-03
