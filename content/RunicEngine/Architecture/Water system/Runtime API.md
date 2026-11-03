---
title: "Runtime API"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Runtime API"
created: "2026-10-14"
modified: "2026-10-30"
---

```cpp
// Illustrative contract, not a frozen API.
class WaterSystem {
public:
    bool TrySample(const WorldPosition& position, WaterSample& out) const;
    bool TrySample(const WorldPosition& position, WaterQueryContext& context,
                   WaterSample& out) const;          // cached locality

    void QueryBodies(const WorldBounds& bounds,
                     SmallVector<WaterBodyId, 8>& out) const;

    void RegisterFragment(const CookedWaterFragment& fragment);
    void UnregisterFragment(WaterFragmentId fragment);
};

struct WaterQueryContext {
    WaterBodyId     previous_body     = InvalidWaterBody;
    WaterFragmentId previous_fragment = InvalidWaterFragment;
};
```

* **Lookup path:** world position, then Sector, 3D Cell, the cell’s candidate water fragments, then the precise sample. The [[Core model water reports facts|WaterSystem]] never scans every river in the world.

* **Cached locality:** moving entities usually stay in the same fragment, so the context tests the previous fragment before any broader cell lookup.

* **Thread safety:** sampling is read-only and safe from any worker in a parallel phase; fragment registration happens only at streaming safe points.

---

↑ [[Water system|Water system (Engine)]] · ← [[Connections form a graph|Connections form a graph]] · [[Buoyancy and movement are separate components|Buoyancy and movement are separate components]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Runtime API · exported 2026-11-03
