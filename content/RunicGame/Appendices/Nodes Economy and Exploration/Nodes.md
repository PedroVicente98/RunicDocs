---
title: "Nodes"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Nodes, Economy and Exploration"
source_url: "https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit"
section: "Nodes"
created: "2026-10-19"
modified: "2026-10-30"
---


## What a node is

* **Decision.** The node is the unit of the regional economy, production and map discovery, defined as a volume. A region is a city node (the parent) with its child nodes: villages, mines, forests, farms, ports and islands. Every point of the map belongs to a node.  
* **Decision.** Each node type has its own [[Regional economy#Prosperity and node missions|prosperity]] and missions (see Prosperity and [[Regional economy#Prosperity and node missions|node missions]]).  
* **Decision.** At sea, a node that can be owned needs an island, a lighthouse or a dock. Open water, reefs and wrecks belong to transitional nodes, which no guild can own and which have no missions or prosperity; they exist so that connections, danger and the route service cover the whole map.  
* **Decision.** Nodes have complex borders: they follow the region's border and close exactly against their neighbors, with no gaps or overlaps. The editor validates this.  
* **Decision.** Some world rules are per node: controlled events and spawns, agriculture, climate and environment.  
* **Decision.** The map has three height bands (sky, surface, underground). The bands exist only in the interface; the engine stays in XYZ.  
* Engine: each node is a single cheap struct of about 64 bytes (1,000 nodes take about 64 KB per map). Node volumes are cooked into node IDs per cell, so "which node am I in" is a lookup done only when an entity changes cell. Cells on a border are marked mixed and resolved with an exact point-in-polygon test, which keeps borders precise. Shared economic state lives in a Go service, not in the struct.

## Node ecology

* **Decision.** Each node carries climate and environment data, which decide the fauna, flora and resources that exist there.  
* **Decision.** Map volumes define where a resource type can grow (ore, flora, fauna and so on), and the node decides which species actually grow. Example: one node has bananas and potatoes as flora and pigs and rats as animals.  
* **Decision.** Volumes can be generic ("potatoes and bananas can grow here") or specific ("only rats here"), so a designer can build a rat-infested area when they want one. This keeps content creation simple.  
* **Decision.** Hostile mobs are placed by hand in volumes. A volume can hold several mob types (goblins and wolves together) and exact positions.

## Connections

* **Decision.** Nodes are linked by connections. Nodes joined by a road are stronger than nodes joined over a mountain, and trade across weak connections costs more, because the resource becomes rarer.  
* **Decision.** A node at war adds an automatic cost to paths through it, and values rise while the war lasts.  
* **Decision.** Connection cost \= length × type factor: road 1.0; sea lane 1.2; trail or river 1.5; mountain pass 3.0.

## Guilds, regions and nodes

* **Decision.** Guilds take child nodes through node wars, and a large guild can take a whole region instead. A guild holds at most 3 nodes or one region, never both, so small guilds hold nodes and large guilds hold regions. The limit is a hard block.  
* **Decision.** On the neutral continent the ruling guild builds a castle in one of the region's castle zones. On the faction continents it uses the city itself and has an exclusive guild building.  
* **Decision.** Guild income works like Black Desert's: a fixed weekly payout by tier and prosperity, paid by the game. A region pays much more than a node, according to how well the ruling guild maintains it. Bonuses (a node mission at 200%, many region projects) count only inside the weekly cap, which is the fixed value of each prosperity level.  
* **Decision.** Wars are scheduled and need an active attacker. Each guild can challenge one node per week.  
* **Decision.** Alliances exist. Admins can regulate guilds that act as an alliance outside the system.  
* **Decision.** A guild needs about 10 active members to hold a node.  
* **Open.** What else the ruling guild decides besides spending packs on the region's projects.

---

↑ [[Nodes Economy and Exploration|Nodes, Economy and Exploration]] · ← [[Combat state|Combat state]] · [[Regional economy|Regional economy]] →  
Source: [RunicGame — Appendix: Nodes, Economy and Exploration](https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit) › Nodes · exported 2026-11-03
