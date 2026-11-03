---
title: "production — Character service (GSRV-7, GSVC-7)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › production — Character service (GSRV-7, GSVC-7)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Proposal.* Crafting history and player music compositions. Gathering and farming results arrive as ledger operations and [[Labor|labor]] events.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| craft\_log | craft\_op uuid PK; character\_id bigint ⇢ character.characters; recipe\_id text; quantity int; labor\_spent int; quality jsonb; ledger\_op uuid ⇢ ledger.operations; at timestamptz | Every craft with labor spent and quality rolls. Partitioned monthly. |
| compositions | composition\_id bigint PK; author\_id bigint ⇢ character.characters; title text; notation text; complexity smallint; created\_at timestamptz | Songs written in the note editor; score items point to them. — notation: the editor's note format |

---

↑ [[Schemas|Schemas]] · ← [[ranking Rankings service GSVC-8|ranking — Rankings service (GSVC-8)]] · [[moderation Moderation service GSVC-12 GSRV-9|moderation — Moderation service (GSVC-12, GSRV-9)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › production — Character service (GSRV-7, GSVC-7) · exported 2026-11-03
