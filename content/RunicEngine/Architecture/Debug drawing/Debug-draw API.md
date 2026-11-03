---
title: "Debug-draw API"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine) › Debug-draw API"
created: "2026-10-14"
modified: "2026-10-30"
---

Shapes are generated on the CPU into DebugGeometry; nothing about a capsule, cone or attack arc reaches Godot except lines and triangles. The API lives with DebugGeometry in Core, so the server can also produce shapes for the [[Tools#RunicEditor|RunicEditor]]’s live attach.

```cpp
// Illustrative contract, not a frozen API. Core/Public/RenderData/DebugDraw.hpp
class DebugDraw {
public:
    explicit DebugDraw(DebugGeometry& out, DebugBatch batch = DebugBatch::WorldDepth);

    void DrawLine(Vec3 a, Vec3 b, uint32_t color);
    void DrawRay(Vec3 origin, Vec3 direction, float length, uint32_t color);
    void DrawArrow(Vec3 start, Vec3 end, uint32_t color);
    void DrawAABB(Vec3 min, Vec3 max, uint32_t color);
    void DrawOBB(Vec3 center, Vec3 axisX, Vec3 axisY, Vec3 axisZ, Vec3 halfExtent, uint32_t color);
    void DrawCircle(Vec3 center, Vec3 normal, float radius, uint32_t color, uint32_t segments = 32);
    void DrawSphere(Vec3 center, float radius, uint32_t color, uint32_t segments = 24);
    void DrawCylinder(Vec3 a, Vec3 b, float radius, uint32_t color, uint32_t segments = 24);
    void DrawCapsule(Vec3 a, Vec3 b, float radius, uint32_t color, uint32_t segments = 24);
    void DrawCone(Vec3 apex, Vec3 direction, float length, float halfAngleRadians,
                  uint32_t color, uint32_t segments = 24);
    void DrawArcSector(Vec3 origin, Vec3 forward, Vec3 up, float innerRadius, float outerRadius,
                       float angleRadians, uint32_t color, uint32_t segments = 24);
    void DrawGridXZ(float halfSize, float spacing, uint32_t color);
    void DrawText(Vec3 position, std::string_view text, uint32_t color);
    void FillTriangle(Vec3 a, Vec3 b, Vec3 c, uint32_t colorWithAlpha);   // opacity in alpha
};
```

Positions are camera-relative floats, like every [[RenderData in Core|RenderData]] type. DebugBatch chooses depth-tested geometry (WorldDepth) or always-visible geometry (Overlay).

---

↑ [[Debug drawing|Debug drawing (Engine)]] · ← [[Ownership (Debug drawing)|Ownership (Debug drawing)]] · [[Math helpers for wire shapes|Math helpers for wire shapes]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) › Debug-draw API · exported 2026-11-03
