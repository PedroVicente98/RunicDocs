---
title: "Cooked world files and packages"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Cooked world files and packages"
created: "2026-10-14"
modified: "2026-10-30"
---

No scene survives cooking. The [[Cooker|Cooker]] reads World.tscn and each region scene and writes the Runic format; at runtime there is no scene, only the manifest and the cells.

| In authoring (Godot) | Becomes when cooked | Who uses it at runtime |
| :---- | :---- | :---- |
| World.tscn | MainWorld.runicworld: region registry (ID, global origin, bounds, neighbors), global ocean and environment, package index | Server and client, at load |
| Regions/Greenvale.tscn | Greenvale/region.header plus 3D cells of 64 m, each as .server and .client | The server loads cells near players; the client near the camera |
| Meshes placed in the region | Visual list per cell (AssetId and transform relative to the cell); [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] collision in the server cell | The presenter creates instances in the RenderingServer; server and prediction use the collision |
| Marker nodes | Placements, volumes, spawn areas, routes, water and nav tiles in the server cells | The server creates [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] entities when the cell loads |
| Meshes, textures and materials in Content/ | The client .pck | Godot inside the client |

The region is the unit of authoring and organization; the cell is the unit of loading; and who owns each part of the world at runtime is decided by the v3 authority partition, never by the file. Every global position is the region origin (double) plus the position the editor saved, and inside a cell it is relative to the cell origin, small and precise in float again.

```text
MainWorld.runicworld
  WorldId and instance policy
  coordinate system and global-origin policy
  world bounds
  volume registry (caves, rule areas, indivisible volumes)
  continent registry
  region registry
  global ocean and environment references
  world transition and portal policies
  package and dependency indices
```

A logical region becomes a header, cells, terrain pages, collision pages, nav tiles and spawn areas, either as loose entries or packed into one .runicpak with an internal random-access table of contents. A continent is never compressed as one sequential stream; packages always allow independent random access so cells can stream.

| Client cook | Server cook |
| :---- | :---- |
| Cell visual lists (AssetId, transform, LOD and proxy references) | Jolt collision data |
| The .pck from Godot’s export: meshes, textures, materials, UI, audio | Detour navigation tiles |
| Client-safe data definitions | Spawn areas, placements and spatial metadata |
| Client water render data | Region rules and server world objects |
| Collision near the player for prediction | Server water fragments and flow representation |

**Incremental cooking and the editor loop.** The Cooker tracks dependencies: moving one rock in Greenvale re-cooks only the cells it touches and their seam-dependent neighbors, and never unrelated continents. In development: you move a rock and save; the Cooker re-cooks its cells in seconds; the local server reloads those cells at a safe point (unload and load, like streaming); the client reloads their visuals. The “see what the server sees” layer draws the cooked collision, volumes, spawn points and nav tiles over the viewport, so a rock that looks solid without collision shows up before the game runs. For a live preview of water or AI in the viewport, the editor can run a local headless Runic simulation; that is still Runic code, not Godot.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Cooker|Cooker]] · [[Authoring work per roadmap slice|Authoring work per roadmap slice]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Cooked world files and packages · exported 2026-11-03
