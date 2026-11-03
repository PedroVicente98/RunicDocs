---
title: "Open world"
tags:
  - "vision"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-10-30"
---

The map is very large and dense, and everything in it is interactable: ruins, magical places, floating islands, desolate places and hard mobs. The inspiration comes from Tales of Demons and Gods (without separate dimensions as a theme) and from Crimson Desert's feeling of exploration and nature. Sailing and exploring are the central activities.

The main world is one continuous map: the surface, with at least three continents separated by seas full of islands, the floating islands above it and the Underground below. The Sky Island is a separate map, the size of the surface. To start, each map is about 600 km², counting land, islands and sea; new regions come in with the game live.

| Map or region | How you get there | What makes it special | Role in the game |
| :---- | :---- | :---- | :---- |
| Faction 1 continent | Character start | Cities, lore and lands of the faction; Humans and Dragonkin | Home, housing, first story |
| Faction 2 continent | Character start | The same, with another culture and gimmick; Elves and Orcs | Home, housing, first story |
| Neutral or wild continent | By sea | Contested land and rare resources; a flight zone with aerial PvP; the base of the island staircase to the Sky Island; the only place with castles | Open PvP, world bosses, the boss region |
| Seas and islands | By ship, or gliding with the wind current | Naval combat, housing islands, the pirate base | Trade packs, naval raids |
| Floating islands | On the surface map itself (e.g. 1,000 m up) | Fixed and indestructible; at most they rise and sink a little | Exploration, resources and magical places |
| Sky Island | The island staircase that rises from the neutral continent | A separate, persistent and shared map, the size of the surface; a flight zone; stronger enemies | Endgame, resources and a story chapter |
| Underground | Caves and rivers that go down from the surface | Caves, rivers and underground oceans in the same map, below the surface; its own NPCs and lore; permanent darkness | Unique resources, exploring with light |

* **A gimmick per region.** Each region changes an exploration rule: tides that open paths, wind currents for gliders, fog that hides islands, storms that affect ships.  
* **The Sky Island and other maps.** The Sky Island is another instance, persistent and shared by everyone. Crossing the clouds at the top of the island staircase, an animation of the character flying covers the loading. The same scheme serves other maps, linked by portals.  
* **Floating islands** are inside the surface map and are never split between two simulation servers.  
* **Flight** exists only on the neutral continent and the Sky Island. Inside those zones flight is unlimited, with an altitude ceiling above which you can only glide *(proposal: a soft ceiling)*. There is aerial PvP on the neutral continent.  
* **Ocean.** Over the ocean you can only glide, using the wind current, which has a direction (any angle) and a speed. Speed 0 has no effect; a negative speed suddenly reverses the direction without changing the angle. Gliding against the current is impossible, and the character is thrown back. Sailing is still necessary.  
* **Sea and wind currents** follow a cyclic, mappable base routine. Admins create events in a panel that change them for a while; then the base routine returns.  
* **Living world.** Escorts, trade routes, ships and mob routines follow schedules mapped to world time, without simulating empty areas: the NPC appears at the right point when a player arrives. The routine drifts slowly (a cycle that doesn't match the clock, plus a small deterministic variation). Exceptions caused by players, such as a delayed escort, are stored in a service and return to the routine over time.  
* **Weather and hazards.** Snow, rain and wet ground, floods, slides, storms and sea events change travel; their rules are in [[RunicGame — Ideias|Ideias]] ([[HAZARD-01 Environmental Hazards|HAZARD-01]], [[SHIP-01 Naval Combat Flooding, Repair and Sea Events|SHIP-01]], [[SEA-01 Ship Handling and Sea Balance|SEA-01]]) and in the Architecture. Hazards go through Resolve and Tolerance unless their own rule says otherwise.  
* **Castles** exist only on the neutral continent: the guild that rules a region there builds its castle in one of the region's designated zones (e.g. 3). Only one per region, fixed once placed. On the faction continents the ruling guild uses the city itself and an exclusive guild building (see [[Economy, housing and land|Economy]]).  
* **A dark Underground.** It uses the same lighting system as the night (see [[Real exploration]]): darkness hides shortcuts, ores and treasure, and creatures react to light.  
* **The boss region.** A whole region is a world boss. Everything done in it (farming mobs, gathering, interactions) advances the summoning, and the fight takes the whole region. Contribution counts per player, guild and faction, with rankings, fixed rewards and luck scaled by contribution; killing enemies in PvP steals part of their contribution.  
* **Camera.** Close to the character, with no far zoom. *Proposal: photo mode only out of combat.*  
* **Technical base.** The world uses sparse 3D cells and activation volumes around the players, described in [[RunicEngine — Technical Architecture]]. Caves, nodes and other rules are volumes authored in the RunicEditor; the Sky Island is another world, with a checkpoint transition.
