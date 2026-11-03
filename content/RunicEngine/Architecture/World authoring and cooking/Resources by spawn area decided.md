---
title: "Resources by spawn area (decided)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Resources by spawn area (decided)"
created: "2026-10-14"
modified: "2026-10-30"
---

Interactive resources (trees that can be cut or harvested, crops such as potatoes and carrots, ores, herbs) are never placed one by one. They spawn by rules inside spawn areas; the map only says where they may appear. Decorative vegetation stays in MultiMesh with no entity.

| Stage | What happens |
| :---- | :---- |
| Authoring | A RunicSpawnArea3D (volume, polygon or painted mask) points at a rule in Data/, such as game:greenvale\_apples |
| Rule | A schema-backed file that says what, how many, when and where inside the area; complexity grows by levels |
| Cooking | The server receives the area and a list of valid candidate points (on the ground, acceptable slope, clear of rocks, reachable); the client receives nothing |
| Runtime | In the maintenance phase the spawn system evaluates the rules of active areas, picks points and queues commands; each resource becomes a [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] entity with a static [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] body |
| Replication | A resource reaches a client when it enters interest (about 20 bytes) and then only on state changes; 300 resources in view cost about 6 KB once |

* **Simple rules:** maximum alive, respawn time, minimum spacing.

* **Weighted rules:** weights by altitude, slope, surface, biome, season and time of day (from the Environment).

* **Complex rules:** a C++ behavior the Game registers (world events, depletion and migration, player activity), on the v3 custom-behavior model.

id: game:greenvale\_apples  
spawns: game:apple\_tree  
max\_alive: 40              \# per area  
respawn\_s: 900  
respawn\_at: new\_point      \# or same\_point: regrows in place  
placement:  
  min\_spacing\_m: 6  
  max\_slope\_deg: 25  
  surface: \[grass, dirt\]  
weights:                   \# optional  
  altitude\_m: { 0-300: 1.0, 300-600: 0.4 }  
  season:     { summer: 1.0, winter: 0.0 }  
custom: game:orchard\_event\_boost   \# optional

```yaml
id: game:apple_tree
kind: resource_node
states:
  full:   { visual: { mesh: game:apple_tree, show: [trunk, leaves, apples] }, collision: trunk }
  picked: { visual: { mesh: game:apple_tree, show: [trunk, leaves] },         collision: trunk }
  stump:  { visual: { mesh: game:apple_tree_stump },                           collision: stump }
interactions:
  pick: { from: full, to: picked, yields: { game:apple: 3-5 }, regrow_s: 600 }
  chop: { from: [full, picked], to: stump, requires: game:axe, yields: { game:wood: 4 }, regrow_s: 3600 }
```

* **No simulation of empty areas:** only areas in active cells spawn. When a cell loads, the area fills up to the count its rule expects for the time since the last visit, seeded, instead of having been simulated meanwhile: the same principle as world routines.

* **Engine and Game:** the Engine provides the volume, candidate sampling at cook time, the spawn API and rule primitives (engine:); the Game writes the rules and registers its own conditions (game:).

* **Persistence:** a common resource is ephemeral; after a restart the area refills by its rule. A rare resource that must survive restarts uses the durable path of the services.

* **States and visuals:** the resource definition maps each state to its visual and its collision; the asset comes from Blender with its states as parts or separate meshes. Falling when chopped is a client presentation cue; the server only records the state change.

* **In the editor:** the area previews its candidate points and expected density so the designer can adjust before running.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Marker nodes and what they cook into|Marker nodes and what they cook into]] · [[Interchange glTF and terrain sources|Interchange: glTF and terrain sources]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Resources by spawn area (decided) · exported 2026-11-03
