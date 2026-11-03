---
title: "Math helpers for wire shapes"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine) › Math helpers for wire shapes"
created: "2026-10-14"
modified: "2026-10-30"
---

Every remaining shape is CPU-side geometry generation. Shapes never become [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] bodies, and Godot never needs to know what a capsule, cone or attack arc means.

```cpp
static Vec3  Add(Vec3 a, Vec3 b)   { return { a.x + b.x, a.y + b.y, a.z + b.z }; }
static Vec3  Sub(Vec3 a, Vec3 b)   { return { a.x - b.x, a.y - b.y, a.z - b.z }; }
static Vec3  Mul(Vec3 v, float s)  { return { v.x * s, v.y * s, v.z * s }; }
static float Dot(Vec3 a, Vec3 b)   { return a.x*b.x + a.y*b.y + a.z*b.z; }
static Vec3  Cross(Vec3 a, Vec3 b) { return { a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x }; }
static float Length(Vec3 v)        { return std::sqrt(Dot(v, v)); }
static Vec3  Normalize(Vec3 v) {
    const float len = Length(v);
    if (len <= 1.0e-6f) return { 0, 0, 0 };
    return Mul(v, 1.0f / len);
}

// Orthonormal basis around an axis: the key to circles in any orientation.
static void MakeBasis(Vec3 normal, Vec3& tangent, Vec3& bitangent) {
    const Vec3 n = Normalize(normal);
    const Vec3 helper = std::abs(n.y) < 0.99f ? Vec3{ 0, 1, 0 } : Vec3{ 1, 0, 0 };  // not parallel to n
    tangent = Normalize(Cross(helper, n));
    bitangent = Cross(n, tangent);
}

void DrawArcInPlane(DebugDraw& d, Vec3 center, Vec3 axisX, Vec3 axisY, float radius,
                    float startRadians, float endRadians, uint32_t color, uint32_t segments) {
    axisX = Normalize(axisX);
    axisY = Normalize(axisY);
    segments = std::max(segments, 1u);
    auto pointAt = [&](float angle) {
        return Add(center, Add(Mul(axisX, std::cos(angle) * radius), Mul(axisY, std::sin(angle) * radius)));
    };
    Vec3 previous = pointAt(startRadians);
    for (uint32_t i = 1; i <= segments; ++i) {
        const float t = float(i) / float(segments);
        const Vec3 current = pointAt(startRadians + (endRadians - startRadians) * t);
        d.DrawLine(previous, current, color);
        previous = current;
    }
}
```

---

↑ [[Debug drawing|Debug drawing (Engine)]] · ← [[Debug-draw API|Debug-draw API]] · [[Shapes|Shapes]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) › Math helpers for wire shapes · exported 2026-11-03
