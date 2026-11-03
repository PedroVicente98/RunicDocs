---
title: "Marker nodes and what they cook into"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Marker nodes and what they cook into"
created: "2026-10-14"
modified: "2026-10-30"
---

Runic marker nodes exist only in the editor: RunicSpawnArea3D, RunicVolume3D, RunicInteractable3D, RunicWaterBody3D, RunicRoute3D and RunicCollider3D. Cooking turns them into placements and volumes, and on load the Engine creates [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] entities by its own rules. The game adds its own marker types through its editor library.

| In the editor | The server receives | The client receives |
| :---- | :---- | :---- |
| Scenery mesh (rock, building) | Cooked [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] collision | Mesh ID and transform per cell; the same collision near the player, for prediction |
| Terrain | Jolt heightfield | Terrain mesh and materials; the heightfield near the player |
| RunicSpawnArea3D (trees, crops, ores, mobs) | The area, its rule and candidate points | Nothing fixed; each spawned entity arrives replicated |
| RunicVolume3D (cave, PvP zone, flight zone) | AuthoredVolume | Only if it has a visible effect, such as fog |
| RunicInteractable3D (door, chest) | A placement that becomes a Flecs entity and a kinematic body | The visual; its state arrives replicated |
| Rivers and water bodies | Water fragments and flow fields | The water surface |
| (derived from collision) | Recast nav tiles | Nothing |
| Textures, materials, shaders | Nothing | Godot’s .pck |

Collision goes to both sides: the server needs it for authority and the client, near the player, for prediction. Both copies are the same [[Cooker|Cooker]] output, in Runic’s Jolt in 64-bit, which is why prediction agrees with the server.

**How collision is marked:**

1. **Asset default:** in Godot’s import settings, each mesh says which collision it generates: the mesh itself, a convex hull, a simplified mesh or none.

2. **Collision mesh in the glTF:** the artist models the simple version and exports it alongside, under the naming convention.

3. **RunicCollider3D:** a box, sphere, capsule or convex shape placed in the map for invisible walls, stairs and similar cases. The colliders are Runic’s because Godot’s physics is not in the build.

**Why server and client agree:**

* **Same ID:** every cooked thing has a stable ID (cell plus placement), so “door 4812 opened” names the same object on both sides.

* **Same coordinates:** the editor saves the local position in float, near the region origin; the Cooker writes the global one in double, region origin plus local.

* **Same version:** each cell carries a hash and the world a build ID. On connect the server states its build; a client with another one updates before entering. In development both read the same output folder.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Seamless terrain and borders|Seamless terrain and borders]] · [[Resources by spawn area decided|Resources by spawn area (decided)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Marker nodes and what they cook into · exported 2026-11-03
