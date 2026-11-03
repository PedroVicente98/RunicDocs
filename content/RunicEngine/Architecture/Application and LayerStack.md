---
title: "Application and LayerStack (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Application and LayerStack (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

Every executable is an Application on the Engine’s ApplicationHost: a stack of layers that receives events top-down and updates bottom-up, while the simulation’s internal order stays inside its scheduler.

## Entry point

The Engine owns main(). It calls CreateApplication(), which each executable defines: RunicGame defines it twice (GameClient and GameServer), and the Engine defines it for the [[Tools#RunicEditor|RunicEditor]] ([[Cooker|the Cooker]] runs inside it) and the [[Tools#Testing at scale|RunicBot]]. The Application then builds its LayerStack and hands control to the ApplicationHost. A whole frame fits in RunFrame and Run only repeats it under the loop policy, so a host that does not own the loop can still drive the Engine one frame at a time.

```cpp
// Illustrative contract, not a frozen API.
class Layer {
public:
    virtual ~Layer() = default;
    virtual void OnAttach() {}                        // acquire resources
    virtual void OnDetach() {}                        // release everything acquired
    virtual void OnEvent(Event& event) {}             // top to bottom; stop when handled
    virtual void OnUpdate(const FrameTime& time) {}   // bottom to top, once per loop
    virtual void OnRender() {}                        // client and tools only
};

class ApplicationHost {
public:
    void Run() {                                      // owners of the loop: GameServer, GameClient, RunicEditor
        while (!m_StopRequested)
            RunFrame(m_LoopPolicy.Next());            // frame loop or fixed 60 Hz
    }
    void RunFrame(const FrameTime& time) {            // one complete step
        DrainQueuedEvents();
        m_Layers.UpdateBottomUp(time);
        m_Layers.RenderBottomUp();
        ApplyPendingLayerChanges();                   // the frame's only safe point
    }
};

int main(int argc, char** argv) {
    // Every argument reaches Godot unchanged (the project manager relaunches the executable with --path).
    Runic::ApplicationHost host(Runic::CreateApplication({ argc, argv }));
    host.Run();
}
```

The development overlay that v3 drew with ImGui is a Godot UI panel inside the GodotLayer in development builds; the Layer contract no longer has an ImGui hook.

## Loop policies

| Executable | Loop | Per iteration |
| :---- | :---- | :---- |
| GameClient | Frame loop (vsync or capped) | Events, OnUpdate, OnRender; the GodotLayer calls Godot’s iteration() last |
| GameServer | Fixed 60 Hz loop that sleeps until the next quantum | Events, OnUpdate; no rendering |
| RunicEditor | Godot’s editor loop through LibGodot | Events, OnUpdate, OnRender |
| Cooker (RunicEditor headless) | Job loop | Events, OnUpdate |
| RunicBot | Fixed 60 Hz loop | Events, OnUpdate; no rendering |

## Stacks per executable

| Executable | Layers, bottom to top | Overlays (always above layers) |
| :---- | :---- | :---- |
| GameServer | Network (Engine: ingress and egress) → Simulation (Engine: scheduler and world) → Services bridge (Platform binding: gRPC, NATS) → Lifecycle (Platform binding: [[Platform and operations#Simulation placement\|Agones]]) → Diagnostics (Engine: metrics, RunicEditor attach endpoint) | None |
| GameClient | Network → Prediction → Presentation (interpolation, camera, render extraction, audio cues) → GodotLayer (presenter, player UI, input, audio backend) | None; GameUI and the development overlay are Godot UI scenes inside the GodotLayer |
| RunicEditor | GodotLayer (editor build) hosting the Runic editor plugins; a local simulation layer for inspection and previews | None |
| Cooker | Job runner inside the RunicEditor | None |
| RunicBot | Network → bot runtime (prediction subset and bot brains for many sessions) | None |

The Engine supplies the Network, Simulation, Prediction, Presentation, GodotLayer and Diagnostics layers as reusable classes. The Platform supplies the services-bridge and lifecycle layers as C++ server bindings that implement the Engine’s Layer interface and the Simulation’s service port, because only the Platform may talk to gRPC, NATS and Agones; the Engine never supplies infrastructure or communication layers. RunicGame configures and composes all of them and adds its own (for example the client’s game-state screens). Dependencies point downward: Platform bindings include Engine interface headers, the Engine includes nothing from the Platform or the Game.

## Transitions

State changes are layer replacements applied at the loop’s safe point, never mid-update.

* **Client:** Boot → Login → Character select → World. Each step replaces the presentation layer of the previous one and shows that state’s Godot UI scene; OnDetach releases its Godot, audio and network resources before OnAttach of the next runs. The world is not a Godot scene: the World state shows the HUD scene while the presenter draws the cells and entities the server sends.

* **Server:** Starting → Ready → Draining → Shutdown, driven by the Lifecycle layer and the [[Platform and operations#Simulation placement|World Coordinator]]. Draining hands regions off before the process exits.

## Implementation rules

The LayerStack is organization and event propagation only; it must cost close to nothing next to the simulation.

| Rule | Prevents |
| :---- | :---- |
| The LayerStack owns layers through std::unique\_ptr; popping hands ownership back or destroys the layer explicitly | Leaks and double deletes from raw pointers |
| Push, pop and replace are queued and applied at one safe point per loop | Iterator invalidation and layers changing mid-update |
| Layers and overlays are separate ranges; overlays always sit above | Insertion-index bugs |
| Input and window events dispatch immediately without heap allocation (stack events, no strings) | Per-frame memory churn |
| Other events (connections, service replies) are queued and drained once per loop by the owning layer | Re-entrancy and ordering surprises |
| No layer blocks: network, services and disk work run on their own threads and only enqueue | Stalls that steal simulation time |
| Time comes from one clock as integer ticks or double seconds, never accumulated floats | Drift over long uptimes |
| No global Application singleton reachable from simulation threads; layers receive what they need at attach | Hidden coupling and data races |
| Simulation order lives in the scheduler, never in layer order | Combat results that depend on UI layers |
| Each layer’s time per loop is measured and exported | Silent overhead |

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · [[Godot integration|Godot integration (Engine)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Application and LayerStack (Engine) · exported 2026-11-03
