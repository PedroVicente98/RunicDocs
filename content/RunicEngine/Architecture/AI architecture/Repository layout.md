---
title: "Repository layout"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Repository layout"
created: "2026-10-14"
modified: "2026-10-30"
---

```text
RunicEngine/
  Engine/
    WorldSystems/AI/
      Public/   AIModule.hpp  AIComponents.hpp  AIDefinition.hpp  AIIntent.hpp
      Source/
        Runtime/        BehaviorTreeRuntime.cpp  BrainPool.cpp
        BehaviorTree/   Conditions.cpp  Actions.cpp  UtilityDecision.cpp
        Systems/        AggroSystem.cpp  AIPerceptionSystem.cpp  AIThinkSystem.cpp
                        AITargetSystem.cpp  AISleepSystem.cpp
      Tests/
    Tools/GodotTools/
      Source/AI/  AIDocks.cpp  BehaviorTreeGraph.cpp  NodePalette.cpp  TreeInspector.cpp
                  PersonalityEditor.cpp  RuntimeAIDebugger.cpp  AIValidation.cpp

RunicGame/
  Data/AI/
    basic_melee.xml  basic_archer.xml  personalities/  perception/  bosses/
  Source/Server/AI/
    GameSpecificAINodes.cpp
```

| Target | Content | Shipped in |
| :---- | :---- | :---- |
| Runic::AI | Generic runtime AI, [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] systems, tree adapter, definitions, intents and events | GameServer; GameClient only if client-side AI is ever needed |
| Runic::GodotTools (AI docks) | GraphEdit tree editor, inspectors, debug tools | [[Tools#RunicEditor\|RunicEditor]] only |
| RunicGame AI | Trees, personalities, perception profiles, game-specific nodes and rules | Game content and RunicGame::Server |

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Runtime AI debugging|Runtime AI debugging]] · [[Performance and scaling|Performance and scaling]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Repository layout · exported 2026-11-03
