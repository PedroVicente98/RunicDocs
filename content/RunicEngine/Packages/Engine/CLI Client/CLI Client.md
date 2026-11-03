---
title: "CLI · Client"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
---

Module **CLI** (Client) in Engine.

| ID | Package | Needs | Slice |
| :---- | :---- | :---- | :---- |
| [[CLI-1\|CLI-1]] | Presentation layer and extractor registry | [[ECS-1\|ECS-1]], [[GDB-2\|GDB-2]], [[CORE-3\|CORE-3]] | [[Slice 05 Moving entities\|5]] |
| [[CLI-2\|CLI-2]] | Input mapping, actions and command builder over the AppEvents… | [[GDB-1\|GDB-1]], [[SIM-2\|SIM-2]] | [[Slice 07 Physics\|7]] |
| [[CLI-3\|CLI-3]] | Prediction layer driving the prediction subset and… | [[SIM-4\|SIM-4]], [[NET-3\|NET-3]] | [[Slice 14 Prediction\|14]] |
| [[CLI-4\|CLI-4]] | Mesh-instance extractor with interpolation, camera-relative… | [[CLI-1\|CLI-1]], [[CORE-4\|CORE-4]] | [[Slice 22 World rendering\|22]] |
| [[CLI-5\|CLI-5]] | Skinned-instance extractor with poses or animation intent, per… | [[CLI-4\|CLI-4]], [[ANIM-1\|ANIM-1]] | [[Slice 23 Animated characters\|23]] |
| [[CLI-6\|CLI-6]] | World-anchor extractor | [[CLI-1\|CLI-1]], [[CORE-4\|CORE-4]] | [[Slice 23a World UI\|23a]] |
| [[CLI-7\|CLI-7]] | Light, environment and volume extractors from Perception and… | [[CLI-1\|CLI-1]], [[CORE-5\|CORE-5]], [[PRC-1\|PRC-1]] | [[Slice 25a Night on screen\|25a]] |
| [[CLI-8\|CLI-8]] | Water-surface and field-grid extractors from Water and… | [[CLI-1\|CLI-1]], [[CORE-6\|CORE-6]], [[WATER-5\|WATER-5]] | [[Slice 42a Water and currents on screen\|42a]] |
| [[CLI-9\|CLI-9]] | [[Tools#Testing at scale\|RunicBot]] | [[CLI-3\|CLI-3]], [[NET-4\|NET-4]] | [[Slice 38 Battle scale\|38]] |

---

↑ [[Packages|Work Packages]]
