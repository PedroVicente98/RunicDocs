---
title: "Seamless terrain and borders"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game) › Seamless terrain and borders"
created: "2026-10-14"
modified: "2026-10-30"
---

* **One continuous terrain truth.** Region terrain derives from one canonical continuous source or canonical shared edge samples; neighboring artists never invent the same border twice.

* **Canonical sample grid.** For large natural terrain, canonical height samples are the truth rather than one arbitrary mesh. Regions own ranges of the global grid and share border samples exactly: if region A covers X 0 to 1024 and region B covers 1024 to 2048, both read the same sample at X \= 1024\. Artists sculpt in Blender or a terrain tool; import samples the result into the grid.

* **Aprons.** Each region and cell cooks slightly past its official boundary so derived data sees neighbor context; a border that matches positions but not normals, masks or LODs still shows a seam.

Aprons keep these continuous across a boundary:

* Geometry and height.

* Normals and tangents.

* Terrain material and biome masks.

* River and road splines.

* LOD and HLOD edges.

* Collision.

* Navmesh boundaries.

* Vegetation distribution, wetness and shoreline masks.

* Lighting and probe data where relevant.

**Region borders are technically boring:** crossing one never implies a terrain, renderer, physics or navmesh seam, a server boundary or a loading screen. Streaming and ownership are separate concerns.

---

↑ [[World authoring and cooking|World authoring and cooking (Engine, Game)]] · ← [[Large worlds in the editor|Large worlds in the editor]] · [[Marker nodes and what they cook into|Marker nodes and what they cook into]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) › Seamless terrain and borders · exported 2026-11-03
