---
title: "Authoring work per roadmap slice"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Authoring work per roadmap slice"
created: "2026-10-14"
modified: "2026-10-30"
---

The pipeline grows inside the vertical-slice roadmap; gameplay never stops for a long “build the whole editor and cooker” phase.

| Roadmap slice | World and asset work |
| :---- | :---- |
| 0\. Build skeleton | libgodot in both targets; the [[Tools#RunicEditor\|RunicEditor]] spike; [[Cooker\|Cooker]] target and module boundaries; no production cooking yet |
| 6\. Editor shell | The RunicEditor opens the RunicGame project; project template and layout |
| 9\. First cooker proof | Blender to GLB, imported by Godot, collision cooked by the Runic Cooker; walk on it |
| 13\. Replication | The Run button feeds the client and the headless server the same cooked data |
| 15–19. Combat | Only the collision and metadata real combat obstacles and queries need |
| 20\. Data-driven content | Runic data files in the editor through schemas, stable asset IDs, live reload |
| 21\. World partitions | Major milestone: World.tscn and region scenes, marker nodes, region, sector, 3D cell, volume and spawn-area cooking, activation-volume streaming, [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] cell collision, manifests, the server view layer; GDScript enabled for editor tools |
| 22\. World rendering | Godot import settings and the client .pck export |
| 23\. Animated characters | Skinned meshes and clips imported by Godot |
| 25\. Interest | Network relevance uses the same spatial vocabulary without coupling replication to presentation |
| 28–30. Persistence, sequences and quests | Persistent world-object IDs and authored gameplay markers in cooked regions |
| 31\. Navigation and spawning | Recast cooking, Detour runtime, spawn-area candidate points checked against the navmesh |
| 36\. Multiple simulations | Packages stay unchanged while different simulations own adjacent space and players transfer |
| 40–43. Water and environment | Water bodies, river curves, current and wind maps authored in the editor |
| 44+. Production world | HLOD, advanced terrain materials, light baking and probes, incremental cooking at scale, large-world validation, plugin compatibility |

**First cooker proof:** test\_region.glb imported by Godot into a test scene, its collision cooked into test.jolt and its placement into a test cell; the client draws the mesh through Godot, client and server collision work, and a character walks on it. Recast, HLOD, terrain splatmaps, world manifests, spawn areas, compression and region tools all wait until after this proof — complexity is earned one slice at a time.

**Graphics quality grows independently.** The full MMO architecture can run on programmer art and Godot’s default materials. Textured meshes, PBR materials, shadows, terrain shaders, sky, fog and water rendering, vegetation, baked lighting, post-processing and polish mature without redesigning the world-file architecture: the pipeline provides data, Godot decides final quality.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Cooked world files and packages|Cooked world files and packages]] · [[Project layout and schemas|Project layout and schemas]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Authoring work per roadmap slice · exported 2026-11-03
