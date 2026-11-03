---
title: "WATER · Water"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
---

Module **WATER** (Water) in Engine.

| ID | Package | Needs | Slice |
| :---- | :---- | :---- | :---- |
| [[WATER-1\|WATER-1]] | [[Core model water reports facts\|WaterSystem]] registry, planar water, WaterSample, cell fragments | [[WORLD-3\|WORLD-3]], [[PHYS-1\|PHYS-1]] | [[Slice 40 Water bodies\|40]] |
| [[WATER-2\|WATER-2]] | Spline rivers, flow, connections and routes | [[WATER-1\|WATER-1]] | [[Slice 40 Water bodies\|40]] |
| [[WATER-3\|WATER-3]] | BuoyantBody on [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] bodies, with an optional righting strength | [[WATER-1\|WATER-1]] | [[Slice 41 Floating and swimming\|41]] |
| [[WATER-4\|WATER-4]] | Character and object water movement | [[WATER-3\|WATER-3]], [[GPL-1\|GPL-1]] | [[Slice 41 Floating and swimming\|41]] |
| [[WATER-5\|WATER-5]] | Ocean current fields from cooked vector grids | [[WATER-1\|WATER-1]] | [[Slice 42 Ships wind and currents\|42]] |
| [[WATER-6\|WATER-6]] | WatercraftMovement | [[WATER-4\|WATER-4]], [[ENV-2\|ENV-2]] | [[Slice 42 Ships wind and currents\|42]] |
| [[WATER-7\|WATER-7]] | Ship-group [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] | [[WATER-6\|WATER-6]], [[DSIM-3\|DSIM-3]] | [[Slice 42b Ships across borders\|42b]] |

---

↑ [[Packages|Work Packages]]
