---
title: "trade — Trade service (GSVC-4)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › trade — Trade service (GSVC-4)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Two-party trades with confirmations, and the transfer holds for new devices and young accounts.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| trade\_sessions | trade\_id bigint PK; a\_character\_id bigint ⇢ character.characters; b\_character\_id bigint ⇢ character.characters; state text; a\_confirmed bool; b\_confirmed bool; op\_id uuid ⇢ ledger.operations null; created\_at timestamptz | Commits as one ledger plus wallet operation. — state: open, locked, committed, cancelled |
| trade\_offers | trade\_id bigint PK → trade\_sessions; side char PK; line smallint PK; item\_id bigint ⇢ ledger.items null; quantity int null; currency\_id text null; amount bigint null | PK (trade\_id, side, line). — side: a or b |
| transfer\_holds | hold\_id bigint PK; account\_id bigint ⇢ account.accounts; reason text; until timestamptz; created\_at timestamptz | New-device and young-account holds on trade, mail and auction withdrawals. — reason: new\_device, young\_account |

---

↑ [[Schemas|Schemas]] · ← [[commerce Economy service|commerce — Economy service]] · [[jobs Economy service|jobs — Economy service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › trade — Trade service (GSVC-4) · exported 2026-11-03
