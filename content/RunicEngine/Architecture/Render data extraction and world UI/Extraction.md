---
title: "Extraction"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Render data, extraction and world UI (Engine, Game) › Extraction"
created: "2026-10-14"
modified: "2026-10-30"
---

Extraction runs in the client’s Presentation layer once per frame, after the latest simulation results are applied. Extractors read [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] and the domain APIs (Water, Perception, Environment, Animation) read-only and write [[RenderData in Core|RenderData]]; they never change the simulation.

* **A registry of extractors.** Each extractor fills one or more kinds. The Engine registers its own under engine: IDs; RunicGame::Client registers its own under game: IDs.

* **Parallel.** Independent extractors run on the worker pool into per-worker arenas that are merged into the frame packet in a fixed order.

* **Change-driven when the source is slow.** Field grids, water state and the environment re-extract only when their source version changes (currents and weather update at 10 Hz), and [[How the Engine uses Godot|GodotBridge]] re-uploads a texture only when its version changes.

* **Culled and capped at the source.** Each extractor culls by frustum and distance and respects a per-kind cap (lights, anchors), so Godot never receives work it will throw away.

* **Interpolation and precision here.** Remote entities are interpolated between snapshots and positions converted to camera-relative floats once, during extraction.

```cpp
// Illustrative
extraction.Register("engine:meshes",  MeshExtractor{});                 // Flecs Transform + RenderMesh
extraction.Register("engine:skinned", SkinnedExtractor{animation});      // poses from Runic::Animation
extraction.Register("engine:anchors", AnchorExtractor{perception});      // carries the PvP visibility tier
extraction.Register("engine:lights",  LightExtractor{perception});       // the server's emitters
extraction.Register("engine:fields",  FieldExtractor{water, environment}, ExtractRate::OnChange);

// RunicGame::Client
extraction.Register("game:chart_overlay", ChartOverlayExtractor{});
```

**Example: showing an ocean current.** The Water module holds the cooked current field and the Environment modulates it over time. The field extractor samples the area around the camera into a 64 by 64 field grid only when the current’s version changes. The debug layers draw it as arrows or animated streaks; later, the production look uses the same grid to animate the water surface or a nautical-chart overlay. Neither Water nor Godot knows about the other.

---

↑ [[Render data extraction and world UI|Render data, extraction and world UI (Engine, Game)]] · ← [[RenderData in Core|RenderData in Core]] · [[Debug layers first the Godot look later|Debug layers first, the Godot look later]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Render data, extraction and world UI (Engine, Game) › Extraction · exported 2026-11-03
