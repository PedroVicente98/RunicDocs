---
title: "Map authoring markers"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Map authoring markers"
created: "2026-10-26"
modified: "2026-10-30"
---

**Decision.** Every marker the map needs is catalogued here, and placing one must be quick and simple. Everything on the map is a painted layer, a point, an area or a path. Floods and slide paths need no markers: the cooker finds them from the elevation layer (terrain hydrology).

**Proposal.** Each marker type has a fixed name prefix (marker_...) and a fixed color in GIMP, and a validation step lists missing or broken markers before cooking, like the asset validation script.

## Painted layers (GIMP)

* **Decision.** One layer per information track: terrain type, elevation, biome, mob spawns, fauna and flora. Terrain type also says which ground turns to mud (soil, grass and farmland) and which never does (rock, sand and paved road), and a flood exclusion mask marks places that must never flood (ex.: cities).
* **Decision.** Snowfields and drift zones. Snow levels (none, light, heavy, deep) follow the weather, a timer drops a level while it isn't snowing, and drift zones at the bottom of slopes count one level deeper ([[HAZARD-01 Environmental Hazards|HAZARD-01]]).
* **Decision.** Every sea region has its own attachment type ([[ATTACH-01 Ship Attachments|ATTACH-01]]).
* **Proposal.** Elevation continues under the sea, so the same layer gives the static seafloor, reefs and sandbanks.
* **Proposal.** A hazard layer with one color per tag: reef, shallow, freezing water (with its Chill rate), vent, kelp, swamp and magnetic anomaly.
* **Proposal.** A sea-region layer for attachment types, sea threats and weather regions.

## Points

* **Decision.** Hand-made content and landmarks (cities, camps, unique content): the generator only places a temporary object there.
* **Decision.** [[Real exploration#Altars, death, respawn and teleports|Altars]]: every city has one, and others are scattered across the world.
* **Decision.** Cave entrances, each with a closed and an open model; earthquakes open them for a while.
* **Decision.** Maelstroms that lead into rifts and raids.
* **Decision.** Packing benches (one per region, near its city node), processing stations, trade-pack delivery points (cities, ports and islands) and the four black-market goblins.
* **Proposal.** Docks and ports, lighthouses, shipwrecks and ocean chests, volcano centers, world boss arenas, and siren and false-light spawns.

## Areas

* **Decision.** Spawn areas for mobs and for trees that can be cut down; the other trees are fixed decorative models.
* **Decision.** Castle zones (the designated zones of each region, on the neutral continent only) and housing zones in 8×8 slots ([[LAND-01 Land Ownership|LAND-01]]).
* **Decision.** Soft barriers around areas that aren't open yet: crossing one shows a countdown and sends the player back.
* **Decision.** Flight zones (the neutral continent and the Sky Island).
* **Decision.** Node volumes with their type (city, capital, village, mine, forest, farm, port, island) and their region, whose parent is the city node; open sea between islands, reefs and wrecks belong to transitional nodes.
* **Proposal.** Fog-bank and calm-zone areas, cave shelter volumes (no weather inside), updrafts, rockfall areas, and the eruption hazard area with its ore-richness ring.

## Paths

* **Decision.** Rivers, drawn as curves; a canyon river can flood.
* **Decision.** Roads, where auto-path works (besides mapped areas). Paved roads never turn to mud; the cooker raises them or bridges the channels where they would flood, and warns when a road would flood in a monsoon.
* **Decision.** Lava channels.
* **Decision.** Avalanche and mudslide paths: the cooker generates them from the elevation layer (start, path and landing area), and hand-placed markers only add, remove or adjust a path.
* **Proposal.** Routes for convoys, escorts, trade and public transport, with their stations ([[TRANSIT-01 Public Transport|TRANSIT-01]]).

## Ship assets (Blender)

* **Decision.** Compartment volumes in ship space, each with its breach limit ([[SHIP-01 Naval Combat Flooding Repair and Sea Events|SHIP-01]]).
* **Decision.** Windows and openings flagged so a bucket throw passes through them.
* **Decision.** The part slots each ship type allows: hull, bow, masts, sails, rigging, helm, cannons and figurehead ([[MOV-02 Travel Depth|MOV-02]]).
* **Proposal.** Hull sockets for attachments, a point and a normal flagged as reachable from the deck or only over the side; a ship type has 1 to 8 of them ([[ATTACH-01 Ship Attachments|ATTACH-01]]).

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Pipeline|Pipeline]] · [[Vertical slice order|Vertical slice order]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Map authoring markers · exported 2026-11-03
