---
title: "SIM · Simulation"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
---

Module **SIM** (Simulation) in Engine.

| ID | Package | Needs | Slice |
| :---- | :---- | :---- | :---- |
| [[SIM-1\|SIM-1]] | SimulationRuntime | [[APP-1\|APP-1]], [[CORE-2\|CORE-2]] | [[Slice 03 Fixed-step clock\|3]] |
| [[SIM-2\|SIM-2]] | Phases, commands and command queue, deferred mutation, event… | [[SIM-1\|SIM-1]], [[ECS-1\|ECS-1]], [[EVT-1\|EVT-1]] | [[Slice 05 Moving entities\|5]] |
| [[SIM-3\|SIM-3]] | Phases on the worker pool, per-worker buffers, deterministic… | [[SIM-2\|SIM-2]], [[PHYS-4\|PHYS-4]] | [[Slice 10 Worker pool\|10]] |
| [[SIM-4\|SIM-4]] | Client prediction subset | [[SIM-3\|SIM-3]] | [[Slice 14 Prediction\|14]] |
| [[SIM-5\|SIM-5]] | Service port | [[SIM-2\|SIM-2]], [[EVT-1\|EVT-1]] | [[Slice 27 Accounts and characters\|27]] |
| [[SIM-6\|SIM-6]] | Replication registry | [[SIM-2\|SIM-2]] | [[Slice 13 Replication\|13]] |
| [[SIM-7\|SIM-7]] | Behavior counters | — | [[Slice 39 Operations\|39]] |

---

↑ [[Packages|Work Packages]]
