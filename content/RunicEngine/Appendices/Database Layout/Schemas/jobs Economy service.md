---
title: "jobs — Economy service"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › jobs — Economy service"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* The community job board with its internal bank: a job can be taken without the collateral; failing leaves a negative balance that blocks new jobs.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| job\_postings | job\_id bigint PK; poster\_id bigint ⇢ character.characters; kind text; node\_id text ⇢ territory.nodes null; spec jsonb; reward bigint; collateral bigint; currency\_id text; escrow\_wallet\_id bigint ⇢ wallet.wallets; state text; deadline\_at timestamptz; created\_at timestamptz | A job and its escrowed reward. — kind: craft, gather, deliver, ceremony...; spec: what must be delivered; state: open, taken, delivered, cancelled, failed, expired |
| job\_assignments | job\_id bigint PK → job\_postings; worker\_id bigint ⇢ character.characters; collateral\_mode text; state text; taken\_at timestamptz; due\_at timestamptz; closed\_at timestamptz null | Who took the job and how the collateral was covered. — collateral\_mode: paid, borrowed; state: active, delivered, cancelled, failed |
| board\_accounts | character\_id bigint PK ⇢ character.characters; balance bigint; blocked bool; updated\_at timestamptz | The board's internal bank; the only balance in the game that may go negative. — balance: below zero \= debt; blocked: true while balance \< 0 |
| board\_entries | entry\_id bigint PK; character\_id bigint → board\_accounts; job\_id bigint → job\_postings null; delta bigint; reason text; at timestamptz | Every debt and repayment. |

---

↑ [[Schemas|Schemas]] · ← [[trade Trade service GSVC-4|trade — Trade service (GSVC-4)]] · [[territory Territory service new|territory — Territory service (new)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › jobs — Economy service · exported 2026-11-03
