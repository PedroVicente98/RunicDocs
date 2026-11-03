---
title: "Behavior-tree runtime"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Behavior-tree runtime"
created: "2026-10-14"
modified: "2026-10-30"
---

```cpp
class BehaviorTreeRuntime {
public:
    BehaviorTreeRuntime(flecs::world& world, AIIntentBuffers& intents);

    void        RegisterTree(AIDefinitionId definition, std::string_view xml);
    BrainHandle Wake(EntityId entity, AIDefinitionId definition);   // barrier only
    void        Sleep(BrainHandle brain);                            // barrier only
    void        Tick(BrainHandle brain, double simulationTime, WorkerIndex worker);

private:
    flecs::world&           m_World;
    BT::BehaviorTreeFactory m_Factory;
    BrainPool               m_Brains;
    AIIntentBuffers&        m_Intents;
};

struct AIBrainContext {
    EntityId          self = 0;
    flecs::world*     world = nullptr;
    AIIntentBuffer*   intents = nullptr;   // the ticking worker's buffer
    RandomStream*     random = nullptr;    // per brain, seeded: decisions are reproducible
    double            simulationTime = 0.0;
};

BrainHandle BehaviorTreeRuntime::Wake(EntityId entity, AIDefinitionId definition) {
    const auto& def = m_Definitions.Get(definition);
    auto blackboard = BT::Blackboard::create();
    BrainHandle handle = m_Brains.Create();
    BrainInstance& brain = m_Brains.Get(handle);

    brain.context.self   = entity;
    brain.context.world  = &m_World;
    brain.context.random = &brain.random;
    blackboard->set("RunicContext", &brain.context);

    brain.tree = m_Factory.createTree(def.behaviorTreeName, blackboard);
    return handle;
}

// 20 Hz pre-realtime phase, in parallel by NPC.
void AIThinkSystem(flecs::world& world, BehaviorTreeRuntime& runtime, double now) {
    auto query = world.query_builder<AIController, AIWorkingMemory>()
        .with<NPC>().with<AIActive>().build();
    query.each([&](flecs::iter& it, size_t, AIController& controller, AIWorkingMemory&) {
        if (controller.brain != 0)
            runtime.Tick(controller.brain, now, it.world().get_stage_id());
    });
}

void BehaviorTreeRuntime::Tick(BrainHandle handle, double now, WorkerIndex worker) {
    BrainInstance& brain = m_Brains.Get(handle);
    brain.context.simulationTime = now;
    brain.context.intents = &m_Intents.ForWorker(worker);
    brain.tree.tickOnce();
}

BehaviorTreeRuntime::BehaviorTreeRuntime(flecs::world& world, AIIntentBuffers& intents)
    : m_World(world), m_Intents(intents)
{
    m_Factory.registerSimpleCondition("HasReactableThreat", HasReactableThreat);
    m_Factory.registerSimpleCondition("HasCombatTarget",    HasCombatTarget);
    m_Factory.registerSimpleCondition("CanAttackTarget",    CanAttackTarget);
    m_Factory.registerSimpleCondition("IsAlerted",          IsAlerted);
    m_Factory.registerSimpleAction("ChooseDefense",   ChooseDefense);
    m_Factory.registerSimpleAction("ChooseAttack",    ChooseAttack);
    m_Factory.registerSimpleAction("ApproachTarget",  ApproachTarget);
    m_Factory.registerSimpleAction("InvestigateAlert", InvestigateAlert);
    m_Factory.registerSimpleAction("Idle",            Idle);
}
```

Threading follows the simulation’s rules: brains tick in parallel, each worker writes intents into its own buffer, and brain creation or release happens only at the barrier.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Events and perception pipeline|Events and perception pipeline]] · [[Reactive combat and personality|Reactive combat and personality]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Behavior-tree runtime · exported 2026-11-03
