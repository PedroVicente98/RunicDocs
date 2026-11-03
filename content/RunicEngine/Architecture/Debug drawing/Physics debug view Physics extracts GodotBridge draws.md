---
title: "Physics debug view (Physics extracts, GodotBridge draws)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine) › Physics debug view (Physics extracts, GodotBridge draws)"
created: "2026-10-14"
modified: "2026-10-30"
---

[[Simulation core Flecs and Jolt#Jolt rules|Jolt]] and Godot never know about each other, and Runic::Physics and Runic::[[How the Engine uses Godot|GodotBridge]] never link each other. Physics fills plain debug-geometry buffers defined in Core; a GodotBridge debug layer draws those buffers like any other debug geometry. There are two paths.

**Path A — draw the shapes the Engine already knows.** The simulation knows a player is a capsule, a trigger is a box and a ship has a hull proxy; read the dimensions from the physics-facing component and call the matching primitive. The debug-draw API receives plain vectors and dimensions, never JPH::Body, JPH::Shape, BodyID or physics pointers. This is the default for gameplay work.

```cpp
void DrawCharacterCollider(DebugDraw& draw, const CharacterPhysics& physics) {
    draw.DrawCapsule(physics.lowerCapCenter, physics.upperCapCenter, physics.radius,
                         PackABGR(80, 220, 120));
}

void DrawBroadphaseBounds(DebugDraw& draw, const Bounds& bounds) {
    draw.DrawAABB(bounds.min, bounds.max, PackABGR(90, 150, 255));
}
```

**Path B — Jolt’s own debug interface,** for Jolt’s internal body and constraint visualization. Jolt calls an application-supplied DebugRenderer. In RunicEngine that adapter lives inside Runic::Physics (Source/Jolt) and writes lines and triangles into a Core DebugGeometry buffer in camera-relative floats; PhysicsSystem::DrawBodies drives it. Jolt shapes can also draw themselves this way, which helps inspect mesh, compound and convex geometry without teaching GodotBridge any Jolt shape type.

```cpp
// Runic::Physics, Source/Jolt (development builds only)
class JoltDebugExtractor final : public JPH::DebugRendererSimple {
public:
    explicit JoltDebugExtractor(DebugGeometry& out) : m_out(out) {}

    void DrawLine(JPH::RVec3Arg from, JPH::RVec3Arg to, JPH::ColorArg color) override {
        m_out.AddLine(ToCameraRelative(from), ToCameraRelative(to), ToABGR(color));
    }
    void DrawTriangle(JPH::RVec3Arg a, JPH::RVec3Arg b, JPH::RVec3Arg c,
                      JPH::ColorArg color, ECastShadow) override {
        DrawLine(a, b, color); DrawLine(b, c, color); DrawLine(c, a, color);   // wireframe first
    }
    void DrawText3D(JPH::RVec3Arg, const JPH::string_view&, JPH::ColorArg, float) override {
        // Optional; later exported as debug text.
    }
private:
    DebugGeometry& m_out;   // plain Core type: lines and triangles, no Godot
};

// Physics public API, no Jolt types:
physicsWorld.ExtractDebugGeometry(cameraOrigin, settings, debugGeometry);

// GodotBridge physics layer, on Godot's main thread:
debugLayers.Upload(debugGeometry, presenterShift);
```

Keep Path B development-only: normal gameplay rendering never depends on JPH\_DEBUG\_RENDERER. Because Jolt runs in double precision, ToCameraRelative subtracts the render origin from each JPH::RVec3 before converting to floats.

---

↑ [[Debug drawing|Debug drawing (Engine)]] · ← [[Drawing DebugGeometry with Godot|Drawing DebugGeometry with Godot]] · [[What to visualize|What to visualize]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) › Physics debug view (Physics extracts, GodotBridge draws) · exported 2026-11-03
