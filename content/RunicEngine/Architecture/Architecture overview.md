---
title: "Architecture overview"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Architecture overview"
created: "2026-10-14"
modified: "2026-10-30"
---

The Engine supplies generic mechanisms, the Game composes them into its two executables and its own services, and the Platform runs the shared services and infrastructure both depend on.

![[arch-architecture-overview-game-engine-platform.png]]
*Architecture overview — Game, Engine, Platform*

*Architecture overview — Game, Engine, Platform*

Arrows point from a part to what it builds on: the executables compose game modules, game code links the Engine and the Platform SDK, and the Platform transport implements the Engine’s transport interface.

## Layered view

![[arch-layered-architecture-game-engine-platform-infrastr.png]]
*Layered architecture — Game, Engine, Platform, infrastructure*

*Layered architecture — Game, Engine, Platform, infrastructure*

Read it as build dependencies: each band links only the bands below it, and nothing points up. RunicPlatform sits above the Engine because its C++ transport and server bindings include Engine interface headers; its Go services need no Engine code. Infrastructure is not a build dependency at all: Platform services and bindings reach it at runtime. Godot (libgodot) is a third-party library linked only by the presentation and tool modules.

## Ownership map

| Area | Engine | Game | Platform |
| :---- | :---- | :---- | :---- |
| Executables | Entry point, Application, ApplicationHost, reusable layers; the [[Tools#RunicEditor\|RunicEditor]] (the Godot editor through LibGodot) with [[Cooker\|the Cooker]] inside; the [[Tools#Testing at scale\|RunicBot]] | GameClient and GameServer compose the layers | Services-bridge and lifecycle layers (C++ server bindings) |
| Simulation | Scheduler, threads, [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]], [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]], world space | Which systems run and their rules | — |
| Skills and combat | GameplayAPI group (Gameplay and Combat modules): ability toolkit, hit timing, tags, statuses, rule pipeline, damage interception | Skill definitions, damage types and formula, resolver order, Stagger, [[Combat#Resolve hard and light CC\|Resolve]] and [[Combat#Conditions, build-up and Tolerance\|Tolerance]] | — |
| Defense and threat | Invulnerability windows, interception hooks, threat table | [[Defense Evasion Guard and armor#Evasion\|Evasion]] charges, [[Defense Evasion Guard and armor#Guard\|Guard]] modes, armor effects, taunt, Challenge | — |
| Custom code | Behavior registries, hooks, context and output buffers | The behaviors | — |
| Movement | CharacterVirtual, movement modes (walk, glide, flight in flight-zone volumes, mount), prediction, validation | Speeds, dashes, mount, glider and wing stats; flight zones | — |
| Light, perception, AI | The APIs, computation, behavior-tree framework and editor | Values, mob profiles, trees, custom nodes | — |
| Items and inventory | Runtime item and container mirrors | Item definitions, grades, upgrade rules; Inventory service rules (stacking, binding, trade limits) | Item ledger and currency wallets as mechanisms, with no game rules |
| Quests, economy, housing, factions | Interaction framework, [[Scripted sequences GameplayFlow and restrictions\|GameplayFlow]] sequences, Quest runtime with its quest-creation API | Quest definitions and encounter scripts; Go services that store quest progress and character state (including faction and crime) and run economy and housing | Go SDK they are built on |
| Scripted sequences and restrictions | GameplayFlow runtime, source-owned restrictions, presentation cues | Boss phases, cutscenes, dungeon and world-event scripts | — |
| Networking | Transport interface, replication, interest, prediction, handoff | Game messages | [[Networking stack sessions and responsiveness#Stack (decided)\|GameNetworkingSockets]] transport, Protobuf contracts, gRPC and NATS wiring |
| Accounts, world control, instances | — | Configuration; guild and mail services | Core services: accounts, entitlements, [[Platform and operations#Simulation placement\|World Coordinator]] (including placement by load and traffic), instance allocation, chat and party groups |
| Infrastructure and monitoring | Metrics recorded in every process (the Platform exports them) | Dashboards for game metrics | [[Platform and operations#Simulation placement\|Agones]], Kubernetes, Prometheus, Grafana |
| Presentation | Client runtime and extraction; [[How the Engine uses Godot\|GodotBridge]] on Godot (presenter, debug layers, world UI, UI binder, audio backend); assets, animation, audio | GameUI scenes, view models, game extraction, art | — |
| Tools and authoring | GodotTools: marker nodes, schema inspectors, region tools, docks, assistants, the Run button; the Cooker; the project template | The game’s marker nodes and docks (editor library); world and region scenes; spawn rules | — |
| Water and environment | [[Core model water reports facts\|WaterSystem]], buoyancy, water movement, wind, tides, waves, weather evaluation, wind and current routines, world routines | Water content, profiles, ship rules, weather patterns, wind and current routines and events, nautical charts | Weather, wind and current event directives with a duration; the Go SDK persistence that Game services use for durable water state |

---

↑ [[Architecture|Technical Architecture v4]] · ← [[About this document (Architecture)|About this document (Architecture)]] · [[Principles and performance targets|Principles and performance targets]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Architecture overview · exported 2026-11-03
