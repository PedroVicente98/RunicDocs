---
title: "Water system (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

Water is a queryable, streamed spatial field, not a global height plane: any position can be sampled for surface, depth, flow and submersion. Buoyancy and movement are separate components that consume those facts, so passive water costs nothing and only ships, swimmers and drifting objects pay.

The system covers oceans, lakes, rivers, canals, cave rivers, underground seas, rapids, waterfalls, currents, swimming characters, floating rigid bodies and watercraft. It deliberately avoids general fluid simulation and models only what gameplay needs: macro surface position, surface normal, depth, flow, submersion, connectivity and optional dynamic state.

## Contents

- [[Ownership (Water system)|Ownership]]
- [[Core model water reports facts|Core model: water reports facts]]
- [[Water bodies and routes|Water bodies and routes]]
- [[Rivers are 3D splines|Rivers are 3D splines]]
- [[Ocean currents|Ocean currents]]
- [[Connections form a graph|Connections form a graph]]
- [[Runtime API|Runtime API]]
- [[Buoyancy and movement are separate components|Buoyancy and movement are separate components]]
- [[Characters ships objects and bosses|Characters, ships, objects and bosses]]
- [[Boundaries with the rest of the Engine|Boundaries with the rest of the Engine]]
- [[Streaming caves and cross-simulation continuity|Streaming, caves and cross-simulation continuity]]
- [[Authoring and cooking|Authoring and cooking]]
- [[Performance|Performance]]
- [[Debugging and validation|Debugging and validation]]
- [[Implementation stages|Implementation stages]]

---

↑ [[Architecture|Technical Architecture v4]] · ← [[World space coordinates cells and activation|World space: coordinates, cells and activation (Engine)]] · [[Environment wind currents tides waves and weather|Environment: wind, currents, tides, waves and weather (Engine)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) · exported 2026-11-03
