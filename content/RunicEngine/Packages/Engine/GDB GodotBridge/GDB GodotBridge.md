---
title: "GDB · GodotBridge"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
created: "2026-11-03"
modified: "2026-11-03"
---

Module **GDB** ([[How the Engine uses Godot|GodotBridge]]) in Engine.

| ID | Package | Needs | Slice |
| :---- | :---- | :---- | :---- |
| [[GDB-1\|GDB-1]] | GodotLayer | [[APP-1\|APP-1]], [[BUILD-1\|BUILD-1]] | [[Slice 01 Application and layers\|1]] |
| [[GDB-2\|GDB-2]] | Debug drawing on Godot | [[GDB-1\|GDB-1]] | [[Slice 02 Debug drawing\|2]] |
| [[GDB-3\|GDB-3]] | Presenter | [[GDB-2\|GDB-2]], [[CORE-3\|CORE-3]] | [[Slice 05 Moving entities\|5]] |
| [[GDB-4\|GDB-4]] | Physics geometry layer | [[GDB-3\|GDB-3]], [[PHYS-3\|PHYS-3]] | [[Slice 08 Physics view\|8]] |
| [[GDB-5\|GDB-5]] | Mesh instances from cooked cells and entities, repeated meshes… | [[GDB-3\|GDB-3]], [[CLI-4\|CLI-4]] | [[Slice 22 World rendering\|22]] |
| [[GDB-6\|GDB-6]] | Skinned instances | [[GDB-5\|GDB-5]], [[CLI-5\|CLI-5]] | [[Slice 23 Animated characters\|23]] |
| [[GDB-7\|GDB-7]] | Lights, environment and volumes as Godot lights, environment… | [[GDB-5\|GDB-5]], [[CLI-7\|CLI-7]] | [[Slice 25a Night on screen\|25a]] |
| [[GDB-8\|GDB-8]] | Water surfaces and field grids | [[GDB-5\|GDB-5]], [[CLI-8\|CLI-8]] | [[Slice 42a Water and currents on screen\|42a]] |
| [[GDB-9\|GDB-9]] | UI bridge | [[GDB-1\|GDB-1]], [[CORE-3\|CORE-3]] | [[Slice 19 Combat prototype\|19]] |
| [[GDB-10\|GDB-10]] | World UI | [[GDB-9\|GDB-9]], [[CLI-6\|CLI-6]] | [[Slice 23a World UI\|23a]] |
| [[GDB-11\|GDB-11]] | Batched world UI and mode fallbacks | [[GDB-10\|GDB-10]] | [[Slice 38 Battle scale\|38]] |
| [[GDB-12\|GDB-12]] | Audio backend | [[GDB-1\|GDB-1]], [[AUD-1\|AUD-1]] | [[Slice 24 Sound and music\|24]] |
| [[GDB-13\|GDB-13]] | Production look | [[GDB-5\|GDB-5]] | [[Slice 44 Expansion\|44+]] |

---

↑ [[Packages|Work Packages]]
