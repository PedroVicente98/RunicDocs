---
title: "Characters, ships, objects and bosses"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Water system (Engine) › Characters, ships, objects and bosses"
created: "2026-10-14"
modified: "2026-10-30"
---

**Characters swim, they do not float as rigid bodies.** CharacterWaterMovement owns the character version of floating, swimming acceleration, vertical swimming, drag, surface behavior and current influence, and feeds desired motion into the CharacterVirtual.

```cpp
struct SwimProfile {
    float max_speed, vertical_speed, acceleration, deceleration;
    float passive_float_strength;   // humanoids drift up; sharks 0
    float sink_speed;               // heavy armor sinks faster
    float water_drag;
    float current_influence;
};

struct WaterInteractionState {      // written once per tick, read by everyone
    WaterBodyId body;
    float submerged_fraction;
    bool  feet_submerged;
    bool  swimming;
    bool  head_submerged;           // the Game drives breath from this
};
```

WaterInteractionState lets animation, audio, combat, UI and Game rules read water facts without each issuing its own query.

**Watercraft** combine player or AI intent with the local flow and the local wind, then apply forces and torques to the [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] body. Downstream is naturally faster than upstream, and a sailing ship depends on the wind angle. The Engine never knows what a ship carries or who owns it. WatercraftMovementProfile gains lateral\_current\_influence: current\_influence scales the flow along the hull and lateral\_current\_influence the flow across it, so a ship class can barely drift in side currents. Draft needs no new field: a hull's collision shape reaches down to its keel, so the seafloor, reefs and sandbanks touch it only where they are shallower.

```cpp
struct WatercraftMovementProfile {
    float propulsion_force;         // oars, engines, magic
    float reverse_force;
    float steering_force;
    float braking_force;
    float current_influence;
    float sail_force;               // 0 = no sails; scaled by wind (see Environment)
    CurveId sail_angle_curve;       // efficiency by angle between wind and heading
    float lateral_resistance;       // keel: resists sideways drift from wind
};

struct ObjectWaterMovementProfile {
    float self_propulsion   = 0.0f;
    float current_influence = 1.0f;
};

struct SwimMovementModifiers {      // temporary boss charges, buffs
    float speed_multiplier = 1.0f, acceleration_multiplier = 1.0f;
    float turn_multiplier  = 1.0f, current_influence_multiplier = 1.0f;
};
```

**Water bosses** stay Characters to the movement system: a SwimProfile with very high speed, acceleration or turn authority, and AI intents such as circle, dive, charge, breach or retreat. The Engine executes the swimming; the Game decides why and when.

---

↑ [[Water system|Water system (Engine)]] · ← [[Buoyancy and movement are separate components|Buoyancy and movement are separate components]] · [[Boundaries with the rest of the Engine|Boundaries with the rest of the Engine]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Water system (Engine) › Characters, ships, objects and bosses · exported 2026-11-03
