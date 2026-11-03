---
title: "Debugging and validation"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Debugging and validation"
created: "2026-10-14"
modified: "2026-10-30"
---

* **Debug drawing:** body bounds and loaded fragments; river centerlines and sampled surface points; width and depth cross sections; flow arrows, vector-field cells and FlowVolumes; the connection graph and navigation rules; buoyancy points, submersion and applied forces; each character’s WaterInteractionState and body; cell and simulation ownership at fragment boundaries; query counts, cache hit rate and active consumers.

* **[[Cooker|Cooker]] validation:** zero or negative width, invalid depth, unintended spline self-intersection, large elevation jumps in a Smooth connection, missing or dangling connection references, neighbor boundary mismatches, a waterfall modeled as a smooth navigable surface without a FlowVolume, invalid route topology, duplicate IDs.

* **Extension points stay small:** planar, ocean, spline river, flow volume, BuoyantBody and the three movement components. New provider interfaces are added only when a real feature needs them.

---

↑ [[Water system|Water system (Engine)]] · ← [[Performance|Performance]] · [[Implementation stages|Implementation stages]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Debugging and validation · exported 2026-11-03
