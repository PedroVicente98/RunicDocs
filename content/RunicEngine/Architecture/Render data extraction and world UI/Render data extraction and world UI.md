---
title: "Render data, extraction and world UI (Engine, Game)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Render data, extraction and world UI (Engine, Game)"
created: "2026-10-14"
modified: "2026-10-30"
---

Godot and the player UI never read [[Simulation core Flecs and Jolt#Flecs rules|Flecs]], [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] or the domain modules. Each frame the Client extracts what must be shown into plain RenderData structs that live in Core, and only [[How the Engine uses Godot|GodotBridge]] consumes them: its presenter, debug layers and world UI turn them into Godot calls. The same [[RenderData in Core|RenderData]] feeds the debug layers, built first, and the production look (materials, shaders, lighting), built once the game slice justifies it.

![[arch-render-data-flow-sources-extraction-renderframe-go.png]]
*Render data flow — sources, extraction, [[RenderData in Core|RenderFrame]], GodotBridge and Godot*

*Render data flow — sources, extraction, RenderFrame, GodotBridge and Godot*

Read top to bottom: the client world feeds extractors, extractors write one RenderFrame of plain data, and only GodotBridge reads that frame and talks to Godot.

| Part | Owner | Contains |
| :---- | :---- | :---- |
| RenderData (Core) | Engine | Plain structs: the frame packet, debug geometry, mesh and skinned instances, world anchors, lights, environment frame, volumes, field grids, water surface state, effects |
| Extractors (Runic::Client) | Engine | The extractor registry and the Engine extractors for meshes, skinned instances, anchors, lights, environment, volumes, water and fields |
| Game extractors (RunicGame::Client) | Game | Game-specific visuals: spell effects, chart overlays, faction markers |
| Debug layers (Runic::GodotBridge) | Engine | One layer per kind of render data, drawn through Godot and toggled on or off |
| Presenter and production look (Runic::GodotBridge) | Engine; the look later | RenderFrame instances in the RenderingServer; later materials, shaders, lighting and shadows, terrain, water shading, VFX and decals as Godot resources |
| Render features (RunicGame::Client) | Game, later | Custom Godot materials, shaders and presenter hooks |
| World UI mechanism (Runic::GodotBridge) | Engine | Diegetic SubViewport panels, anchored Label3D and Sprite3D, the batched MultiMesh fallback, budgets and input routing |
| World UI content (RunicGame::Client) | Game | Nameplates, prompts, boards, ship panels; their Godot UI scenes, themes and view models |

## Contents

- [[RenderData in Core|RenderData in Core]]
- [[Extraction|Extraction]]
- [[Debug layers first the Godot look later|Debug layers first, the Godot look later]]
- [[World UI diegetic first with fallbacks|World UI: diegetic first, with fallbacks]]

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Client runtime Game on Engine|Client runtime (Game on Engine)]] · [[Audio|Audio (Engine, Game)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Render data, extraction and world UI (Engine, Game) · exported 2026-11-03
