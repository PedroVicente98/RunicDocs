---
title: "economy — Economy service (GSVC-4)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Schemas › economy — Economy service (GSVC-4)"
created: "2026-10-26"
modified: "2026-10-30"
---

*Game · shard database · Built on decisions.* Upgrades and their RNG, the global auction, price history and bounds, the black market, [[Inventory equipment and the Market Isle#Market Isle (working name)|Market Isle]] limits.

| Table | Columns | Notes |
| :---- | :---- | :---- |
| upgrade\_attempts | attempt\_op uuid PK; character\_id bigint ⇢ character.characters; item\_id bigint ⇢ ledger.items; kind text; before jsonb; after jsonb; success bool; at timestamptz | Upgrades, grade attempts, rerolls and dismantling (destroys the item and returns part of its materials; a unique effect becomes a gem holding an Infusion Rune). Partitioned monthly. — kind: level, grade, reroll, dismantle |
| pity\_counters | lineage\_id bigint PK ⇢ character.lineages; counter\_key text PK; value int; updated\_at timestamptz | Guarantee counters live on the server, never the client. PK (lineage\_id, counter\_key). |
| auction\_houses | house\_id int PK; node\_id text ⇢ territory.nodes; faction\_scope text null | Auction counters where players list and claim; every counter serves the same global auction. |
| listings | listing\_id bigint PK; house\_id int → auction\_houses; seller\_id bigint ⇢ character.characters; item\_id bigint ⇢ ledger.items; template\_id text; quantity int; unit\_price bigint; currency\_id text; status text; listed\_at timestamptz; expires\_at timestamptz | Listed items wait in the auction's escrow container until they sell. The seller fills a gross or a net price and the buyer pays the listed price; an expired listing sends a mail notice and is claimed at any counter. — house\_id: the counter where it was listed; status: active, sold, expired, claimed, cancelled |
| sales | sale\_id bigint PK; listing\_id bigint → listings; buyer\_id bigint ⇢ character.characters; quantity int; unit\_price bigint; tax bigint; at timestamptz | Every sale with the seller's tax, kept entirely by the NPC as a sink. Partitioned monthly. |
| price\_history | template\_id text PK; day date PK; low bigint; high bigint; avg\_price bigint; volume int | Daily figures of the global auction; the 7-day median feeds [[Regional economy#Prosperity and node missions\|node missions]], pack payouts and the black market. PK (template\_id, day). |
| price\_bounds | template\_id text PK; min\_price bigint; max\_price bigint; set\_by bigint; updated\_at timestamptz | Minimum and maximum price per item, tunable by admins. When an item is out of stock or above the maximum, an NPC listing sells it at a high price. |
| vendor\_limits | lineage\_id bigint PK ⇢ character.lineages; offer\_id text PK; period\_start date PK; bought int | Market Isle purchase limits. PK (lineage\_id, offer\_id, period\_start). |

---

↑ [[Schemas|Schemas]] · ← [[quest Quest service GSVC-3|quest — Quest service (GSVC-3)]] · [[commerce Economy service|commerce — Economy service]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Schemas › economy — Economy service (GSVC-4) · exported 2026-11-03
