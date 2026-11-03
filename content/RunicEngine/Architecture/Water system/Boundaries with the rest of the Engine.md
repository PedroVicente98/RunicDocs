---
title: "Boundaries with the rest of the Engine"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Boundaries with the rest of the Engine"
created: "2026-10-14"
modified: "2026-10-30"
---

| Boundary | Rule |
| :---- | :---- |
| [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] | Jolt owns collision, integration, mass, contacts and dynamic ship motion. Buoyancy and watercraft systems turn samples into forces before the Jolt step; CharacterWaterMovement turns them into desired motion for the CharacterVirtual. |
| [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] | River samples, vector-field cells and water tiles are never entities. Flecs holds WaterInteractionState, profile references, movement components, dynamic modifiers, AI intent and tags. |
| Scheduler | Buoyancy and water movement run in the 30 Hz realtime phase, step 4, before the Jolt step. Static water never ticks; tide and weather state update at 10 Hz in the Environment. |
| Movement and [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] | Ships carry passengers on deck because CharacterVirtuals update every tick on moving bodies. A ship hands off as a group with its passengers and cargo in one authority epoch. |
| Light and perception | Each water body may define underwater light attenuation by depth (Game values); luminosity and visibility use it like any ambient profile. |
| AI | Sea creatures use CharacterWaterMovement; AI intents are executed by the same movement as players. |
| Audio | WaterInteractionState drives water sound events; the Game’s presentation picks the sailing music context. |
| Presentation | The [[Core model water reports facts\|WaterSystem]] never calls Godot. Presentation extracts water render data; Godot adds all visual detail. |
| Network | Static water ships in cooked world packages and is never replicated per tick. Replication carries only dynamic changes: flow multipliers, water-level offsets, lock or dam state, temporary current modifiers, world-event changes. |
| Persistence | Durable water state is stored by a Game service on the Platform Go SDK and reaches the simulation through the service port when the owning region loads. |

| Server and runtime water data | Client presentation additions |
| :---- | :---- |
| Spline and planar surface samples | Render surface mesh and LODs |
| Bounds and spatial fragments | Water material and shader parameters |
| Depth and flow representation | Normal maps, foam, visual flow maps |
| Connections and navigation metadata | Reflection and refraction parameters |
| Dynamic gameplay state | Particles, spray, wakes |

---

↑ [[Water system|Water system (Engine)]] · ← [[Characters ships objects and bosses|Characters, ships, objects and bosses]] · [[Streaming caves and cross-simulation continuity|Streaming, caves and cross-simulation continuity]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Boundaries with the rest of the Engine · exported 2026-11-03
