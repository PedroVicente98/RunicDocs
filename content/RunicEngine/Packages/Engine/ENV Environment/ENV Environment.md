---
title: "ENV · Environment"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
created: "2026-11-03"
modified: "2026-11-03"
---

Module **ENV** (Environment) in Engine.

| ID | Package | Needs | Slice |
| :---- | :---- | :---- | :---- |
| [[ENV-1\|ENV-1]] | Environment clock | [[SIM-1\|SIM-1]], [[WORLD-1\|WORLD-1]] | [[Slice 25 Interest\|25]] |
| [[ENV-2\|ENV-2]] | Deterministic wind field with a cyclic baseline routine | [[ENV-1\|ENV-1]] | [[Slice 42 Ships wind and currents\|42]] |
| [[ENV-3\|ENV-3]] | Current modulation over time | [[ENV-1\|ENV-1]], [[WATER-5\|WATER-5]] | [[Slice 42 Ships wind and currents\|42]] |
| [[ENV-4\|ENV-4]] | Tides and gameplay waves | [[ENV-1\|ENV-1]] | [[Slice 43 Tides waves and weather\|43]] |
| [[ENV-5\|ENV-5]] | Weather state and time-boxed overrides | [[ENV-1\|ENV-1]] | [[Slice 43 Tides waves and weather\|43]] |
| [[ENV-6\|ENV-6]] | World routines | [[ENV-1\|ENV-1]] | [[Slice 43a Living world\|43a]] |

---

↑ [[Packages|Work Packages]]
