---
title: "Debug drawing (Engine)"
tags:
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

Debug drawing is the first thing the client shows through Godot: a debug-draw API that turns shapes into plain DebugGeometry, and GodotBridge layers that draw it with Godot. That alone is enough to debug movement, Jolt collision, client reconciliation, attack volumes, projectiles, cells, paths, ships, gliders, water flow and boss telegraphs before any production art exists.

**Core rule:** simulation owns meaning; GodotBridge owns visualization. Flecs, Jolt, combat, networking and gameplay systems never call Godot.

### Ownership

| Layer | Owner | Owns | Does not own |
| :---- | :---- | :---- | :---- |
| Simulation and client world | Engine and Game | Transforms, prediction, collision state, combat volumes | Godot resources, materials, draw calls |
| Debug-draw API (Core) | Engine | Turning abstract shapes into DebugGeometry lines, triangles and text | Jolt bodies, gameplay entities, Godot |
| Debug layers (Runic::GodotBridge) | Engine | Uploading DebugGeometry to the RenderingServer, materials, toggles, the development overlay | Combat rules, physics authority, ECS behavior |
| Physics view | Engine (development only) | Runic::Physics extracts Jolt debug geometry into plain Core buffers; a GodotBridge layer draws them | Gameplay rendering; a link between Physics and GodotBridge |
| Godot | Third party | Rendering, windows, the RenderingServer | Scenes of the game, gameplay objects, skill meaning |
| What gets drawn and in which color | Game | Debug overlays for its own systems | — |

**First milestone (slice 2):** a grid, one movable capsule, one camera, one attack arc, one ray, and text showing the simulation tick and network state, all drawn by Godot from the debug-draw API. If that works reliably, debug drawing is already useful.

### Debug-draw API

Shapes are generated on the CPU into DebugGeometry; nothing about a capsule, cone or attack arc reaches Godot except lines and triangles. The API lives with DebugGeometry in Core, so the server can also produce shapes for the RunicEditor’s live attach.

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

Positions are camera-relative floats, like every RenderData type. DebugBatch chooses depth-tested geometry (WorldDepth) or always-visible geometry (Overlay).

### Math helpers for wire shapes

Every remaining shape is CPU-side geometry generation. Shapes never become Jolt bodies, and Godot never needs to know what a capsule, cone or attack arc means.

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

### Shapes

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

### Drawing DebugGeometry with Godot

GodotBridge keeps one mesh per batch in the RenderingServer and rebuilds it each frame from the DebugGeometry; lines use a line primitive, filled shapes a triangle primitive, and text becomes Label3D instances from a small pool.

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

### Physics debug view (Physics extracts, GodotBridge draws)

Jolt and Godot never know about each other, and Runic::Physics and Runic::GodotBridge never link each other. Physics fills plain debug-geometry buffers defined in Core; a GodotBridge debug layer draws those buffers like any other debug geometry. There are two paths.

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

### What to visualize

| System | Visualization | Why |
| :---- | :---- | :---- |
| Movement prediction | Predicted capsule, server sphere, correction arrow | Makes reconciliation error obvious |
| Melee combat | Arc sector or arc volume plus victim capsules | Shows exact spatial coverage and timing |
| Projectiles | Sphere or capsule, direction arrow, past path | Debugs speed, collision and latency |
| Ground AoE | Circle or cylinder at the server-validated point | Separates cursor preview from authoritative placement |
| Boss telegraphs | Cone, ring, line or cylinder | Verifies encounter geometry before VFX |
| Aim assist | Crosshair ray, candidate rays, assist cone | Shows why one entity was picked |
| Cells and interest | AABBs, grid cells, colored boundaries, visibility tiers | Makes spatial ownership and visibility visible |
| Navigation and AI | Path lines, waypoint spheres, query rays, warn, detect and leash radii | Debugs navigation and perception without art |
| Ships and gliders | OBBs, hull bounds, buoyancy points, velocity, current and wind arrows | Exposes water and movement math |

| Meaning | Color |
| :---- | :---- |
| Predicted or local state | Green |
| Authoritative server state | Yellow or orange |
| Damage or harmful volume | Red |
| Healing or beneficial volume | Cyan or green |
| Physics bounds and broadphase | Blue |
| Queries and rays | Magenta or white |
| Inactive or past geometry | Dim gray |

### Performance and correctness

* **Segments are a budget.** A 32-segment circle is 32 lines (64 vertices); a three-circle sphere is 192 vertices. Global quality levels (8, 16, 24, 32 segments) and fewer segments for distant or tiny shapes keep thousands of shapes cheap.

* **A vertex budget per frame.** The debug layers cap the vertices they upload; dropped vertices are counted in development builds so a missing shape is explainable.

* **Threading.** Godot calls stay in the GodotLayer on Godot’s main thread. Simulation workers write debug commands into per-worker buffers merged at the barrier, matching the simulation’s model.

* **Render geometry is never collision truth.** Combat uses exact math and Jolt queries; drawing samples that data for people.

* **Large coordinates.** Every conversion from 64-bit world positions to floats happens during extraction and in the presenter shift, before anything reaches Godot.

### Implementation order and definition of done

1. Start the GodotLayer and open a window (GDB-1).

2. Implement DebugDraw lines and the line upload with the depth-tested and overlay materials.

3. Add a camera from the client into Godot’s viewport.

4. Implement grid, AABB, circle and sphere.

5. Implement cylinder, capsule, arrow, cone and OBB.

6. Implement the combat arc sector and arc volume.

7. Add filled shapes with opacity and debug text.

8. Visualize the predicted movement and the authoritative server position.

9. Add Path A of the Jolt bridge; add the full Jolt debug interface only when needed.

10. Add the development overlay panel with layer toggles.

**Done when** a predicted capsule moves around a grid, the authoritative correction shows separately, attack volumes render with the same dimensions combat uses, and Jolt collision state can be inspected — without any simulation system calling Godot.
