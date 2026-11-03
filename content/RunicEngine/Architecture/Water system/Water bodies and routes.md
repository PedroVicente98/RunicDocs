---
title: "Water bodies and routes"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Water bodies and routes"
created: "2026-10-14"
modified: "2026-10-30"
---

Every water body has a stable namespaced ID (game:great\_western\_ocean, game:aster\_river\_upper, game:aster\_river\_cave, game:deepwater\_sea). A WaterRoute groups the fragments of one logical waterway — the surface, cave and underground parts of the Aster River load independently but share game:aster\_river.

| Body type | Representation | Typical uses |
| :---- | :---- | :---- |
| PlanarWaterBody | Bounded polygon with a constant or offset surface height | Lakes, reservoirs, enclosed water, tests |
| OceanWaterBody | Very large bounded surface, a deterministic gameplay swell and a cooked current field | Seas and oceans, including underground oceans |
| SplineRiverBody | 3D centerline spline with width, depth and flow profiles | Rivers, canals, cave rivers, descending waterways |
| FlowVolume | 3D volume with a directional or vector flow field | Waterfalls, rapids, spillways, whirlpools, underwater current tunnels |

---

↑ [[Water system|Water system (Engine)]] · ← [[Core model water reports facts|Core model: water reports facts]] · [[Rivers are 3D splines|Rivers are 3D splines]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Water bodies and routes · exported 2026-11-03
