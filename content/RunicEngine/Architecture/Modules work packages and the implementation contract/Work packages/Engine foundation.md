---
title: "Engine: foundation"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: foundation"
created: "2026-10-14"
modified: "2026-10-30"
---

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| [[BUILD-1\|BUILD-1]] | Build skeleton in all three repositories: runic\_add\_module helper, presets, CI, the chosen test framework, automated headless and forbidden-dependency checks, submodule pins (Game pins Engine and Platform; Platform pins Engine; Engine pins Godot and godot-cpp at a release tag) with a local option for sibling checkouts, an AVX2 (x86-64-v3) CPU baseline; libgodot built from source in the editor and template targets with the module lists and the SCons cache; libgodot, godot-cpp, [[How the Engine uses Godot\|GodotBridge]] and GodotTools catalogued as presentation | Every repository configures and builds; libgodot builds in both targets; the server target links no graphics library and no Godot; a forbidden link fails CI | — | [[Slice 00 Build skeleton\|0]] |
| [[CORE-1\|CORE-1]] | Plain ID types (GlobalEntityId, GlobalPlayerId, SimulationId, WorldId, TickId, AuthorityEpoch, and value types other modules give meaning to, such as AssetId, WaterBodyId, FieldId and WidgetId), Result, asserts, logging hooks, time types, GLM math | Unit tests cover IDs, Result and time conversions | [[BUILD-1\|BUILD-1]] | [[Slice 01 Application and layers\|1]] |
| [[CORE-2\|CORE-2]] | Worker pool, metrics registry (per-tick timings and counters) and debug-stream registry where modules publish traces | Jobs run on the pool; metrics are recorded per tick domain | [[CORE-1\|CORE-1]] | [[Slice 03 Fixed-step clock\|3]] |
| [[CORE-3\|CORE-3]] | RenderData foundation: the double-buffered [[RenderData in Core\|RenderFrame]] and DebugGeometry (lines, triangles, text, cached debug meshes) | A frame is written on one thread and read on another with no lock; debug vertices need no conversion before upload | [[CORE-1\|CORE-1]] | [[Slice 05 Moving entities\|5]] |
| [[CORE-4\|CORE-4]] | [[RenderData in Core\|RenderData]] scene kinds: mesh instances with a stable RenderInstanceId, skinned instances with pose buffers and animation intent, world anchors | Every kind round-trips through a frame packet in tests | [[CORE-3\|CORE-3]] | [[Slice 22 World rendering\|22]] |
| [[CORE-5\|CORE-5]] | RenderData world-state kinds: lights, environment frame, volumes | Every kind round-trips through a frame packet in tests | [[CORE-3\|CORE-3]] | [[Slice 25a Night on screen\|25a]] |
| [[CORE-6\|CORE-6]] | RenderData water and field kinds: water surface state, field grids | Versions change only when their source changes | [[CORE-3\|CORE-3]] | [[Slice 42a Water and currents on screen\|42a]] |
| [[CORE-7\|CORE-7]] | RenderData effect kinds: particles, decals, trails | Defined when the production look is planned | [[CORE-3\|CORE-3]] | [[Slice 44 Expansion\|44+]] |
| [[APP-1\|APP-1]] | Entry point, Application, ApplicationHost, Layer, [[Application and LayerStack\|LayerStack]] with queued changes at safe points, application events, loop policies, RunFrame so a host can drive one frame at a time | Layer order, events top-down until handled, updates bottom-up, safe-point push and pop, no allocation per event | [[CORE-1\|CORE-1]] | [[Slice 01 Application and layers\|1]] |
| [[EVT-1\|EVT-1]] | Typed tick-safe event buffers and readers, multi-consumer delivery, stable event IDs (SimulationId plus sequence) | Two consumers read the same fact; IDs stay stable on replay | [[CORE-1\|CORE-1]] | [[Slice 04 ECS and world coordinates\|4]] |
| [[CNT-1\|CNT-1]] | ContentId with engine: and game: namespaces, registries, lookup | Duplicate and unknown IDs are reported with their source | [[CORE-1\|CORE-1]] | [[Slice 09 First cooker proof\|9]] |
| [[CNT-2\|CNT-2]] | Versioned schemas, validation, loading, live-reload hooks | A changed definition reloads without a restart | [[CNT-1\|CNT-1]] | [[Slice 20 Data-driven content\|20]] |
| [[ASSET-1\|ASSET-1]] | AssetId, handles, cache, loading of native cooked mesh and collision formats | A cooked test mesh loads on client and server | [[CNT-1\|CNT-1]] | [[Slice 09 First cooker proof\|9]] |
| [[ASSET-2\|ASSET-2]] | Random-access packages and manifests with Zstandard decompression, client and server package selection, asynchronous streaming | Cells load from a package without stalling a tick or a frame | [[ASSET-1\|ASSET-1]], [[WORLD-3\|WORLD-3]] | [[Slice 21 World partitions\|21]] |

---

↑ [[Work packages|Work packages]] · [[Engine simulation core|Engine: simulation core]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: foundation · exported 2026-11-03
