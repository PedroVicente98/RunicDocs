---
title: "Implementation stages"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Implementation stages"
created: "2026-10-14"
modified: "2026-10-30"
---

| Stage | Contents |
| :---- | :---- |
| A. Vertical proof | WaterSystem registry and sampling; planar water and one descending spline river; fragment registration in cells; four-point BuoyantBody on a [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] body; current-only ObjectWaterMovement; basic WatercraftMovement; CharacterWaterMovement; basic editor authoring (RunicWaterBody3D); [[Debug drawing\|debug drawing]] of centerline, surface and current |
| B. Generalize | Connections, river-to-ocean blending, rapids and waterfalls; ocean current fields; profiles and stable IDs; client and server package split; incremental water cooking; dynamic water-level state; WaterInteractionState for animation, audio and gameplay; navigation metadata; ocean gameplay swell, wave events (big waves, whirlpools) and the righting strength |
| C. Production | Large fleet profiling and telemetry; tides, locks and stateful waterways; advanced rendering, shoreline foam and wakes; water navigation graph and AI vessel routes; cross-simulation stress tests on long waterways |

**Definition of done for the first water slice:** author a descending river in the [[Tools#RunicEditor|RunicEditor]] and cook it; stream it across at least two cells with no seam; render it on the client and sample its surface and current on the server; a boat with BuoyantBody and WatercraftMovement travels downstream faster than upstream; a BuoyantBody-only object floats without drifting; a crate with ObjectWaterMovement drifts with zero self-propulsion; a character swims with current influence and no rigid-body buoyancy; the river enters a cave volume continuously and reaches an underground lake or ocean without a teleport or instance; repeated with two networked clients, ship and character transitions stay continuous.

---

↑ [[Water system|Water system (Engine)]] · ← [[Debugging and validation|Debugging and validation]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Implementation stages · exported 2026-11-03
