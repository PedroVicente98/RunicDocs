---
title: "Cooker"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Cooker"
created: "2026-10-14"
modified: "2026-10-30"
---

The Cooker is Runic code: the orchestration layer and native-format writer. It runs inside the [[Tools#RunicEditor|RunicEditor]] from an export plugin, and build machines run the same RunicEditor without a window.

| Pipeline stage | Technology | Where it runs |
| :---- | :---- | :---- |
| Asset modeling | Blender | External application |
| Interchange | glTF 2.0 and GLB | Source data |
| Import, textures, LODs and materials | Godot importers | RunicEditor |
| World assembly and markers | RunicEditor (GodotTools) | Editor |
| Collision cooking and runtime | [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] Physics | Cooker, client and server |
| Collision simplification | meshoptimizer | Cooker |
| Navmesh cooking | Recast | Cooker |
| Navigation runtime | Detour and DetourTileCache | GameServer |
| Package compression | Zstandard | Cooker, plus runtime decompression |
| Client visual package | Godot export (.pck) | RunicEditor |
| Rendering | Godot (libgodot, template target) | GameClient |
| Gameplay and world ECS | [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] | Runtime |

| Executable | Links |
| :---- | :---- |
| GameClient | libgodot (template), godot-cpp, Jolt (for prediction and local collision), Flecs, Zstandard, Engine runtime |
| GameServer | Jolt, Flecs, Detour, Zstandard, Engine runtime |
| RunicEditor | libgodot (editor), godot-cpp, the Cooker (Jolt cooking, Recast, meshoptimizer, Zstandard, Runic writers), Engine runtime |

**One authored truth, many runtime products.** From one castle, terrain patch or region the Cooker emits Jolt collision shapes, Recast and Detour nav tiles, terrain cells and masks, world placements and metadata, water fragments and flow fields, spawn areas with candidate points, server-only gameplay and spatial data and client cell visual lists; Godot’s export emits the textures, meshes and materials. The runtime never needs to understand an editor scene.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Interchange glTF and terrain sources|Interchange: glTF and terrain sources]] · [[Cooked world files and packages|Cooked world files and packages]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Cooker · exported 2026-11-03
