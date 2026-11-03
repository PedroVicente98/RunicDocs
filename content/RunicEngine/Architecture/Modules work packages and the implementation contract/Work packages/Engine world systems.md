---
title: "Engine: world systems"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: world systems"
created: "2026-10-14"
modified: "2026-10-30"
---

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| [[PRC-1\|PRC-1]] | Light: emitters, ambient profiles, skylight curve driven by the Environment clock, luminosity at a point | Luminosity matches emitter falloff; client and server agree | [[WORLD-2\|WORLD-2]], [[GPL-2\|GPL-2]], [[ENV-1\|ENV-1]] | [[Slice 25 Interest\|25]] |
| [[PRC-2\|PRC-2]] | PvP visibility tiers (Full, Silhouette, Hidden) with reveal on contact | Tiers change at the configured distances and light levels | [[PRC-1\|PRC-1]] | [[Slice 25 Interest\|25]] |
| [[PRC-3\|PRC-3]] | Perception profiles: warn and detect radii from light and concealment, with a minimum | Radii shrink with darkness and stealth but never below the minimum | [[PRC-1\|PRC-1]] | [[Slice 33 Perception at night\|33]] |
| [[NAV-1\|NAV-1]] | Detour runtime, nav tiles streamed by cell, path queries behind MoveGoal | Paths cross cell borders; tiles load and unload with cells | [[WORLD-3\|WORLD-3]], [[COOK-6\|COOK-6]] | [[Slice 31 Navigation and spawning\|31]] |
| [[NAV-2\|NAV-2]] | Flight navigation: 3D paths through free space over the sparse cells for flying actors, respecting volumes and altitude ceilings | A flying NPC reaches a target behind an obstacle without entering a forbidden volume | [[NAV-1\|NAV-1]], [[WORLD-2\|WORLD-2]] | [[Slice 44 Expansion\|44+]] |
| [[AI-1\|AI-1]] | AI contracts and runtime shell: components, intents, working memory, AIDefinition, BehaviorTree.CPP adapter, brain pool, wake and sleep | A test tree ticks only while its NPC is awake | [[GPL-2\|GPL-2]], [[SIM-3\|SIM-3]] | [[Slice 32 AI brains\|32]] |
| [[AI-2\|AI-2]] | Command bridge and data assets: intents become movement and combat commands; tree loading, registries, personality profiles | AI commands pass the same validation as player commands | [[AI-1\|AI-1]], [[NAV-1\|NAV-1]], [[CMB-2\|CMB-2]] | [[Slice 32 AI brains\|32]] |
| [[AI-3\|AI-3]] | Perception lifecycle: Aggroable, warn and detect wake, target validation, leash, return home, sleep | A mob walks toward a warning, attacks on detection and returns past its leash | [[AI-1\|AI-1]], [[PRC-3\|PRC-3]] | [[Slice 33 Perception at night\|33]] |
| [[AI-4\|AI-4]] | Reactive combat: SkillStarted perception, incoming threat, reaction timer, defense choice | A mob answers a telegraphed skill with a defensive action within its reaction time | [[AI-2\|AI-2]], [[CMB-5\|CMB-5]] | [[Slice 34 Reactive combat\|34]] |
| [[AI-5\|AI-5]] | Instrumentation: per-brain trace, memory, utility and intent diagnostics | The trace explains each decision | [[AI-2\|AI-2]] | [[Slice 34 Reactive combat\|34]] |
| [[AI-6\|AI-6]] | Scale tests with thousands of loaded NPCs and controlled awake percentages | The tick budget holds at the target counts | [[AI-4\|AI-4]] | [[Slice 38 Battle scale\|38]] |
| [[ENV-1\|ENV-1]] | Environment clock: world time, day and night phase, sun direction and the skylight input Perception reads; the world epoch comes from configuration until [[PCS-2\|PCS-2]] issues it | Two simulations agree on the time of day; night starts at the same world time everywhere | [[SIM-1\|SIM-1]], [[WORLD-1\|WORLD-1]] | [[Slice 25 Interest\|25]] |
| [[ENV-2\|ENV-2]] | Deterministic wind field with a cyclic baseline routine: per-region direction at any angle and a signed speed (0 has no effect; a negative speed reverses the push without changing the angle) | The same position and time give the same wind on two simulations; a negative speed reverses the push without changing its angle | [[ENV-1\|ENV-1]] | [[Slice 42 Ships wind and currents\|42]] |
| [[ENV-3\|ENV-3]] | Current modulation over time: cyclic baseline routine, tide phase, season, weather | Every simulation samples the same current at the same time | [[ENV-1\|ENV-1]], [[WATER-5\|WATER-5]] | [[Slice 42 Ships wind and currents\|42]] |
| [[ENV-4\|ENV-4]] | Tides and gameplay waves | A tide opens and closes a path on schedule | [[ENV-1\|ENV-1]] | [[Slice 43 Tides waves and weather\|43]] |
| [[ENV-5\|ENV-5]] | Weather state and time-boxed overrides (effective time and duration) for weather, wind and currents; the baseline routine returns when they end | A storm and a wind event reach two simulations at the same world time and end on schedule, after which the routine resumes | [[ENV-1\|ENV-1]] | [[Slice 43 Tides waves and weather\|43]] |
| [[ENV-6\|ENV-6]] | World routines: cooked routes and schedules evaluated as position \= f(route, world time, seed), with slow deterministic drift (a cycle that does not match the clock plus a small seeded variation) | Two simulations compute the same routine position at the same world time, drift included | [[ENV-1\|ENV-1]] | [[Slice 43a Living world\|43a]] |
| [[WATER-1\|WATER-1]] | [[Core model water reports facts\|WaterSystem]] registry, planar water, WaterSample, cell fragments | Height and flow can be sampled anywhere; fragments load with cells | [[WORLD-3\|WORLD-3]], [[PHYS-1\|PHYS-1]] | [[Slice 40 Water bodies\|40]] |
| [[WATER-2\|WATER-2]] | Spline rivers, flow, connections and routes | A descending river crosses two cells without a seam | [[WATER-1\|WATER-1]] | [[Slice 40 Water bodies\|40]] |
| [[WATER-3\|WATER-3]] | BuoyantBody on [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] bodies, with an optional righting strength | A platform floats without drifting | [[WATER-1\|WATER-1]] | [[Slice 41 Floating and swimming\|41]] |
| [[WATER-4\|WATER-4]] | Character and object water movement | A crate drifts with the current; a character swims with current influence | [[WATER-3\|WATER-3]], [[GPL-1\|GPL-1]] | [[Slice 41 Floating and swimming\|41]] |
| [[WATER-5\|WATER-5]] | Ocean current fields from cooked vector grids | Current interpolates smoothly across the grid | [[WATER-1\|WATER-1]] | [[Slice 42 Ships wind and currents\|42]] |
| [[WATER-6\|WATER-6]] | WatercraftMovement: sail force, sail angle, lateral resistance | Faster downstream and with a favorable wind; a crosswind pushes sideways | [[WATER-4\|WATER-4]], [[ENV-2\|ENV-2]] | [[Slice 42 Ships wind and currents\|42]] |
| [[WATER-7\|WATER-7]] | Ship-group [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]]: a watercraft, its crew, passengers and cargo registered as one transfer-snapshot group | A ship with passengers and cargo crosses a simulation border with nothing lost or left behind | [[WATER-6\|WATER-6]], [[DSIM-3\|DSIM-3]] | [[Slice 42b Ships across borders\|42b]] |

---

↑ [[Work packages|Work packages]] · ← [[Engine GameplayAPI group|Engine: GameplayAPI group]] · [[Engine networking|Engine: networking]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: world systems · exported 2026-11-03
