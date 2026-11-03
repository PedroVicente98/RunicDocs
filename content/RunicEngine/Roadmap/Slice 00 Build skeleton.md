---
title: "Slice 0 · Build skeleton"
aliases:
  - "Slice 0"
tags:
  - "runicengine"
  - "slice"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
slice: "0"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Runnable result:** Engine library plus empty GameClient, GameServer and [[Tools#RunicEditor|RunicEditor]] build in CI in all three repositories; libgodot builds in the editor and template targets; the client starts Godot headless and exits; the server links no graphics

**Proves:** CMake module helper, dependency and headless checks, test framework, Godot as a library

**Packages:** [[BUILD-1|BUILD-1]], [[GDT-1|GDT-1]]

**Owner:** Engine, Platform, Game

**Godot:** Godot and godot-cpp pinned; libgodot in both targets; spike: client starts Godot headless, RunicEditor opens with a test plugin

**Packages first needed here:** [[BUILD-1|BUILD-1]], [[GDT-1|GDT-1]]

**Defined in:** [[Vertical-slice roadmap|Technical Architecture v4 › Vertical-slice roadmap]]

---

↑ [[Roadmap|Roadmap]] · [[Slice 01 Application and layers|Slice 1 · Application and layers]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
