---
title: "Textures and materials"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Textures and materials"
created: "2026-10-26"
modified: "2026-10-30"
---

* **Decision.** Textures are either procedural (ship wood, grass) or made by hand (items).
* **Decision.** Texture and asset quality is not a priority for the vertical slice.

|  | **Image texture** | **Procedural in the Godot shader** |
| :---- | :---- | :---- |
| Memory | 2K about 5.3 MB, 1K about 1.3 MB, 512 tiling about 0.35 MB | About 0 MB, only parameters |
| GPU work | A cheap hardware texture read per pixel | Math for every pixel, every frame: each noise layer is about 50 operations, so 4 layers are about 200 |
| At a distance | Mipmaps handle it | Shimmers unless fine detail fades out with distance |
| Variation | Fixed; repetition shows on large surfaces | Unlimited: changes with world position and live parameters |
| Ease of replicating | Hand-painted images cannot be regenerated; variety through masks and tints | Code in the repository with per-object parameters, but no files: it exists only while the game runs |

Four noise layers over half of a 1080p screen are about 300M operations per frame, a fraction of a percent of a mid-range GPU. The cost scales with pixels (4× at 4K) and with the number of such materials on screen.

* **Proposal.** Blender's procedural materials do not run in Godot, so they are always baked into images. A node graph plus a seed is a recipe: change a parameter and the pipeline re-bakes every variant (apple and cherry, oak and pine, new and old wood). The same look at runtime needs a Godot shader rewrite.
* **Proposal.** Characters, armor, weapons and items: unique image textures, baked or painted, with [[Characters|dye masks]].
* **Proposal.** Ship wood, stone, grass and terrain: small tiling images (512 to 1K) reused across thousands of objects, with runtime variation by world position (tint, wear).
* **Proposal.** Weather and biome layers (snow, wetness, moss, autumn): procedural in the Godot shader, driven by node climate.

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Ships (Content Pipeline)|Ships (Content Pipeline)]] · [[Pipeline|Pipeline]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Textures and materials · exported 2026-11-03
