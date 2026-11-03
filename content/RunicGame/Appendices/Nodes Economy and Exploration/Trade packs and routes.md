---
title: "Trade packs and routes"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Nodes, Economy and Exploration"
source_url: "https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit"
section: "Trade packs and routes"
created: "2026-10-19"
modified: "2026-10-30"
---

* **Decision.** Only trade packs keep an origin node. Other items have no origin, because resources are already specific to certain areas.  
* **Decision.** Payout uses the node distance between origin and destination, not the path traveled.  
* **Decision.** A Go service records the pack's route, ignores repeated nodes, loops and convoluted paths, and builds a direct route that rewards the dangerous nodes crossed. This encourages crossing dangerous areas without rewarding walking in circles.  
* **Decision.** Payout \= cheapest-path distance × (1 \+ danger of the route's nodes). Each node's danger is recorded on entry. A detour longer than 1.5× the cheapest path only gets the cheapest path's danger. If the pack is stolen, the record continues with the new carrier.  
* **Decision.** Pack types, copied from ArcheAge: specialty packs from the region's packing bench (one per region, near its city node, with that region's recipes); aged packs from the larder, where aging honey, wine or cheese raises the value; cargo packs, consolidated by Commerce, which pay more the faster they arrive; resource packs (wood, iron, stone, fabric) from the processing stations (sawmill, smelter, loom, mason's table), which are less limited than the packing bench; and military aid packs.  
* **Decision.** Specialty packs combine several resources, sometimes with extra steps, and can pay well above their inputs: the route payout times the destination region's demand.  
* **Decision.** Resource packs never pay more than the auction value of their contents plus the effort. They build and repair the regions' structures and feed [[Regional economy#Prosperity and node missions|node missions]], paying more before a mission reaches 100% and less after.  
* **Decision.** Military aid packs: a weapon pack and an armor pack made from basic crafted gear. The pack's tier is the items' tier, tiers can't be mixed, and no weapon type is required. They feed missions (village defense, watch towers) and nodes at war.  
* **Decision.** Demand per region works like a stock market: each delivery lowers that pack type's price there, it recovers over time, and events move it. Packs are delivered at specific points: cities, ports and islands.  
* **Decision.** The board in each city shows its own region's demand live; other regions' demand comes from a Commerce demand report, which goes stale.  
* **Decision.** When someone else delivers a pack, the deliverer gets 80% of the profit and the crafter 20%.  
* **Decision.** Construction uses packs, as in ArcheAge: buildings and their repairs, and vehicles at creation, except vehicles made at a bench, such as gliders. Resource amounts use the simplest clipper as the standard and [[Labor|labor]] costs copy ArcheAge's for now; every number is for balancing.  
* **Decision.** Packs delivered to a city go entirely to its projects; they never return to the auction.

---

↑ [[Nodes Economy and Exploration|Nodes, Economy and Exploration]] · ← [[Market Isle|Market Isle]] · [[Maps and cartography|Maps and cartography]] →  
Source: [RunicGame — Appendix: Nodes, Economy and Exploration](https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit) › Trade packs and routes · exported 2026-11-03
