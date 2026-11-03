---
title: "wallet — Currency wallets (PBB-2, PBB-3)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › wallet — Currency wallets (PBB-2, PBB-3)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Platform · shard database (same database as ledger) · Built on decisions.* Balances and atomic transfers in double entry: every transfer's entries sum to zero, and faucets and sinks are system wallets. Same database as the ledger so item and currency move in one transaction.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| wallets | wallet\_id bigint PK; owner\_kind text; owner\_id bigint; currency\_id text; balance bigint; version int | UNIQUE (owner\_kind, owner\_id, currency\_id). — owner\_kind: character, lineage, guild, node, escrow, system; currency\_id: ContentId: gold, honor, profession tokens, [[Inventory equipment and the Market Isle#Market Isle (working name)\|Market Isle]] coins...; balance: CHECK \>= 0, smallest unit |
| system\_wallets | wallet\_id bigint PK → wallets; purpose text | Faucets and sinks, so the economy's inflow and outflow are visible. — purpose: loot\_faucet, npc\_vendor\_sink, tax\_sink, repair\_sink, quest\_faucet... |
| transfers | op\_id uuid PK; kind text; requested\_by text; status text; created\_at timestamptz; committed\_at timestamptz null | One per currency operation; shares the op\_id space with the ledger. — status: committed, rejected, compensated |
| entries | entry\_id bigint PK; op\_id uuid → transfers; wallet\_id bigint → wallets; delta bigint; balance\_after bigint | Double-entry lines. Partitioned monthly. |
| currency\_supply | currency\_id text PK; period\_start date PK; minted bigint; burned bigint | Minted and burned per period. PK (currency\_id, period\_start). |

---

↑ [[Schemas|Schemas]] · ← [[ledger Item ledger PBB-1|ledger — Item ledger (PBB-1)]] · [[character Character service GSVC-1 5 7 10|character — Character service (GSVC-1, 5, 7, 10)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › wallet — Currency wallets (PBB-2, PBB-3) · exported 2026-11-03
