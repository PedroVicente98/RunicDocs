---
title: "Environment"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Environment"
created: "2026-10-26"
modified: "2026-10-30"
---

* **Decision.** Modular objects and sets of trees, rocks and props that change per biome and type. Species share a model with different textures and colors (apple and cherry). Trees are made of 3 or 4 parts (roots, trunk, canopy and leaves) that combine into different types and states.
* **Proposal.** Modular for authoring, merged for runtime: the pipeline combines the parts into finished meshes per type and state (full, harvested, stump, cut), so each tree draws as one mesh.
* **Proposal.** Decorative trees and rocks use MultiMesh, and species differ by per-instance color and texture-layer data instead of separate materials.
* **Proposal.** Distant trees become impostors, flat two-triangle images of the tree. Godot has no built-in impostors, so this is an Engine task or a plugin.
* **Proposal.** Biome variation (snow on upward faces, autumn color, dryness, wetness) comes from shader parameters driven by each node's climate, with no new models or textures.
* **Proposal.** Rocks, crates, planks and modular walls are good candidates for parametric generators.

Example with 2,000 trees on screen: as four separate parts with no instancing, about 8,000 draw calls and about 10M triangles. Merged, instanced and with LODs (100 near at 5k, 400 mid at 1k, 1,500 far as impostors), about 0.9M triangles and a few dozen draw calls.

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Mobs|Mobs]] · [[Ships (Content Pipeline)|Ships (Content Pipeline)]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Environment · exported 2026-11-03
