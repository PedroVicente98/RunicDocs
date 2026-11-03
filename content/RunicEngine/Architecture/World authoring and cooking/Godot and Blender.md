---
title: "Godot and Blender"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Godot and Blender"
created: "2026-10-14"
modified: "2026-10-30"
---

Blender makes assets; Godot assembles the world. The border is glTF (plus the terrain heightmap): nothing from a .blend reaches Godot or [[Cooker|the Cooker]], Blender never knows a game rule, and Godot never edits a mesh.

| Task | Where | Leaves as |
| :---- | :---- | :---- |
| Modeling rocks, buildings, props, weapons and characters | Blender | glTF |
| UVs and texture baking (normals, occlusion) | Blender or a texturing tool | Textures |
| Simplified collision meshes and hand-made LODs | Blender | glTF, with the naming convention |
| Rigs, skinning and animations | Blender | glTF with its clips |
| Large-scale terrain sculpting | Blender or a terrain tool | Heightmap (.exr) and masks |
| Asset import: default collision, LOD, compression | Godot | Import settings |
| Final materials and shaders | Godot | The project’s materials and shaders |
| World layout: regions, each region’s origin, asset placement | Godot | World and region scenes (.tscn) |
| Runic markers: spawn areas, volumes, interactables, routes, colliders | Godot | Marker nodes |
| Water: rivers, lakes, ocean | Godot | RunicWaterBody3D (rivers on Path3D) |
| Decorative vegetation and scattering | Godot, through tools | MultiMesh; interactive resources spawn by rule |
| Terrain painting and fine shaping | Godot, through a Runic tool or plugin | Terrain layers |
| Lighting, sky, environment and post-processing | Godot | Environment resources |
| Player UI | Godot | UI scenes |
| Data: skills, items, AI, quests, spawn rules | Godot, through schema inspectors | Runic data files |
| Cooking and export | Godot ([[Tools#RunicEditor\|RunicEditor]]) | Server and client packages |

* **One path:** meshes and animation enter through glTF; when an asset is re-exported, Godot re-imports it and updates the scenes that use it.

* **Units and axes:** meters and scale 1\. glTF is Y-up; Blender’s exporter converts from Blender’s Z-up, and Godot is already Y-up.

* **Identity:** an asset gets a stable UID in Godot, and the Cooker maps that UID to the Runic AssetId.

* **Collision:** the naming convention is decided once and documented in the project template, so the artist in Blender and the importer in Godot speak the same language.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Ownership (World authoring and cooking)|Ownership (World authoring and cooking)]] · [[World scene and region scenes|World scene and region scenes]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Godot and Blender · exported 2026-11-03
