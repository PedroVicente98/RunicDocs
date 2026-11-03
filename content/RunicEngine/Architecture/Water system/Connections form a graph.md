---
title: "Connections form a graph"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Connections form a graph"
created: "2026-10-14"
modified: "2026-10-30"
---

Water bodies link into a graph. One route can run from a mountain lake through the upper river, rapids and the lower river (with a side canal), into a cave river, a deep river and finally an underground sea.

| Connection | Meaning | Navigation example |
| :---- | :---- | :---- |
| Smooth | Continuous surface and flow blend | Ordinary river segments |
| Estuary | River-to-lake or river-to-ocean blend | Current fades into the sea |
| Rapids | Navigable, high flow and turbulence | Fast downstream passage |
| Waterfall | Surface discontinuity plus a downward FlowVolume | Often downstream-only or non-navigable |
| Canal | Authored controlled connection | Artificial waterway |
| Lock | Stateful controlled elevation change | Later feature |
| Custom | Game policy on Engine connection data | Special world mechanics |

* **Smooth transitions** blend surface position, normal, flow and presentation parameters across a transition region, so a vessel never hits a physics discontinuity where one body ends and another begins.

* **Waterfalls** are a FlowVolume between the upper and lower surfaces; the Game’s navigation policy marks them navigable, downstream-only, restricted or non-navigable.

* **Rapids** stay a continuous sloped surface with stronger flow and optional vector-field turbulence.

---

↑ [[Water system|Water system (Engine)]] · ← [[Ocean currents|Ocean currents]] · [[Runtime API|Runtime API]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Connections form a graph · exported 2026-11-03
