---
title: "Performance and correctness"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine) › Performance and correctness"
created: "2026-10-14"
modified: "2026-10-30"
---

* **Segments are a budget.** A 32-segment circle is 32 lines (64 vertices); a three-circle sphere is 192 vertices. Global quality levels (8, 16, 24, 32 segments) and fewer segments for distant or tiny shapes keep thousands of shapes cheap.

* **A vertex budget per frame.** The debug layers cap the vertices they upload; dropped vertices are counted in development builds so a missing shape is explainable.

* **Threading.** Godot calls stay in the GodotLayer on Godot’s main thread. Simulation workers write debug commands into per-worker buffers merged at the barrier, matching the simulation’s model.

* **Render geometry is never collision truth.** Combat uses exact math and [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] queries; drawing samples that data for people.

* **Large coordinates.** Every conversion from 64-bit world positions to floats happens during extraction and in the presenter shift, before anything reaches Godot.

---

↑ [[Debug drawing|Debug drawing (Engine)]] · ← [[What to visualize|What to visualize]] · [[Implementation order and definition of done|Implementation order and definition of done]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) › Performance and correctness · exported 2026-11-03
