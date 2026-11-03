---
title: "Simulation core: Flecs and Jolt (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Simulation core: Flecs and Jolt (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

Geometry answers spatial questions; Flecs answers what entities are, how they relate and which rules apply.

| Concern | Owner | Role |
| :---- | :---- | :---- |
| Gameplay state and rules | Flecs | Components, relationships, systems |
| Geometry and collision | Jolt \+ Runic spatial index | Answers “what intersects?” |
| Durable state | Go services \+ [[Physical layout Proposal\|PostgreSQL]] | Flecs keeps only what the active simulation needs |
| Client visuals and prediction | Client ECS \+ renderer | Non-authoritative mirror |

## Flecs rules

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

## Jolt rules

| Runic concept | Jolt representation |
| :---- | :---- |
| Terrain, buildings | Static Body |
| Doors, elevators, platforms | Kinematic Body |
| Ships, crates, physical objects | Dynamic Body |
| Players and combat NPCs | CharacterVirtual (not a Body) |
| Melee volumes, AoEs | Shape used in CollideShape |
| Projectiles | Shape used in CastShape, one cast per tick segment |
| Triggers | Sensor Body |

* Shapes are immutable and shared through a registry: many skills reuse one SwordArcSmall.

* Structural changes are batched at the 30 Hz boundary (AddBodiesPrepare and AddBodiesFinalize).

* Characters are discovered through the Runic cell grid and tested exactly with CharacterVirtual::GetTransformedShape. The same test with a past transform serves capped-rewind skills.

* Jolt results (BodyID, contact, fraction) are facts; Runic decides what they mean.

* CharacterVirtuals update every 30 Hz tick even without input, so moving platforms and ships carry them.

* Jolt is built in double-precision mode (JPH\_DOUBLE\_PRECISION) for 64-bit world positions.

* The Jolt version is pinned in the build; v5.6 is the documented baseline.

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Simulation core clock and threads|Simulation core: clock and threads (Engine)]] · [[World space coordinates cells and activation|World space: coordinates, cells and activation (Engine)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Simulation core: Flecs and Jolt (Engine) · exported 2026-11-03
