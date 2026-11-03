---
title: "Streaming, caves and cross-simulation continuity"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Streaming, caves and cross-simulation continuity"
created: "2026-10-14"
modified: "2026-10-30"
---

* **Fragments follow cells:** World, Region, Sector, Cell, then the cell’s cooked water fragments. A simulation loads only the fragments of its own space; a 50 km river is never resident everywhere.

* **Rivers enter caves without instances:** a surface river enters a cave volume and becomes an underground river that reaches an underground ocean, as one logical route with no teleport or loading screen.

* **Seams:** [[Cooker|the Cooker]] emits fragments with boundary aprons from the same source spline, so position, width, depth, tangent, normal and flow agree across region and cell boundaries.

* **Cross-simulation ships:** water is static data, not transferred in a [[Networking replication interest and handoff#Simulations, handoff and ghosts|handoff]]. Neighbor simulations load matching fragments, and the ship moves with the make-before-break protocol, prepared before authority commits.

* **Open ocean** is analytic inside the OceanWaterBody’s bounds; only coastlines, current fields and special areas are cooked, so huge seas cost almost no storage.

---

↑ [[Water system|Water system (Engine)]] · ← [[Boundaries with the rest of the Engine|Boundaries with the rest of the Engine]] · [[Authoring and cooking|Authoring and cooking]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Streaming, caves and cross-simulation continuity · exported 2026-11-03
