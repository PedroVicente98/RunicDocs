---
title: "Requirements by repository (Content Pipeline)"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Requirements by repository"
created: "2026-10-26"
modified: "2026-10-30"
---


## Engine

* Blender export helper grown into a game-agnostic build tool: recipe runner for headless Blender, validation with budgets read from project settings, attachment-point and collision naming, hit-marker export.
* Skinned characters ([[ANIM-1|ANIM-1]], [[COOK-5|COOK-5]], [[CLI-5|CLI-5]], [[GDB-6|GDB-6]]): one skeleton per creature family, twist and corrective bones computed at runtime, animation update rates by distance, attachment points for weapons, cloak and back slot.
* Presenter ([[GDB-5|GDB-5]]): MultiMesh with per-instance color and texture-layer data, one mesh per resource state, impostors for distant vegetation, merged meshes and small texture versions for distant characters.
* Production look ([[GDB-13|GDB-13]]): shader layers for weather and biome driven by environment data.
* Map marker import: painted layers, points, areas and paths cooked into volumes, routes and placed objects, with a validation step that lists missing or broken markers.
* Terrain hydrology at cook time: channels, height above the channel, low spots and slide paths, with editor views for the flood at monsoon and the slide paths.

## Game

* [[Art direction|Art direction]] and texture approach, locked after the side-by-side test.
* Two base bodies, three armor bases per body type, one base per weapon type, variant recipes and [[Characters|dye masks]].
* Creature families: humanoid (goblin) and quadruped (wolf) rigs and animations.
* Tree, rock and prop sets with their states; ship hulls, stations and masts.
* Swing animations per weapon timing profile, with hit markers.
* License manifest for every third-party asset.
* The map marker catalog (Map authoring markers), filled while authoring the map.

## Platform

* Nothing new.

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Vertical slice order|Vertical slice order]] · [[Open (Content Pipeline)|Open (Content Pipeline)]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Requirements by repository · exported 2026-11-03
