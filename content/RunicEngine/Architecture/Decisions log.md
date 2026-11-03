---
title: "Decisions log"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Decisions log"
created: "2026-10-14"
modified: "2026-10-30"
---

| Area | Decision |
| :---- | :---- |
| Ownership | Engine provides generic mechanisms, Game provides rules, content and executables, Platform provides shared services, SDK and infrastructure |
| Executables | GameClient and GameServer belong to RunicGame; the Engine owns the entry point, the ApplicationHost (Run and RunFrame), the [[Tools#RunicEditor\|RunicEditor]] and the [[Tools#Testing at scale\|RunicBot]] |
| Application | Layers with events top-down and updates bottom-up; changes at safe points; loop policy per executable |
| Authority | The C++ simulation is authoritative; Go services own durable and distributed state |
| Scale | 5,000 players per world; 100 vs 100 must feel perfect; 500 in one region supported |
| Coordinates | 64-bit double positions with a real Y axis and a 1 cm minimum unit; [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] double precision; camera-relative rendering; network positions quantized relative to the cell |
| World | One main world in continuous coordinates (surface, floating islands, underground spaces); separate persistent maps such as the Game’s sky world are their own WorldId; about 600 km² per map to start, land and sea included; expandable live; continent-scale capable |
| Clock | 60 Hz master; 30/20/10 Hz domains; combat and physics at 30 Hz |
| Threading | Every simulation is multi-threaded with fixed phases and barriers |
| Placement | One region per pod by default; quiet neighbors may share a pod or a process; grow by in-place resize or move by handoff; the [[Platform and operations#Simulation placement\|World Coordinator]] places by load, memory and inter-simulation traffic over [[Platform and operations#Simulation placement\|Agones]] and co-locates high-traffic pairs up to a per-node cap; busy areas get their own simulation through authority partitions |
| Networking stack | Engine transport interface; Platform [[Networking stack sessions and responsiveness#Stack (decided)\|GameNetworkingSockets]] transport; gRPC with answers; Protobuf service contracts; Engine-encoded realtime messages; NATS publish/subscribe; Go services; Agones and Kubernetes |
| Hit timing | ServerTime by default; CappedRewind per skill; full rewind not offered |
| Responsiveness | Prediction runs shared game code; predicted skill starts; input queue |
| Gameplay split | Engine GameplayAPI group (Gameplay, Combat, [[Scripted sequences GameplayFlow and restrictions\|GameplayFlow]] and Quest modules): ability toolkit, tags, statuses, rule pipeline, interception, threat table, registries, restrictions, sequences, quest runtime; Game: skills, resolver, damage, defense, threat rules |
| Light and perception | Engine API with game values; warn and detect radii; concealment; detection at zero light |
| PvP visibility | Full, Silhouette and Hidden tiers with reveal on contact |
| Custom logic | Data first; custom behaviors in C++ through registries; no scripting language in the game; GDScript only for editor tools |
| Cold content | The quest runtime runs in the simulation; quests are made through the Engine quest API from data plus registered Game C++; the Go Quest service stores progress; dialogue is data; physical interactions in C++ |
| Services split | Platform: core services (accounts, World Coordinator, instances, directives, chat and party groups), Go SDK, item ledger and wallets as mechanisms; Game: character, inventory rules, economy, trade, guild, mail, housing, rankings, quest progress |
| Item grades | A data table; adding or removing grades needs no code |
| Inventory | Slots only; expansions paid in game currency |
| Rendering | Godot’s renderer through LibGodot; the presenter draws an extracted RenderFrame and never reads Physics; physics debug drawing is a [[How the Engine uses Godot\|GodotBridge]] layer fed by plain geometry that Physics extracts; debug layers first, the production look later; Godot stays single precision with a presenter origin rebased about every 4 km |
| UI | Godot UI scenes for players and the development overlay, bound to C++ view models; the editor is Godot’s; no RmlUi or ImGui |
| Monitoring | Grafana as the single operations panel; live inspection through the RunicEditor; no Godot on servers |
| Tools | The RunicEditor is the Godot editor run through LibGodot with the Runic tools; [[Cooker\|the Cooker]] runs inside it or headless on build machines; the AI editor is a dock in it |
| Audio | Client presentation only; semantic sound-effect routing for developers; players customize only the soundtrack through presets, albums and radio-style playback; the server has no audio dependency |
| Water | Queryable, streamed water field; buoyancy separate from movement; no fluid simulation; static water never replicated per tick |
| Environment | Wind, currents over time, tides, waves and weather are deterministic functions of world time, position and a small replicated weather state; wind and sea currents follow a cyclic baseline routine, and operator events change them for a duration |
| Naval play | Ships, sails, cargo, naval combat, breath and nautical charts are Game rules on the Engine water and environment APIs |
| Modules | A module is a CMake target with Public, Source, Tests and ARCHITECTURE.md; groups such as GameplayAPI are umbrella targets; the window comes from Godot through the GodotLayer |
| Work packages | One Claude Code session and one pull request per package, writing inside one module; interface and tests approved before code; Stage A first |
| Server layers | The Engine supplies the Network, Simulation and Diagnostics layers; the Platform supplies the services-bridge and lifecycle layers; the Engine never supplies infrastructure or communication layers |
| Scripted gameplay | GameplayFlow runs quests, boss phases, cutscenes and world events through commands; restrictions are owned by their source and released on every exit path |
| Jolt version | Jolt 5.6, pinned in the build, in double precision, with its AVX2 path enabled |
| Roadmap | Small slices, each tagged with the modules’ work packages it needs |
| Render data | [[RenderData in Core\|RenderData]] lives in Core as plain structs shared by extraction, GodotBridge and debug tools; instances carry a stable RenderInstanceId; the debug layers come first, the production look later |
| World UI | Diegetic first, authored as Godot UI scenes; anchored (Label3D, Sprite3D) and batched (MultiMesh) modes as fallbacks chosen by distance, count and battle budgets |
| Class system | Named classes: one of ten fixed loadouts plus one of five [[Weapon Class System#Disciplines\|Disciplines]] make one class with one role; weapon skills unlocked by level and one merged tree with points in the Discipline skills, from levels only; Vertentes, versatile weapons, Maestria and Infusion removed; the Character service stores the [[Weapon Class System#Loadouts\|loadout]], Discipline, points and level choices and derives class and role |
| Spatial index | No SpatialLayers: sparse 3D cells (XZ columns holding only occupied Y cells), exact XYZ in every test, authored volumes for caves and rules, and [[World space coordinates cells and activation#Activation volumes\|activation volumes]] (asymmetric ellipsoids around players) whose union decides what loads and simulates |
| Worlds | Separate maps are separate WorldIds; no [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] or ghosts between worlds; a transition is a checkpoint plus a new connect ticket |
| Distributed simulation | Handoff between simulations is required (ships cross borders); indivisible volumes (an island, a castle, a docked ship) are never cut by an ownership boundary |
| Simulation links | Chosen by locality: in-memory queue in one process, local socket or shared memory on one machine, GameNetworkingSockets between machines; DistributedSimulation semantics unchanged; no central memory shared between simulations |
| World routines | Cooked routes; position \= f(route, world time, seed) with deterministic drift; spawn when a cell activates; a Game service stores only player-caused exceptions |
| Contextual values | Every value has a base; skills, items and effects may declare PvE and PvP values; Proposal: the target of each hit chooses the context |
| Archived and discarded | Archived: a moving island carrying a castle (the architecture keeps room for it as a kinematic indivisible volume that hands off as one group). Discarded: destructible islands, exploration points that unlock combat skills or cosmetics, a central memory shared between simulations, an aerial counterpart for every skill |
| Engine seams | Combat owns the input queue; Network owns all wire encoding, including ghost deltas; the Simulation’s service port is the Engine’s only door to durable services; Physics runs Jolt jobs on the Core worker pool; DistributedSimulation carries other modules’ state through a snapshot-contributor registry; the Environment clock arrives before night-time perception; interfaces the Platform implements ship as header-only Engine targets with Core types only (Runic::NetworkTransport, Runic::SimulationPort); Runic::Network encodes all realtime traffic and Protobuf carries only service APIs, facts and tickets |
| Public headers | Library types stay out of Public/; four approved exceptions: GLM math types in Core, the [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] world handle for modules that register systems, BehaviorTree.CPP node base types for Game custom AI nodes, and godot-cpp types in GodotTools for the Game’s editor library |
| Repository wiring | Hybrid: RunicGame pins Engine and Platform as submodules and RunicPlatform pins the Engine, for CI and releases; a CMake option points at sibling checkouts for daily work |
| CPU baseline | x86-64-v3 (AVX2, FMA) for servers and clients; Jolt and the Engine build with AVX2 on |
| Test framework | GoogleTest (with GoogleMock) for C++ in all three repositories, pinned in the build; module-local Tests/ registered with CTest through test discovery; Go uses its standard testing package |
| Development endpoints | The RunicEditor attach channel is compiled only into development and staging builds; production servers expose metrics only through the Platform exporter |
| Connect tickets | Test-signed with a local key from slice [[Slice 12 Transport\|12]] until the accounts service ([[PCS-1\|PCS-1]], slice [[Slice 27 Accounts and characters\|27]]\) issues real ones |
| Godot | Integrated as a library (LibGodot) from slice [[Slice 00 Build skeleton\|0]] in two roles: renderer, window, input, audio and player UI in the client, and the editor in the RunicEditor; never in the server; never runs game rules; the [[RenderData in Core\|RenderFrame]] is its only input |
| Godot build | Built from source at a pinned tag in two targets (editor, template) with unused modules off and a build profile; no fork; small documented patches only if needed |
| Projects | The Engine is game-agnostic: the RunicEditor opens with no project and offers New (from a template) and Open; a project’s editor code is a reloadable library; game executables are built by the project’s CMake |
| World authoring | Godot assembles the world (World.tscn, region scenes, marker nodes, water, materials, data); Blender makes assets (modeling, rigs, animation, terrain sculpting); glTF is the border; no scene survives cooking |
| Resources | Interactive resources (trees, crops, ores) spawn by rule inside spawn areas; the map only marks where they may appear; decorative vegetation is MultiMesh with no entity |
| GDScript | Off until slices [[Slice 20 Data-driven content\|20]]–21, then only in the editor, with locks in every layer; the client is built without it and the export refuses scripts |
| Code workflow | C++ and Go in an external IDE; the editor generates IDE files and runs assistants; the Run button compiles, cooks, keeps the local stack and starts server and clients |
| Type rule | WorldPosition and WorldDelta are 64-bit; directions, velocities, sizes, rotations, local offsets and shapes are 32-bit; going down only through ToLocal; float-conversion warnings are errors |
| Open in v4 | Data file format, the New project flow, client animation, MusicDirector placement, the fallback if the editor cannot run as a library (see Godot integration) |

---

**Consolidated sources:** RunicEngine Project Context; Technical Architecture v2 and v2.1 (Cherno Layers); Flecs Simulation Architecture; Jolt Physics and Multi-Rate Tick Contract v2; Platform Fabric and Networking Architecture; Combat System Context v1; AI Architecture v1; World Authoring and Layered Spatial Partitioning; bgfx Debug Renderer tutorial; Audio Routing and Custom Soundtrack Architecture v1; Water System API and Architecture v1; Technical Architecture v2.1 Appendix J (Module Boundaries, Distributed Simulation, Gameplay Flow and Service Integration); Technical Architecture v3 (rev 503); Godot integration proposal for v4 (October 2026).

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Vertical-slice roadmap|Vertical-slice roadmap]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Decisions log · exported 2026-11-03
