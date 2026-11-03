---
title: "Drawing DebugGeometry with Godot"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine) › Drawing DebugGeometry with Godot"
created: "2026-10-14"
modified: "2026-10-30"
---

[[How the Engine uses Godot|GodotBridge]] keeps one mesh per batch in the RenderingServer and rebuilds it each frame from the DebugGeometry; lines use a line primitive, filled shapes a triangle primitive, and text becomes Label3D instances from a small pool.

```cpp
// Illustrative: GodotBridge debug layer, on Godot's main thread
void DebugLayers::Upload(const DebugGeometry& g, Vec3 presenterShift) {
    auto* rs = godot::RenderingServer::get_singleton();
    rs->mesh_clear(m_LinesMesh);
    if (g.lines.empty()) return;

    godot::Array arrays;
    arrays.resize(godot::RenderingServer::ARRAY_MAX);
    arrays[godot::RenderingServer::ARRAY_VERTEX] = ToPackedVector3(g.lines, presenterShift);
    arrays[godot::RenderingServer::ARRAY_COLOR]  = ToPackedColor(g.lines);
    rs->mesh_add_surface_from_arrays(m_LinesMesh, godot::RenderingServer::PRIMITIVE_LINES, arrays);
    rs->mesh_surface_set_material(m_LinesMesh, 0, m_DepthTestedMaterial);   // the Overlay batch uses a no-depth material
}
```

The materials are unshaded and take their color from the vertex color, one with depth testing and one without, so the two batches of v3 keep their meaning. Native lines are one pixel wide; thick or stylized lines become camera-facing quads in the triangle batch.

---

↑ [[Debug drawing|Debug drawing (Engine)]] · ← [[Shapes|Shapes]] · [[Physics debug view Physics extracts GodotBridge draws|Physics debug view (Physics extracts, GodotBridge draws)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) › Drawing DebugGeometry with Godot · exported 2026-11-03
