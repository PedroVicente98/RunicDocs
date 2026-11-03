---
title: "Requirements by repository (Nodes and Economy)"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Nodes, Economy and Exploration"
source_url: "https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit"
section: "Requirements by repository"
created: "2026-10-19"
modified: "2026-10-30"
---


## Engine

* Attacker-side target discovery filtered by target category, and collision layers that let PvE and PvP characters pass through each other while riding the same ship (pending since 13 Oct).  
* Node volumes that tile a region exactly, with editor validation (shared borders, no gaps or overlaps); cooked node IDs per cell, with mixed border cells resolved by an exact point-in-polygon test.  
* Resource-type volumes (generic or specific) and mob placement volumes with several types and exact positions, cooked with the world.  
* A climbing movement mode: wall cast, climb class and drain per physics material, asset-type defaults, cliff meshes and climbable line segments attached to moving ships.  
* A generic action entry gate in the owning simulation: action envelopes per type, a 0.25 s floor per rate key, a flood budget per connection, a short input buffer, and timers in the [[Networking replication interest and handoff#Simulations, handoff and ghosts|handoff]] snapshot.  
* Map rendering on the client: a baked static "discovered" image per map at cook time, and a real-time top-down terrain view from a cooked low-detail world model plus live state (time of day, weather, island motion), with no entities.

## Game

* Participation, Jurisdiction and [[Factions PvP and crime#Outlaw and Infamy|Outlaw]] rules (pending since 13 Oct).  
* Combat state: enters on the first hostile action, ends 30 s after the last.  
* [[Stamina and climbing#Stamina|Stamina]]: two cost modes, percentage regeneration, server ownership and client prediction in RunicGame::Shared; climb drain tables, gear, pitons, ropes, boarding hooks and crew ropes.  
* Node data: climate, environment, species lists, specialty and connections.  
* Territory service (Go): regions and nodes, [[Regional economy#Prosperity and node missions|prosperity]], weekly [[Regional economy#Prosperity and node missions|node missions]], region projects, fixed weekly guild payouts, scheduled wars, the 3-node limit, alliances and admin tools.  
* Trade-pack route service (Go), with node entries recorded by the server.  
* The global auction (seller tax, gross and net price fields, NPC listings at the cap), pack demand per region, the black market, the global chest, mail postage per unit and teleport fees.  
* [[Labor|Labor]] and the reserve, account-wide, computed at login.  
* Charts per node and per layer, survey minigames, server-side [[Maps and cartography#Triangulation (base chart on land)|triangulation]] scoring, layer data only to owners, event visibility rules, charts consumed on use.  
* Professions: server-seeded minigames, batch mode, profession gear slots, Larceny coin purse tiers, farming and husbandry with animal sickness.  
* [[Inventory equipment and the Market Isle#Market Isle (working name)|Market Isle]] designs, ship construction platforms (protected, timed, near lighthouse ports) and house constructions on owned land.  
* Action policies per action type, as game data.

## Platform

* Nothing new. The appendix reuses existing Platform mechanisms: entitlements for the subscriber-only [[Labor#Labor reserve|labor reserve]], the item ledger's binding for Market Isle designs and their products, and instance allocation for the Market Isle.

---

↑ [[Nodes Economy and Exploration|Nodes, Economy and Exploration]] · ← [[Progression|Progression]] · [[Open (Nodes and Economy)|Open (Nodes and Economy)]] →  
Source: [RunicGame — Appendix: Nodes, Economy and Exploration](https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit) › Requirements by repository · exported 2026-11-03
