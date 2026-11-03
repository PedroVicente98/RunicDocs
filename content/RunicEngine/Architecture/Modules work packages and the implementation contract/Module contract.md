---
title: "Module contract"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Module contract"
created: "2026-10-14"
modified: "2026-10-30"
---

Every C++ module in the three repositories has the same shape; a module inside a group nests under the group folder. Go packages follow the same idea with Go’s own layout: one directory per package, internal/ for private code, tests beside the code.

Engine/GameplayAPI/Combat/  
├── Public/                 \# the only headers other modules may include  
│   ├── CombatModule.hpp  
│   ├── Ability.hpp  
│   └── CombatEvents.hpp  
├── Source/                 \# implementation; each subsystem is a folder  
│   ├── Abilities/  
│   ├── Cooldowns/  
│   └── Damage/  
├── Tests/  
├── ARCHITECTURE.md         \# the module's contract  
└── CMakeLists.txt

Group folders are Foundation, SimulationCore, GameplayAPI, WorldSystems, Networking, Presentation and Tools; every module lives at Engine/\<Group\>/\<Module\>/.

* **Public/ is the compile boundary.** Library types ([[Simulation core Flecs and Jolt#Flecs rules|Flecs]], [[Simulation core Flecs and Jolt#Jolt rules|Jolt]], Godot and godot-cpp, BehaviorTree.CPP, Detour, [[Networking stack sessions and responsiveness#Stack (decided)|GameNetworkingSockets]]) never appear in a public header; they stay in Source/ behind Runic types. An exception is approved and recorded in the module’s ARCHITECTURE.md. Four are approved: GLM math types in Core’s public headers (the Engine’s math vocabulary), the Flecs world handle for modules that register systems into the simulation (for example AIModule), BehaviorTree.CPP node base types for Game custom AI nodes, and godot-cpp types in Runic::GodotTools’ public headers so the Game’s editor library can extend marker nodes and docks. Jolt, Detour and GameNetworkingSockets stay hidden, and Godot types appear nowhere else.

* **One target per module**, named Runic::\<Module\> in the Engine, RunicPlatform::\<Module\> in the Platform and RunicGame::\<Module\> in the Game. A group is an INTERFACE target that only links its modules. A module may also export one header-only interface target for an interface the Platform implements (Runic::NetworkTransport from Network, Runic::SimulationPort from Simulation); those headers include only Core types.

* **Allowed dependencies are a ceiling.** A package links only what it uses. A module dependency is PUBLIC only when its types appear in this module’s public headers; third-party libraries are PRIVATE except the approved exceptions (GLM is a PUBLIC dependency of Core).

* **Headless modules** never link libgodot, godot-cpp, [[How the Engine uses Godot|GodotBridge]], GodotTools, an audio backend or editor code. CI builds the server target alone and fails if any of them appears.

* **Explicit names.** Public files say what they hold (PhysicsWorld.hpp, never Types.hpp), and the namespace matches the module (Runic::Physics).

* **Tests live inside the module** and register with CTest. One C++ test framework, GoogleTest, is used in all three repositories (decided in slice [[Slice 00 Build skeleton|0]]); Go uses its standard testing package.

* **No Game content in public repositories.** Game rules, names and numbers never appear in Engine or Platform code, tests included; tests use neutral IDs such as engine:test\_ability.

\# Illustrative: one call per module. The helper creates the target and alias,  
\# wires Public/Source/Tests, warnings, test registration and the headless check.  
\# Combat at its final shape: DistributedSimulation is linked from [[CMB-8|CMB-8]]  
\# (foreign combat) on, because a package links only what it uses.  
runic\_add\_module(Combat  
    GROUP        GameplayAPI  
    PUBLIC\_DEPS  Runic::Gameplay Runic::Physics  
    PRIVATE\_DEPS Runic::DistributedSimulation  
    HEADLESS)

\# A group is an umbrella that only links its modules.  
add\_library(RunicGameplayAPI INTERFACE)  
target\_link\_libraries(RunicGameplayAPI INTERFACE  
    Runic::Gameplay Runic::Combat Runic::[[Scripted sequences GameplayFlow and restrictions|GameplayFlow]] Runic::Quest)  
add\_library(Runic::GameplayAPI ALIAS RunicGameplayAPI)

Each module’s ARCHITECTURE.md is written from its catalog row and the sections of this document that concern it, and changes in the same pull request as its code.

| ARCHITECTURE.md section | What it answers |
| :---- | :---- |
| Purpose | Why the module exists and what it provides |
| Public API | The headers and types other modules may use |
| Owns | State, lifetimes, threads, resources and meanings owned here |
| Does not own | Responsibilities that belong elsewhere |
| Allowed dependencies | Modules and libraries it may link |
| Forbidden dependencies | Links that would invert the architecture |
| Threading and tick model | Which threads and tick domains call it, and where mutation happens |
| Data ownership | Who owns authoritative state, caches, handles and IDs |
| Integration points | Commands, events, hooks and registries used to talk to other modules |
| Work packages | Its packages, each with acceptance tests and status |
| Future extensions | Work allowed later that must not leak into current packages |

---

↑ [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · ← [[Why the code is segmented this way|Why the code is segmented this way]] · [[Dependency rules|Dependency rules]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Module contract · exported 2026-11-03
