---
title: "quest — Quest service (GSVC-3)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › quest — Quest service (GSVC-3)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Quest progress and rewards, stored idempotently from quest facts; branching story chapters and skips for alts.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| quest\_progress | character\_id bigint PK ⇢ character.characters; quest\_id text PK; state text; branch jsonb; objectives jsonb; started\_at timestamptz; updated\_at timestamptz; completed\_at timestamptz null; version int | Active and finished quests. PK (character\_id, quest\_id). — state: active, completed, failed, abandoned; branch: choices taken so far (quests are trees); objectives: counter per objective |
| quest\_completions | character\_id bigint PK ⇢ character.characters; quest\_id text PK; times int; last\_completed\_at timestamptz | Repeatables and profession quest lines. PK (character\_id, quest\_id). |
| processed\_facts | fact\_id uuid PK; character\_id bigint ⇢ character.characters; quest\_id text; applied\_at timestamptz | Every quest fact applied, by its stable ID: a replayed fact changes nothing. Partitioned weekly. |
| quest\_rewards | reward\_op uuid PK; character\_id bigint ⇢ character.characters; quest\_id text; ledger\_op uuid ⇢ ledger.operations null; wallet\_op uuid ⇢ wallet.transfers null; status text; created\_at timestamptz | Reward commits through the ledger and wallets. |
| story\_progress | character\_id bigint PK ⇢ character.characters; chapter\_id text PK; branch\_path jsonb; completed\_at timestamptz null | Main story chapters with every branch kept for replay. PK (character\_id, chapter\_id). |
| lineage\_story\_skips | lineage\_id bigint PK ⇢ character.lineages; chapter\_id text PK; first\_completed\_at timestamptz | Chapters an alt of the same account may skip. PK (lineage\_id, chapter\_id). |

---

↑ [[Schemas|Schemas]] · ← [[vehicle Inventory service|vehicle — Inventory service]] · [[economy Economy service GSVC-4|economy — Economy service (GSVC-4)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › quest — Quest service (GSVC-3) · exported 2026-11-03
