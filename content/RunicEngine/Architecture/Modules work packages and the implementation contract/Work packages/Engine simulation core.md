---
title: "Engine: simulation core"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: simulation core"
created: "2026-10-14"
modified: "2026-10-30"
---

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| [[ECS-1\|ECS-1]] | [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] world wrapper, component registration, query helpers, conventions | Entities are created, queried and destroyed; Flecs types appear in public headers only through the approved world-registration exception | [[CORE-1\|CORE-1]] | [[Slice 04 ECS and world coordinates\|4]] |
| [[WORLD-1\|WORLD-1]] | 64-bit double coordinates (real Y, 1 cm minimum unit), WorldId, region-local origins, Region, Sector and sparse 3D Cell keys | Conversions round-trip exactly far from the origin; a cell key round-trips at any altitude or depth | [[ECS-1\|ECS-1]] | [[Slice 04 ECS and world coordinates\|4]] |
| [[WORLD-2\|WORLD-2]] | Sparse 3D spatial index (XZ columns holding only occupied Y cells), exact XYZ candidate queries (radius, box, ellipsoid), membership updates; authored volumes (caves, rule areas, indivisible volumes) with point-in-volume queries | Query results match brute force in 3D and draw in the debug view; a point inside a cave volume is reported inside it | [[WORLD-1\|WORLD-1]] | [[Slice 11 Spatial index\|11]] |
| [[WORLD-3\|WORLD-3]] | Activation: per-player asymmetric ellipsoid [[World space coordinates cells and activation#Activation volumes\|activation volumes]], their union, prepare, commit and release hysteresis, load and unload requests per cell | Walking back and forth on an edge never thrashes loads; a cell far above or below the player stays unloaded until approached | [[WORLD-2\|WORLD-2]] | [[Slice 21 World partitions\|21]] |
| [[PHYS-1\|PHYS-1]] | PhysicsWorld, bodies, shapes and collision layers on [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] v5.6 in double precision, kept private | Bodies collide without jitter far from the origin | [[WORLD-1\|WORLD-1]] | [[Slice 07 Physics\|7]] |
| [[PHYS-2\|PHYS-2]] | CharacterVirtual integration and ground movement | A capsule walks, climbs steps and stops at walls | [[PHYS-1\|PHYS-1]] | [[Slice 07 Physics\|7]] |
| [[PHYS-3\|PHYS-3]] | Debug-geometry extraction: Jolt’s debug interface implemented inside Physics, written into Core DebugGeometry buffers | Bodies and shapes come out as plain lines and triangles; Physics links no [[How the Engine uses Godot\|GodotBridge]] | [[PHYS-1\|PHYS-1]], [[CORE-3\|CORE-3]] | [[Slice 08 Physics view\|8]] |
| [[PHYS-4\|PHYS-4]] | Jolt job system on the Core worker pool: a JobSystem adapter inside Physics, so Jolt never owns threads | A physics step on the pool matches a single-thread step; no thread is created outside the pool | [[PHYS-1\|PHYS-1]], [[CORE-2\|CORE-2]] | [[Slice 10 Worker pool\|10]] |
| [[PHYS-5\|PHYS-5]] | Gameplay queries: ray, shape cast, overlap, per-worker query queues | Results are identical for a fixed scene with any worker count | [[PHYS-1\|PHYS-1]], [[SIM-3\|SIM-3]] | [[Slice 15 Character state\|15]] |
| [[SIM-1\|SIM-1]] | SimulationRuntime: 60 Hz master clock, 30/20/10 Hz domains, TickContext, the Simulation layer, domain metrics | Domain tick counts stay exact over a long run, with no drift | [[APP-1\|APP-1]], [[CORE-2\|CORE-2]] | [[Slice 03 Fixed-step clock\|3]] |
| [[SIM-2\|SIM-2]] | Phases, commands and command queue, deferred mutation, event flush at barriers | Commands apply in phase order; facts are visible to the next phase | [[SIM-1\|SIM-1]], [[ECS-1\|ECS-1]], [[EVT-1\|EVT-1]] | [[Slice 05 Moving entities\|5]] |
| [[SIM-3\|SIM-3]] | Phases on the worker pool, per-worker buffers, deterministic merge; the physics step runs through [[PHYS-4\|PHYS-4]] | The same scene with one worker and with many gives identical results | [[SIM-2\|SIM-2]], [[PHYS-4\|PHYS-4]] | [[Slice 10 Worker pool\|10]] |
| [[SIM-4\|SIM-4]] | Client prediction subset: selected systems run on the client with RunicGame::Shared | The same inputs give the same result on client and server | [[SIM-3\|SIM-3]] | [[Slice 14 Prediction\|14]] |
| [[SIM-5\|SIM-5]] | Service port: an outbox of durable operations with stable operation IDs and an inbox of accepted results drained at safe ticks; the Engine interface the Platform services bridge implements, shipped as the header-only Runic::SimulationPort target (Core types only) | A fake port that delivers a result twice is applied once; no I/O callback touches Flecs | [[SIM-2\|SIM-2]], [[EVT-1\|EVT-1]] | [[Slice 27 Accounts and characters\|27]] |
| [[SIM-6\|SIM-6]] | Replication registry: modules register replicated components and world-state values (schema, quantization profile, relevance); Network encodes only what is registered | A test component and a world-state value replicate without Network depending on the modules that own them | [[SIM-2\|SIM-2]] | [[Slice 13 Replication\|13]] |

---

↑ [[Work packages|Work packages]] · ← [[Engine foundation|Engine: foundation]] · [[Engine GameplayAPI group|Engine: GameplayAPI group]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: simulation core · exported 2026-11-03
