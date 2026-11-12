---
title: "Modules, work packages and the implementation contract (Engine, Platform, Game)"
tags:
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-12"
---

The code is organized at two working sizes. A **module** is a build target with one owner, a public interface and its own tests; the dependency rules are written between modules. A **work package** is what one Claude Code session implements and one pull request delivers: one subsystem of one module, with its tests. Modules keep the architecture honest; packages keep each piece of work small enough to be built well.

### Sizes of work

| Size | What it is | Example | Who uses it |
| :---- | :---- | :---- | :---- |
| Group | A folder plus an umbrella build target that links related modules under one name; no code of its own | Runic::GameplayAPI \= Gameplay, Combat, GameplayFlow, Quest | The Game links one name; the documents categorize by it |
| Module | A CMake target with its own folder, public headers, tests and ARCHITECTURE.md; the unit of ownership and dependency | Runic::Combat | Other modules link it and include only its public headers |
| Subsystem | A folder inside a module’s Source/; not linkable on its own | Combat/Cooldowns | Only its own module |
| Work package | One Claude Code session and one pull request: a subsystem, or part of one, at a stated maturity stage, with its tests and docs | CMB-3: statuses, cooldowns and resource costs | You review and merge it; the roadmap lists it |

### Why the code is segmented this way

* **A session builds well what it can hold in mind at once.** One package needs the module’s ARCHITECTURE.md, the public headers of the modules it depends on and its own code. When a session must also design an interface, change neighboring modules or juggle several subsystems, shortcuts and inconsistencies appear.

* **The design decision stays with you.** The public interface and the acceptance tests are written and approved before the implementation. The implementing session then solves a closed problem: make these tests pass inside this folder.

* **One package writes inside one module.** When it needs something elsewhere, it reports the interface change instead of making it, so changes never ripple silently across the codebase.

* **Reviewable size.** As a rule of thumb a package changes at most about 1,500 to 2,500 lines, which fits a careful review of about 30 minutes. Bigger changes get skimmed, and skimmed code is where defects hide.

* **Modules stay coarse on purpose.** Many tiny libraries add build, link and dependency overhead without making the code better. Big modules are split into packages, not into more libraries; a subsystem becomes its own module only when build isolation or reuse proves it necessary.

* **Progress is visible and testable.** Every roadmap slice lists the packages it needs, so done means specific packages merged with green tests.

* **Independent packages run in parallel.** Packages whose prerequisites are merged can be built at the same time in separate sessions.

### Module contract

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

* **Public/ is the compile boundary.** Library types (Flecs, Jolt, Godot and godot-cpp, BehaviorTree.CPP, Detour, GameNetworkingSockets) never appear in a public header; they stay in Source/ behind Runic types. An exception is approved and recorded in the module’s ARCHITECTURE.md. Three are approved: GLM math types in Core’s public headers (the Engine’s math vocabulary), BehaviorTree.CPP node base types for Game custom AI nodes, and godot-cpp types in Runic::GodotTools’ public headers so the Game’s editor library can extend marker nodes and docks. Modules register components, states, systems and queries through Runic types (see [[Simulation core Flecs and Jolt (Engine)#The Runic API over Flecs and Jolt|The Runic API over Flecs and Jolt]]); the Flecs world itself is reachable only through the opt-in Runic::ECSNative target, which is discouraged, and the configure-time dependency check lists every module that links it. Jolt, Detour and GameNetworkingSockets stay hidden, and Godot types appear nowhere else.

* **One target per module**, named Runic::\<Module\> in the Engine, RunicPlatform::\<Module\> in the Platform and RunicGame::\<Module\> in the Game. A group is an INTERFACE target that only links its modules. A module may also export one header-only interface target for an interface the Platform implements (Runic::NetworkTransport from Network, Runic::SimulationPort from Simulation); those headers include only Core types.

* **Allowed dependencies are a ceiling.** A package links only what it uses. A module dependency is PUBLIC only when its types appear in this module’s public headers; third-party libraries are PRIVATE except the approved exceptions (GLM is a PUBLIC dependency of Core).

* **Headless modules** never link libgodot, godot-cpp, GodotBridge, GodotTools, an audio backend or editor code. CI builds the server target alone and fails if any of them appears.

* **Explicit names.** Public files say what they hold (PhysicsWorld.hpp, never Types.hpp), and the namespace matches the module (Runic::Physics).

* **Tests live inside the module** and register with CTest. One C++ test framework, GoogleTest, is used in all three repositories (decided in slice 0); Go uses its standard testing package.

* **No Game content in public repositories.** Game rules, names and numbers never appear in Engine or Platform code, tests included; tests use neutral IDs such as engine:test\_ability.

\# Illustrative: one call per module. The helper creates the target and alias,  
\# wires Public/Source/Tests, warnings, test registration and the headless check.  
\# Combat at its final shape: DistributedSimulation is linked from CMB-8  
\# (foreign combat) on, because a package links only what it uses.  
runic\_add\_module(Combat  
    GROUP        GameplayAPI  
    PUBLIC\_DEPS  Runic::Gameplay Runic::Physics  
    PRIVATE\_DEPS Runic::DistributedSimulation  
    HEADLESS)

\# A group is an umbrella that only links its modules.  
add\_library(RunicGameplayAPI INTERFACE)  
target\_link\_libraries(RunicGameplayAPI INTERFACE  
    Runic::Gameplay Runic::Combat Runic::GameplayFlow Runic::Quest)  
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

### Dependency rules

Dependencies point one way. RunicGame depends on the Engine and the Platform. The Platform implements Engine interfaces (the transport, the service port, and the services-bridge and lifecycle layers) and depends only on the Engine’s public interface headers. The Engine never includes Platform or Game code. Inside the Engine, low-level modules never depend on the feature modules that use them; a feature plugs in by registering into a registry or interface owned by the lower module.

The layered view in the Architecture overview shows the groups from bottom to top; the module catalogs under Repositories, build targets and processes list every module’s allowed dependencies.

| Forbidden dependency | Why |
| :---- | :---- |
| Engine → Platform or Game | Wrong direction: the Platform implements Engine interfaces and the Game composes both |
| Engine → Agones, Kubernetes, gRPC, NATS, databases | Engine code runs locally and headless with no infrastructure; the Platform supplies those layers |
| Physics → Combat, Gameplay or Game | Physics answers geometric questions; it never knows damage, factions, blocks or dodges |
| Physics ↔ GodotBridge | Physics extracts debug geometry as plain data and GodotBridge draws plain data; neither links the other |
| GodotBridge or Godot → Simulation or Physics state | Godot draws an extracted frame; it never becomes game logic |
| Simulation → feature modules or Game code | Gameplay modules and the Game register systems into the Simulation, which stays reusable |
| AI → direct combat, physics or persistence mutation | AI emits intents that become validated commands |
| GameplayFlow or Quest → Combat or AI internals | Sequences act through Simulation commands and Gameplay APIs, the same doors players use |
| Platform → Game rules | The Platform stays reusable: mechanisms, never policy |
| Game client → server-only rules or content | The client gets presentation data and request contracts only |
| Region, Sector or Cell → simulation process identity | The world partition is stable; which simulation owns what is an operational decision |
| Any module → another module’s Source/ | Only Public/ headers cross a module boundary |
| Headless modules → libgodot, godot-cpp, GodotBridge, GodotTools, audio backend | The server stays headless |
| Domain modules → Godot or godot-cpp types | Godot is a presentation and tool library; only GodotBridge and GodotTools include it |
| GameClient → GodotTools or Godot’s editor build | Editor code never ships to players |
| Player UI scenes → Flecs or simulation state | The UI reads world anchors from the RenderFrame and content from Game view models |

### Work packages

A package ID is the module prefix plus its build order inside the module: CMB-3 is the third Combat package. Every package is defined by five things:

* **Write scope:** one module folder, its CMake target and its docs. Nothing else is edited.

* **Interface change:** the public headers it adds or changes, approved before the implementation.

* **Done when:** the acceptance behavior, written as automated tests.

* **Needs:** the packages that must be merged first. A package starts only when all of them are merged.

* **Slice:** the roadmap slice that first needs it. Packages are Stage A unless the table says otherwise (see [[Modules, work packages and the implementation contract (Engine, Platform, Game)#Maturity stages|Maturity stages]]).

Big modules carry several packages; small ones one or two. The tables cover every package through the current roadmap; expansion packages (slice 44 onward) get their full definition when those slices are planned.

**Prefixes.** Engine: BUILD build skeleton, CORE Core, APP Application, EVT Events, CNT Content, ASSET Assets, ECS, WORLD World, PHYS Physics, SIM Simulation, GPL Gameplay, CMB Combat, FLOW GameplayFlow, QST Quest, PRC Perception, NAV Navigation, AI, ENV Environment, WATER Water, NET Network, DSIM DistributedSimulation, CLI Client, GDB GodotBridge, ANIM Animation, AUD Audio, GDT GodotTools, COOK Cooker. Platform: PCT Contracts, PTR Transport, PSDK Go SDK, PBND Server bindings, PCS Core services, PBB Building blocks, PINF Infrastructure. Game: GAME executables, GSH Shared rules, GSRV Server module, GCL Client module, GCNT content, GSVC Go game services, GNAV naval rules, GWTH weather rules.

#### Engine: foundation

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| BUILD-1 | Build skeleton in all three repositories: runic\_add\_module helper, presets, CI, the chosen test framework, automated headless and forbidden-dependency checks, submodule pins (Game pins Engine and Platform; Platform pins Engine; Engine pins Godot and godot-cpp at a release tag) with a local option for sibling checkouts, an AVX2 (x86-64-v3) CPU baseline; libgodot built from source in the editor and template targets with the module lists and the SCons cache; libgodot, godot-cpp, GodotBridge and GodotTools catalogued as presentation | Every repository configures and builds; libgodot builds in both targets; the server target links no graphics library and no Godot; a forbidden link fails CI | — | 0 |
| CORE-1 | Plain ID types (GlobalEntityId, GlobalPlayerId, SimulationId, WorldId, TickId, AuthorityEpoch, and value types other modules give meaning to, such as AssetId, WaterBodyId, FieldId and WidgetId), Result, asserts, logging hooks, time types, GLM math | Unit tests cover IDs, Result and time conversions | BUILD-1 | 1 |
| CORE-2 | Worker pool, metrics registry (per-tick timings and counters) and debug-stream registry where modules publish traces | Jobs run on the pool; metrics are recorded per tick domain | CORE-1 | 3 |
| CORE-3 | RenderData foundation: the double-buffered RenderFrame and DebugGeometry (lines, triangles, text, cached debug meshes) | A frame is written on one thread and read on another with no lock; debug vertices need no conversion before upload | CORE-1 | 5 |
| CORE-4 | RenderData scene kinds: mesh instances with a stable RenderInstanceId, skinned instances with pose buffers and animation intent, world anchors | Every kind round-trips through a frame packet in tests | CORE-3 | 22 |
| CORE-5 | RenderData world-state kinds: lights, environment frame, volumes | Every kind round-trips through a frame packet in tests | CORE-3 | 25a |
| CORE-6 | RenderData water and field kinds: water surface state, field grids | Versions change only when their source changes | CORE-3 | 42a |
| CORE-7 | RenderData effect kinds: particles, decals, trails | Defined when the production look is planned | CORE-3 | 44+ |
| APP-1 | Entry point, Application, ApplicationHost, Layer, LayerStack with queued changes at safe points, application events, loop policies, RunFrame so a host can drive one frame at a time | Layer order, events top-down until handled, updates bottom-up, safe-point push and pop, no allocation per event | CORE-1 | 1 |
| EVT-1 | Typed tick-safe event buffers and readers, multi-consumer delivery, stable event IDs (SimulationId plus sequence) | Two consumers read the same fact; IDs stay stable on replay | CORE-1 | 4 |
| CNT-1 | ContentId with engine: and game: namespaces, registries, lookup | Duplicate and unknown IDs are reported with their source | CORE-1 | 9 |
| CNT-2 | Versioned schemas, validation, loading, live-reload hooks | A changed definition reloads without a restart | CNT-1 | 20 |
| ASSET-1 | AssetId, handles, cache, loading of native cooked mesh and collision formats | A cooked test mesh loads on client and server | CNT-1 | 9 |
| ASSET-2 | Random-access packages and manifests with Zstandard decompression, client and server package selection, asynchronous streaming | Cells load from a package without stalling a tick or a frame | ASSET-1, WORLD-3 | 21 |

#### Engine: simulation core

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| ECS-1 | Flecs world wrapper on Flecs 4.2; component, system and query registration through Runic types; conventions; the opt-in Runic::ECSNative target | Entities are created, queried and destroyed through Runic types; Flecs types appear only in Runic::ECSNative, and the configure check lists every module that links it | CORE-1 | 4 |
| ECS-2 | State declarations: one declaration per state, whose category picks its Flecs storage (hot flag as a toggle, fact with a target as a relationship with DontFragment for high-cardinality targets, content flag as a bit in a compact per-entity container, value as a container field, derived as a computed condition), with owner, observable, visibility and lifetime fields; a benchmark harness for tag, toggle, container and DontFragment | A state of each category is set, read and cleared through the API, and hot and content flags never move the entity to another table; observable states emit StateEntered and StateExited facts; the benchmark reports nanoseconds per operation and milliseconds per tick for 2,000 entities, recorded in the package docs | ECS-1, EVT-1 | 4 |
| WORLD-1 | 64-bit double coordinates (real Y, 1 cm minimum unit), WorldId, region-local origins, Region, Sector and sparse 3D Cell keys | Conversions round-trip exactly far from the origin; a cell key round-trips at any altitude or depth | ECS-1 | 4 |
| WORLD-2 | Sparse 3D spatial index (XZ columns holding only occupied Y cells), exact XYZ candidate queries (radius, box, ellipsoid), membership updates; authored volumes (caves, rule areas, indivisible volumes) with point-in-volume queries; the volume kind picks the backend (static rule areas in the index, a volume that moves with an entity as a Physics sensor) | Query results match brute force in 3D and draw in the debug view; a point inside a cave volume is reported inside it; a static rule area creates no Physics body | WORLD-1 | 11 |
| WORLD-3 | Activation: per-player asymmetric ellipsoid activation volumes, their union, prepare, commit and release hysteresis, load and unload requests per cell | Walking back and forth on an edge never thrashes loads; a cell far above or below the player stays unloaded until approached | WORLD-2 | 21 |
| PHYS-1 | PhysicsWorld, bodies, shapes and collision layers on Jolt v5.6 in double precision, kept private | Bodies collide without jitter far from the origin | WORLD-1 | 7 |
| PHYS-2 | CharacterVirtual integration and ground movement | A capsule walks, climbs steps and stops at walls | PHYS-1 | 7 |
| PHYS-3 | Debug-geometry extraction: Jolt’s debug interface implemented inside Physics, written into Core DebugGeometry buffers | Bodies and shapes come out as plain lines and triangles; Physics links no GodotBridge | PHYS-1, CORE-3 | 8 |
| PHYS-4 | Jolt job system on the Core worker pool: a JobSystem adapter inside Physics, so Jolt never owns threads | A physics step on the pool matches a single-thread step; no thread is created outside the pool | PHYS-1, CORE-2 | 10 |
| PHYS-5 | Gameplay queries: ray, shape cast, overlap, per-worker query queues | Results are identical for a fixed scene with any worker count | PHYS-1, SIM-3 | 15 |
| SIM-1 | SimulationRuntime: 60 Hz master clock, 30/20/10 Hz domains, TickContext, the Simulation layer, domain metrics | Domain tick counts stay exact over a long run, with no drift | APP-1, CORE-2 | 3 |
| SIM-2 | Phases, commands and command queue, deferred mutation, event flush at barriers | Commands apply in phase order; facts are visible to the next phase | SIM-1, ECS-1, EVT-1 | 5 |
| SIM-3 | Phases on the worker pool, per-worker buffers, deterministic merge; the physics step runs through PHYS-4 | The same scene with one worker and with many gives identical results | SIM-2, PHYS-4 | 10 |
| SIM-4 | Client prediction subset: selected systems run on the client with RunicGame::Shared | The same inputs give the same result on client and server | SIM-3 | 14 |
| SIM-5 | Service port: an outbox of durable operations with stable operation IDs and an inbox of accepted results drained at safe ticks; the Engine interface the Platform services bridge implements, shipped as the header-only Runic::SimulationPort target (Core types only) | A fake port that delivers a result twice is applied once; no I/O callback touches Flecs | SIM-2, EVT-1 | 27 |
| SIM-6 | Replication registry: modules register replicated components and world-state values (schema, quantization profile, relevance); Network encodes only what is registered | A test component and a world-state value replicate without Network depending on the modules that own them | SIM-2 | 13 |
| SIM-7 | Behavior counters: modules and the project register small per-player counters (histograms, counts, route fingerprints). The Simulation keeps them in fixed memory and flushes one compact summary per player per interval through the service port. Enqueue only; when the queue is full the oldest summaries are dropped and counted. | Summaries flush on the interval with no measurable tick cost, and a RunicBot session shows in them | SIM-5, CLI-9 | 39 |
| SIM-8 | Physics bridge: Flecs holds transforms and opaque Physics handles; a sync phase writes kinematic targets and character movement before the step and transforms back after it; body creation and removal follow their entities at the barrier; contact and sensor callbacks only fill buffers read as facts in the next phase | The capsule’s Flecs transform matches its CharacterVirtual after every step; destroying an entity removes its body at the next barrier; a contact reaches the next phase as a fact and no callback touches Flecs | SIM-2, PHYS-2 | 7 |

#### Engine: GameplayAPI group

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| GPL-1 | Movement-mode registry and modes (walk, sprint, dash hook, glide, mount; Water registers swimming) with movement parameters from data; gliding reads wind once ENV-2 provides it | Modes switch without teleporting; parameters come from Game data | PHYS-2 | 14 |
| GPL-2 | Attribute API and modifiers: attributes the Game declares (ID, type, default, limits, replication, prediction) plus the Engine’s own movement and interaction attributes; modifier stacks with a replaceable aggregation; resource pools with a regeneration scheduler that runs Game rules; tags; the lifecycle API Kill(entity, source), which emits the death and kill facts (Combat fills in the source); the relation hook | Modifier order is deterministic; pools clamp; a test game declares Health and dies through Kill; the Engine declares no game attribute | SIM-2, CNT-1 | 15 |
| GPL-3 | Restrictions: source-owned restriction sets, acquire and release by source, command-validation hooks | Blocked commands are rejected on the server; releasing a source clears everything it held | GPL-2 | 18 |
| GPL-4 | Item and equipment runtime that mirrors ledger containers | Equipping changes modifiers; the mirror matches the ledger after a reload | GPL-2 | 28 |
| GPL-5 | Interaction framework: interactables, reservation, interaction facts | Two players cannot reserve the same target | GPL-2, EVT-1 | 29 |
| GPL-6 | Spawn primitives, including spawn areas driven by rule data over cooked candidate points | A spawner keeps its population; a spawn area keeps its rule’s count and refills by elapsed time when its cell loads | GPL-2, COOK-3 | 31 |
| GPL-7 | Flight and climbing movement modes: flight, glide and climbing as separate modes, the modes each mount or vehicle can use set by data, flying vehicles, climbing mounts; mode permission through restrictions and Game rules | A Game rule that forbids flight hands over to gliding; a restriction blocks both; a mount climbs a marked wall | GPL-1, GPL-3, WORLD-2, ENV-2 | 44+ |
| GPL-8 | Routine spawning: when a cell activates, routine entities (escorts, caravans, ships, mob routines) spawn where their routine puts them; stored exceptions override the routine and fade back into it | A caravan appears at the right point of its route when a player arrives; a delayed escort rejoins its routine over time | GPL-6, ENV-6, WORLD-3 | 43a |
| CMB-1 | Ability toolkit: timelines of named phases from data, phase lengths set by a Game hook when the ability starts, phase events, cancel requests and phase-time adjustment, a release input routed to the active ability; hit timing per skill (ServerTime, CappedRewind) | Timeline phases fire on exact ticks; a Game hook lengthens a phase | GPL-2, CNT-1 | 16 |
| CMB-2 | Targeting: target slots the Game names, selection helpers (under the aim ray, nearest in a cone, cycling a filtered list), targets in the command payload checked for range, line of sight and relation, aim-assist and homing hooks; combat volumes and hit detection over Physics queries, with each hit target’s relation | A melee arc and a projectile each hit a dummy exactly once; a target out of range or out of sight is rejected | CMB-1, PHYS-5 | 16 |
| CMB-3 | Status storage (instances, timers, periodic ticks, apply, refresh and remove, events, queries by tag, replication), every application going through a policy the Game registers; cooldowns with shared groups and charges; costs as a list against Game pools | Durations, ticks and cooldowns expire on the right tick; two test policies (refresh and intensity stacking) change the result with no Engine change; a shared cooldown group behaves as a global cooldown | CMB-1 | 17 |
| CMB-4 | Rule pipeline and behavior registries (fixed hooks for Game code); value variants selected by a per-hit context the Game defines | A test rule and a test behavior run in order; a value with a base and a contextual variant resolves by the hit context; the Engine holds no game rule | CMB-3 | 17 |
| CMB-5 | Impact pipeline: hits become impacts with Game-defined fields and run through Game-registered stages in order; invulnerability as a restriction that ignores impacts by tag | Stages run in registration order; an invulnerability restriction blocks tagged impacts; the Engine applies no damage of its own | CMB-4, GPL-3 | 18 |
| CMB-6 | Threat table and control primitives: control restriction sets (input, movement, abilities), forced motion (push, launch, pull) through Movement, control-state hooks | A test policy built on statuses and primitives stuns and knocks back a dummy; threat orders an NPC’s targets | CMB-5 | 19 |
| CMB-7 | Input buffer: depth, window and priority classes set by the Game; a buffered action starts on the first legal tick and is validated then; priority inputs skip it when the current ability allows the cancel | An early input fires on the first legal tick; a restriction in between cancels it | CMB-1, SIM-4 | 19 |
| CMB-8 | Foreign combat: volumes crossing an authority border become requests to the owner | The target is damaged exactly once, by its owner | CMB-5, DSIM-4 | 37 |
| CMB-9 | Combat behavior samples: reaction time from a telegraph cue to the defense input's view-time stamp (the server estimates when the cue could first be shown to that client from the fact's send tick and the client's latency), and aim error against player targets, recorded into the behavior counters. No extra traffic. | A scripted defender that reacts instantly produces a reaction histogram at zero; a delayed one shows its delay | SIM-7, CMB-5 | 39 |
| FLOW-1 | Sequence runtime: trigger, condition and action registries, scheduler, timers on simulation time | A sequence waits, branches and acts only through commands and Gameplay APIs | GPL-5 | 29 |
| FLOW-2 | Termination path, restriction ownership, watchdog, presentation cues | Complete, abort, timeout, disconnect and shutdown all release everything the sequence held | FLOW-1, GPL-3 | 29 |
| FLOW-3 | Handoff policies and sequence state in the transfer snapshot | Transferable keeps its timers; PinAuthority blocks transfer; AbortOnTransfer cleans up | FLOW-2, DSIM-3 | 37 |
| QST-1 | Quest runtime and quest-creation API: definitions, objectives, triggers from facts, instances | A quest defined only in data advances from kill and interaction facts | FLOW-1 | 30 |
| QST-2 | Durable bridge: outgoing quest facts with stable IDs through the service port; accepted results applied at safe ticks | A replayed fact never doubles progress; no service callback touches Flecs | QST-1, SIM-5 | 30 |
| QST-3 | Quest instances registered as a transfer-snapshot contributor | A quest in progress crosses a simulation border with its objectives and timers intact | QST-1, DSIM-3 | 37 |

#### Engine: world systems

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| PRC-1 | Light: emitters, ambient profiles, skylight curve driven by the Environment clock, luminosity at a point | Luminosity matches emitter falloff; client and server agree | WORLD-2, GPL-2, ENV-1 | 25 |
| PRC-2 | Visibility tiers as data (what each tier sends), picked per pair by a Game-registered function, with a reveal hook | Tiers change with a test function’s distances and light levels | PRC-1 | 25 |
| PRC-3 | Perception profiles: warn and detect radii from light and concealment, with a minimum | Radii shrink with darkness and stealth but never below the minimum | PRC-1 | 33 |
| NAV-1 | Detour runtime, nav tiles streamed by cell, path queries behind MoveGoal | Paths cross cell borders; tiles load and unload with cells | WORLD-3, COOK-6 | 31 |
| NAV-2 | Flight navigation: 3D paths through free space over the sparse cells for flying actors, respecting volumes and altitude ceilings | A flying NPC reaches a target behind an obstacle without entering a forbidden volume | NAV-1, WORLD-2 | 44+ |
| AI-1 | AI contracts and runtime shell: components, intents, working memory, AIDefinition, BehaviorTree.CPP adapter, brain pool, wake and sleep | A test tree ticks only while its NPC is awake | GPL-2, SIM-3 | 32 |
| AI-2 | Command bridge and data assets: intents become movement and combat commands; tree loading, registries, personality profiles | AI commands pass the same validation as player commands | AI-1, NAV-1, CMB-2 | 32 |
| AI-3 | Perception lifecycle: Aggroable, warn and detect wake, target validation, leash, return home, sleep | A mob walks toward a warning, attacks on detection and returns past its leash | AI-1, PRC-3 | 33 |
| AI-4 | Reactive combat: SkillStarted perception, incoming threat, reaction timer, defense choice | A mob answers a telegraphed skill with a defensive action within its reaction time | AI-2, CMB-5 | 34 |
| AI-5 | Instrumentation: per-brain trace, memory, utility and intent diagnostics | The trace explains each decision | AI-2 | 34 |
| AI-6 | Scale tests with thousands of loaded NPCs and controlled awake percentages | The tick budget holds at the target counts | AI-4 | 38 |
| ENV-1 | Environment clock: world time, day and night phase, sun direction and the skylight input Perception reads; the world epoch comes from configuration until PCS-2 issues it | Two simulations agree on the time of day; night starts at the same world time everywhere | SIM-1, WORLD-1 | 25 |
| ENV-2 | Deterministic wind field with a cyclic baseline routine: per-region direction at any angle and a signed speed (0 has no effect; a negative speed reverses the push without changing the angle) | The same position and time give the same wind on two simulations; a negative speed reverses the push without changing its angle | ENV-1 | 42 |
| ENV-3 | Current modulation over time: cyclic baseline routine, tide phase, season, weather | Every simulation samples the same current at the same time | ENV-1, WATER-5 | 42 |
| ENV-4 | Tides and gameplay waves | A tide opens and closes a path on schedule | ENV-1 | 43 |
| ENV-5 | Weather state and time-boxed overrides (effective time and duration) for weather, wind and currents; the baseline routine returns when they end | A storm and a wind event reach two simulations at the same world time and end on schedule, after which the routine resumes | ENV-1 | 43 |
| ENV-6 | World routines: cooked routes and schedules evaluated as position \= f(route, world time, seed), with slow deterministic drift (a cycle that does not match the clock plus a small seeded variation) | Two simulations compute the same routine position at the same world time, drift included | ENV-1 | 43a |
| WATER-1 | WaterSystem registry, planar water, WaterSample, cell fragments | Height and flow can be sampled anywhere; fragments load with cells | WORLD-3, PHYS-1 | 40 |
| WATER-2 | Spline rivers, flow, connections and routes | A descending river crosses two cells without a seam | WATER-1 | 40 |
| WATER-3 | BuoyantBody on Jolt bodies, with an optional righting strength | A platform floats without drifting | WATER-1 | 41 |
| WATER-4 | Character and object water movement | A crate drifts with the current; a character swims with current influence | WATER-3, GPL-1 | 41 |
| WATER-5 | Ocean current fields from cooked vector grids | Current interpolates smoothly across the grid | WATER-1 | 42 |
| WATER-6 | WatercraftMovement: sail force, sail angle, lateral resistance | Faster downstream and with a favorable wind; a crosswind pushes sideways | WATER-4, ENV-2 | 42 |
| WATER-7 | Ship-group handoff: a watercraft, its crew, passengers and cargo registered as one transfer-snapshot group | A ship with passengers and cargo crosses a simulation border with nothing lost or left behind | WATER-6, DSIM-3 | 42b |

#### Engine: networking

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| NET-1 | Transport interface, tick-safe ingress and egress queues, connect-ticket hook, the Network layer; the interface and hook ship as the header-only Runic::NetworkTransport target (Core types only) | A loopback transport passes ping and echo tests | SIM-1 | 12 |
| NET-2 | Snapshots: extraction, quantization, deltas against the last acknowledged state, interpolation buffers | Two clients see each other move smoothly under packet loss | NET-1, SIM-6 | 13 |
| NET-3 | Prediction and reconciliation: input history, replay, blend or snap | Movement stays responsive under simulated lag; corrections show in the debug view | NET-2, SIM-4 | 14 |
| NET-4 | Interest: candidates by cell, priority and budgets, visibility tiers applied, detail levels per component and the client’s focus hint | Only relevant entities arrive and per-client budgets hold; a focused entity arrives with its full detail level | NET-2, WORLD-2, PRC-2 | 25 |
| NET-5 | Simulation links: ghost deltas and transfer messages encoded with the snapshot codec over simulation-to-simulation connections | Ghosts stay in sync across a border under packet loss; a message with a stale epoch is dropped | NET-2, DSIM-2 | 36 |
| NET-6 | Parallel replication and the degradation order | 500 bots in one region fit the per-client budget | NET-4, SIM-3 | 38 |
| NET-7 | Diagnostics layer: network and replication metrics recorded in the Core metrics registry; RunicEditor attach channel over a development socket transport inside Network, streaming debug shapes and the traces modules publish in Core’s debug-stream registry (compiled only into development and staging builds) | The RunicEditor attaches to a development server and sees its shapes; a production build has no attach endpoint | NET-1, CORE-2 | 39 |
| NET-8 | World transitions: the session leaves one world’s simulation after a checkpoint and joins another world’s simulation with a new connect ticket; no handoff or ghosts across worlds | A character moves between two worlds with its checkpointed state, and the old simulation keeps no copy | NET-1, SIM-5, PCS-1 | 44+ |
| NET-9 | Client-integrity channel: opaque messages between a client-side and a server-side integrity provider (a commercial anti-cheat), on their own lane with a budget; a server hook lets the provider close a connection. No provider types in public headers. | A test provider exchanges messages through the channel and closes a connection it rejects | NET-1 | 44+ |
| NET-10 | Occlusion-aware interest: a hostile player is sent only when it could become visible to the client soon (precomputed visibility per cell plus a short margin), so wallhacks have nothing to draw. | Defined when PvP measurements show wallhack ESP is a real problem | NET-4 | 44+ |
| DSIM-1 | Authority state, epochs, GlobalEntityId mapping | Messages with a stale epoch are rejected | SIM-2 | 36 |
| DSIM-2 | Ghosts: ghost state near borders as plain data; Network encodes the deltas (NET-5) | Ghosts follow their owners near the border | DSIM-1 | 36 |
| DSIM-3 | Transfer: prepare, final snapshot, authority commit; a snapshot-contributor registry where modules add their state (sequences, quests, ship groups) | A player walks from A to B with no loading screen; the input sequence continues | DSIM-2 | 36 |
| DSIM-4 | Foreign-interaction contract | A request carries enough context for the owner to resolve it | DSIM-1 | 37 |
| DSIM-5 | Authority partitions inside one region (busy areas such as a city) that never cut an indivisible volume (an island, a castle, a docked ship) | Two simulations share a city, each entity has one owner, and no indivisible volume is split | DSIM-3 | 44+ |

#### Engine: presentation

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| CLI-1 | Presentation layer and extractor registry; the first extractor writes entities as debug shapes; camera | Entities are drawn from the RenderFrame only | ECS-1, GDB-2, CORE-3 | 5 |
| CLI-2 | Input mapping, actions and command builder over the AppEvents the GodotLayer forwards: modifiers, chords, press and release events, and the layouts and presets the Game defines | Key presses become movement commands; a modifier plus a key maps to its own action; input Godot’s UI consumed never reaches them | GDB-1, SIM-2 | 7 |
| CLI-3 | Prediction layer driving the prediction subset and reconciliation each frame | The local player moves at once and corrects on server state | SIM-4, NET-3 | 14 |
| CLI-4 | Mesh-instance extractor with interpolation, camera-relative conversion and a stable RenderInstanceId | Cooked meshes appear at their entities’ positions far from the origin | CLI-1, CORE-4 | 22 |
| CLI-5 | Skinned-instance extractor with poses or animation intent, per the open animation decision | Characters animate on screen | CLI-4, ANIM-1 | 23 |
| CLI-6 | World-anchor extractor: position, distance, visibility tier and priority per entity | Anchors follow entities; an entity in a tier without anchors produces none | CLI-1, CORE-4 | 23a |
| CLI-7 | Light, environment and volume extractors from Perception and Environment | Darkness and torches on screen match the server’s light values | CLI-1, CORE-5, PRC-1 | 25a |
| CLI-8 | Water-surface and field-grid extractors from Water and Environment, change-driven | Grids re-extract only when the current or the wind changes | CLI-1, CORE-6, WATER-5 | 42a |
| CLI-9 | RunicBot: the client runtime without presentation, many bot sessions per process, a simple brain (walk, fight, follow a quest) | One process holds hundreds of bots against a local server; no Godot is linked | CLI-3, NET-4 | 38 |
| GDB-1 | GodotLayer: the LibGodot instance (create, start, iteration, stop) at the top of the client LayerStack; window from the DisplayServer; input forwarded as AppEvents after Godot’s UI; headless mode | The client starts Godot windowed and headless and exits cleanly; UI clicks never reach the stack | APP-1, BUILD-1 | 1 |
| GDB-2 | Debug drawing on Godot: a debug-draw API (lines, shapes, text) uploaded as immediate meshes with depth-tested and overlay materials; toggled layers; development overlay panel; it reads Core DebugGeometry once CORE-3 lands | Every debug shape and text renders batched in one frame; layers toggle | GDB-1 | 2 |
| GDB-3 | Presenter: RenderFrame instances created, moved and freed in the RenderingServer by RenderInstanceId; presenter origin with a rare rebase (about every 4 km) | 50,000 static instances cost nothing per frame unless they change; a 20 km walk shows no jitter | GDB-2, CORE-3 | 5 |
| GDB-4 | Physics geometry layer: DebugGeometry from PHYS-3 with cached debug meshes for large shapes; the “see what the server sees” overlay | Collision shapes line up with gameplay shapes and the layer toggles | GDB-3, PHYS-3 | 8 |
| GDB-5 | Mesh instances from cooked cells and entities, repeated meshes as MultiMesh, assets from the project or the .pck | Cooked meshes draw correctly far from the origin | GDB-3, CLI-4 | 22 |
| GDB-6 | Skinned instances: poses into RenderingServer skeletons, or AnimationTree driven by intent, per the open animation decision | An animated character renders | GDB-5, CLI-5 | 23 |
| GDB-7 | Lights, environment and volumes as Godot lights, environment and fog volumes | Torches, skylight, darkness zones and fog show and toggle | GDB-5, CLI-7 | 25a |
| GDB-8 | Water surfaces and field grids (arrows, streaks, heatmaps, water materials) | A river surface and the ocean current draw from cooked data | GDB-5, CLI-8 | 42a |
| GDB-9 | UI bridge: one Godot UI scene per client state; the view-model binder that writes only changed fields to controls | The skill bar triggers abilities and UI clicks never attack | GDB-1, CORE-3 | 19 |
| GDB-10 | World UI: anchored Label3D and Sprite3D elements; diegetic panels in SubViewports on quads or mesh surfaces, with ray input into panel coordinates | Nameplates follow entities; a click on a world board reaches its panel and becomes a command | GDB-9, CLI-6 | 23a |
| GDB-11 | Batched world UI and mode fallbacks: MultiMesh nameplates and bars from an atlas; widgets move between diegetic, anchored, batched and hidden by distance, count and battle budgets | 500 nameplates draw in one call and the frame budget holds in a 500-player fight | GDB-10 | 38 |
| GDB-12 | Audio backend: implements the Runic::Audio backend interface on the AudioServer (buses, mixing, streams, spatial playback) | A sound event plays through its bus with volume control | GDB-1, AUD-1 | 24 |
| GDB-13 | Production look: materials, terrain, water shading, VFX and decals as Godot resources fed by RenderData; Game render features as materials and presenter hooks | Defined when a substantial game slice justifies it | GDB-5 | 44+ |
| ANIM-1 | Skeletons, clips, animator and blending (scope set by the open animation decision) | Clips blend without pops | ASSET-1 | 23 |
| AUD-1 | Audio backend interface, buses, mixing, semantic sound events | A sound event resolves through the registry to a backend call | ASSET-1 | 24 |
| AUD-2 | MusicDirector: contexts, fallback chains, albums, presets, radio playback, local profile | A context change switches album and remembers the position | AUD-1 | 24 |

#### Engine: tools

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| GDT-1 | Spike: the RunicEditor executable on libgodot (editor target) opens the Godot editor with a test plugin; the editor target builds and opens without GDScript | The editor opens, loads the plugin and exits cleanly in CI; the spike’s findings decide the fallback | BUILD-1 | 0 |
| GDT-2 | Project model: runic.project.json, the runic-mmo template, New and Open (per the open decision), loading and reloading the project’s editor library; IDE bridge (compile\_commands.json, go.work, VS Code tasks); first dock with world and ECS inspectors over a local simulation in the editor process | The editor opens a project and inspects entities of a local world; a rebuilt editor library reloads without restarting | GDT-1, APP-1, SIM-2 | 6 |
| GDT-3 | Physics inspector and the “see what the server sees” viewport layer | Bodies are selectable with their properties; cooked collision draws over the visual | GDT-2, PHYS-3 | 8 |
| GDT-4 | Cooker integration: export plugin that calls the Cooker; collision presets in Godot’s import settings; RunicCollider3D; the collision naming convention for glTF | A Blender mesh imported by Godot cooks into collision and is walkable | GDT-2, COOK-1 | 9 |
| GDT-5 | Resolver debugger dock | It shows which rules applied to a hit and why | GDT-2, CMB-4 | 17 |
| GDT-6 | Runic data in the editor: ResourceFormatLoader and ResourceFormatSaver for Runic files, inspectors and validation generated from schemas, live reload into a running server, background cooking with progress | A skill edited in the inspector reloads in the running server; a long cook never freezes the editor | GDT-2, CNT-2, COOK-2 | 20 |
| GDT-7 | Marker nodes and world cooking from scenes: RunicVolume3D, RunicSpawnArea3D, RunicInteractable3D, RunicRoute3D, RunicCollider3D; incremental cooking of the touched cells; spawn-area preview of candidate points | A region scene with a cave volume and a spawn area cooks into cells; moving a rock re-cooks only its cells | GDT-4, COOK-3 | 21 |
| GDT-8 | Region tools: World.tscn with RunicRegion3D proxies, New region from layout, read-only neighbor proxies with a border band, 64-bit region origins | Opening a 100 km² world loads only proxies; a region opens with its neighbors as proxies | GDT-7 | 21 |
| GDT-9 | Run orchestration: compile what changed, cook, start the local server and one or more development clients with a development ticket; development checkpoint on stop | Run from the editor starts a server and two clients connected as test characters | GDT-2, NET-2 | 13 |
| GDT-10 | Assistants: New Flecs system, New behavior, New quest condition or action, New AI node, New data type, New marker node, New Go service | Each assistant writes compiling files, registers them and opens them in the IDE | GDT-6 | 20 |
| GDT-11 | AI editor: behavior-tree canvas on GraphEdit, palette from the runtime registration, inspector, asset browser, XML save and load | A tree is edited, saved and reloaded | GDT-2, AI-2 | 35 |
| GDT-12 | AI tools: NPC definition and personality editors, content-ID validation, live NPC debugger | A running NPC’s tree state is visible live | GDT-11, AI-5 | 35 |
| GDT-13 | Live attach docks to development and staging servers | Entity inspector and debug shapes come from a remote server | GDT-2, NET-7 | 39 |
| GDT-14 | GDScript for editor tools: the module in the editor target, the export lock, the development-client check, Run-scene interception, script templates and the problems dock | A scripted node in a content scene fails export with a teaching message; an @tool script in Tools/ runs in the editor | GDT-7 | 21 |
| GDT-15 | Water and field authoring: RunicWaterBody3D on Path3D, flow profiles, current and wind map painting | A river drawn in a region cooks into fragments and its flow arrows match the cooked data | GDT-7, WATER-2 | 40 |
| GDT-16 | Plugin compatibility: published extension API per build, install validator, runic.plugin.json, Cooker adapters for plugin formats | Defined when the expansion slices are planned | GDT-14 | 44+ |
| COOK-1 | First cooker proof: geometry read from a scene Godot imported (no second glTF importer) into Jolt collision and a cell visual list | A Blender mesh renders through Godot and is walkable | ASSET-1, PHYS-1, GDT-1 | 9 |
| COOK-2 | Validation of data-driven definitions | Invalid definitions fail the cook with clear errors | CNT-2 | 20 |
| COOK-3 | World cooking from scenes: regions, sectors, sparse 3D cells, authored volumes, spawn areas, manifests, packages, Zstandard; client cell visual lists | Two region scenes and a cave volume cook into random-access packages | COOK-1, WORLD-2 | 21 |
| COOK-4 | Client export: the .pck from Godot’s export (textures, LODs and materials as Godot imports them), presets that exclude Tools/ and scripts, with the client cook packages | A shipping client runs from the .pck and the client packages alone | COOK-1 | 22 |
| COOK-5 | Skinned meshes and animation clips (Runic clip data only if the animation decision needs it) | A rigged character and its clips cook | COOK-1 | 23 |
| COOK-6 | Navigation tiles with Recast; candidate points for spawn areas checked against the navmesh | Tiles cook per cell; every candidate point is reachable | COOK-3 | 31 |
| COOK-7 | Water fragments and current fields | A river and an ocean field cook with their cells | COOK-3 | 40 |
| COOK-8 | Incremental cooking at scale | Only changed inputs cook again across a continent | COOK-3 | 44+ |

#### Platform

The server bindings implement the Engine’s Layer interface and the Simulation’s service port, and depend only on Engine interface targets: Runic::Core, Runic::Application and Runic::SimulationPort (the service port), while the Transport links Runic::NetworkTransport (the transport interface); the Engine never includes them. Those headers include only Core types, so a Platform build configures Core and Application and never Flecs, Jolt or the gameplay modules. Platform CI builds them against the Engine commit pinned as a submodule, so the Platform builds and tests on its own.

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| PCT-1 | Protobuf service APIs, fact messages and the connect-ticket format; C++ and Go code generation | Both languages round-trip the same message | BUILD-1 | 12 |
| PTR-1 | GameNetworkingSockets transport implementing the Engine transport interface | A client and a local server exchange reliable and unreliable messages | NET-1, PCT-1 | 12 |
| PTR-2 | Connect-ticket verification inside the simulation (signature, expiry, key ID) against a configured set of public keys; tickets are test-signed with a local key until PCS-1 issues real ones | Bad or expired tickets are rejected with no service call | PTR-1 | 12 |
| PTR-3 | Candidate connections (up to three), promotion, simulation-to-simulation links | Promotion happens with no loading screen | PTR-2, DSIM-3 | 36 |
| PTR-4 | Simulation links chosen by locality: an in-memory queue in one process, a local socket or shared-memory channel on one machine, GameNetworkingSockets between machines | The same transfer test passes on every channel with identical results; the link picks its channel from the peers’ placement | PTR-3 | 44+ |
| PSDK-1 | Go service skeleton: configuration, gRPC wiring, metrics | A sample service answers a gRPC call and reports metrics | PCT-1 | 26 |
| PSDK-2 | Persistence: PostgreSQL, transactions, migrations, idempotency store | A retried operation commits once | PSDK-1 | 26 |
| PSDK-3 | NATS wiring: publish, subscribe, JetStream where replay is needed | A fact published once is consumed once per subscriber | PSDK-1 | 30 |
| PBND-1 | ServicesBridgeLayer: implements the Engine service port with asynchronous gRPC calls; completions queued for safe ticks | A slow service never delays a tick | PCT-1, APP-1, SIM-5 | 27 |
| PBND-2 | LifecycleLayer: Agones SDK ready, health and shutdown, plus a local stub mode for development without Agones | Against the Agones local SDK server the layer reports Ready, sends health pings and drains on shutdown; the stub mode runs with no Agones | APP-1 | 39 |
| PBND-3 | Prometheus exporter that publishes the Core metrics registry (tick-domain timings, and the network metrics the Diagnostics layer records) | A scrape returns time per tick domain in Prometheus format | CORE-2, SIM-1 | 39 |
| PBND-4 | NATS in the services bridge: durable facts published from the outbox; world directives and other subscriptions delivered to the inbox at safe ticks | A fact published from a tick reaches a test subscriber once; a slow broker never delays a tick | PBND-1, PSDK-3 | 30 |
| PBND-5 | Behavior summaries from the service port published to NATS on a lossy stream; never blocks a tick; drops under backpressure and counts the drops. | Summaries from a simulation reach a test subscriber, and a stalled subscriber never slows the simulation | PBND-4, SIM-7 | 39 |
| PCS-1 | Accounts and entitlements, GlobalPlayerId issue, login, connect tickets signed with rotating keys whose public halves the simulations load | Login returns a signed ticket the simulation accepts | PSDK-2, PTR-2 | 27 |
| PCS-2 | World Coordinator: worlds and region map, neighbor topology, handoff candidates, the world epoch | The Coordinator names the candidates for a border | PSDK-1 | 36 |
| PCS-3 | World directives with an effective time and a duration (weather, wind and current events) | A directive applies and expires at the same world time everywhere | PSDK-3, PBND-4 | 43 |
| PCS-4 | Instance allocation from Agones fleets | Defined when the expansion slices are planned | PCS-2, PINF-2 | 44+ |
| PCS-5 | Chat and party groups | Defined when the expansion slices are planned | PSDK-3 | 44+ |
| PCS-6 | Admission: per-world capacity limits, login queue and cohort waves for the launch phases | Defined when the expansion slices are planned | PCS-1 | 44+ |
| PCS-7 | Placement by load and traffic over Agones: scores by load, memory and inter-simulation traffic, with distance from the regions’ global coordinates; moves high-traffic pairs onto one node by move-by-handoff, up to a per-node cap | Two simulations with heavy link traffic end on one node with no loading screen; no node passes its cap | PCS-2, PINF-2, PTR-4 | 44+ |
| PBB-1 | Item ledger: containers, slots, atomic transfers, operation IDs; mechanisms only | Concurrent transfers never duplicate or lose an item | PSDK-2 | 28 |
| PBB-2 | Currency wallets: balances and atomic transfers with operation IDs; mechanisms only | A balance changes once per operation ID under concurrent requests | PSDK-2 | 33a |
| PBB-3 | One-transaction transfers that move ledger items and wallet currency together; mechanisms only | Defined when the expansion slices are planned | PBB-1, PBB-2 | 44+ |
| PINF-1 | Local development stack (PostgreSQL, NATS) started by one command | The stack starts and the service tests pass against it | — | 26 |
| PINF-2 | Agones fleets, Kubernetes manifests, Prometheus and Grafana dashboards | A fleet runs in a development cluster, servers report Ready, and Grafana shows time per tick domain | PBND-2, PBND-3 | 39 |
| PINF-3 | Edge and DDoS protection: clients reach only an edge (a filtering provider, an anycast accelerator or own relays), never a simulation's own address; login, website and APIs behind a CDN with rate limits; a kernel-level filter (eBPF or XDP) that drops non-handshake packets at scale; the same edge carries relay routing for latency; a flooded node is handled as a lost node. | Defined when the launch plan is made; provider to be chosen | PINF-2 | 44+ |

#### Game

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| GAME-0 | GameClient and GameServer executables on the Engine entry point, composing their first layers; the client’s GodotLayer on top | Both start and stop cleanly in CI; the server links no Godot | APP-1, GDB-1 | 1 |
| GAME-1 | RunicGame as a RunicEngine project: project.godot, runic.project.json, the template’s folder layout, the game’s editor library target | The RunicEditor opens RunicGame and loads its editor library | GDT-2 | 6 |
| GAME-2 | Client anti-cheat: Easy Anti-Cheat through Epic Online Services in RunicGameClient, with its server counterpart in RunicGameServer over the Engine integrity channel (NET-9). Kernel driver on Windows; user mode only on Linux and Steam Deck. RunicGameServer stays headless. | Defined when the launch plan is made; a client that fails the provider's checks is disconnected | NET-9 | 44+ |
| GAME-3 | Signed releases and the launcher: builds and patch manifests signed with an offline key that never touches CI; the launcher verifies signatures before running anything and repairs changed files; the client does not connect after a failed integrity check (there is no mod support, so any change is tampering or damage); Windows code signing. Player soundtrack files live outside the checked files. | A changed byte in an installed file is repaired by the launcher, and an unsigned patch is refused | ASSET-2, COOK-4 | 44+ |
| GSH-1 | Movement parameters and the prediction set in RunicGame::Shared | Client and server move identically for the same inputs | SIM-4, GPL-1 | 14 |
| GSH-2 | First skills on the ability toolkit: one melee, one projectile | Both hit a dummy with Game timings | CMB-2, GSH-8, GSH-9 | 16 |
| GSH-3 | Damage types, resolver order, status application policies (build-up and stacking), Bleed, Stagger and one interaction | A Stagger on an already staggered target becomes Trip | CMB-4 | 17 |
| GSH-4 | Defense rules: impact stages (Guard modes, armor), Evasion charges and the dodge’s invulnerability restriction, Resolve T1 and T2 and Tolerance as status application policies | A dodge spends a charge; Guard blocks from the front | CMB-5 | 18 |
| GSH-5 | Crowd-control types and the CC target cap on the control primitives; threat, taunt, Challenge; FriendlyLock and the aim-assist strength on the targeting API; input-buffer settings (one slot, Dodge and Guard first); the combat prototype acceptance list | The full prototype list passes; FriendlyLock never selects a hostile | CMB-6, CMB-7 | 19 |
| GSH-6 | Arena class set: three named classes, one per role (from Sword \+ Shield, Spear and Wand \+ Focus), their weapon and Discipline skill trees and armor weights as Shared data and rules | Each class fills its role in a 3v3 arena test with Game values and equal point totals | GSH-5, GCNT-1 | 20a |
| GSH-7 | Context kits: mount and aerial skill trees per named class with their own points; mount, glider and wing kit swaps and modifications; flight zones and the altitude ceiling as movement-mode permissions | Defined when the expansion slices are planned | GSH-6, GPL-7 | 44+ |
| GSH-8 | Character attributes and pools: Health, Stamina and Mana declared on the Engine attribute API, their regeneration rules, and the death rule (Health at zero calls Kill) | A dummy loses Health, dies through Kill and emits one kill fact; pools regenerate by RunicGame’s rule | GPL-2 | 15 |
| GSH-9 | Relations: the function the Engine asks (hostile, friendly or neutral), built from factions, PvE mode, Outlaw, pirates and groups | A dummy is hostile and a party member friendly; changing a test character’s faction flips the result | GPL-2 | 16 |
| GCNT-1 | Skills, items and effects as data; one custom behavior | A skill changes through data with live reload | CNT-2 | 20 |
| GCL-1 | First GameUI scenes in Godot: HUD and skill bar, bound to view models | The skill bar triggers abilities and UI clicks never attack | GDB-9 | 19 |
| GCL-2 | Soundtrack settings screens and audio content | A player assigns an album to a music context | AUD-2, GDB-9 | 24 |
| GCL-3 | First world UI: nameplates and health bars, an interaction prompt, one diegetic notice board | The board accepts clicks in the world; Hidden players show no nameplate | GDB-10 | 23a |
| GCL-4 | Map screen with fog of war over the character’s map knowledge | The map shows only what this character has discovered | GDB-9, GSRV-6 | 33a |
| GSVC-1 | Character service | A character saves and reloads | PSDK-2 | 27 |
| GSVC-2 | Inventory service: stacking, binding and trade rules over the Platform item ledger | A loot grant is applied once across reconnects | PBB-1 | 28 |
| GSVC-3 | Quest service: stores progress, deduplicates facts, commits rewards | Replaying a fact changes nothing | QST-2, PSDK-3 | 30 |
| GSVC-4 | Economy, trade, the global auction house, guild, mail and housing services | Defined when the expansion slices are planned | PBB-2, PBB-3 | 44+ |
| GSVC-5 | Build persistence in the Character service: loadout, Discipline, skill points and level choices (class and role are derived); Altar reset that redistributes the points | A build survives relog; an Altar reset rebuilds the loadout and redistributes the points exactly once | GSVC-1, GSH-6, PBB-2 | 33a |
| GSVC-6 | Account-wide collections: transmog wardrobe, mounts, pets | Defined when the expansion slices are planned | GSVC-1 | 44+ |
| GSVC-7 | Labor: spending and regeneration, offline regeneration for subscribers checked through entitlements | Defined when the expansion slices are planned | GSVC-1, PCS-1 | 44+ |
| GSVC-8 | Rankings service: region-boss contribution, PvP honor and ranking | Defined when the expansion slices are planned | PSDK-3 | 44+ |
| GSVC-9 | World routines service: stores player-caused exceptions to routines and how they fade back | A delayed escort stays delayed across a simulation restart and rejoins its routine on schedule | PSDK-2 | 43a |
| GSVC-10 | Exploration XP, the exploration shop and profession proficiency in the Character service | Defined when the expansion slices are planned | GSVC-1 | 44+ |
| GSVC-11 | Behavior scoring service (Go): consumes behavior summaries and scores how human each player looks: reaction-time distributions, consistency over a session, route repetition, session shape, and currency or items flowing from many accounts to one. Flags players for human review; never bans by itself. Thresholds, features and scores are secret and server-side. | RunicBot sessions are flagged for review and a human test session is not | PBND-5, PSDK-3 | 39 |
| GSVC-12 | Moderation service: a review queue fed by reports and the scoring service; reports weighted by the reporter's history; a sanction ladder (warning, mute, trade lock, temporary ban, permanent ban; bots and real-money trading go straight to a ban); appeals; ban waves; an audit log of every GM action. | Defined when the launch plan is made | PSDK-2, GSVC-11 | 44+ |
| GSRV-1 | Loot rules and durable grant requests | Kill, loot, log out and keep the item | GPL-4, PBND-1 | 28 |
| GSRV-2 | First encounter: a boss phase and a cutscene on GameplayFlow | Every exit path releases the player’s restrictions | FLOW-2 | 29 |
| GSRV-5 | Death and respawn at the nearest discovered Altar in the same world, Altar discovery, durability loss, Altars as interactables | A character dies to a mob, respawns at an Altar and its gear loses durability | GPL-5, GSVC-1 | 33a |
| GSRV-6 | Map knowledge: discovered cells per Lineage, charts per node and layer, and cartography | Explored cells persist per Lineage; a chart unlocks its node layer for the Lineage | WORLD-2, GSVC-1 | 33a |
| GSRV-7 | Gathering, crafting, farming and trade-pack production | Defined when the expansion slices are planned | GSVC-2, GSVC-7 | 44+ |
| GSRV-8 | Castles (neutral continent only): one per region in a designated zone, built by the ruling guild, fixed once placed, an indivisible volume | Defined when the expansion slices are planned | GSVC-4, WORLD-2 | 44+ |
| GSRV-9 | Reports and in-world sanctions: a report command that attaches the last 60 seconds (example) of facts and positions around the reported player; mute, trade lock and kick enforced in the simulation from moderation decisions. | A report reaches the moderation service with its evidence, and a trade lock stops a trade at once | GSVC-12, PBND-1 | 44+ |
| GSRV-10 | Visibility tiers: Full, Silhouette and Hidden with reveal on contact, registered as the Engine’s visibility function | Tiers change at RunicGame’s distances and light levels; contact reveals for a few seconds | PRC-2 | 25 |
| GSRV-3 | First quests built with the Quest API | A kill-and-interact quest completes and persists | QST-1 | 30 |
| GSRV-4 | Mob profiles, light values, behavior trees and custom nodes | Mobs warn, detect and leash at night with Game values | AI-3, PRC-3 | 33 |
| GNAV-1 | Ship classes, sails and naval rules | A ship class sails with its Game stats | WATER-6 | 42 |
| GWTH-1 | Weather patterns, tide gameplay and the wind and current routines; the world-events service that decides storms and schedules operator events | A Game weather pattern runs on schedule; an operator event changes a current for its duration and the routine resumes | ENV-5, PCS-3 | 43 |

### Building with Claude Code

Every package goes through the same short cycle. It keeps design decisions with you and gives each coding session a closed, testable problem.

1. **Contract session.** Claude Code writes or updates the module’s ARCHITECTURE.md, the public headers the package adds and the acceptance tests, which fail at first. Nothing in Source/ yet.

2. **Contract review.** You approve the interface and the tests or ask for changes. This is the cheapest moment to change a design.

3. **Implementation session.** A fresh session implements Source/ until the tests pass, inside the write scope only. When it needs something from another module, it stops and reports the interface change.

4. **Checks.** CI runs the module tests, the headless server build and the dependency checks.

5. **Code review and merge.** The pull request carries the code, the tests, the updated ARCHITECTURE.md and the package status.

Small packages, with a few hundred lines and no new public types, may combine steps 1 and 3 in one session.

Each repository’s docs folder is written from this document: the shared rules once, one ARCHITECTURE.md per module and the package tables. Claude Code reads those files, so the repositories and this document never disagree.

```text
TASK
  Implement CMB-3 (Stage A): statuses and effects, cooldowns, resource costs.

WRITE SCOPE
  Engine/GameplayAPI/Combat/**   (Public, Source, Tests, ARCHITECTURE.md)
  the Runic::Combat target in CMake

READ-ONLY
  Public headers of Runic::Core, Events, Simulation, Gameplay
  Docs: Engine gameplay APIs, Simulation core, Modules and work packages

APPROVED INTERFACE
  [public headers from the contract session]

DONE WHEN
  [acceptance tests from the package table and ARCHITECTURE.md]

RULES
  - Edit nothing outside the write scope; report needed interface changes.
  - No library types in Public/; the server build stays headless.
  - No game rules, names or numbers; tests use engine: test IDs.
  - Never block a tick on I/O; never mutate Flecs from an I/O callback.
  - Build only what the tests need; no placeholders in other modules.
```

### Maturity stages

| Stage | Meaning | When |
| :---- | :---- | :---- |
| A — vertical proof | The smallest real implementation that proves the module’s boundaries inside a roadmap slice | Every package starts here |
| B — generalize | Broader interface and data coverage once a second real consumer exists | When a later slice needs more |
| C — harden | Performance, scale, recovery, tooling, compatibility and adversarial tests | Battle scale, operations and pre-launch slices |

A consumer never waits for its dependency to reach Stage C; vertical slices validate the architecture first, then it is generalized and hardened.

### Parallel work

* Packages whose Needs are all merged can run at the same time, each in its own Claude Code session and git worktree. Examples: GDB-2 alongside SIM-1; PCT-1 alongside NET-1; GDT-2 alongside PHYS-1.

* Two or three sessions at once is the practical limit, because every contract and pull request still needs your review.

* Two packages that write the same module never run at the same time.

### Automated checks

| Check | Catches |
| :---- | :---- |
| Headless build of GameServer | Godot, UI, audio or editor code reaching the server |
| Dependency check per module | Links outside the allowed list; includes of another module’s Source/ |
| Public-header scan | Library types in Public/, and Godot types outside GodotBridge and GodotTools |
| Client export check | Scripts, editor-only classes or Tools/ content in the client .pck |
| Module tests | The Done when behavior of every merged package |
| Docs check | A code change without its ARCHITECTURE.md or package-status update |
