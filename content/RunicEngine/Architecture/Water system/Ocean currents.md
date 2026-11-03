---
title: "Ocean currents"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Ocean currents"
created: "2026-10-14"
modified: "2026-10-30"
---

* Each OceanWaterBody carries a cooked current field: a coarse vector grid (for example one vector per 512 m), interpolated at sample time. A 600 km² map needs about 2,300 vectors.

* Current fields are authored as painted vector layers or generated from coastlines and a prevailing direction, then cooked with the world.

* The Environment modulates them over time — tide phase, season, weather — with deterministic functions, so the same position and world time always give the same current everywhere.

* The same cooked field feeds nautical charts on the Game side.

---

↑ [[Water system|Water system (Engine)]] · ← [[Rivers are 3D splines|Rivers are 3D splines]] · [[Connections form a graph|Connections form a graph]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Ocean currents · exported 2026-11-03
