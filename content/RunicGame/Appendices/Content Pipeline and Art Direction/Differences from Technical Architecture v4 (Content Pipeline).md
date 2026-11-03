---
title: "Differences from Technical Architecture v4 (Content Pipeline)"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Differences from Technical Architecture v4"
created: "2026-10-26"
modified: "2026-10-30"
---

| **Architecture section** | **What the Architecture says today** | **What this appendix changes** |
| :---- | :---- | :---- |
| World authoring and cooking › Godot and Blender | Blender makes assets and glTF is the border. Godot imports textures, LODs and materials; final materials and shaders live in Godot | Unchanged. Added on the Blender side: recipes, headless batch builds and a validation script that runs before the glTF export (Proposal) |
| World authoring and cooking › Ownership: Blender export helper | Optional Engine tool for collision and LOD naming conventions and glTF export presets | Grows into the build pipeline: recipe runner, attachment-point naming, budget validation and hit-marker export (Proposal). It stays game-agnostic; budgets and recipes are project data |
| Resources by spawn area › apple_tree example | Each state shows or hides parts of one mesh (show: [trunk, leaves, apples]) | Each state points at its own pre-merged mesh, built by the pipeline from the modular parts, so a tree draws as one mesh instead of three or four (Proposal) |
| Decorative vegetation; presenter ([[GDB-5\|GDB-5]]) | Decorative vegetation in MultiMesh; repeated static meshes of a cell in one MultiMesh | Unchanged, plus per-instance color and texture-layer data for species variants, and impostors for distant trees (Proposal). HLOD stays at slice [[Slice 44 Expansion\|44+]] |
| Godot integration › Open decisions, item 3 (client animation) | (A) the Runic evaluator with poses sent to RenderingServer skeletons, or (B) Godot's AnimationTree driven by the animation intent | Not decided here. The crowd budget below needs update rates per distance and twist bones computed in code. Both are direct in option A and need checking in option B |
| Render data › Debug layers first, the Godot look later | Production look ([[GDB-13\|GDB-13]]) from slice [[Slice 44 Expansion\|44]] | The proposed texture approach works with Godot's standard PBR material, so assets made before [[GDB-13\|GDB-13]] need no rework. Weather and biome shader layers wait for [[GDB-13\|GDB-13]] |
| Principles and performance targets › Targets | 100 vs 100 must feel perfect; 500 players in one region must still work | Character budgets below are derived from these targets |
| Client runtime › Animation | The server never evaluates animation; gameplay timing comes from ability timelines | Unchanged. The pipeline exports each clip's hit marker and checks it against the timeline (Proposal) |

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Differences from the Vision (Content Pipeline)|Differences from the Vision (Content Pipeline)]] · [[Related entries in Ideias|Related entries in Ideias]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Differences from Technical Architecture v4 · exported 2026-11-03
