---
title: "PTR · Transport"
tags:
  - "runicengine"
  - "package"
  - "repo/platform"
created: "2026-11-03"
modified: "2026-11-03"
---

Module **PTR** (Transport) in Platform.

| ID | Package | Needs | Slice |
| :---- | :---- | :---- | :---- |
| [[PTR-1\|PTR-1]] | [[Networking stack sessions and responsiveness#Stack (decided)\|GameNetworkingSockets]] transport implementing the Engine… | [[NET-1\|NET-1]], [[PCT-1\|PCT-1]] | [[Slice 12 Transport\|12]] |
| [[PTR-2\|PTR-2]] | Connect-ticket verification inside the simulation | [[PTR-1\|PTR-1]] | [[Slice 12 Transport\|12]] |
| [[PTR-3\|PTR-3]] | Candidate connections | [[PTR-2\|PTR-2]], [[DSIM-3\|DSIM-3]] | [[Slice 36 Multiple simulations\|36]] |
| [[PTR-4\|PTR-4]] | Simulation links chosen by locality | [[PTR-3\|PTR-3]] | [[Slice 44 Expansion\|44+]] |

---

↑ [[Packages|Work Packages]]
