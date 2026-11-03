---
title: "Decisions this layout builds on"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Decisions this layout builds on"
created: "2026-10-26"
modified: "2026-10-30"
---

* [[Physical layout Proposal|PostgreSQL]] is the only database; every service is built on the Platform Go SDK ([[Architecture|Architecture v4]], [[PSDK-2|PSDK-2]]).  
* The C++ simulation never talks to a database. The Engine may not depend on databases, gRPC or NATS, and nothing blocks the 30 Hz tick (principle 5).  
* The simulation sends durable operations through the Engine's service port ([[SIM-5|SIM-5]]); the Platform's ServicesBridgeLayer turns them into asynchronous gRPC calls and NATS messages ([[PBND-1|PBND-1]], [[PBND-4|PBND-4]]), and results come back at safe ticks.  
* Every durable change is an operation with an ID, so retries are safe. Durable writes happen at explicit boundaries: logout, trade, upgrade, loot, world transition and the periodic checkpoint.  
* The item ledger and the currency wallets are Platform mechanisms with no game rules ([[PBB-1|PBB-1]] to [[PBB-3|PBB-3]]); the Game's Inventory, Economy and Trade services apply the rules.  
* Accounts are global; worlds (shards) are hosted in regional datacenters.  
* Game definitions (items, skills, creatures, quests, nodes) are data files with namespaced ContentIds, cooked and loaded by server and services. The database stores references to them, never the definitions.

---

↑ [[Database Layout|Database Layout]] · [[Physical layout Proposal|Physical layout (Proposal)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Decisions this layout builds on · exported 2026-11-03
