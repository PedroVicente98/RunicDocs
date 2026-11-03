---
title: "Differences from Technical Architecture v4 (Nodes and Economy)"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Nodes, Economy and Exploration"
source_url: "https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit"
section: "Differences from Technical Architecture v4"
created: "2026-10-19"
modified: "2026-10-30"
---

| Architecture section | What the Architecture says today | What this appendix changes |
| :---- | :---- | :---- |
| None (PvE and PvP participation) | v4 has no participation modes, Jurisdiction, mode isolation or [[Factions PvP and crime#Outlaw and Infamy\|Outlaw]]; [[Vision\|the Vision]] has them since 13 Oct | Small component with mode, faction, Outlaw state and timers; target discovery decided by the attacker, filtered by target category; [[Factions PvP and crime#Jurisdiction\|Jurisdiction]] as a rule volume ([[WORLD-2\|WORLD-2]]); PvE and PvP characters do not collide with each other but ride the same ship; timers in world time, inside the [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] snapshot |
| World space: volumes ([[WORLD-2\|WORLD-2]]) | Authored volumes for caves, flight zones, build zones, rule areas and indivisible volumes | New volume kind: the Node. Nodes have complex borders that follow the region border and tile it exactly with their neighbors. A region is a city node with its child nodes; open sea between islands belongs to transitional nodes. Cooked into node IDs per cell; cells on a border are marked mixed and resolved with an exact point-in-polygon test. About 64 bytes per node |
| World authoring: resources by spawn area | Volumes define the possible spawn locations of interactive resources | Kept, and extended: volumes mark which resource type can grow there, generically or for specific species. Each node's climate and environment decide which species actually exist. Hostile mobs are placed by hand in volumes that can hold several mob types and exact positions |
| Environment: weather | Weather state per region | Each node carries climate and environment data, which drives its fauna, flora and resources. Open: how node climate maps onto the runtime weather state per region |
| [[GPL-1\|GPL-1]]: movement modes | Walk, sprint, dash, glide, mount; Water registers swimming | Character climbing as a movement mode. [[Stamina and climbing#Stamina\|Stamina]] is spent by sprinting, fast swimming and climbing |
| [[GPL-7\|GPL-7]]: flight and climbing | "Climbing mounts"; a mount climbs a marked wall | Free character climbing: a short cast to the wall, climb class and drain stored in the physics material per triangle, defaults by asset type (structures never climbable). Vertical cliffs need meshes because heightfields are 2.5D. Pitons, fixed ropes and hooks as world entities; ship ropes and hook ropes as climbable segments |
| Swimming, diving and breath | Breath meter when submerged; the sea folk swim faster | Breath stays; fast swimming spends stamina |
| None (stamina) | No stamina resource | Stamina with two cost modes (percentage of max in combat, flat value out of combat), regeneration as a percentage of max, owned by the server and predicted on the client through RunicGame::Shared |
| None (combat state) | No combat state rule | Combat starts on the first hostile action and ends 30 s after the last one; it gates teleports and switches stamina costs |
| Map knowledge ([[GSRV-6\|GSRV-6]], [[GCL-4\|GCL-4]]) | One bit per explored cell per character; reading a Carta merges the cells its cartographer recorded; cartography records cells traveled | The per-cell bit stays and marks "discovered". Discovered areas show one static image, the same for everyone, baked when the world is cooked. Mapped areas show a real-time top-down render of terrain only, never players, ships or mobs. Charts are per node and per layer, made by survey minigames resolved on the server, and consumed when used. Layer data goes only to chart owners. The player's exact position is always shown; a node's chart adds the node's information |
| Nautical charts | Made by sailing with a kit; cells sailed set coverage and value | Nautical charts per node, made by a minigame (star fixes, soundings, drift buoys), with no grade. The overlay is still sent only to chart owners |
| Services: Character; [[GSVC-7\|GSVC-7]] | [[Labor\|Labor]] in the Character service, per character; offline regeneration only for subscribers | Labor and its reserve are account-wide; the reserve is subscriber-only and computed at login from the logout time |
| Services: Economy | Regional auction houses, taxes and land fund | Territory and economy services: regions and nodes, [[Regional economy#Prosperity and node missions\|prosperity]] through weekly missions, region projects, fixed weekly guild payouts, scheduled wars and the 3-node limit. One global auction with a seller tax kept by the NPC, NPC listings at the price cap, pack demand per region and the black market. Rolling market averages for missions, packs and the black market |
| Services: Guild | Membership, roles, progression and rules | Alliances, with admin tools to regulate guilds acting as unofficial alliances; up to 3 nodes per guild, or one region |
| Services: Mail | Delivery and claim rules | Mail carries items, with postage per unit that grows with the item's tier or value |
| Items: [[Trade packs and routes\|trade packs]] | World entities carried on the back or in vehicles | Go route service: node entries recorded by the server, danger recorded on entry, loops erased, detour cap. The pack keeps its origin node |
| Instances and world entities: [[Inventory equipment and the Market Isle#Market Isle (working name)\|Market Isle]] | Shop island as an instance | The island sells designs. Ship construction platforms become protected, timed world entities near lighthouse ports; house constructions become entities on the player's land |
| [[Scripted sequences GameplayFlow and restrictions\|GameplayFlow]]: movement | "Teleport where explicitly legal" | Teleport only when idle (out of combat, no event, survey, trade pack or vehicle); a fixed fee plus distance, more between continents, computed on the server, with no cargo fee; game-started teleports are free; unstuck limited to the surroundings |
| Rule pipeline: "resolved [[Weapon Class System#Loadouts\|loadout]]" | "Loadout" is the rule set compiled per character | Open: the clash is back, since the game now calls its fixed weapon pairs loadouts ([[CLASS-02 Weapons and Named Classes\|CLASS-02]]); the compiled rule set may need another name. Profession gear never feeds the combat rule set |
| Input queue | Combat queue with a 200 to 400 ms window and one queued action | A 0.25 s floor on every discrete action, per rate key, skills included; the combat queue stays for combat |
| Sessions | The client connects straight to the simulation; interaction commands delivered per command type | Actions are envelopes per type, each with its own code and destination (simulation, quests, economy). The entry gate lives in the simulation that owns the player, with the floor per rate key and a flood budget per connection; its timers go into the handoff snapshot |
| [[GSRV-7\|GSRV-7]], [[GSVC-10\|GSVC-10]]: professions | Gathering, crafting, farming and trade-pack production defined later; nine professions | Minigames seeded and resolved on the server, with the client sending only timestamped inputs; batch mode; profession gear slots; Larceny coin purse tiers; animal sickness; expanded list; labor tied to professions |

---

↑ [[Nodes Economy and Exploration|Nodes, Economy and Exploration]] · ← [[Differences from the Vision (Nodes and Economy)|Differences from the Vision (Nodes and Economy)]] · [[Already applied to the Vision on 30 Oct the English rewrite also took|Already applied to the Vision (on 30 Oct the English rewrite also took in every row of the table above)]] →  
Source: [RunicGame — Appendix: Nodes, Economy and Exploration](https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit) › Differences from Technical Architecture v4 · exported 2026-11-03
