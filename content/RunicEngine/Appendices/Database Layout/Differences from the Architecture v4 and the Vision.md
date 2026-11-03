---
title: "Differences from the Architecture v4 and the Vision"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Differences from the Architecture v4 and the Vision"
created: "2026-10-26"
modified: "2026-10-30"
---

* Naming: the Architecture uses "world" both for a server copy and for the Engine's WorldId. This layout calls the server copy a shard (shard\_id) and the Engine's WorldId a map (map\_id).  
* Map knowledge is account-wide, so it hangs on the Lineage (character.map\_knowledge); the Lineage also records the [[Real exploration#Altars, death, respawn and teleports|Altars]] it has found, for the map only (character.lineage\_altars), while respawn and teleports use each character's own discovered Altars (character\_altar\_visits, proposed).  
* Vertentes were removed, and the Architecture was updated on 30 Oct; character\_build stores the class's weapon set and the [[Weapon Class System#Disciplines|Discipline]].  
* New Game services not in the Architecture's list: Territory (nodes, node wars, castles), Moderation and Behavior scoring (already in the Security appendix). The job board joins Economy, Family and marriage join Guild, Justice and Cartography join Character, Vehicles join Inventory.  
* New Platform tables: the directory schema in the global cluster (shards, capacity, login queue, lineage index for server select) and the standard per-schema tables (idempotency, outbox, inbox, audit).  
* [[Labor|Labor]] and its return reserve are account-wide (Lineage), not per character.  
* Economy review of 2026-10-30 ([[Nodes Economy and Exploration|RunicGame — Appendix: Nodes, Economy and Exploration]]): one global auction whose counters all serve the same market, one global chest, the auction tax kept entirely by the NPC, mail priced per unit, regions made of a city node and its child nodes, [[Regional economy#Prosperity and node missions|node missions]] and fixed guild payouts. Proposed tables not drawn yet: region\_pack\_demand (pack price per region and type, recovering over time), black\_market\_stock (goblin price and stock per type and tier), region\_projects (structures, wear and tier limit), pack\_deliveries (payout, deliverer and crafter shares) and character\_altar\_visits (Altars each character has discovered, for respawn and teleports).

---

↑ [[Database Layout|Database Layout]] · ← [[Schemas|Schemas]] · [[Open (Database Layout)|Open (Database Layout)]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Differences from the Architecture v4 and the Vision · exported 2026-11-03
