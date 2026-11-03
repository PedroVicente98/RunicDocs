---
title: "Data model"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Data model"
created: "2026-10-14"
modified: "2026-10-30"
---

```cpp
// Illustrative contract, not a frozen API.
using EntityId       = uint64_t;
using AbilityId      = uint32_t;
using AIDefinitionId = uint32_t;
using BrainHandle    = uint32_t;

struct NPC {};
struct Player {};
struct Aggroable {};          // toggle: off when dead, GM or protected

struct AggroSensor {
    PerceptionProfileId perception;   // warn/detect radii, min/max, light curve
    float leashRadius = 30.0f;
};

struct AIController {
    AIDefinitionId definition = 0;
    BrainHandle brain = 0;            // 0 while sleeping
};
```

struct AIActive {};           // toggle (CanToggle): active decision brain

```cpp
struct CombatPersonality {
    float aggression = 0.5f, caution = 0.5f;
    float blockBias = 0.5f, dodgeBias = 0.5f, counterBias = 0.5f;
    float minReactionTime = 0.20f, maxReactionTime = 0.40f;
    float decisionNoise = 0.10f;
};

struct IncomingThreat {
    EntityId attacker = 0;
    AbilityId ability = 0;
    double perceivedAt = 0.0, reactAt = 0.0;
    float estimatedTimeToImpact = 0.0f;
    bool blockable = false, dodgeable = false, valid = false;
};

struct AIWorkingMemory {
    EntityId combatTarget = 0;
    IncomingThreat incomingThreat;
    double lastEnemySeenTime = 0.0, lastCombatTime = 0.0;
    bool hasTarget = false;
    bool alerted = false;             // warn radius reached; investigating
    WorldPosition alertPosition {};
};

struct AIDefinition {                 // shared content; many NPCs reference one
    AIDefinitionId id = 0;
    std::string behaviorTreeName;
    CombatPersonality defaultPersonality;
    PerceptionProfileId defaultPerception;
    float defaultLeashRadius = 30.0f;
};
```

BehaviorTree.CPP tree instances, nodes, blackboards, allocators and library-owned objects stay in the AI runtime; [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] stores only a lightweight BrainHandle that refers to the runtime-owned brain.

| Stored in Flecs | Stored in the AI runtime |
| :---- | :---- |
| AIController, AIActive, AIWorkingMemory, CombatPersonality, target IDs, timers, aggro and leash state | BT::Tree instances, blackboards, node factories, per-brain random stream, tree-debug instrumentation |
| State other systems need or tools inspect | Implementation details needed to execute trees |

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Module boundaries|Module boundaries]] · [[Perception wake leash and sleep|Perception, wake, leash and sleep]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Data model · exported 2026-11-03
