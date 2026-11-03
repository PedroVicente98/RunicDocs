---
title: "Shapes"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine) › Shapes"
created: "2026-10-14"
modified: "2026-10-30"
---

The shape implementations of v3 move into DebugDraw unchanged except for the class name: they only ever produced lines, so they never depended on bgfx.

These implementations favor clarity and predictable output over cleverness; segment counts are exposed so smoothness can be traded for CPU and vertex cost.

**Ray and arrow** — rays for line-of-sight and query visualization; arrows when direction matters: velocity, knockback, aim, surface normals, wind, currents, ship heading, reconciliation error.

```cpp
void DebugDraw::DrawRay(Vec3 origin, Vec3 direction, float length, uint32_t color) {
    DrawLine(origin, Add(origin, Mul(Normalize(direction), length)), color);
}

void DebugDraw::DrawArrow(Vec3 start, Vec3 end, uint32_t color) {
    const Vec3 delta = Sub(end, start);
    const float len = Length(delta);
    if (len <= 1.0e-6f) return;
    const Vec3 dir = Mul(delta, 1.0f / len);
    Vec3 right, up;
    MakeBasis(dir, right, up);
    const float headLength = std::min(0.25f * len, 0.35f);
    const float headWidth = headLength * 0.45f;
    const Vec3 base = Sub(end, Mul(dir, headLength));
    DrawLine(start, end, color);
    DrawLine(end, Add(base, Mul(right, headWidth)), color);
    DrawLine(end, Sub(base, Mul(right, headWidth)), color);
    DrawLine(end, Add(base, Mul(up, headWidth)), color);
    DrawLine(end, Sub(base, Mul(up, headWidth)), color);
}
```

**AABB and OBB** — an oriented box is a box whose three local axes are rotated; pass normalized axes and half-extents.

```cpp
void DebugDraw::DrawAABB(Vec3 min, Vec3 max, uint32_t color) {
    const Vec3 p[8] = {
        { min.x, min.y, min.z }, { max.x, min.y, min.z }, { max.x, max.y, min.z }, { min.x, max.y, min.z },
        { min.x, min.y, max.z }, { max.x, min.y, max.z }, { max.x, max.y, max.z }, { min.x, max.y, max.z } };
    static constexpr uint8_t edges[12][2] = {
        {0,1},{1,2},{2,3},{3,0}, {4,5},{5,6},{6,7},{7,4}, {0,4},{1,5},{2,6},{3,7} };
    for (auto& e : edges) DrawLine(p[e[0]], p[e[1]], color);
}

void DebugDraw::DrawOBB(Vec3 center, Vec3 axisX, Vec3 axisY, Vec3 axisZ, Vec3 halfExtent, uint32_t color) {
    axisX = Normalize(axisX); axisY = Normalize(axisY); axisZ = Normalize(axisZ);
    Vec3 p[8];
    int index = 0;
    for (int z = -1; z <= 1; z += 2)
    for (int y = -1; y <= 1; y += 2)
    for (int x = -1; x <= 1; x += 2)
        p[index++] = Add(center, Add(Add(Mul(axisX, halfExtent.x * float(x)),
                                         Mul(axisY, halfExtent.y * float(y))),
                                     Mul(axisZ, halfExtent.z * float(z))));
    // Corner layout: 0-1 / 2-3 at z = -1, 4-5 / 6-7 at z = +1
    static constexpr uint8_t edges[12][2] = {
        {0,1},{0,2},{1,3},{2,3}, {4,5},{4,6},{5,7},{6,7}, {0,4},{1,5},{2,6},{3,7} };
    for (auto& e : edges) DrawLine(p[e[0]], p[e[1]], color);
}
```

**Circle, sphere, cylinder** — a debug sphere needs no mesh: three great circles show position and radius.

```cpp
void DebugDraw::DrawCircle(Vec3 center, Vec3 normal, float radius, uint32_t color, uint32_t segments) {
    if (radius <= 0.0f) return;
    Vec3 tangent, bitangent;
    MakeBasis(normal, tangent, bitangent);
    constexpr float TwoPi = 6.28318530718f;
    DrawArcInPlane(*this, center, tangent, bitangent, radius, 0.0f, TwoPi, color, std::max(segments, 3u));
}

void DebugDraw::DrawSphere(Vec3 center, float radius, uint32_t color, uint32_t segments) {
    DrawCircle(center, {1,0,0}, radius, color, segments);
    DrawCircle(center, {0,1,0}, radius, color, segments);
    DrawCircle(center, {0,0,1}, radius, color, segments);
}

void DebugDraw::DrawCylinder(Vec3 a, Vec3 b, float radius, uint32_t color, uint32_t segments) {
    const Vec3 axisVector = Sub(b, a);
    if (Length(axisVector) <= 1.0e-6f || radius <= 0.0f) return;
    const Vec3 axis = Normalize(axisVector);
    Vec3 tangent, bitangent;
    MakeBasis(axis, tangent, bitangent);
    segments = std::max(segments, 4u);
    DrawCircle(a, axis, radius, color, segments);
    DrawCircle(b, axis, radius, color, segments);
    constexpr uint32_t sideLines = 8;
    constexpr float TwoPi = 6.28318530718f;
    for (uint32_t i = 0; i < sideLines; ++i) {
        const float angle = TwoPi * float(i) / float(sideLines);
        const Vec3 radial = Add(Mul(tangent, std::cos(angle) * radius), Mul(bitangent, std::sin(angle) * radius));
        DrawLine(Add(a, radial), Add(b, radial), color);
    }
}
```

**Capsule** — defined by the centers of its two spherical caps plus a radius, which maps naturally to character collision and avoids ambiguity about total height. For a standing character, a and b are the lower and upper sphere centers; the capsule extends radius units beyond both.

```cpp
void DebugDraw::DrawCapsule(Vec3 a, Vec3 b, float radius, uint32_t color, uint32_t segments) {
    if (radius <= 0.0f) return;
    const Vec3 axisVector = Sub(b, a);
    if (Length(axisVector) <= 1.0e-6f) { DrawSphere(a, radius, color, segments); return; }

    const Vec3 axis = Normalize(axisVector);
    Vec3 tangent, bitangent;
    MakeBasis(axis, tangent, bitangent);
    segments = std::max(segments, 8u);

    DrawCircle(a, axis, radius, color, segments);           // equator rings at both cap centers
    DrawCircle(b, axis, radius, color, segments);
    DrawLine(Add(a, Mul(tangent, radius)),   Add(b, Mul(tangent, radius)),   color);
    DrawLine(Sub(a, Mul(tangent, radius)),   Sub(b, Mul(tangent, radius)),   color);
    DrawLine(Add(a, Mul(bitangent, radius)), Add(b, Mul(bitangent, radius)), color);
    DrawLine(Sub(a, Mul(bitangent, radius)), Sub(b, Mul(bitangent, radius)), color);

    constexpr float Pi = 3.14159265359f;
    DrawArcInPlane(*this, a, tangent,   axis, radius, Pi, 2.0f * Pi, color, segments / 2);   // bottom hemisphere
    DrawArcInPlane(*this, a, bitangent, axis, radius, Pi, 2.0f * Pi, color, segments / 2);
    DrawArcInPlane(*this, b, tangent,   axis, radius, 0.0f, Pi,      color, segments / 2);   // top hemisphere
    DrawArcInPlane(*this, b, bitangent, axis, radius, 0.0f, Pi,      color, segments / 2);
}
```

**Cone** — for perception, breath attacks, vision, targeting assistance and broad combat shapes; the base radius is tan(halfAngle) × length.

```cpp
void DebugDraw::DrawCone(Vec3 apex, Vec3 direction, float length, float halfAngleRadians,
                         uint32_t color, uint32_t segments) {
    if (length <= 0.0f) return;
    const Vec3 axis = Normalize(direction);
    if (Length(axis) <= 1.0e-6f) return;
    const float radius = std::tan(halfAngleRadians) * length;
    const Vec3 baseCenter = Add(apex, Mul(axis, length));
    Vec3 tangent, bitangent;
    MakeBasis(axis, tangent, bitangent);
    DrawCircle(baseCenter, axis, radius, color, std::max(segments, 4u));
    constexpr float TwoPi = 6.28318530718f;
    constexpr uint32_t spokes = 8;
    for (uint32_t i = 0; i < spokes; ++i) {
        const float angle = TwoPi * float(i) / float(spokes);
        const Vec3 radial = Add(Mul(tangent, std::cos(angle) * radius), Mul(bitangent, std::sin(angle) * radius));
        DrawLine(apex, Add(baseCenter, radial), color);
    }
}
```

**Combat arc (annular sector) and arc volume** — a melee swing needs an outer radius, an optional inner radius, a forward direction and a total angle. The volume draws the sector at a bottom and top height and connects the boundary corners; combat still owns the exact intersection math.

```cpp
void DebugDraw::DrawArcSector(Vec3 origin, Vec3 forward, Vec3 up, float innerRadius, float outerRadius,
                              float angleRadians, uint32_t color, uint32_t segments) {
    if (outerRadius <= 0.0f || angleRadians <= 0.0f) return;
    up = Normalize(up);
    forward = Normalize(Sub(forward, Mul(up, Dot(forward, up))));   // remove vertical component
    if (Length(forward) <= 1.0e-6f) return;

    const Vec3 right = Normalize(Cross(up, forward));
    const float halfAngle = angleRadians * 0.5f;
    segments = std::max(segments, 2u);
    auto pointAt = [&](float radius, float angle) {
        const Vec3 dir = Add(Mul(forward, std::cos(angle)), Mul(right, std::sin(angle)));
        return Add(origin, Mul(dir, radius));
    };

    Vec3 prevOuter = pointAt(outerRadius, -halfAngle);
    Vec3 prevInner = innerRadius > 0.0f ? pointAt(innerRadius, -halfAngle) : origin;
    for (uint32_t i = 1; i <= segments; ++i) {
        const float angle = -halfAngle + angleRadians * (float(i) / float(segments));
        const Vec3 outer = pointAt(outerRadius, angle);
        DrawLine(prevOuter, outer, color);
        prevOuter = outer;
        if (innerRadius > 0.0f) {
            const Vec3 inner = pointAt(innerRadius, angle);
            DrawLine(prevInner, inner, color);
            prevInner = inner;
        }
    }
    const Vec3 outerStart = pointAt(outerRadius, -halfAngle);
    const Vec3 outerEnd   = pointAt(outerRadius,  halfAngle);
    if (innerRadius > 0.0f) {
        DrawLine(pointAt(innerRadius, -halfAngle), outerStart, color);
        DrawLine(pointAt(innerRadius,  halfAngle), outerEnd, color);
    } else {
        DrawLine(origin, outerStart, color);
        DrawLine(origin, outerEnd, color);
    }
}

void DrawArcVolume(DebugDraw& d, Vec3 origin, Vec3 forward, Vec3 up, float innerRadius,
                   float outerRadius, float angleRadians, float height, uint32_t color) {
    up = Normalize(up);
    const Vec3 offset = Mul(up, height * 0.5f);
    const Vec3 bottom = Sub(origin, offset), top = Add(origin, offset);
    d.DrawArcSector(bottom, forward, up, innerRadius, outerRadius, angleRadians, color);
    d.DrawArcSector(top,    forward, up, innerRadius, outerRadius, angleRadians, color);

    const Vec3 flatForward = Normalize(Sub(forward, Mul(up, Dot(forward, up))));
    const Vec3 right = Normalize(Cross(up, flatForward));
    const float half = angleRadians * 0.5f;
    auto radial = [&](float radius, float angle) {
        return Mul(Add(Mul(flatForward, std::cos(angle)), Mul(right, std::sin(angle))), radius);
    };
    for (float angle : { -half, half }) {
        d.DrawLine(Add(bottom, radial(outerRadius, angle)), Add(top, radial(outerRadius, angle)), color);
        if (innerRadius > 0.0f)
            d.DrawLine(Add(bottom, radial(innerRadius, angle)), Add(top, radial(innerRadius, angle)), color);
    }
}
```

**XZ grid**

```cpp
void DebugDraw::DrawGridXZ(float halfSize, float spacing, uint32_t color) {
    if (halfSize <= 0.0f || spacing <= 0.0f) return;
    for (float i = -halfSize; i <= halfSize + 0.0001f; i += spacing) {
        DrawLine({ i, 0.0f, -halfSize }, { i, 0.0f, halfSize }, color);
        DrawLine({ -halfSize, 0.0f, i }, { halfSize, 0.0f, i }, color);
    }
}
```

| Debug concept | Built from |
| :---- | :---- |
| Transform gizmo | Three DrawArrow calls for local X, Y and Z |
| Velocity | DrawArrow(position, position \+ velocity × scale) |
| Projectile | DrawSphere plus DrawArrow for direction |
| Line AoE | OBB or cylinder aligned to forward |
| Ground AoE | Circle or cylinder at the server-validated point |
| Damage-over-time zone | Persistent circle or cylinder plus text for the next tick |
| Cell or sector boundary | AABB or grid rectangle |
| Navigation path | Lines between consecutive path nodes |
| Hit normal | Arrow from the impact point along the normal |
| Water flow and wind | Arrows on a grid of sample points |

---

↑ [[Debug drawing|Debug drawing (Engine)]] · ← [[Math helpers for wire shapes|Math helpers for wire shapes]] · [[Drawing DebugGeometry with Godot|Drawing DebugGeometry with Godot]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) › Shapes · exported 2026-11-03
