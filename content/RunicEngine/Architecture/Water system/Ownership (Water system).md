---
title: "Ownership (Water system)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Ownership"
created: "2026-10-14"
modified: "2026-10-30"
---

| Part | Owner | Contains |
| :---- | :---- | :---- |
| [[Core model water reports facts\|WaterSystem]] and water bodies | Engine | Stable WaterBody and WaterRoute identities, cooked runtime fragments, the sampling API, planar, ocean, spline-river and flow-volume implementations, connection semantics |
| Interaction components | Engine | BuoyantBody, CharacterWaterMovement, ObjectWaterMovement, WatercraftMovement, WaterInteractionState |
| Streaming and [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] integration | Engine | Water fragments inside Region, Sector and Cell streaming; continuity across simulations |
| Authoring, cooking and debugging | Engine | RunicWaterBody3D and flow-painting tools in the [[Tools#RunicEditor\|RunicEditor]], [[Cooker\|the Cooker]]’s water pipeline, validation, [[Debug drawing\|debug drawing]] |
| Water content | Game | Named oceans, rivers, lakes, cave waterways, current and wind maps, waterfalls; materials, VFX, audio, wave style, foam |
| Profiles | Game | SwimProfile, BuoyancyProfile, ObjectWaterMovementProfile, WatercraftMovementProfile values |
| Water gameplay rules | Game | Breath and drowning, ability restrictions in water, magical currents, tide events, boss modifiers, navigation policy per connection |
| Ship contents | Game | Cargo, cannons, sails, crew, faction, equipment, trade and combat rules |
| Durable water state | A Game service stores it on the Go SDK; Game decides | Dam, lock or water-level states that must survive restarts |

---

↑ [[Water system|Water system (Engine)]] · [[Core model water reports facts|Core model: water reports facts]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Ownership · exported 2026-11-03
