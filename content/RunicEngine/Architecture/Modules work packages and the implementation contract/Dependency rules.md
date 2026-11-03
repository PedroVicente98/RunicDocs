---
title: "Dependency rules"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Dependency rules"
created: "2026-10-14"
modified: "2026-10-30"
---

Dependencies point one way. RunicGame depends on the Engine and the Platform. The Platform implements Engine interfaces (the transport, the service port, and the services-bridge and lifecycle layers) and depends only on the Engine’s public interface headers. The Engine never includes Platform or Game code. Inside the Engine, low-level modules never depend on the feature modules that use them; a feature plugs in by registering into a registry or interface owned by the lower module.

The layered view in the Architecture overview shows the groups from bottom to top; the module catalogs under Repositories, build targets and processes list every module’s allowed dependencies.

| Forbidden dependency | Why |
| :---- | :---- |
| Engine → Platform or Game | Wrong direction: the Platform implements Engine interfaces and the Game composes both |
| Engine → [[Platform and operations#Simulation placement\|Agones]], Kubernetes, gRPC, NATS, databases | Engine code runs locally and headless with no infrastructure; the Platform supplies those layers |
| Physics → Combat, Gameplay or Game | Physics answers geometric questions; it never knows damage, factions, blocks or dodges |
| Physics ↔ [[How the Engine uses Godot\|GodotBridge]] | Physics extracts debug geometry as plain data and GodotBridge draws plain data; neither links the other |
| GodotBridge or Godot → Simulation or Physics state | Godot draws an extracted frame; it never becomes game logic |
| Simulation → feature modules or Game code | Gameplay modules and the Game register systems into the Simulation, which stays reusable |
| AI → direct combat, physics or persistence mutation | AI emits intents that become validated commands |
| [[Scripted sequences GameplayFlow and restrictions\|GameplayFlow]] or Quest → Combat or AI internals | Sequences act through Simulation commands and Gameplay APIs, the same doors players use |
| Platform → Game rules | The Platform stays reusable: mechanisms, never policy |
| Game client → server-only rules or content | The client gets presentation data and request contracts only |
| Region, Sector or Cell → simulation process identity | The world partition is stable; which simulation owns what is an operational decision |
| Any module → another module’s Source/ | Only Public/ headers cross a module boundary |
| Headless modules → libgodot, godot-cpp, GodotBridge, GodotTools, audio backend | The server stays headless |
| Domain modules → Godot or godot-cpp types | Godot is a presentation and tool library; only GodotBridge and GodotTools include it |
| GameClient → GodotTools or Godot’s editor build | Editor code never ships to players |
| Player UI scenes → [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] or simulation state | The UI reads world anchors from the [[RenderData in Core\|RenderFrame]] and content from Game view models |

---

↑ [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · ← [[Module contract|Module contract]] · [[Work packages|Work packages]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Dependency rules · exported 2026-11-03
