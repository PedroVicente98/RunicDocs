---
title: "RenderData in Core"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Render data, extraction and world UI (Engine, Game) › RenderData in Core"
created: "2026-10-14"
modified: "2026-10-30"
---

RenderData is a separate folder and namespace inside Runic::Core (Core/Public/RenderData/, Runic::RenderData). It is shared by the Client’s extractors, GodotBridge (presenter, debug layers, world UI) and the debug tools, and the headless server uses its debug geometry for the [[Tools#RunicEditor|RunicEditor]]’s live attach.

* **Plain data only.** Header-only structs with trivial helpers; no [[Simulation core Flecs and Jolt#Flecs rules|Flecs]], [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] or Godot types; nothing that allocates on its own.

* **Camera-relative.** Each frame carries one 64-bit origin; every position inside it is a 32-bit float relative to that origin.

* **Stable references.** Meshes, materials and textures are AssetIds; entities are GlobalEntityIds; every mesh or skinned instance carries a RenderInstanceId (the GlobalEntityId for entities, the cooked PlacementId for static objects), so the presenter updates a Godot instance instead of recreating it; nothing points into Flecs memory.

* **Double-buffered.** Extraction writes frame N+1 while [[How the Engine uses Godot|GodotBridge]] reads frame N, so the two never lock each other.

* **Grown by packages.** A kind is added by the package that first needs it ([[CORE-3|CORE-3]] to [[CORE-7|CORE-7]]), so the folder never holds unused types.

| Kind | Example | Filled from | Debug layers draw it as | Package |
| :---- | :---- | :---- | :---- | :---- |
| Debug geometry | Collision shapes, paths, cells, volumes, telegraphs | Physics, AI, any system; also the server | Lines, triangles, text, cached debug meshes | [[CORE-3\|CORE-3]] |
| Mesh instance | Buildings, props, ships, terrain pieces | Flecs Transform and RenderMesh | Flat-shaded meshes | [[CORE-4\|CORE-4]] |
| Skinned instance | Characters, creatures | Flecs and Animation poses | Flat-shaded skinned meshes | [[CORE-4\|CORE-4]] |
| World anchor | Where a nameplate, prompt or panel belongs | Flecs Transform, visibility tier, distance | Markers; used by the world UI | [[CORE-4\|CORE-4]] |
| Light | Torches, spells, lanterns | Perception’s emitters, the same ones the server uses | Gizmos and simple lighting | [[CORE-5\|CORE-5]] |
| Environment frame | Sun, skylight, darkness, fog, wind, rain | Environment clock and weather state | Global shading values | [[CORE-5\|CORE-5]] |
| Volume | Darkness zones, fog banks, magic areas | Flecs components, Perception | Tinted boxes and spheres | [[CORE-5\|CORE-5]] |
| Field grid | Ocean current, wind map, darkness map, fog of war | Water current fields, Environment wind | Arrows, streaks or heatmaps from a small texture | [[CORE-6\|CORE-6]] |
| Water surface state | Tide level, wave strength, flow scale per water body | Water and Environment; surfaces themselves are cooked assets | Flat water surfaces | [[CORE-6\|CORE-6]] |
| Effect and decal | Spell impacts, footprints, ground telegraphs | Flecs, ability timelines | Production look only | [[CORE-7\|CORE-7]] |

```cpp
// Illustrative: Core/Public/RenderData/RenderFrame.hpp
namespace Runic::RenderData {
struct MeshInstance      { RenderInstanceId id; AssetId mesh; AssetId material; Mat4 transform;
                           uint8_t lod; uint32_t flags; };
struct AnimationIntent   { AnimStateId state; ClipId clips[2]; float blend; float normalizedTime; };
struct SkinnedInstance   { MeshInstance base; uint32_t poseOffset; uint16_t boneCount;
                           AnimationIntent intent; };   // poses or intent, per the open animation decision
struct WorldAnchor       { GlobalEntityId entity; Vec3 position; float distance;
                           uint8_t visibilityTier; uint8_t priority; WidgetId widget; };
struct Light             { LightType type; Vec3 position; Vec3 direction; Color color;
                           float intensity; float radius; float coneAngle; };
struct EnvironmentFrame  { Vec3 sunDirection; float skylight; float darkness;
                           Color fogColor; float fogDensity; Vec2 wind; float rain; };
struct Volume            { VolumeShape shape; Mat4 transform; VolumeKind kind; float density; Color tint; };
struct FieldGrid         { FieldId id; Vec3 origin; float cellSize; uint16_t width, height;
                           FieldFormat format; uint32_t version; std::span<const std::byte> texels; };
struct WaterSurfaceState { WaterBodyId body; float level; float waveAmplitude;
                           Vec2 waveDirection; Vec2 flowScale; uint32_t version; };

struct RenderFrame {
    WorldPosition origin;                  // 64-bit; everything below is relative to it
    Camera camera;
    EnvironmentFrame environment;
    std::span<const MeshInstance> meshes;
    std::span<const SkinnedInstance> skinned;
    std::span<const Mat4> poses;
    std::span<const WorldAnchor> anchors;
    std::span<const Light> lights;
    std::span<const Volume> volumes;
    std::span<const FieldGrid> fields;
    std::span<const WaterSurfaceState> water;
    DebugGeometry debug;                   // lines, triangles, text, cached debug meshes
};
}
```

---

↑ [[Render data extraction and world UI|Render data, extraction and world UI (Engine, Game)]] · [[Extraction|Extraction]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Render data, extraction and world UI (Engine, Game) › RenderData in Core · exported 2026-11-03
