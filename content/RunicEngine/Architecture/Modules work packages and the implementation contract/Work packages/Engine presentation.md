---
title: "Engine: presentation"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: presentation"
created: "2026-10-14"
modified: "2026-10-30"
---

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| [[CLI-1\|CLI-1]] | Presentation layer and extractor registry; the first extractor writes entities as debug shapes; camera | Entities are drawn from the [[RenderData in Core\|RenderFrame]] only | [[ECS-1\|ECS-1]], [[GDB-2\|GDB-2]], [[CORE-3\|CORE-3]] | [[Slice 05 Moving entities\|5]] |
| [[CLI-2\|CLI-2]] | Input mapping, actions and command builder over the AppEvents the GodotLayer forwards | Key presses become movement commands; input Godot’s UI consumed never reaches them | [[GDB-1\|GDB-1]], [[SIM-2\|SIM-2]] | [[Slice 07 Physics\|7]] |
| [[CLI-3\|CLI-3]] | Prediction layer driving the prediction subset and reconciliation each frame | The local player moves at once and corrects on server state | [[SIM-4\|SIM-4]], [[NET-3\|NET-3]] | [[Slice 14 Prediction\|14]] |
| [[CLI-4\|CLI-4]] | Mesh-instance extractor with interpolation, camera-relative conversion and a stable RenderInstanceId | Cooked meshes appear at their entities’ positions far from the origin | [[CLI-1\|CLI-1]], [[CORE-4\|CORE-4]] | [[Slice 22 World rendering\|22]] |
| [[CLI-5\|CLI-5]] | Skinned-instance extractor with poses or animation intent, per the open animation decision | Characters animate on screen | [[CLI-4\|CLI-4]], [[ANIM-1\|ANIM-1]] | [[Slice 23 Animated characters\|23]] |
| [[CLI-6\|CLI-6]] | World-anchor extractor: position, distance, visibility tier and priority per entity | Anchors follow entities; Hidden players produce none | [[CLI-1\|CLI-1]], [[CORE-4\|CORE-4]] | [[Slice 23a World UI\|23a]] |
| [[CLI-7\|CLI-7]] | Light, environment and volume extractors from Perception and Environment | Darkness and torches on screen match the server’s light values | [[CLI-1\|CLI-1]], [[CORE-5\|CORE-5]], [[PRC-1\|PRC-1]] | [[Slice 25a Night on screen\|25a]] |
| [[CLI-8\|CLI-8]] | Water-surface and field-grid extractors from Water and Environment, change-driven | Grids re-extract only when the current or the wind changes | [[CLI-1\|CLI-1]], [[CORE-6\|CORE-6]], [[WATER-5\|WATER-5]] | [[Slice 42a Water and currents on screen\|42a]] |
| [[CLI-9\|CLI-9]] | [[Tools#Testing at scale\|RunicBot]]: the client runtime without presentation, many bot sessions per process, a simple brain (walk, fight, follow a quest) | One process holds hundreds of bots against a local server; no Godot is linked | [[CLI-3\|CLI-3]], [[NET-4\|NET-4]] | [[Slice 38 Battle scale\|38]] |
| [[GDB-1\|GDB-1]] | GodotLayer: the LibGodot instance (create, start, iteration, stop) at the top of the client [[Application and LayerStack\|LayerStack]]; window from the DisplayServer; input forwarded as AppEvents after Godot’s UI; headless mode | The client starts Godot windowed and headless and exits cleanly; UI clicks never reach the stack | [[APP-1\|APP-1]], [[BUILD-1\|BUILD-1]] | [[Slice 01 Application and layers\|1]] |
| [[GDB-2\|GDB-2]] | Debug drawing on Godot: a debug-draw API (lines, shapes, text) uploaded as immediate meshes with depth-tested and overlay materials; toggled layers; development overlay panel; it reads Core DebugGeometry once [[CORE-3\|CORE-3]] lands | Every debug shape and text renders batched in one frame; layers toggle | [[GDB-1\|GDB-1]] | [[Slice 02 Debug drawing\|2]] |
| [[GDB-3\|GDB-3]] | Presenter: RenderFrame instances created, moved and freed in the RenderingServer by RenderInstanceId; presenter origin with a rare rebase (about every 4 km) | 50,000 static instances cost nothing per frame unless they change; a 20 km walk shows no jitter | [[GDB-2\|GDB-2]], [[CORE-3\|CORE-3]] | [[Slice 05 Moving entities\|5]] |
| [[GDB-4\|GDB-4]] | Physics geometry layer: DebugGeometry from [[PHYS-3\|PHYS-3]] with cached debug meshes for large shapes; the “see what the server sees” overlay | Collision shapes line up with gameplay shapes and the layer toggles | [[GDB-3\|GDB-3]], [[PHYS-3\|PHYS-3]] | [[Slice 08 Physics view\|8]] |
| [[GDB-5\|GDB-5]] | Mesh instances from cooked cells and entities, repeated meshes as MultiMesh, assets from the project or the .pck | Cooked meshes draw correctly far from the origin | [[GDB-3\|GDB-3]], [[CLI-4\|CLI-4]] | [[Slice 22 World rendering\|22]] |
| [[GDB-6\|GDB-6]] | Skinned instances: poses into RenderingServer skeletons, or AnimationTree driven by intent, per the open animation decision | An animated character renders | [[GDB-5\|GDB-5]], [[CLI-5\|CLI-5]] | [[Slice 23 Animated characters\|23]] |
| [[GDB-7\|GDB-7]] | Lights, environment and volumes as Godot lights, environment and fog volumes | Torches, skylight, darkness zones and fog show and toggle | [[GDB-5\|GDB-5]], [[CLI-7\|CLI-7]] | [[Slice 25a Night on screen\|25a]] |
| [[GDB-8\|GDB-8]] | Water surfaces and field grids (arrows, streaks, heatmaps, water materials) | A river surface and the ocean current draw from cooked data | [[GDB-5\|GDB-5]], [[CLI-8\|CLI-8]] | [[Slice 42a Water and currents on screen\|42a]] |
| [[GDB-9\|GDB-9]] | UI bridge: one Godot UI scene per client state; the view-model binder that writes only changed fields to controls | The skill bar triggers abilities and UI clicks never attack | [[GDB-1\|GDB-1]], [[CORE-3\|CORE-3]] | [[Slice 19 Combat prototype\|19]] |
| [[GDB-10\|GDB-10]] | World UI: anchored Label3D and Sprite3D elements; diegetic panels in SubViewports on quads or mesh surfaces, with ray input into panel coordinates | Nameplates follow entities; a click on a world board reaches its panel and becomes a command | [[GDB-9\|GDB-9]], [[CLI-6\|CLI-6]] | [[Slice 23a World UI\|23a]] |
| [[GDB-11\|GDB-11]] | Batched world UI and mode fallbacks: MultiMesh nameplates and bars from an atlas; widgets move between diegetic, anchored, batched and hidden by distance, count and battle budgets | 500 nameplates draw in one call and the frame budget holds in a 500-player fight | [[GDB-10\|GDB-10]] | [[Slice 38 Battle scale\|38]] |
| [[GDB-12\|GDB-12]] | Audio backend: implements the Runic::Audio backend interface on the AudioServer (buses, mixing, streams, spatial playback) | A sound event plays through its bus with volume control | [[GDB-1\|GDB-1]], [[AUD-1\|AUD-1]] | [[Slice 24 Sound and music\|24]] |
| [[GDB-13\|GDB-13]] | Production look: materials, terrain, water shading, VFX and decals as Godot resources fed by [[RenderData in Core\|RenderData]]; Game render features as materials and presenter hooks | Defined when a substantial game slice justifies it | [[GDB-5\|GDB-5]] | [[Slice 44 Expansion\|44+]] |
| [[ANIM-1\|ANIM-1]] | Skeletons, clips, animator and blending (scope set by the open animation decision) | Clips blend without pops | [[ASSET-1\|ASSET-1]] | [[Slice 23 Animated characters\|23]] |
| [[AUD-1\|AUD-1]] | Audio backend interface, buses, mixing, semantic sound events | A sound event resolves through the registry to a backend call | [[ASSET-1\|ASSET-1]] | [[Slice 24 Sound and music\|24]] |
| [[AUD-2\|AUD-2]] | MusicDirector: contexts, fallback chains, albums, presets, radio playback, local profile | A context change switches album and remembers the position | [[AUD-1\|AUD-1]] | [[Slice 24 Sound and music\|24]] |

---

↑ [[Work packages|Work packages]] · ← [[Engine networking|Engine: networking]] · [[Engine tools|Engine: tools]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: presentation · exported 2026-11-03
