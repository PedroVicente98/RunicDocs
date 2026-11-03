---
title: "Simulation core: clock and threads (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Simulation core: clock and threads (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

The simulation advances in fixed steps on a 60 Hz master clock with 30, 20 and 10 Hz domains, and every step runs its work across a pool of worker threads.

## Multi-rate fixed-step scheduler

| Domain | Interval | Typical work |
| :---- | :---- | :---- |
| Hz60 | 16.7 ms | Master clock; no mandatory gameplay work |
| Hz30 | 33.3 ms | Commands, movement, CharacterVirtual, skill timelines, projectiles, AoE queries, ships, the [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] step, replication extraction |
| Hz20 | 50 ms | AI decisions and perception |
| Hz10 | 100 ms | Aggro wake scans, luminosity updates, weather and tide state, quest and loot consumers, spawning, world maintenance |

* Wall-clock time only decides how many 60 Hz steps are owed; the simulation advances in exact fixed steps.

* Rates decide when a system is due; explicit phases decide order: 20/10 Hz producers, then the 30 Hz realtime phase, then 20/10 Hz consumers, then the Hz60 hook.

* Systems receive a TickContext (domain, master tick, domain tick, dt, simulation time); nothing reads the wall clock.

* Durations are times, or tick counts tagged with their domain (DomainTickCount). An untagged “9 ticks” is a bug.

* Falling behind is measured and alarmed, never silently skipped.

**Realtime 30 Hz phase, in order**

1. Apply queued player and AI commands; start queued skills whose recovery has ended.

2. Advance movement and skill timelines; advance projectiles.

3. Commit structural physics changes in batches (bodies created and removed).

4. Apply kinematic targets, buoyancy forces and water-movement forces; step Jolt once.

5. Update CharacterVirtuals against the new world; write positions to [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] and spatial membership; record position history for skills that use [[Part 1 Locked ping resolution#5. Capped rewind|capped rewind]].

6. Run combat, projectile and AoE queries; pass hit candidates to the resolver.

7. Commit events and build replication state.

## Threading model (decided)

Every simulation is multi-threaded. Phases stay in a fixed order; the work inside a phase is split across workers, and nobody starts the next phase until every worker finishes the current one (a barrier).

* One SimulationRuntime per simulation, with a worker pool sized from the pod’s CPU allotment; a process normally hosts one simulation, and quiet neighbors may share a process.

* Inside a parallel phase, each worker writes only to the entities it owns. Effects on other entities (damage, events, spawns) go to per-worker buffers that are merged at the barrier in a fixed order, so results never depend on thread timing.

* Jolt runs on the same pool through its job-system interface, adapted inside Runic::Physics so Jolt stays private; Flecs multi-threaded systems run only in phases that allow them.

* Network I/O and service clients run on their own threads and only enqueue.

* The worker count can change at a safe point between ticks, for example after a CPU resize.

* Early slices run the pool with one worker for easier debugging. The code is written phase-safe from day one, so more workers is a configuration change.

| Work | Parallel? | Why |
| :---- | :---- | :---- |
| Movement and CharacterVirtual updates | Yes, by entity | Each character is independent |
| AI brains and perception | Yes, by NPC | Each brain reads state and writes intents |
| Combat queries | Yes, by attack or projectile | Read-only geometry; results buffered |
| Hit resolution (damage, effects) | Grouped by target | Two attacks on one target must apply in a fixed order |
| Per-client replication building | Yes, by client | The largest cost in big battles, and fully independent |
| Structural changes (spawn, despawn, bodies) | No, batched at the barrier | Keeps Flecs and Jolt consistent |

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Godot integration|Godot integration (Engine)]] · [[Simulation core Flecs and Jolt|Simulation core: Flecs and Jolt (Engine)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Simulation core: clock and threads (Engine) · exported 2026-11-03
