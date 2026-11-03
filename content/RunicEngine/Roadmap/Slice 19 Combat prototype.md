---
title: "Slice 19 · Combat prototype"
aliases:
  - "Slice 19"
tags:
  - "runicengine"
  - "slice"
  - "repo/engine"
  - "repo/game"
slice: "19"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Runnable result:** The full acceptance list below

**Proves:** Game systems end to end, threat and CC, input queue, first GameUI in Godot

**Packages:** [[CMB-6|CMB-6]], [[CMB-7|CMB-7]], [[GDB-9|GDB-9]], [[GCL-1|GCL-1]], [[GSH-5|GSH-5]]

**Owner:** Engine, Game

**Godot:** HUD as Godot UI scenes with the view-model binder

**Packages first needed here:** [[CMB-6|CMB-6]], [[CMB-7|CMB-7]], [[GDB-9|GDB-9]], [[GSH-5|GSH-5]], [[GCL-1|GCL-1]]

**Combat prototype acceptance list (slice 19):** two players and a dummy; one melee attack and one projectile; a dodge using one [[Defense Evasion Guard and armor#Evasion|Evasion]] charge; directional shield [[Defense Evasion Guard and armor#Guard|Guard]]; a full CC, Stagger and immunity chain; an AoE that proves damage falloff and the CC target cap; one skill interaction (a Stagger on an already staggered target becomes Trip); a FriendlyLock heal; a PvE taunt; a PvP Challenge; and [[Debug drawing|debug drawing]] of all of it.

**Defined in:** [[Vertical-slice roadmap|Technical Architecture v4 › Vertical-slice roadmap]]

---

↑ [[Roadmap|Roadmap]] · ← [[Slice 18 Defense|Slice 18 · Defense]] · [[Slice 20 Data-driven content|Slice 20 · Data-driven content]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
