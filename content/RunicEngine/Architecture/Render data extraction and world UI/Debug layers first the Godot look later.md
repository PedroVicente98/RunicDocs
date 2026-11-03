---
title: "Debug layers first, the Godot look later"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Render data, extraction and world UI (Engine, Game) › Debug layers first, the Godot look later"
created: "2026-10-14"
modified: "2026-10-30"
---

Both the debug layers and the final look read the same [[RenderData in Core|RenderFrame]], so moving from one to the other, or showing both side by side, needs no gameplay change.

**Debug layers come first.** One layer per kind of render data, each drawn simply by GodotBridge and toggled from the development overlay or the RunicEditor, so a developer chooses exactly what to see. They are built layer by layer, starting with [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] geometry and adding a layer whenever a slice needs it. They run in development builds of the client and in the [[Tools#RunicEditor|RunicEditor]] viewport; the RunicEditor also draws debug geometry streamed from development and staging servers.

| Debug layer | Draws | Slice | Package |
| :---- | :---- | :---- | :---- |
| Debug shapes | Lines, shapes and text issued by any system | [[Slice 02 Debug drawing\|2]] | [[GDB-2\|GDB-2]] |
| Physics geometry | Collision bodies and shapes extracted by Physics, with cached debug meshes for large shapes | [[Slice 08 Physics view\|8]] | [[GDB-4\|GDB-4]] |
| Meshes | Cooked mesh instances | [[Slice 22 World rendering\|22]] | [[GDB-5\|GDB-5]] |
| Skinned meshes | Characters with their animation | [[Slice 23 Animated characters\|23]] | [[GDB-6\|GDB-6]] |
| Lights, environment, volumes | Godot lights, skylight and darkness, fog, darkness zones | [[Slice 25a Night on screen\|25a]] | [[GDB-7\|GDB-7]] |
| Water and fields | Water surfaces; currents and wind as arrows, streaks or heatmaps | [[Slice 42a Water and currents on screen\|42a]] | [[GDB-8\|GDB-8]] |

**The production look comes later.** Materials, shaders, lighting and shadows, terrain, water shading, VFX and decals are Godot resources fed by [[RenderData in Core|RenderData]], built once a substantial game slice justifies the investment (slice [[Slice 44 Expansion|44]] onward, package [[GDB-13|GDB-13]]). Game render features register then, as materials and presenter hooks. Until that point every slice is proven with Godot’s default materials and the debug layers, which already show the true state of the world.

**The presenter.** Godot keeps objects between frames, so the presenter creates an instance once (by its RenderInstanceId), moves it only when its transform changes and frees it when it leaves interest; repeated static meshes of a cell go into one MultiMesh. Its origin is rebased rarely (see Client runtime).

---

↑ [[Render data extraction and world UI|Render data, extraction and world UI (Engine, Game)]] · ← [[Extraction|Extraction]] · [[World UI diegetic first with fallbacks|World UI: diegetic first, with fallbacks]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Render data, extraction and world UI (Engine, Game) › Debug layers first, the Godot look later · exported 2026-11-03
