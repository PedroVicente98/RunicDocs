---
title: "Maps and cartography"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Nodes, Economy and Exploration"
source_url: "https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit"
section: "Maps and cartography"
created: "2026-10-19"
modified: "2026-10-30"
---


## Map detail levels

| Level | How it is reached | What the map shows |
| :---- | :---- | :---- |
| Fog | Default | Black, no map detail |
| Discovered | Walking through the area | One static image, the same for every player, baked when the world is cooked and refreshed when the world changes in an update |
| Mapped | The node's base chart | Real-time top-down render of the terrain, with zoom and a tilt into 3D; time of day, weather and floating-island motion. Never players, ships or mobs |

* **Decision.** The three detail levels above are the only levels of the map itself. Other charts add markers on top: monster spawns, flora types, resources, air and water currents, events.  
* **Decision.** The player always sees their exact position. Without a node's chart, the map shows nothing about the node; the chart adds the node's information in a Black Desert-style layout of nodes and connections: specialty, biome, environment, [[Regional economy#Prosperity and node missions|prosperity]], owner and region.  
* **Decision.** The most basic chart already shows packing benches and vendors as icons and never expires. The map has many filters, one per kind of information the player buys or maps.  
* **Decision.** Charts unlock useful interactions in the game. That is why fan sites are fine: they show the information but cannot give the benefit.  
* **Decision.** A chart is consumed when used.  
* Engine: per Lineage, only the "discovered" bit per cell is stored (about 18 KB per map before compression). The real-time view is rendered from a cooked low-detail model of the world plus live state, so it reveals nothing about other players.

## Events on the map

* **Decision.** Without the events chart for a node, a player still sees that an event is happening there, but only while it runs or a few minutes before, as a marker on the region.  
* **Decision.** With it, the player sees a constant timer to the next events and their exact location.

## Chart layers

**Decision.** Each chart covers one layer of one node; no map holds everything. A finished chart has no quality grade.

| Layer | What it shows | In-game interaction |
| :---- | :---- | :---- |
| Base | Terrain, coast, paths, [[Real exploration#Altars, death, respawn and teleports\|Altars]], cave entrances; unlocks the Mapped level | Position on the map inside the node; route plotting |
| Resources | Spawn areas and what grows in them | Nearby resource areas highlighted in the world |
| Fauna | Species, danger, dens, patrol routines | Threat and aggro radius; patrol timing |
| Events | Where events happen and in which windows | Constant timers and exact locations; prediction at high proficiency |
| Environment | Currents, depth, reefs, whirlpools, weather | Live currents while sailing; prediction at high proficiency |

## Surveying

* **Decision.** Surveying is a PvP activity.  
* **Decision.** Each kind of cartography has its own tools and minigame (nautical charts use a sextant and other instruments). A survey applies only to the node where it is done.  
* **Decision.** Starter areas come surveyed, with charts for sale, so every player learns the mechanic.  
* **Consequence.** Since surveying is PvP, PvE players do not create base maps; they buy charts. This changes items 10 and 12.17 of the PvE/PvP contract v1.1 and [[Vision|the Vision]]'s mode table.  
* **Decision.** Minigames of the other layers: nautical charts in open sea with star fixes at night and a line of soundings; environment with drift buoys tracked over time; fauna observed with a spyglass without being detected; resources from collected samples, whose quality depends on the gathering profession; events recorded by being present.

## Triangulation (base chart on land)

* **Decision.** The player places 3 tools in the world, inside the node. They exist for everyone, like trade packs: other factions, pirates and active [[Factions PvP and crime#Outlaw and Infamy|Outlaws]] can destroy them and gain resources from it, and mobs attack them too. Hiding them until the survey ends is part of the game. They can be picked back up and are neither cheap nor expensive.  
* **Decision.** Placement quality is computed by geometry only: node area, triangle coverage and the angles of the three points. There is no line of sight.  
* **Decision.** Quality changes the survey's time and [[Labor|labor]], not the finished chart.  
* **Decision.** Flow: place the 3 tools, see coverage and angle, see the computed time and labor, interact with the last tool and create the chart.  
* **Decision.** Coverage \= triangle area ÷ node area, up to 1\. The smallest angle scores 0 below 20° and 1 from 50°. Score \= coverage^0.6 × angle^0.4, with a minimum of 0.2 to start. Time \= base time ÷ score, up to 3×. Labor \= base labor × (2 − score).  
* **Decision.** Locks: one active set per character; tools expire after about 24 h; the cartographer stays inside the node during the survey; all 3 tools must survive to the end; the server recomputes the score from the real positions.

---

↑ [[Nodes Economy and Exploration|Nodes, Economy and Exploration]] · ← [[Trade packs and routes|Trade packs and routes]] · [[Stamina and climbing|Stamina and climbing]] →  
Source: [RunicGame — Appendix: Nodes, Economy and Exploration](https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit) › Maps and cartography · exported 2026-11-03
