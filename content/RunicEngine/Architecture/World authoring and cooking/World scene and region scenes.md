---
title: "World scene and region scenes"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › World scene and region scenes"
created: "2026-10-14"
modified: "2026-10-30"
---

The v3 model stays: one low-detail map with the layout and one file per region with the detail, together one world. In Godot both levels are scenes.

* **World.tscn** is the master plan (the old WorldLayout.blend): region boundaries, low-resolution macro terrain, major routes, large rivers and landmarks. Each region appears in it as a RunicRegion3D node that shows only a lightweight proxy of the region; a double click opens the detailed scene.

* **Regions/Greenvale.tscn** is the region with all its detail, edited near its local origin. Its root is a RunicRegion node with the RegionId, the boundary polygon and the global origin.

* **Neighbors and borders:** while a region is edited, its neighbors show as read-only proxies, placed by the difference between origins (computed in double and only then converted), with an overlap band on the border to match terrain and assets.

* **New region from layout** is v3’s “Create Region From Layout”: from a boundary drawn in World.tscn it creates the region scene with its origin, the cut of the macro terrain and the neighbor references. It is a one-time step; afterwards the region owns its detail.

* **64-bit origins:** Godot’s Vector3 is float32 and, 712 km from the origin, moves in 6.25 cm steps. A region origin is stored as three float properties (which Godot keeps as doubles) or as 64-bit integer centimeters, never as a Vector3.

```cpp
// Illustrative: in World.tscn
class RunicRegion3D : public godot::Node3D {
    GDCLASS(RunicRegion3D, godot::Node3D)
    godot::String regionScene;                    // "uid://…" of the detailed scene; never loaded here
    double originX = 0, originY = 0, originZ = 0; // global origin in double
    godot::Ref<godot::Mesh> proxy;                // lightweight version, rebuilt when the region is saved
};
```

**Gameplay regions are not terrain tiles.** A designer-facing region can have any polygon that follows geography, politics, biome or content, while terrain and streaming subdivisions stay a regular grid.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Godot and Blender|Godot and Blender]] · [[Large worlds in the editor|Large worlds in the editor]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › World scene and region scenes · exported 2026-11-03
