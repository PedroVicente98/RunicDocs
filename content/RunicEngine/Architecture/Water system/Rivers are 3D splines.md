---
title: "Rivers are 3D splines"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Rivers are 3D splines"
created: "2026-10-14"
modified: "2026-10-30"
---

A river surface descends continuously through world space; it is never a stack of horizontal planes. Each control point, or sampled distance along the spline, can define width, depth, flow speed, cross-section, bank metadata and rapids markers; [[Cooker|the Cooker]] turns them into an efficient sampled runtime form.

```cpp
struct RiverControlPoint {
    WorldPosition position;
    float width;
    float depth;
    float base_flow_speed;
    RiverPointFlags flags;
};

// Simplest flow: along the spline tangent at the authored speed.
Vec3 direction = Normalize(river.Centerline().TangentAt(s));
Vec3 flow      = direction * river.FlowSpeedAt(s);
```

Flow speed is an authored profile with an optional slope contribution. The Engine promises deterministic, understandable gameplay water, not exact hydrodynamics. Complex bodies use a cooked low-resolution vector field for bends, eddies, side currents, currents around islands, harbor circulation, rapids or magical flows — still a cheap interpolation at runtime.

---

↑ [[Water system|Water system (Engine)]] · ← [[Water bodies and routes|Water bodies and routes]] · [[Ocean currents|Ocean currents]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Rivers are 3D splines · exported 2026-11-03
