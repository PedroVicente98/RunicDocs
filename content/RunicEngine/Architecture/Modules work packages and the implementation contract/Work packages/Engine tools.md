---
title: "Engine: tools"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: tools"
created: "2026-10-14"
modified: "2026-10-30"
---

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| [[GDT-1\|GDT-1]] | Spike: the [[Tools#RunicEditor\|RunicEditor]] executable on libgodot (editor target) opens the Godot editor with a test plugin; the editor target builds and opens without GDScript | The editor opens, loads the plugin and exits cleanly in CI; the spike’s findings decide the fallback | [[BUILD-1\|BUILD-1]] | [[Slice 00 Build skeleton\|0]] |
| [[GDT-2\|GDT-2]] | Project model: runic.project.json, the runic-mmo template, New and Open (per the open decision), loading and reloading the project’s editor library; IDE bridge (compile\_commands.json, go.work, VS Code tasks); first dock with world and ECS inspectors over a local simulation in the editor process | The editor opens a project and inspects entities of a local world; a rebuilt editor library reloads without restarting | [[GDT-1\|GDT-1]], [[APP-1\|APP-1]], [[SIM-2\|SIM-2]] | [[Slice 06 Editor shell\|6]] |
| [[GDT-3\|GDT-3]] | Physics inspector and the “see what the server sees” viewport layer | Bodies are selectable with their properties; cooked collision draws over the visual | [[GDT-2\|GDT-2]], [[PHYS-3\|PHYS-3]] | [[Slice 08 Physics view\|8]] |
| [[GDT-4\|GDT-4]] | [[Cooker\|Cooker]] integration: export plugin that calls the Cooker; collision presets in Godot’s import settings; RunicCollider3D; the collision naming convention for glTF | A Blender mesh imported by Godot cooks into collision and is walkable | [[GDT-2\|GDT-2]], [[COOK-1\|COOK-1]] | [[Slice 09 First cooker proof\|9]] |
| [[GDT-5\|GDT-5]] | Resolver debugger dock | It shows which rules applied to a hit and why | [[GDT-2\|GDT-2]], [[CMB-4\|CMB-4]] | [[Slice 17 Statuses and rules\|17]] |
| [[GDT-6\|GDT-6]] | Runic data in the editor: ResourceFormatLoader and ResourceFormatSaver for Runic files, inspectors and validation generated from schemas, live reload into a running server, background cooking with progress | A skill edited in the inspector reloads in the running server; a long cook never freezes the editor | [[GDT-2\|GDT-2]], [[CNT-2\|CNT-2]], [[COOK-2\|COOK-2]] | [[Slice 20 Data-driven content\|20]] |
| [[GDT-7\|GDT-7]] | Marker nodes and world cooking from scenes: RunicVolume3D, RunicSpawnArea3D, RunicInteractable3D, RunicRoute3D, RunicCollider3D; incremental cooking of the touched cells; spawn-area preview of candidate points | A region scene with a cave volume and a spawn area cooks into cells; moving a rock re-cooks only its cells | [[GDT-4\|GDT-4]], [[COOK-3\|COOK-3]] | [[Slice 21 World partitions\|21]] |
| [[GDT-8\|GDT-8]] | Region tools: World.tscn with RunicRegion3D proxies, New region from layout, read-only neighbor proxies with a border band, 64-bit region origins | Opening a 100 km² world loads only proxies; a region opens with its neighbors as proxies | [[GDT-7\|GDT-7]] | [[Slice 21 World partitions\|21]] |
| [[GDT-9\|GDT-9]] | Run orchestration: compile what changed, cook, start the local server and one or more development clients with a development ticket; development checkpoint on stop | Run from the editor starts a server and two clients connected as test characters | [[GDT-2\|GDT-2]], [[NET-2\|NET-2]] | [[Slice 13 Replication\|13]] |
| [[GDT-10\|GDT-10]] | Assistants: New [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] system, New behavior, New quest condition or action, New AI node, New data type, New marker node, New Go service | Each assistant writes compiling files, registers them and opens them in the IDE | [[GDT-6\|GDT-6]] | [[Slice 20 Data-driven content\|20]] |
| [[GDT-11\|GDT-11]] | AI editor: behavior-tree canvas on GraphEdit, palette from the runtime registration, inspector, asset browser, XML save and load | A tree is edited, saved and reloaded | [[GDT-2\|GDT-2]], [[AI-2\|AI-2]] | [[Slice 35 AI editor\|35]] |
| [[GDT-12\|GDT-12]] | AI tools: NPC definition and personality editors, content-ID validation, live NPC debugger | A running NPC’s tree state is visible live | [[GDT-11\|GDT-11]], [[AI-5\|AI-5]] | [[Slice 35 AI editor\|35]] |
| [[GDT-13\|GDT-13]] | Live attach docks to development and staging servers | Entity inspector and debug shapes come from a remote server | [[GDT-2\|GDT-2]], [[NET-7\|NET-7]] | [[Slice 39 Operations\|39]] |
| [[GDT-14\|GDT-14]] | GDScript for editor tools: the module in the editor target, the export lock, the development-client check, Run-scene interception, script templates and the problems dock | A scripted node in a content scene fails export with a teaching message; an @tool script in Tools/ runs in the editor | [[GDT-7\|GDT-7]] | [[Slice 21 World partitions\|21]] |
| [[GDT-15\|GDT-15]] | Water and field authoring: RunicWaterBody3D on Path3D, flow profiles, current and wind map painting | A river drawn in a region cooks into fragments and its flow arrows match the cooked data | [[GDT-7\|GDT-7]], [[WATER-2\|WATER-2]] | [[Slice 40 Water bodies\|40]] |
| [[GDT-16\|GDT-16]] | Plugin compatibility: published extension API per build, install validator, runic.plugin.json, Cooker adapters for plugin formats | Defined when the expansion slices are planned | [[GDT-14\|GDT-14]] | [[Slice 44 Expansion\|44+]] |
| [[COOK-1\|COOK-1]] | First cooker proof: geometry read from a scene Godot imported (no second glTF importer) into [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] collision and a cell visual list | A Blender mesh renders through Godot and is walkable | [[ASSET-1\|ASSET-1]], [[PHYS-1\|PHYS-1]], [[GDT-1\|GDT-1]] | [[Slice 09 First cooker proof\|9]] |
| [[COOK-2\|COOK-2]] | Validation of data-driven definitions | Invalid definitions fail the cook with clear errors | [[CNT-2\|CNT-2]] | [[Slice 20 Data-driven content\|20]] |
| [[COOK-3\|COOK-3]] | World cooking from scenes: regions, sectors, sparse 3D cells, authored volumes, spawn areas, manifests, packages, Zstandard; client cell visual lists | Two region scenes and a cave volume cook into random-access packages | [[COOK-1\|COOK-1]], [[WORLD-2\|WORLD-2]] | [[Slice 21 World partitions\|21]] |
| [[COOK-4\|COOK-4]] | Client export: the .pck from Godot’s export (textures, LODs and materials as Godot imports them), presets that exclude Tools/ and scripts, with the client cook packages | A shipping client runs from the .pck and the client packages alone | [[COOK-1\|COOK-1]] | [[Slice 22 World rendering\|22]] |
| [[COOK-5\|COOK-5]] | Skinned meshes and animation clips (Runic clip data only if the animation decision needs it) | A rigged character and its clips cook | [[COOK-1\|COOK-1]] | [[Slice 23 Animated characters\|23]] |
| [[COOK-6\|COOK-6]] | Navigation tiles with Recast; candidate points for spawn areas checked against the navmesh | Tiles cook per cell; every candidate point is reachable | [[COOK-3\|COOK-3]] | [[Slice 31 Navigation and spawning\|31]] |
| [[COOK-7\|COOK-7]] | Water fragments and current fields | A river and an ocean field cook with their cells | [[COOK-3\|COOK-3]] | [[Slice 40 Water bodies\|40]] |
| [[COOK-8\|COOK-8]] | Incremental cooking at scale | Only changed inputs cook again across a continent | [[COOK-3\|COOK-3]] | [[Slice 44 Expansion\|44+]] |

---

↑ [[Work packages|Work packages]] · ← [[Engine presentation|Engine: presentation]] · [[Platform|Platform]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: tools · exported 2026-11-03
