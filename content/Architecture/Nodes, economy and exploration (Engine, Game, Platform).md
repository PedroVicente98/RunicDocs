---
title: "Nodes, economy and exploration (Engine, Game, Platform)"
tags:
  - "architecture"
  - "appendix/nodes-economy-exploration"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-11-16"
modified: "2026-11-16"
---

How the systems of [[RunicGame — Appendix Nodes, Economy and Exploration|RunicGame — Appendix: Nodes, Economy and Exploration]] (13 to 30 October 2026) are built: nodes, the regional economy, maps and charts, stamina and climbing, professions, teleports and actions. The rules are in the Vision ([[Economy, housing and land]], [[Real exploration]], [[Factions, PvP and crime]], [[Movement and vehicles]]); this note says how each area implements them. Numbers are examples for tuning.

### Design by area

| Area | Design |
| :---- | :---- |
| PvE and PvP participation | Small component with mode, faction, Outlaw state and timers; target discovery decided by the attacker, filtered by target category; Jurisdiction as a rule volume (WORLD-2); PvE and PvP characters do not collide with each other but ride the same ship; timers in world time, inside the handoff snapshot |
| World space: volumes (WORLD-2) | New volume kind: the Node. Nodes have complex borders that follow the region border and tile it exactly with their neighbors. A region is a city node with its child nodes; open sea between islands belongs to transitional nodes. Cooked into node IDs per cell; cells on a border are marked mixed and resolved with an exact point-in-polygon test. About 64 bytes per node |
| World authoring: resources by spawn area | Kept, and extended: volumes mark which resource type can grow there, generically or for specific species. Each node's climate and environment decide which species actually exist. Hostile mobs are placed by hand in volumes that can hold several mob types and exact positions |
| Environment: weather | Each node carries climate and environment data, which drives its fauna, flora and resources. Open: how node climate maps onto the runtime weather state per region |
| GPL-1: movement modes | Character climbing as a movement mode. Stamina is spent by sprinting, fast swimming and climbing |
| GPL-7: flight and climbing | Free character climbing: a short cast to the wall, climb class and drain stored in the physics material per triangle, defaults by asset type (structures never climbable). Vertical cliffs need meshes because heightfields are 2.5D. Pitons, fixed ropes and hooks as world entities; ship ropes and hook ropes as climbable segments |
| Swimming, diving and breath | Breath stays; fast swimming spends stamina |
| Stamina | One bar with flat costs, the same in and out of combat (decided on 12 November; it replaces the two cost modes); maximum stamina and its regeneration are separate stats; owned by the server and predicted on the client through RunicGame::Shared |
| Combat state | Combat starts on the first hostile action and ends 30 s after the last one; it gates teleports |
| Map knowledge (GSRV-6, GCL-4) | The per-cell bit stays and marks "discovered". Discovered areas show one static image, the same for everyone, baked when the world is cooked. Mapped areas show a real-time top-down render of terrain only, never players, ships or mobs. Charts are per node and per layer, made by survey minigames resolved on the server, and consumed when used. Layer data goes only to chart owners. The player's exact position is always shown; a node's chart adds the node's information |
| Nautical charts | Nautical charts per node, made by a minigame (star fixes, soundings, drift buoys), with no grade. The overlay is still sent only to chart owners |
| Services: Character; GSVC-7 | Labor and its reserve are account-wide; the reserve is subscriber-only and computed at login from the logout time |
| Services: Economy | Territory and economy services: regions and nodes, prosperity through weekly missions, region projects, fixed weekly guild payouts, scheduled wars and the 3-node limit. One global auction with a seller tax kept by the NPC, NPC listings at the price cap, pack demand per region and the black market. Rolling market averages for missions, packs and the black market |
| Services: Guild | Alliances, with admin tools to regulate guilds acting as unofficial alliances; up to 3 nodes per guild, or one region |
| Services: Mail | Mail carries items, with postage per unit that grows with the item's tier or value |
| Items: trade packs | Go route service: node entries recorded by the server, danger recorded on entry, loops erased, detour cap. The pack keeps its origin node |
| Instances and world entities: Market Isle | The island sells designs. Ship construction platforms become protected, timed world entities near lighthouse ports; house constructions become entities on the player's land |
| GameplayFlow: movement | Teleport only when idle (out of combat, no event, survey, trade pack or vehicle); a fixed fee plus distance, more between continents, computed on the server, with no cargo fee; game-started teleports are free; unstuck limited to the surroundings |
| Rule pipeline: "resolved loadout" | Open: the clash is back, since the game now calls its fixed weapon pairs loadouts (CLASS-02); the compiled rule set may need another name. Profession gear never feeds the combat rule set |
| Input queue | A 0.25 s floor on every discrete action, per rate key, skills included; the combat queue stays for combat |
| Sessions | Actions are envelopes per type, each with its own code and destination (simulation, quests, economy). The entry gate lives in the simulation that owns the player, with the floor per rate key and a flood budget per connection; its timers go into the handoff snapshot |
| GSRV-7, GSVC-10: professions | Minigames seeded and resolved on the server, with the client sending only timestamped inputs; batch mode; profession gear slots; Larceny coin purse tiers; animal sickness; expanded list; labor tied to professions |

### Climbing: Engine notes

* Climbing is a third movement component next to gliding and flying. A short cast finds the wall and reads the material, stored per triangle in the collision data.  
* Estimated cost: 2 to 4 casts per climber per tick, about 5 to 40 µs each. A hundred people climbing at once in one simulation use 0.5 to 4 ms of a 33 ms tick.  
* Heightfields are 2.5D and cannot make vertical walls or overhangs; large cliffs need meshes, with collision within 10 to 20 cm of the visuals. A 1 km by 500 m face at about 4 m² per triangle has about 125,000 triangles, loaded with the region.  
* Ship crew ropes and hook ropes are climbable line segments attached to the ship in ship-local coordinates, so they move with it and migrate with it in a handoff.  
* Hand and foot animation is visual only on the client; the server sees only the capsule and owns stamina.

### Requirements by repository

#### Engine

* Attacker-side target discovery filtered by target category, and collision layers that let PvE and PvP characters pass through each other while riding the same ship (pending since 13 Oct).  
* Node volumes that tile a region exactly, with editor validation (shared borders, no gaps or overlaps); cooked node IDs per cell, with mixed border cells resolved by an exact point-in-polygon test.  
* Resource-type volumes (generic or specific) and mob placement volumes with several types and exact positions, cooked with the world.  
* A climbing movement mode: wall cast, climb class and drain per physics material, asset-type defaults, cliff meshes and climbable line segments attached to moving ships.  
* A generic action entry gate in the owning simulation: action envelopes per type, a 0.25 s floor per rate key, a flood budget per connection, a short input buffer, and timers in the handoff snapshot.  
* Map rendering on the client: a baked static "discovered" image per map at cook time, and a real-time top-down terrain view from a cooked low-detail world model plus live state (time of day, weather, island motion), with no entities.

#### Game

* Participation, Jurisdiction and Outlaw rules (pending since 13 Oct).  
* Combat state: enters on the first hostile action, ends 30 s after the last.  
* Stamina: one bar with flat costs, maximum and regeneration as separate stats, server ownership and client prediction in RunicGame::Shared; climb drain tables, gear, pitons, ropes, boarding hooks and crew ropes.  
* Node data: climate, environment, species lists, specialty and connections.  
* Territory service (Go): regions and nodes, prosperity, weekly node missions, region projects, fixed weekly guild payouts, scheduled wars, the 3-node limit, alliances and admin tools.  
* Trade-pack route service (Go), with node entries recorded by the server.  
* The global auction (seller tax, gross and net price fields, NPC listings at the cap), pack demand per region, the black market, the global chest, mail postage per unit and teleport fees.  
* Labor and the reserve, account-wide, computed at login.  
* Charts per node and per layer, survey minigames, server-side triangulation scoring, layer data only to owners, event visibility rules, charts consumed on use.  
* Professions: server-seeded minigames, batch mode, profession gear slots, Larceny coin purse tiers, farming and husbandry with animal sickness.  
* Market Isle designs, ship construction platforms (protected, timed, near lighthouse ports) and house constructions on owned land.  
* Action policies per action type, as game data.

#### Platform

* Nothing new. The appendix reuses existing Platform mechanisms: entitlements for the subscriber-only labor reserve, the item ledger's binding for Market Isle designs and their products, and instance allocation for the Market Isle.
