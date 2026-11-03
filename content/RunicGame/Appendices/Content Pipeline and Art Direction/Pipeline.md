---
title: "Pipeline"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Pipeline"
created: "2026-10-26"
modified: "2026-10-30"
---


## Sources and scripts

* **Decision.** Models are made by people. AI only writes Blender scripts that recreate a given model, so it can be imported into Blender and adjusted directly in the script.
* **Proposal.** Scripts suit models built from primitives and modifiers (weapons, masts, planks, crates, rocks, walls): 50 to 300 lines with readable parameters. For detailed meshes (bodies, detailed armor, faces), a 1:1 script is the mesh data written as Python numbers. A 20k-triangle model becomes 2 to 4 MB of code against about 0.7 MB of glTF, it must also carry UVs, weights and shape keys, and nobody edits it by hand. Those models stay as .blend or glTF files, and scripts store the operations applied on top: morphs, scaling, attaching parts, LODs and export.
* **Proposal.** Variants are recipes: a small JSON file per variant with the base model, morph values, parts, materials and colors. Headless Blender (blender -b -P build.py) rebuilds every variant from its recipe, so a change to a base updates all of its variants.

## Build flow

**Proposal.** Base .blend files and recipes, then the headless Blender build, then the validation script, then the glTF export. From glTF on, the flow is the one in [[Architecture|Architecture v4]]: Godot import (textures, LODs, materials), [[Tools#RunicEditor|RunicEditor]] scenes, [[Cooker|the Cooker]] for server and client packages, and Godot's export for the client .pck.

## Naming and attachment points

**Proposal.** Attachment points are Blender empties with fixed names, read by the Engine when it imports the asset:

| **Name** | **Used for** |
| :---- | :---- |
| socket_grip, socket_sheath, socket_tip | Weapons: hand, carry position, trails and effects |
| socket_back | Glider, wing or [[Trade packs and routes\|trade pack]] |
| socket_cannon_NN, socket_helm, socket_anchor, socket_mast_NN | Ship stations and masts |
| socket_fruit_NN | Fruit on tree canopies |

## Validation script

**Proposal.** Every export runs the checks below; an asset that fails does not go into the game.

* Triangle count against the budget of its category.
* Bone names against the shared skeleton of its family.
* Scale (1 unit is 1 m) and origin (feet at 0 for characters, grip for weapons).
* Material count and texture sizes.
* Required attachment points present.
* Hit markers against the weapon's timing profile.
* A license entry for every third-party source.

## Version control and licenses

* **Proposal.** Sources (.blend files, textures, recipes) live in Git LFS. Generated outputs are not committed; they are rebuilt from the recipes.
* **Proposal.** A license manifest records the source and license of every asset (CC0, Mixamo, own work, AI-assisted scripts). Because the Engine is distributed, its templates and samples contain only CC0 or own assets.

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Textures and materials|Textures and materials]] · [[Map authoring markers|Map authoring markers]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Pipeline · exported 2026-11-03
