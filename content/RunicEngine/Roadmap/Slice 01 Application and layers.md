---
title: "Slice 1 · Application and layers"
aliases:
  - "Slice 1"
tags:
  - "runicengine"
  - "slice"
  - "repo/engine"
  - "repo/game"
slice: "1"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Runnable result:** A Godot window opens from the client; layers push, pop and replace at safe points; events stop when handled

**Proves:** Entry point, ApplicationHost with RunFrame, [[Application and LayerStack|LayerStack]], GodotLayer

**Packages:** [[CORE-1|CORE-1]], [[APP-1|APP-1]], [[GDB-1|GDB-1]], [[GAME-0|GAME-0]]

**Owner:** Engine, Game

**Godot:** GodotLayer on top of the client stack; the window comes from Godot

**Packages first needed here:** [[CORE-1|CORE-1]], [[APP-1|APP-1]], [[GDB-1|GDB-1]], [[GAME-0|GAME-0]]

**Defined in:** [[Vertical-slice roadmap|Technical Architecture v4 › Vertical-slice roadmap]]

---

↑ [[Roadmap|Roadmap]] · ← [[Slice 00 Build skeleton|Slice 0 · Build skeleton]] · [[Slice 02 Debug drawing|Slice 2 · Debug drawing]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
