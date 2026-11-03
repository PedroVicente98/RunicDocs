---
title: "Client runtime (Game on Engine)"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Client runtime (Game on Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

GameClient is its own implementation on the Engine: it predicts with the shared game code, presents an interpolated world through Godot, and runs the player UI the server never has. The v3 layer stack stays; only presentation changes backend, and the GodotLayer at the top replaces the GLFW window, the bgfx renderer, RmlUi and the audio backend at once.

```text
GameClient — your main, your loop
  LayerStack (bottom to top)
    Network        ingress and egress
    Prediction     RunicGame::Shared in double precision, reconciliation
    Presentation   interpolation, camera, extraction → RenderFrame, audio and VFX cues
    GodotLayer     presenter, player UI, input, audio backend; iteration() last
```

* **Prediction:** RunicGame::Shared on a subset of systems; see Networking. Godot never computes a gameplay position; its physics is not even built.

* **Interpolation:** other entities are drawn slightly in the past between snapshots, with a short buffer kept small for nearby enemies.

* **Render extraction:** each frame the Presentation layer reads the client world and fills a RenderFrame of plain RenderData (meshes, transforms, lights, anchors, debug geometry). Only [[How the Engine uses Godot|GodotBridge]] reads that frame (see Render data, extraction and world UI).

* **Godot (Engine):** the GodotLayer owns the LibGodot instance. Its presenter turns the [[RenderData in Core|RenderFrame]] into RenderingServer instances on Godot’s main thread; prediction and extraction stay on Runic workers.

* **Animation (Engine):** how characters animate is an open decision: the Runic evaluator sending poses to RenderingServer skeletons, or Godot’s AnimationTree driven by the animation intent in the RenderFrame. The server never evaluates animation either way; gameplay timing comes from ability timelines.

* **Precision:** 64-bit positions become 32-bit relative to the camera in the RenderFrame; inside Godot they are relative to the presenter’s own origin, rebased about every 4 km. Godot stays in single precision. The Game’s camera stays close to the character with no distant zoom; Proposal: a photo mode only out of combat.

* **Streaming:** cells inside the client’s [[World space coordinates cells and activation#Activation volumes|activation volume]], with levels of detail and simplified proxies at distance; cell visual lists come from the client cook, meshes and textures from the project (development) or the .pck (shipping).

* **Light:** rendered from the same emitters and ambient profiles the server uses, so what the server treats as lit matches what the player sees.

* **GameUI (Game):** Godot UI scenes (Control), one per client state (Boot, Login, server and character select, loading, World HUD), bound to view models in C++ by the GodotBridge binder; the map with fog of war is one of them. Most UI lives in the world as diegetic panels, anchored elements and batched nameplates. The UI never reads [[Simulation core Flecs and Jolt#Flecs rules|Flecs]].

* **Audio (client only):** sound effects play through semantic audio events on Godot’s AudioServer, and players customize only the soundtrack (see Audio).

* **Development builds:** a Godot UI overlay shows metrics, layer toggles and debug views; it replaces the v3 ImGui overlay and never ships.

```cpp
// Illustrative contract, not a frozen API.
class GodotLayer final : public Runic::Layer {
public:
    void OnAttach() override               { m_Godot = StartGodot(m_Args, &RegisterRunicClasses); } // create the instance, start()
    void OnUpdate(const FrameTime&) override { m_Presenter.Apply(m_Frames.Front()); }                // RenderFrame → RenderingServer
    void OnRender() override               { if (m_Godot->iteration()) RequestStop(); }             // true = Godot wants to quit
    void OnDetach() override               { StopGodot(m_Godot); }
};
```

**Presenter origin.** bgfx would redraw everything each frame, so a new origin per frame was free; Godot keeps objects between frames, and moving the origin every frame would rewrite every transform (50,000 instances is 3 million writes per second at 60 fps). The presenter keeps its own origin and moves it only when the camera drifts about 4 km away, which keeps the float step under 0.5 mm. The RenderFrame contract does not change.

```cpp
constexpr double kRebaseDistanceM = 4'000.0;

void GodotPresenter::Apply(const RenderFrame& frame) {
    if (DistanceSq(frame.origin, m_GodotOrigin) > kRebaseDistanceM * kRebaseDistanceM) {
        m_GodotOrigin = frame.origin;   // one large, rare shift
        ShiftAllInstances();
    }
    const Vec3 shift = ToLocal(frame.origin - m_GodotOrigin);   // under 4 km
    ApplyChangedInstances(frame, shift);   // position in Godot = shift + the frame's relative position
}
```

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Platform and operations|Platform and operations]] · [[Render data extraction and world UI|Render data, extraction and world UI (Engine, Game)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Client runtime (Game on Engine) · exported 2026-11-03
