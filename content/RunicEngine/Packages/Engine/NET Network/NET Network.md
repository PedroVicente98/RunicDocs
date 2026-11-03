---
title: "NET · Network"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
created: "2026-11-03"
modified: "2026-11-03"
---

Module **NET** (Network) in Engine.

| ID | Package | Needs | Slice |
| :---- | :---- | :---- | :---- |
| [[NET-1\|NET-1]] | Transport interface, tick-safe ingress and egress queues,… | [[SIM-1\|SIM-1]] | [[Slice 12 Transport\|12]] |
| [[NET-2\|NET-2]] | Snapshots | [[NET-1\|NET-1]], [[SIM-6\|SIM-6]] | [[Slice 13 Replication\|13]] |
| [[NET-3\|NET-3]] | Prediction and reconciliation | [[NET-2\|NET-2]], [[SIM-4\|SIM-4]] | [[Slice 14 Prediction\|14]] |
| [[NET-4\|NET-4]] | Interest | [[NET-2\|NET-2]], [[WORLD-2\|WORLD-2]], [[PRC-2\|PRC-2]] | [[Slice 25 Interest\|25]] |
| [[NET-5\|NET-5]] | Simulation links | [[NET-2\|NET-2]], [[DSIM-2\|DSIM-2]] | [[Slice 36 Multiple simulations\|36]] |
| [[NET-6\|NET-6]] | Parallel replication and the degradation order | [[NET-4\|NET-4]], [[SIM-3\|SIM-3]] | [[Slice 38 Battle scale\|38]] |
| [[NET-7\|NET-7]] | Diagnostics layer | [[NET-1\|NET-1]], [[CORE-2\|CORE-2]] | [[Slice 39 Operations\|39]] |
| [[NET-8\|NET-8]] | World transitions | [[NET-1\|NET-1]], [[SIM-5\|SIM-5]], [[PCS-1\|PCS-1]] | [[Slice 44 Expansion\|44+]] |
| [[NET-9\|NET-9]] | Client-integrity channel | — | [[Slice 44 Expansion\|44+]] |
| [[NET-10\|NET-10]] | Occlusion-aware interest | — | [[Slice 44 Expansion\|44+]] |

---

↑ [[Packages|Work Packages]]
