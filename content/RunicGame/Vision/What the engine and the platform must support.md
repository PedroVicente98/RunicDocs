---
title: "What the engine and the platform must support"
tags:
  - "runicgame"
  - "vision"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
section: "What the engine and the platform must support"
created: "2026-10-13"
modified: "2026-10-30"
---

A summary of the requirements this document creates for RunicEngine and the platform, grouped by area. The appendices add their own requirements per repository.

| Area | What must exist |
| :---- | :---- |
| Skills | Skills as component data; an interaction resolver at activation and on hit; timelines in ticks (30 Hz domain); one timing profile per weapon; base values with PvE and PvP variants per skill, item and effect |
| Control and conditions | [[Combat#Resolve hard and light CC\|Resolve]] per target (T1 lowers a CC by a level, T2 immunity) and a light-CC slow cap; condition build-up bars per source and condition, one acting instance, peaks and [[Combat#Conditions, build-up and Tolerance\|Tolerance]] per condition; effect cooldowns and effect costs |
| Defense | [[Defense Evasion Guard and armor#Evasion\|Evasion]] state (charges, iframe, recovery) and [[Defense Evasion Guard and armor#Guard\|Guard]] with modes per weapon (free, timed, during a dash or a sprint skill), filtered by the hit's domain and delivery; physical and magical armor pools blended per piece |
| Balance as data | Coefficients per component (PvE and PvP), efficiency per role, item grades, timing profiles, armor, condition speeds and caps in reloadable tables, without recompiling |
| Classes | A named class derived from the loadout plus the [[Weapon Class System#Disciplines\|Discipline]], with one role; the weapon kit unlocked by level; Discipline skills bought with points; one merged tree per class, built at cook time; the [[Real exploration#Altars, death, respawn and teleports\|Altar]] reset that redistributes points and level choices; no weapon-type change outside the reset |
| Context kit | Mount and aerial trees with their own points; mounts, gliders and wings that swap and modify the kit; the same mount kit on the ground and in flight |
| World | One continuous map in sparse 3D cells, loaded and simulated by [[World space coordinates cells and activation#Activation volumes\|activation volumes]] around the players, with no loading screens; fixed floating islands; the Underground below the surface; the Sky Island and other maps as separate worlds, with a transition; nodes as volumes; a day and night cycle |
| Flight and gliding | Flight zones with an altitude ceiling; gliding guided by the wind current over the ocean; gliding and flying as separate mount capabilities; the wing as equipment; [[Trade packs and routes\|trade packs]] that block flight and gliding |
| Movement | [[Stamina and climbing#Stamina\|Stamina]] owned by the server, with in-combat and out-of-combat cost modes; climbing as a movement mode with a drain per surface; climbable ship ropes; a 0.25 s floor on every action |
| Living world | Routines of escorts, trade routes, ships and mobs computed from world time, with deterministic drift; exceptions stored in a service; sea and wind currents with a cyclic routine and admin events |
| Light as gameplay | Light exists on the server as data (radius, intensity, duration), not only in rendering: mobs perceive light and it reveals position in PvP |
| Maps | Map knowledge per Lineage; chart items per node and layer; [[Maps and cartography#Surveying\|surveying]] minigames; the real-time map render of mapped nodes; current charts that sync and predict |
| Altars and teleports | Respawn at the nearest Altar the character has discovered, in the same map; Altars per character for respawn and teleports, and known by the Lineage for the map; teleports with an idle check, fees by distance, a consumable and a cooldown from the field |
| Items and inventory | A slot inventory with no weight, expandable; a special tab and binding rules enforced by the server; items with item level, grade, stats and a unique effect; extraction and dismantling into gems, with one socket per weapon; trade packs as world objects, with vehicle slots |
| Progression | [[Real exploration#Exploration XP\|Exploration XP]] and the exploration shop; 23 professions with labor per Lineage, masteries per character and the [[Labor#Labor reserve\|labor reserve]] |
| Quests | A quest graph with triggers from every system; the knowledge store and tag taxonomy; NPC knowledge profiles and a dialogue resolver; guidance levels; Chronicle storage |
| Instances | Dungeons, raids, naval raids with lent ships, and the [[Inventory equipment and the Market Isle#Market Isle (working name)\|Market Isle]] |
| Housing and economy | The 8x8 grid, frozen Deeds, the tax fund, the limit per Lineage and region; one world auction with NPC listings, the global chest and mail by unit; nodes, [[Regional economy#Prosperity and node missions\|prosperity]], missions, region projects and guild payouts; castles on the neutral continent; trade-pack demand per region; the black market |
| Factions | Faction, [[Factions PvP and crime#Outlaw and Infamy\|Outlaw]], [[Factions PvP and crime#Outlaw and Infamy\|Infamy]] and piracy; group rules per faction, with pirates able to group with everyone; Outlaw through the normal skill pipeline (cooldown, activation, replication), with the cooldown kept in world time to survive a [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] between simulations |
| Platform | Accounts and the Lineage; the [[Business model launch visuals and audio#Subscription\|subscription]] tied to land, offline [[Labor\|labor]] and the labor reserve; no real-money shop; the base model (free-to-play or buy-to-play) is open |
| Client | A custom soundtrack (albums, presets and radios per context), with no swapping of sound effects; optional key combos; a close camera with no far zoom |
| PvE and PvP participation | A persistent Participation mode and [[Factions PvP and crime#Jurisdiction\|Jurisdiction]] per area (Open world, Sanctuary, Safe route, PvE instance); target discovery decided by the attacker, filtered by target category (player, mob, world boss), and a small component with mode, faction, Outlaw state and timers; PvE and PvP characters without collision between them, carried by the same ship; a ship with a trade pack becomes a PvP ship automatically; server validation of trade packs, ships, world bosses, surveying and mode changes |

---

↑ [[Vision|Vision]] · ← [[Runes|Runes]] · [[Recorded decisions and next steps|Recorded decisions and next steps]] →  
Source: [RunicGame — Complete MMORPG Vision](https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit) › What the engine and the platform must support · exported 2026-11-03
