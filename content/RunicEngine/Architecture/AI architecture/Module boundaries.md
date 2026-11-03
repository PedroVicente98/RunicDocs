---
title: "Module boundaries"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Module boundaries"
created: "2026-10-14"
modified: "2026-10-30"
---

```cpp
class AIModule {
public:
    void Register(flecs::world& world);
private:
    BehaviorTreeRuntime m_BehaviorTrees;
    AIIntentBuffers     m_Intents;      // one buffer per worker
};

void AIModule::Register(flecs::world& world) {
    RegisterAIComponents(world);
    RegisterAggroSystem(world);
    RegisterPerceptionSystem(world);
    RegisterThinkSystem(world);
    RegisterTargetSystem(world);
    RegisterSleepSystem(world);
}
```

Runic::AI is a [[Simulation core Flecs and Jolt#Flecs rules|Flecs]]-integrated module, not a second simulation engine: the SimulationRuntime owns the Flecs world, and AI registers data and work into it, owning only AI-specific runtime objects such as brain instances and intent buffers.

| Module | May depend on | Must not depend on |
| :---- | :---- | :---- |
| Runic::AI | Core and runtime contracts, Flecs, gameplay command and event contracts, Perception, Navigation, BehaviorTree.CPP | Godot, editor docks, client presentation |
| Runic::GodotTools (AI docks) | Runic::AI definitions and contracts, GodotTools, Godot’s GraphEdit | Authoritative simulation ownership; direct mutation of live combat state |
| RunicGame AI content | The public Runic AI extension API, game ability and content registries | Internal BehaviorTreeRuntime details where avoidable |

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Mental model|Mental model]] · [[Data model|Data model]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Module boundaries · exported 2026-11-03
