---
title: "Buoyancy and movement are separate components"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Buoyancy and movement are separate components"
created: "2026-10-14"
modified: "2026-10-30"
---

BuoyantBody makes a [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] dynamic body float. A BuoyancyProfile can also set a righting strength that keeps the body upright: ships roll and pitch with the swell but never capsize. Current does not belong to buoyancy: a movement component decides how much flow an entity follows and how much it propels itself. An object can therefore float without moving, drift with the current, sail, or use a future custom movement.

![[arch-water-interaction-environment-to-jolt-and-characte.png]]
*Water interaction — environment to Jolt and characters*

*Water interaction — environment to Jolt and characters*

The Environment shapes every sample (tide level, current over time, swell) and gives ships their wind; only the four components turn those facts into forces for Jolt or desired motion for characters.

```cpp
struct BuoyancyProfile {
    Span<BuoyancyPoint> points;   // sampled every tick
    float buoyancy_scale;
    float linear_water_drag;
    float angular_water_drag;

    float righting_strength;      // keeps the body upright; ships never capsize
};

struct BuoyantBody { BuoyancyProfileId profile; };
```

| Movement component | Physical model | Current behavior | Examples |
| :---- | :---- | :---- | :---- |
| CharacterWaterMovement | CharacterVirtual | Profile-controlled current influence | Players, NPCs, enemies, bosses, sharks |
| ObjectWaterMovement | Jolt dynamic body \+ BuoyantBody | Follows current; self-propulsion may be zero | Crates, debris, drifting wreckage, lost cargo |
| WatercraftMovement | Jolt dynamic body \+ BuoyantBody | Current plus propulsion, sails (wind), steering and braking | Boats, ships, rafts |
| Custom movement | Engine extension point | Defined by its policy | Future special vehicles |

```text
AnchoredFloatingPlatform : Transform, JoltDynamicBody, BuoyantBody
                           (floats, does not follow current)
DriftingCrate            : Transform, JoltDynamicBody, BuoyantBody,
                           ObjectWaterMovement (self velocity 0, current coupling > 0)
MerchantShip             : Transform, JoltDynamicBody, ShipTag, BuoyantBody,
                           WatercraftMovement
Player                   : Transform, CharacterVirtual, CharacterTag,
                           CharacterMovement, CharacterWaterMovement
```

Tags such as ShipTag and CharacterTag classify entities but never select behavior: a floating crate is not a ship, and a future magical floating vehicle can use BuoyantBody with a different movement component.

---

↑ [[Water system|Water system (Engine)]] · ← [[Runtime API|Runtime API]] · [[Characters ships objects and bosses|Characters, ships, objects and bosses]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Buoyancy and movement are separate components · exported 2026-11-03
