---
title: "Simulation core: Flecs and Jolt (Engine)"
tags:
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-10"
---

Geometry answers spatial questions; Flecs answers what entities are, how they relate and which rules apply.

| Concern | Owner | Role |
| :---- | :---- | :---- |
| Gameplay state and rules | Flecs | Components, relationships, systems |
| Geometry and collision | Jolt \+ Runic spatial index | Answers “what intersects?” |
| Durable state | Go services \+ PostgreSQL | Flecs keeps only what the active simulation needs |
| Client visuals and prediction | Client ECS \+ renderer | Non-authoritative mirror |

### The Runic API over Flecs and Jolt

Everything goes through the Runic API. Content, tools, Game code and Engine modules speak one vocabulary, organized in categories, and each category decides which Flecs or Jolt calls run underneath. Whatever the API lacks is added to the API.

| Category | What it is | Backend |
| :---- | :---- | :---- |
| State | A lasting fact about an entity: Mounted, Swimming, a quest flag | Flecs, in the storage its category picks (see State declarations) |
| Fact | Something that happened: EntityKilled, StateEntered, VolumeEntered | Event buffers |
| Volume | A region of space with a meaning: a quest area, an Overhear zone, a spawn area, a wall | Runic spatial index or Jolt, by volume kind (see Flecs and Jolt together) |
| Condition | A question about states and volumes | Registry; reads states, queries and the spatial index |
| Trigger | A fact that starts an evaluation | Registry; consumes facts |
| Action | A request to the system that owns what changes | Registry; becomes commands to that owner |

* **One registration feeds every consumer.** Each item is registered once with its metadata (name, category, description, parameters, owner, allowed contexts). The runtime, the RunicEditor’s palettes and the Cooker’s validation read the same registry, as AI nodes already do (see [[AI architecture (Engine, Game)|AI architecture]]).

* **Native Flecs is an escape hatch.** The Flecs world is reachable only through the opt-in Runic::ECSNative target. Using it is discouraged and is the responsibility of whoever uses it; the configure-time dependency check lists every module that links it. A need more than one module shares is a gap in the API and goes into the API instead.

* **Jolt has no native door.** It stays private to Runic::Physics.

### State declarations

A state is declared once, and its category picks how Flecs stores it, so whoever declares a state never chooses between fragmenting and non-fragmenting storage. The categories apply the Flecs rules below.

| Category | Examples | Storage in Flecs |
| :---- | :---- | :---- |
| Hot flag | Mounted, Swimming, Gliding, InCombat | A toggled component (CanToggle): flipping it never moves the entity to another table |
| Fact with a target | MountedOn(horse), PassengerOf(ship) | A relationship; DontFragment for high-cardinality targets |
| Content flag | Talked to an NPC, saw a cutscene, a quest step | One bit in a compact per-entity container, indexed by the registered StateId |
| Value | Reputation, a counter | A field in a compact container or a component |
| Derived | It is night, inside a volume, near an NPC | Not stored: a condition computed when asked |

Besides its category, a declaration carries four fields:

* **Owner:** the one system that writes the state. Mounted belongs to the mount system; everyone else reads it or requests the owner’s action.

* **Observable:** whether changes emit StateEntered and StateExited facts. Only observable states can be triggers; any state can be a condition.

* **Visibility:** server only (hidden quest conditions), the owner, or everyone (the client needs Mounted for animation).

* **Lifetime:** transient, carried in the transfer snapshot, or durable through a service.

The four fields exist from the first declaration, and each is wired when its consumer arrives: observability with the event buffers (EVT-1), visibility with the replication registry (SIM-6), lifetime with persistence and the transfer snapshot. Replication, handoff and persistence then come from the declaration instead of code written per component.

```cpp
// Illustrative. IDs resolve to StateIds at load; no strings per tick.
states.Declare("engine:mounted", {
    .kind = StateKind::HotFlag, .owner = "engine:mount",
    .observable = true, .visibility = Visibility::Everyone, .lifetime = Lifetime::Handoff });

states.Declare("game:met_stablemaster", {
    .kind = StateKind::ContentFlag, .owner = "engine:quest",
    .visibility = Visibility::ServerOnly, .lifetime = Lifetime::Durable });

ctx.Set(player, MetStablemaster);   // a bit in the container
ctx.Has(player, Mounted);           // a toggle test
```

**Why the category matters (planning numbers until the benchmark replaces them).** Every distinct combination of tags is a Flecs table. If each quest flag were a tag, 2,000 players at different points of their quests could spread over about 2,000 one-entity tables, and a system that walks players would visit 2,000 tables instead of one. At about 50 to 100 ns per table (overhead plus a cache miss), that is 0.1 to 0.2 ms per system per tick, or 2 to 4 ms of the 33 ms tick across 20 systems. Each add or remove also moves the entity and copies all its components: from hundreds of nanoseconds to about 1 µs for an entity with about 40 components. In a container, 3,000 flags (about 250 quests × 12) take about 375 bytes per character, about 750 KB for 2,000 characters, and fragment nothing.

**Benchmark.** A harness measures tag, toggle, container and DontFragment with 2,000 entities, in nanoseconds per operation and milliseconds per tick. Its numbers replace the planning numbers above, and DontFragment is used where it wins.

### Flecs rules

* Hot state is dense and owned by the entity: Transform, Velocity, Health, resources, combat state, cooldowns.

* Definitions are prefabs (IsA); hot mutable state is never inherited.

* Relationships hold lasting facts: OwnedBy, PlantedOn, PassengerOf, CarriedBy, CargoOf, MemberOf, IsA. High-cardinality targets (any player) use DontFragment after a benchmark.

* Per-tick geometry results (overlaps, line of sight) are never relationships; they are scratch lists.

* Recurring work uses cached queries; per-owner lookups use one variable-bound query, never one query per player.

* States that flip often (AIActive, Replicated, CombatEnabled) are toggles, not add and remove.

* Many dynamic buffs or quest states live in compact containers, not one tag each.

* Observers handle lifecycle bookkeeping only; hot combat facts use event buffers.

* Only the simulation’s own phases mutate the Flecs world.

* GlobalEntityId, stable across simulations, is separate from local Flecs IDs.

* The Flecs version is pinned in the build; 4.2 is the baseline (non-fragmenting components, DontFragment, need 4.1 or later).

### Jolt rules

| Runic concept | Jolt representation |
| :---- | :---- |
| Terrain, buildings | Static Body |
| Doors, elevators, platforms | Kinematic Body |
| Ships, crates, physical objects | Dynamic Body |
| Players and combat NPCs | CharacterVirtual (not a Body) |
| Melee volumes, AoEs | Shape used in CollideShape |
| Projectiles | Shape used in CastShape, one cast per tick segment |
| Triggers that move with an entity (a ship’s deck, a boss aura) | Sensor Body |
| Static rule areas (quest areas, nodes, Overhear zones, spawn areas) | None: authored volumes in the Runic spatial index |

* Shapes are immutable and shared through a registry: many skills reuse one SwordArcSmall.

* Structural changes are batched at the 30 Hz boundary (AddBodiesPrepare and AddBodiesFinalize).

* Characters are discovered through the Runic cell grid and tested exactly with CharacterVirtual::GetTransformedShape. The same test with a past transform serves capped-rewind skills.

* Jolt results (BodyID, contact, fraction) are facts; Runic decides what they mean.

* CharacterVirtuals update every 30 Hz tick even without input, so moving platforms and ships carry them.

* Jolt is built in double-precision mode (JPH\_DOUBLE\_PRECISION) for 64-bit world positions.

* The Jolt version is pinned in the build; v5.6 is the documented baseline.

### Flecs and Jolt together

* **Flecs holds the truth.** An entity’s transform lives in Flecs; its body or CharacterVirtual is an opaque Physics handle in a component.

* **A sync phase on each side of the step.** Before the step it writes kinematic targets and character movement into Physics; after the step it writes the resulting transforms back into Flecs.

* **Bodies follow their entities at the barrier.** Creation and removal follow the batching rule above; destroying an entity removes its body at the next barrier, so Flecs and Jolt never disagree inside a phase.

* **Contacts are facts.** Jolt’s contact and sensor callbacks run on worker threads and only fill buffers; the next phase reads them as facts. No callback touches Flecs.

* **The volume kind picks the backend.** Whoever authors a volume picks its kind (a quest area, an Overhear zone, a spawn area, a wall, a ship’s deck), and World decides where it lives: static rule areas in the Runic spatial index, solid collision as a static body in its object layer, a volume that moves with an entity as a sensor body.

SIM-8 implements the first four rules and WORLD-2 the last (see [[Modules, work packages and the implementation contract (Engine, Platform, Game)|Modules and work packages]]).
