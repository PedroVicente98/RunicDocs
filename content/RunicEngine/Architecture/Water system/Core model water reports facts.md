---
title: "Core model: water reports facts"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Core model: water reports facts"
created: "2026-10-14"
modified: "2026-10-30"
---

```cpp
// Illustrative contract, not a frozen API.
struct WaterSample {
    bool         valid = false;
    WaterBodyId  body  = InvalidWaterBody;

    WorldPosition surface_position;  // 64-bit world position
    Vec3  surface_normal {0, 1, 0};
    Vec3  flow_velocity {0, 0, 0};   // world space; includes current modulation

    float depth      = 0.0f;
    float submersion = 0.0f;
    WaterFlags flags {};
};

WaterSample sample;
if (water.TrySample(position, sample)) { /* ocean, lake, river or flow volume */ }
```

* The caller never needs to know which kind of water body answered.

* The WaterSystem reports facts; it never decides an entity’s response. Each movement component consumes the same sample in its own way.

* The server samples the macro gameplay surface. Godot on the client adds ripples, foam, displacement, spray, reflections, refraction, wakes and visual waves on top without the server simulating them.

* The sample already includes the environment’s contribution (tide level, time-varying current and, on oceans, gameplay swell and wave events), so consumers never query the environment separately for water.

**Non-goals:** no Navier-Stokes grid, no SPH or per-particle server simulation, no pressure, erosion or real-time river formation, no centimeter agreement between shader waves and gameplay water, and no assumption that water is horizontal.

---

↑ [[Water system|Water system (Engine)]] · ← [[Ownership (Water system)|Ownership (Water system)]] · [[Water bodies and routes|Water bodies and routes]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Core model: water reports facts · exported 2026-11-03
