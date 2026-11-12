---
title: "Repositories, build targets and processes"
tags:
  - "architecture"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-12"
---

Three repositories and one CMake build graph: RunicGame owns the executables, the Engine and Platform are libraries and services it builds on, and the server never links rendering or player UI code.

### Repositories

| Repository | License | Owns |
| :---- | :---- | :---- |
| RunicEngine | Open source (C++) | Engine modules, the entry point and ApplicationHost, the RunicEditor (the Godot editor through LibGodot) with GodotTools and the Cooker, GodotBridge, the RunicBot, the project template; pins Godot and godot-cpp |
| RunicPlatform | Open source (C++ and Go) | GameNetworkingSockets transport, server bindings (services bridge and lifecycle layers), Protobuf contracts, Go SDK, core services, building blocks, Agones and Kubernetes manifests, dashboards |
| RunicGame | Closed source | GameClient and GameServer executables (RunicGameClient, RunicGameServer), game modules and the game’s editor library, Go game services, content; it is a RunicEngine project (project.godot, runic.project.json) |

RunicGame is the superproject: it pins RunicEngine and RunicPlatform as git submodules, which CI and releases build from. RunicPlatform pins RunicEngine the same way, so its C++ bindings build and test on their own. For daily work, a CMake option (RUNIC\_ENGINE\_DIR, RUNIC\_PLATFORM\_DIR) points at sibling checkouts instead. The Game’s executable targets are RunicGameClient and RunicGameServer; this document calls them GameClient and GameServer. RunicEngine pins Godot and godot-cpp as submodules at a release tag and builds libgodot from source in two targets (see [[Godot integration (Engine)|Godot integration]]).

### Engine modules

| Group | Module | Contains | Depends on | Headless | Packages |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Foundation | Runic::Core | Plain ID types, time types, math (GLM), memory, logging, config, worker pool, metrics registry, debug-stream registry; RenderData (plain render structs shared by the Client, GodotBridge and debug tools, including DebugGeometry and the debug-draw API) | — | yes | CORE-1 to CORE-7 |
| Foundation | Runic::Application | Entry point, Application, ApplicationHost (Run and RunFrame), LayerStack, loop policies, application events; no window class (the window comes from Godot) | Core | yes | APP-1 |
| Foundation | Runic::Events | Typed tick-safe event buffers and readers, multi-consumer delivery, stable event IDs | Core | yes | EVT-1 |
| Foundation | Runic::Content | Namespaced ContentId (engine:, game:), registries, versioned schemas, validation, loading, live reload | Core | yes | CNT-1, CNT-2 |
| Foundation | Runic::Assets | AssetId, handles, cache, native cooked formats, random-access packages with Zstandard decompression, manifests, client and server package selection, streaming | Core, Content | yes | ASSET-1, ASSET-2 |
| Simulation core | Runic::ECS | Flecs integration behind the Runic API, conventions, state declarations and their storage categories; the opt-in Runic::ECSNative target | Core; Flecs stays private, reachable only through Runic::ECSNative | yes | ECS-1, ECS-2 |
| Simulation core | Runic::World | 64-bit double coordinates (real Y, 1 cm minimum unit), worlds (WorldId), region-local origins, Regions, Sectors, sparse 3D Cells, authored volumes (including indivisible ones), spatial index and exact XYZ queries, activation volumes and streaming state | Core, ECS | yes | WORLD-1 to WORLD-3 |
| Simulation core | Runic::Physics | Jolt v5.6 in double precision behind Runic types: bodies, shapes, CharacterVirtual, queries, collision layers, debug-geometry extraction, the Jolt job system on the Core worker pool | Core, World (Jolt private) | yes | PHYS-1 to PHYS-5 |
| Simulation core | Runic::Simulation | SimulationRuntime: multi-rate scheduler, phases, barriers, commands, event flush, worker integration, client prediction subset, the replication registry, the service port (outgoing durable operations, accepted results applied at safe ticks; header-only Runic::SimulationPort target); the physics bridge (transforms and Physics handles in Flecs, sync around the step); the Simulation layer | Core, Application, ECS, Events, World, Physics, Content | yes | SIM-1 to SIM-8 |
| GameplayAPI | Runic::Gameplay | The attribute API and modifiers, resource pools, tags, the lifecycle API (Kill, death and kill facts), the relation hook, the movement-mode registry and modes, restrictions, interaction framework, item and equipment runtime, spawn and routine spawning | Simulation, Environment (wind for gliding) | yes | GPL-1 to GPL-8 |
| GameplayAPI | Runic::Combat | Ability toolkit and phase timelines, hit timing per skill, the input buffer, target slots and selection helpers, combat volumes and hit detection, status storage with Game application policies, cooldowns, rule pipeline, behavior registries, the impact pipeline, invulnerability restrictions, threat table, control primitives, foreign combat | Gameplay, Physics, Environment (projectile wind), DistributedSimulation | yes | CMB-1 to CMB-8 |
| GameplayAPI | Runic::GameplayFlow | Sequences with trigger, condition and action registries, timers on simulation time, presentation cues, source-owned cleanup, handoff policies | Gameplay, DistributedSimulation (handoff snapshot) | yes | FLOW-1 to FLOW-3 |
| GameplayAPI | Runic::Quest | Quest runtime and the quest-creation API: definitions, objectives, triggers from facts, instances, durable-fact bridge | GameplayFlow, DistributedSimulation (handoff snapshot) | yes | QST-1 to QST-3 |
| World systems | Runic::Perception | Light emitters, ambient and skylight, luminosity queries, concealment, warn and detect radii, visibility tiers chosen by a Game function | Gameplay, World, Environment (time of day, weather), Water (underwater light) | yes | PRC-1 to PRC-3 |
| World systems | Runic::Navigation | Detour and DetourTileCache runtime, nav tiles streamed by cell, path queries behind the MoveGoal contract, 3D flight paths for flying actors | World, Simulation, Assets (Detour private) | yes | NAV-1, NAV-2 |
| World systems | Runic::AI | BehaviorTree.CPP adapter, working memory, AI scheduling (wake, sleep, leash), intents to commands, reactive combat | Gameplay, Combat, Perception, Navigation (BehaviorTree.CPP private) | yes | AI-1 to AI-6 |
| World systems | Runic::Environment | Environment clock, wind and current routines (cyclic baseline, direction and signed speed), current modulation, tides, gameplay waves, weather state and time-boxed overrides, world routines (route positions from world time) | Core, World, Simulation | yes | ENV-1 to ENV-6 |
| World systems | Runic::Water | WaterSystem, bodies, rivers and routes, ocean current fields, cooked fragments, buoyancy, character, object and watercraft movement | World, Physics, Simulation, Gameplay, Environment, DistributedSimulation (ship-group handoff) | yes | WATER-1 to WATER-7 |
| Networking | Runic::Network | Transport interface (header-only Runic::NetworkTransport target), ingress and egress queues, all wire encoding (snapshots, quantization, deltas, simulation-link messages such as ghost deltas and transfers), interest and priority budgets, prediction and reconciliation, parallel replication, world transitions; the Network and Diagnostics layers | Application, Simulation, DistributedSimulation, Gameplay, Perception | yes | NET-1 to NET-8 |
| Networking | Runic::DistributedSimulation | Authority state and epochs, ghost state as plain data (Network encodes it), transfer (prepare, final snapshot, commit) with a snapshot-contributor registry that other modules register into, foreign-interaction contract, authority partitions that never cut indivisible volumes | Simulation, Events, World | yes | DSIM-1 to DSIM-5 |
| Presentation | Runic::Client | Client runtime: the Prediction and Presentation layers, the extractor registry and Engine extractors, camera, interpolation, input mapping and command builder; the RunicBot runtime | Application, Simulation, Network, Perception, Environment, Water, Animation, Audio, Assets | no | CLI-1 to CLI-9 |
| Presentation | Runic::GodotBridge | The GodotLayer (LibGodot instance, window, input), the presenter (RenderFrame to RenderingServer), debug layers, world UI (anchored, diegetic, batched), the view-model binder, the audio backend on the AudioServer; the production look later | Application, Client, Audio, Assets (libgodot and godot-cpp private) | no | GDB-1 to GDB-13 |
| Presentation | Runic::Animation | Skeletons, clips, animator, blending, poses (scope set by the open animation decision) | Core, Assets | no | ANIM-1 |
| Presentation | Runic::Audio | Backend interface (implemented by GodotBridge on the AudioServer), buses and mixing, semantic sound events, MusicDirector, albums, soundtrack presets, local profiles | Core, Assets | no | AUD-1, AUD-2 |
| Tools | Runic::GodotTools | RunicEditor plugins: marker nodes, schema inspectors and Runic file formats in the editor, world and region tools, docks (world, ECS, physics, resolver, AI editor on GraphEdit, live attach), the project template and assistants, Run orchestration, the export plugin that calls the Cooker | Most modules, Cooker (libgodot editor build and godot-cpp private) | never shipped | GDT-1 to GDT-16 |
| Tools | Runic::Cooker | Cooking orchestration and Runic format writers: Jolt cooking, Recast, meshoptimizer for collision, Zstandard; reads geometry from the scenes Godot imported; runs inside the RunicEditor and headless on build machines | Core, Content, Assets, World, Physics, Navigation, Water (each runtime module owns its cooked format; the Cooker links its writer) | tool | COOK-1 to COOK-8 |

Runic::GameplayAPI is the umbrella target of the GameplayAPI group: it links Gameplay, Combat, GameplayFlow and Quest so the Game links one name, while each module keeps its own boundary and tests.

Godot never reads Physics or the simulation: the client builds a list of what to show each frame (render extraction) and GodotBridge hands it to Godot. Physics debug drawing works the same way: Physics fills plain debug-geometry buffers defined in Core, and a GodotBridge debug layer draws them, so neither module links the other. Collision shapes and render meshes are different data.

### Game modules

| Target | Contains | Depends on |
| :---- | :---- | :---- |
| RunicGame::Shared | Rules compiled into both executables. GameCombat: skills mapped to the ability toolkit, the character’s attributes and pools and the death rule, status application policies and crowd control, damage types and formula, resolver order, impact stages and defense, targeting selectors and input-buffer settings, threat, relations (factions, PvE mode, Outlaw, pirates, groups), custom behaviors. GameBuilds: ten fixed loadouts, named classes (loadout \+ Discipline, one role each), weapon skills unlocked by level and one merged tree per class with points in the Discipline skills, context kits (mount and aerial trees), armor rules. Movement parameters, item rules, client-safe content definitions | Runic::GameplayAPI, Perception |
| RunicGame::Server | Server-only rules. GameCore registers Game systems, hooks and actions. GameWorld: continents, regions, volumes (caves, flight zones, castle zones), world rules, castles, world routines. GameAI: mob profiles, trees, custom nodes. GameQuests: quests built with the Quest API. GameEncounters: boss phases, dungeon scripts and cutscenes on GameplayFlow. GameNaval, GameInstances. GameExploration: death and respawn, durability, Altars, map knowledge, cartography and exploration XP. GameProduction (expansion): gathering, crafting, farming, professions, trade packs, labor. Spawns, loot, world events, service clients, persistence bridge | Shared, Runic::Simulation, Network, AI, Water, Environment; Platform server bindings and contracts |
| RunicGame::Client | GameClientPresentation: camera rules, animation, VFX and audio binding, cutscene presentation. GameUI: Godot UI scenes bound to view models, including the map with fog of war. Audio content, input bindings | Shared, Runic::Client, GodotBridge, Animation, Audio |
| RunicGame::Editor | The game’s marker nodes, docks and inspectors, built as the project’s editor library and loaded by the RunicEditor | Runic::GodotTools |
| GameServer (executable) | Composes the server layers: the Engine’s Network, Simulation and Diagnostics layers and the Platform’s services-bridge and lifecycle layers | RunicGame::Server, Runic::Application, Platform transport and server bindings |
| GameClient (executable) | Composes the client layers, the GodotLayer on top; links libgodot (template build) | RunicGame::Client, Runic::Application, Platform transport |
| Game services (Go) | Character (characters, builds — loadout, Discipline, skill points and level choices, with class and role derived — exploration XP and professions, faction and crime state, map knowledge (per Lineage), discovered Altars (per character), labor (per Lineage), account-wide collections); Inventory (rules over the Platform item ledger); Quest (stores progress, commits rewards); Economy and upgrades with a global auction house, the auction tax and the land fund; Trade; Guild; Mail; Housing and land; World events; Rankings; World routines (player-caused exceptions to routines) | Platform Go SDK, item ledger, wallets |
| Game content | Scenes, assets and data authored in the RunicEditor (Content/, Data/), split into Shared, Client and Server, cooked by the Cooker and exported as the client .pck | — |

### Platform modules (Platform)

| Module | Contains | Depends on | Packages |
| :---- | :---- | :---- | :---- |
| Transport (C++) | GameNetworkingSockets implementation of the Engine transport interface; connect-ticket checks; authoritative and candidate connections; simulation-to-simulation links chosen by locality (in-memory queue, local socket or shared memory, GameNetworkingSockets) | Runic::NetworkTransport (the Engine transport interface), Contracts | PTR-1 to PTR-4 |
| Contracts | Protobuf service APIs, published facts and the connect-ticket format, generated for C++ and Go; games add their own messages. Realtime messages are encoded by Runic::Network, not Protobuf | — | PCT-1 |
| Server bindings (C++) | ServicesBridgeLayer (implements the Engine service port with asynchronous gRPC and NATS; completions queued for safe ticks), LifecycleLayer (Agones SDK), Prometheus exporter for the Core metrics registry; they implement the Engine’s Layer interface | Engine interface targets only: Runic::Application (Layer), Runic::SimulationPort (service port), Runic::Core (metrics registry); Contracts | PBND-1 to PBND-4 |
| Go SDK | Service skeleton, configuration, gRPC and NATS wiring, persistence (PostgreSQL), transactions, migrations, idempotency store, metrics | Contracts | PSDK-1 to PSDK-3 |
| Core services (Go) | Accounts and entitlements, connect tickets, World Coordinator (worlds, regions and placement by load and traffic), instance allocation, world directives, chat and party groups, admission | Go SDK | PCS-1 to PCS-7 |
| Building blocks (Go) | Item ledger (containers, slots, atomic transfers, operation IDs), currency wallets and transfers that move items and currency in one transaction; mechanisms only, with no game rules | Go SDK | PBB-1 to PBB-3 |
| Infrastructure | Local development stack, Agones fleets, Kubernetes manifests, Prometheus and Grafana dashboards | — | PINF-1, PINF-2 |

### Processes

| Process | Owner | Runs | Shipped |
| :---- | :---- | :---- | :---- |
| GameClient | Game | Client layers on the Engine; Godot renders, plays audio and owns the window | Yes; shipping builds use Godot’s template build and no development overlay |
| GameServer | Game | Server layers on the Engine, one region per pod | Yes, to the server fleet |
| RunicEditor | Engine | The Godot editor with the Runic tools and the project’s editor library; attaches to development and staging servers | Never |
| Cooker | Engine | Inside the RunicEditor, or the RunicEditor headless on build machines | Never |
| RunicBot | Engine | The client runtime without presentation, many bot sessions per process, for scale tests | Never |
| Game services | Game | Go services built on the Platform SDK | Yes, to the server fleet |
| Platform services | Platform | Core services and building blocks | Yes, to the server fleet |

### Four axes that must stay separate

| Axis | Question it answers | Mechanism |
| :---- | :---- | :---- |
| Compile-time dependencies | Which code may use which code? | CMake targets |
| Process composition | Which coarse features run in this executable, and in what order? | ApplicationHost \+ LayerStack |
| Simulation scheduling | What simulation work runs now, and before what? | 60 Hz master scheduler, 30/20/10 Hz domains, explicit phases |
| Distributed topology | Which process owns this region or entity? | World Coordinator, SimulationOwner, authority epochs |

### Three event families

| Family | Examples | Delivery |
| :---- | :---- | :---- |
| Application events | Key press, resize, UI focus, connection state | LayerStack: top layer first, can be marked handled |
| Simulation facts | HitEvent, DamageEvent, EntityKilled, RegionChanged | Tick-safe buffers; every consumer receives them |
| Distributed messages | Quest facts, inventory operations, world-event directives | Transport, gRPC or NATS, with explicit reliability and idempotency |
