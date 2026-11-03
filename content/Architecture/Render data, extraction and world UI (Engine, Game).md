---
title: "Render data, extraction and world UI (Engine, Game)"
tags:
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

Godot and the player UI never read Flecs, Jolt or the domain modules. Each frame the Client extracts what must be shown into plain RenderData structs that live in Core, and only GodotBridge consumes them: its presenter, debug layers and world UI turn them into Godot calls. The same RenderData feeds the debug layers, built first, and the production look (materials, shaders, lighting), built once the game slice justifies it.

![[arch-render-data-flow-sources-extraction-renderframe-go.png]]
*Render data flow — sources, extraction, RenderFrame, GodotBridge and Godot*

*Render data flow — sources, extraction, RenderFrame, GodotBridge and Godot*

Read top to bottom: the client world feeds extractors, extractors write one RenderFrame of plain data, and only GodotBridge reads that frame and talks to Godot.

| Part | Owner | Contains |
| :---- | :---- | :---- |
| RenderData (Core) | Engine | Plain structs: the frame packet, debug geometry, mesh and skinned instances, world anchors, lights, environment frame, volumes, field grids, water surface state, effects |
| Extractors (Runic::Client) | Engine | The extractor registry and the Engine extractors for meshes, skinned instances, anchors, lights, environment, volumes, water and fields |
| Game extractors (RunicGame::Client) | Game | Game-specific visuals: spell effects, chart overlays, faction markers |
| Debug layers (Runic::GodotBridge) | Engine | One layer per kind of render data, drawn through Godot and toggled on or off |
| Presenter and production look (Runic::GodotBridge) | Engine; the look later | RenderFrame instances in the RenderingServer; later materials, shaders, lighting and shadows, terrain, water shading, VFX and decals as Godot resources |
| Render features (RunicGame::Client) | Game, later | Custom Godot materials, shaders and presenter hooks |
| World UI mechanism (Runic::GodotBridge) | Engine | Diegetic SubViewport panels, anchored Label3D and Sprite3D, the batched MultiMesh fallback, budgets and input routing |
| World UI content (RunicGame::Client) | Game | Nameplates, prompts, boards, ship panels; their Godot UI scenes, themes and view models |

### RenderData in Core

RenderData is a separate folder and namespace inside Runic::Core (Core/Public/RenderData/, Runic::RenderData). It is shared by the Client’s extractors, GodotBridge (presenter, debug layers, world UI) and the debug tools, and the headless server uses its debug geometry for the RunicEditor’s live attach.

* **Plain data only.** Header-only structs with trivial helpers; no Flecs, Jolt or Godot types; nothing that allocates on its own.

* **Camera-relative.** Each frame carries one 64-bit origin; every position inside it is a 32-bit float relative to that origin.

* **Stable references.** Meshes, materials and textures are AssetIds; entities are GlobalEntityIds; every mesh or skinned instance carries a RenderInstanceId (the GlobalEntityId for entities, the cooked PlacementId for static objects), so the presenter updates a Godot instance instead of recreating it; nothing points into Flecs memory.

* **Double-buffered.** Extraction writes frame N+1 while GodotBridge reads frame N, so the two never lock each other.

* **Grown by packages.** A kind is added by the package that first needs it (CORE-3 to CORE-7), so the folder never holds unused types.

| Kind | Example | Filled from | Debug layers draw it as | Package |
| :---- | :---- | :---- | :---- | :---- |
| Debug geometry | Collision shapes, paths, cells, volumes, telegraphs | Physics, AI, any system; also the server | Lines, triangles, text, cached debug meshes | CORE-3 |
| Mesh instance | Buildings, props, ships, terrain pieces | Flecs Transform and RenderMesh | Flat-shaded meshes | CORE-4 |
| Skinned instance | Characters, creatures | Flecs and Animation poses | Flat-shaded skinned meshes | CORE-4 |
| World anchor | Where a nameplate, prompt or panel belongs | Flecs Transform, visibility tier, distance | Markers; used by the world UI | CORE-4 |
| Light | Torches, spells, lanterns | Perception’s emitters, the same ones the server uses | Gizmos and simple lighting | CORE-5 |
| Environment frame | Sun, skylight, darkness, fog, wind, rain | Environment clock and weather state | Global shading values | CORE-5 |
| Volume | Darkness zones, fog banks, magic areas | Flecs components, Perception | Tinted boxes and spheres | CORE-5 |
| Field grid | Ocean current, wind map, darkness map, fog of war | Water current fields, Environment wind | Arrows, streaks or heatmaps from a small texture | CORE-6 |
| Water surface state | Tide level, wave strength, flow scale per water body | Water and Environment; surfaces themselves are cooked assets | Flat water surfaces | CORE-6 |
| Effect and decal | Spell impacts, footprints, ground telegraphs | Flecs, ability timelines | Production look only | CORE-7 |

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

### Extraction

Extraction runs in the client’s Presentation layer once per frame, after the latest simulation results are applied. Extractors read Flecs and the domain APIs (Water, Perception, Environment, Animation) read-only and write RenderData; they never change the simulation.

* **A registry of extractors.** Each extractor fills one or more kinds. The Engine registers its own under engine: IDs; RunicGame::Client registers its own under game: IDs.

* **Parallel.** Independent extractors run on the worker pool into per-worker arenas that are merged into the frame packet in a fixed order.

* **Change-driven when the source is slow.** Field grids, water state and the environment re-extract only when their source version changes (currents and weather update at 10 Hz), and GodotBridge re-uploads a texture only when its version changes.

* **Culled and capped at the source.** Each extractor culls by frustum and distance and respects a per-kind cap (lights, anchors), so Godot never receives work it will throw away.

* **Interpolation and precision here.** Remote entities are interpolated between snapshots and positions converted to camera-relative floats once, during extraction.

```cpp
// Illustrative
extraction.Register("engine:meshes",  MeshExtractor{});                 // Flecs Transform + RenderMesh
extraction.Register("engine:skinned", SkinnedExtractor{animation});      // poses from Runic::Animation
extraction.Register("engine:anchors", AnchorExtractor{perception});      // carries the PvP visibility tier
extraction.Register("engine:lights",  LightExtractor{perception});       // the server's emitters
extraction.Register("engine:fields",  FieldExtractor{water, environment}, ExtractRate::OnChange);

// RunicGame::Client
extraction.Register("game:chart_overlay", ChartOverlayExtractor{});
```

**Example: showing an ocean current.** The Water module holds the cooked current field and the Environment modulates it over time. The field extractor samples the area around the camera into a 64 by 64 field grid only when the current’s version changes. The debug layers draw it as arrows or animated streaks; later, the production look uses the same grid to animate the water surface or a nautical-chart overlay. Neither Water nor Godot knows about the other.

### Debug layers first, the Godot look later

Both the debug layers and the final look read the same RenderFrame, so moving from one to the other, or showing both side by side, needs no gameplay change.

**Debug layers come first.** One layer per kind of render data, each drawn simply by GodotBridge and toggled from the development overlay or the RunicEditor, so a developer chooses exactly what to see. They are built layer by layer, starting with Jolt geometry and adding a layer whenever a slice needs it. They run in development builds of the client and in the RunicEditor viewport; the RunicEditor also draws debug geometry streamed from development and staging servers.

| Debug layer | Draws | Slice | Package |
| :---- | :---- | :---- | :---- |
| Debug shapes | Lines, shapes and text issued by any system | 2 | GDB-2 |
| Physics geometry | Collision bodies and shapes extracted by Physics, with cached debug meshes for large shapes | 8 | GDB-4 |
| Meshes | Cooked mesh instances | 22 | GDB-5 |
| Skinned meshes | Characters with their animation | 23 | GDB-6 |
| Lights, environment, volumes | Godot lights, skylight and darkness, fog, darkness zones | 25a | GDB-7 |
| Water and fields | Water surfaces; currents and wind as arrows, streaks or heatmaps | 42a | GDB-8 |

**The production look comes later.** Materials, shaders, lighting and shadows, terrain, water shading, VFX and decals are Godot resources fed by RenderData, built once a substantial game slice justifies the investment (slice 44 onward, package GDB-13). Game render features register then, as materials and presenter hooks. Until that point every slice is proven with Godot’s default materials and the debug layers, which already show the true state of the world.

**The presenter.** Godot keeps objects between frames, so the presenter creates an instance once (by its RenderInstanceId), moves it only when its transform changes and frees it when it leaves interest; repeated static meshes of a cell go into one MultiMesh. Its origin is rebased rarely (see [[Client runtime (Game on Engine)|Client runtime]]).

### World UI: diegetic first, with fallbacks

Most UI lives in the world. Every world widget is authored once by the Game as a Godot UI scene (Control nodes and a theme), and the Engine decides how it is drawn from distance, on-screen count and frame budget. A widget declares its preferred mode and its fallbacks, so the same nameplate can be a full element up close and one instance in a batched draw across a battlefield. Player UI scenes are the one accepted use of nodes in the game: they are interface only and never hold game state.

| Mode | In Godot | Typical use | Cost |
| :---- | :---- | :---- | :---- |
| Diegetic panel | A UI scene inside a SubViewport whose texture sits on a quad or a mesh surface; input by ray, converted into panel coordinates | Notice boards, ship helm, crafting stations, shop signs, spell tomes | One offscreen render per visible panel, only when its content changes |
| Anchored element | Label3D or Sprite3D with an MSDF font, facing the camera or fixed to the object | The target’s nameplate, the interaction prompt tilted on a rock, a mount’s saddle, a chair, speech bubbles | A position update each frame; text layout when content changes |
| Batched | One MultiMesh of labels and bars from an atlas | Nameplates and damage numbers in crowds and battles | One draw call for all; the atlas changes only when a name or a style changes |
| Screen HUD | Ordinary UI scenes | Skill bar, inventory, map, chat | Standard Godot UI |

A diegetic panel at 512 by 512 in RGBA8 is 1 MB of video memory, so 20 active panels cost about 20 MB; a SubViewport redraws only when its content changes. Compared with RmlUi, Godot’s UI brings a visual scene editor, themes, localization, HarfBuzz text shaping and ready 3D UI; it has no declarative data binding, so GodotBridge adds a small binder.

```cpp
// Illustrative: GodotBridge view-model binder
binder.Bind(vm.health,     hud, "HealthBar:value");
binder.Bind(vm.playerName, hud, "Name:text");
binder.Bind(vm.skills,     hud, "SkillBar:slots");   // list → slots
binder.Flush();   // each frame: only changed fields become set() calls on controls
```

* **Visibility follows gameplay.** Anchors carry the PvP visibility tier, so a Hidden player shows no nameplate and a Silhouette shows a reduced one.

* **Input reaches the UI first.** A click on a diegetic panel becomes a ray, the ray hits the panel’s quad, the hit becomes panel coordinates, and that panel’s SubViewport receives the event. Any action becomes a normal command that the server validates.

* **The UI never reads Flecs.** Positions come from world anchors in the frame packet; content comes from Game view models.

* **Budgets protect the frame.** Each widget type has a cap per mode; beyond it, widgets fall back to the next mode, and battle mode lowers the caps.

```yaml
# Example values; the Game sets its own.
WorldWidget: game:nameplate
  Scene:     ui/nameplate.tscn      Theme: ui/world.theme
  Modes:     Anchored (targeted or within 30 m) -> Batched (within 120 m) -> Hidden
  Budget:    40 anchored, 500 batched; battle mode: 10 anchored
  Binds:     name, guild, health, visibilityTier

WorldWidget: game:notice_board
  Scene:     ui/notice_board.tscn
  Modes:     Diegetic (within 12 m) -> Hidden
  Surface:   mesh socket board_face, 1024 by 768 texels
```
