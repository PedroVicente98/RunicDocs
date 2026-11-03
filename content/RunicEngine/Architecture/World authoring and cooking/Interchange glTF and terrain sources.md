---
title: "Interchange: glTF and terrain sources"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Interchange: glTF and terrain sources"
created: "2026-10-14"
modified: "2026-10-30"
---

glTF 2.0 and GLB are the mesh and scene interchange from Blender, imported by Godot. glTF is a source format, never the runtime world representation, and [[Cooker|the Cooker]] reads geometry from the scenes Godot imported instead of running a second importer.

```text
.blend -> .glb/.gltf + terrain sources -> Godot import -> scenes in the RunicEditor -> Cooker -> Runic packages
                                                                                    -> Godot export -> client .pck
```

Large terrain is never forced into one glTF triangle mesh. Heightfield-like land uses a terrain source (for example a high-precision height.exr plus biome, material and hole or cave masks), while cliffs, caves, arches, overhangs, buildings, ruins, bridges and floating islands stay general meshes.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Resources by spawn area decided|Resources by spawn area (decided)]] · [[Cooker|Cooker]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Interchange: glTF and terrain sources · exported 2026-11-03
