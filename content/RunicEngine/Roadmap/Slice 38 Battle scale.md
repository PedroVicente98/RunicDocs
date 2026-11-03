---
title: "Slice 38 · Battle scale"
aliases:
  - "Slice 38"
tags:
  - "runicengine"
  - "slice"
  - "repo/engine"
slice: "38"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Runnable result:** 200, then 500 bots fighting in one region; nameplates fall back to the batched path

**Proves:** Parallel replication, budgets, degradation order, AI at scale, batched world UI in MultiMesh, [[Tools#Testing at scale|RunicBot]]

**Packages:** [[NET-6|NET-6]], [[AI-6|AI-6]], [[GDB-11|GDB-11]], [[CLI-9|CLI-9]]

**Owner:** Engine

**Godot:** Batched nameplates in MultiMesh; RunicBot for network load

**Packages first needed here:** [[AI-6|AI-6]], [[NET-6|NET-6]], [[CLI-9|CLI-9]], [[GDB-11|GDB-11]]

**Defined in:** [[Vertical-slice roadmap|Technical Architecture v4 › Vertical-slice roadmap]]

---

↑ [[Roadmap|Roadmap]] · ← [[Slice 37 Cross-border combat|Slice 37 · Cross-border combat]] · [[Slice 39 Operations|Slice 39 · Operations]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
