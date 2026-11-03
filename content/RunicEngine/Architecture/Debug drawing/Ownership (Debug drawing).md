---
title: "Ownership (Debug drawing)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine) › Ownership"
created: "2026-10-14"
modified: "2026-10-30"
---

| Layer | Owner | Owns | Does not own |
| :---- | :---- | :---- | :---- |
| Simulation and client world | Engine and Game | Transforms, prediction, collision state, combat volumes | Godot resources, materials, draw calls |
| Debug-draw API (Core) | Engine | Turning abstract shapes into DebugGeometry lines, triangles and text | [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] bodies, gameplay entities, Godot |
| Debug layers (Runic::[[How the Engine uses Godot\|GodotBridge]]) | Engine | Uploading DebugGeometry to the RenderingServer, materials, toggles, the development overlay | Combat rules, physics authority, ECS behavior |
| Physics view | Engine (development only) | Runic::Physics extracts Jolt debug geometry into plain Core buffers; a GodotBridge layer draws them | Gameplay rendering; a link between Physics and GodotBridge |
| Godot | Third party | Rendering, windows, the RenderingServer | Scenes of the game, gameplay objects, skill meaning |
| What gets drawn and in which color | Game | Debug overlays for its own systems | — |

**First milestone (slice [[Slice 02 Debug drawing|2]]):** a grid, one movable capsule, one camera, one attack arc, one ray, and text showing the simulation tick and network state, all drawn by Godot from the debug-draw API. If that works reliably, [[Debug drawing|debug drawing]] is already useful.

---

↑ [[Debug drawing|Debug drawing (Engine)]] · [[Debug-draw API|Debug-draw API]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) › Ownership · exported 2026-11-03
