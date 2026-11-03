---
title: "Schemas"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas"
created: "2026-10-26"
modified: "2026-10-30"
---

Notation: PK primary key (several PK columns \= composite key), UQ unique, → foreign key inside the schema, ⇢ logical reference to another service's schema (no constraint), null \= nullable; every other column is NOT NULL. double \= double precision.

## Contents

- [[account Accounts service PCS-1|account — Accounts service (PCS-1)]]
- [[ticket Accounts service PCS-1|ticket — Accounts service (PCS-1)]]
- [[directory Accounts and Admission services PCS-1 PCS-6|directory — Accounts and Admission services (PCS-1, PCS-6)]]
- [[coordinator World Coordinator PCS-2 PCS-7|coordinator — World Coordinator (PCS-2, PCS-7)]]
- [[instance Instance allocation PCS-4|instance — Instance allocation (PCS-4)]]
- [[directive World directives PCS-3|directive — World directives (PCS-3)]]
- [[social Chat and party groups PCS-5|social — Chat and party groups (PCS-5)]]
- [[ledger Item ledger PBB-1|ledger — Item ledger (PBB-1)]]
- [[wallet Currency wallets PBB-2 PBB-3|wallet — Currency wallets (PBB-2, PBB-3)]]
- [[character Character service GSVC-1 5 7 10|character — Character service (GSVC-1, 5, 7, 10)]]
- [[cartography Character service|cartography — Character service]]
- [[justice Character service|justice — Character service]]
- [[inventory Inventory service GSVC-2|inventory — Inventory service (GSVC-2)]]
- [[vehicle Inventory service|vehicle — Inventory service]]
- [[quest Quest service GSVC-3|quest — Quest service (GSVC-3)]]
- [[economy Economy service GSVC-4|economy — Economy service (GSVC-4)]]
- [[commerce Economy service|commerce — Economy service]]
- [[trade Trade service GSVC-4|trade — Trade service (GSVC-4)]]
- [[jobs Economy service|jobs — Economy service]]
- [[territory Territory service new|territory — Territory service (new)]]
- [[mail Mail service|mail — Mail service]]
- [[guild Guild service|guild — Guild service]]
- [[family Guild service|family — Guild service]]
- [[access Housing service|access — Housing service]]
- [[housing Housing service|housing — Housing service]]
- [[world World events and World routines services GWTH-1 GSVC-9|world — World events and World routines services (GWTH-1, GSVC-9)]]
- [[ranking Rankings service GSVC-8|ranking — Rankings service (GSVC-8)]]
- [[production Character service GSRV-7 GSVC-7|production — Character service (GSRV-7, GSVC-7)]]
- [[moderation Moderation service GSVC-12 GSRV-9|moderation — Moderation service (GSVC-12, GSRV-9)]]
- [[behavior Behavior scoring service GSVC-11|behavior — Behavior scoring service (GSVC-11)]]
- [[content Deploy pipeline read-only for services|content — Deploy pipeline (read-only for services)]]
- [[std Go SDK PSDK-2 PSDK-3|_std — Go SDK (PSDK-2, PSDK-3)]]

---

↑ [[Database Layout|Database Layout]] · ← [[Connections|Connections]] · [[Differences from the Architecture v4 and the Vision|Differences from the Architecture v4 and the Vision]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas · exported 2026-11-03
