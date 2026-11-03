---
title: "Ownership (World authoring and cooking)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Ownership"
created: "2026-10-14"
modified: "2026-10-30"
---

| Part | Owner | Contains |
| :---- | :---- | :---- |
| [[Tools#RunicEditor\|RunicEditor]] world tools (GodotTools) | Engine (tool) | World and region scenes, RunicRegion3D proxies, New region from layout, neighbor proxies, marker nodes, validation, the “see what the server sees” layer, cook launch |
| [[Cooker\|Cooker]] | Engine (tool) | Orchestration, Runic format writers, collision, nav and water cooking, incremental builds, validation |
| Runtime formats | Engine | World manifest, region headers, cell files, packages, collision, nav tiles, water fragments, spawn areas |
| Godot import and export | Godot, configured by Engine presets | Imported meshes, textures and materials; the client .pck |
| Blender export helper | Engine (optional tool) | Collision and LOD naming conventions and glTF export presets |
| World content | Game | World.tscn, region scenes, terrain, shared assets, marker nodes, spawn rules, water and wind maps, metadata values |
| Platform | Platform | Nothing in authoring or cooking |

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · [[Godot and Blender|Godot and Blender]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Ownership · exported 2026-11-03
