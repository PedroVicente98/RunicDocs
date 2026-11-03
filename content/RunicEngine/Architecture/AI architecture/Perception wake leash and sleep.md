---
title: "Perception, wake, leash and sleep"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Perception, wake, leash and sleep"
created: "2026-10-14"
modified: "2026-10-30"
---

* **Radii:** each scan asks the light and perception API for the target’s warn and detect radii (base × light curve × concealment, clamped). The minimum guarantees detection in total darkness.

* **Warn:** the NPC wakes in the Alerted state and walks to where it sensed something; it does not attack.

* **Detect:** the NPC wakes engaged, with a combat target.

* **Concealment toggles:** stealth and invisibility change a value, not the archetype, so switching them often costs no structural churn.

| Wake source | Reason |
| :---- | :---- |
| Perception | A valid hostile Aggroable entity enters the warn radius (alert) or the detect radius (engage) |
| Damage received | An attacker wakes the NPC even from outside its radii |
| Encounter or script activation | Bosses, dungeons, world events, escorts or scripts wake the AI explicitly |
| Game-specific extension | RunicGame may add wake signals through the public AI API |

```cpp
// Runs in the 10 Hz maintenance phase, in parallel by NPC.
// Wakes are queued per worker and applied at the barrier.
void AggroWakeSystem(flecs::world& world, const SpatialWorld& spatial,
                     const PerceptionApi& perception, WakeRequestBuffers& wakes)
{
    auto query = world.query_builder<const Transform, const AggroSensor,
                                     const AIWorkingMemory>()
        .with<NPC>().without<AIActive>().build();

    query.each([&](flecs::iter& it, size_t i, const Transform& t,
                   const AggroSensor& sensor, const AIWorkingMemory& memory)
    {
        const PerceptionProfile& profile = perception.Profile(sensor.perception);
        SmallVector<EntityId, 32> nearby;
        spatial.QueryActorsSphere(t.position, profile.max_radius, nearby);

        for (EntityId id : nearby) {
            flecs::entity other = world.entity(id);
            if (!other.has<Player>() || !other.has<Aggroable>()) continue;
            if (!IsHostile(it.entity(i), other)) continue;

            const PerceptionRadii r = perception.RadiiFor(profile, other); // light x concealment
            const double d = Distance(t.position, other.get<Transform>()->position);

            if (d <= r.detect) {
                wakes.Local(it).Push({it.entity(i).id(), id, WakeReason::Detect});
                return;
            }
            if (d <= r.warn && !memory.alerted)
                wakes.Local(it).Push({it.entity(i).id(), id, WakeReason::Warn});
        }
    });
}

// At the barrier: create brains, set memory, enable AIActive.
void ApplyWakes(flecs::world& world, WakeRequestBuffers& wakes,
                BehaviorTreeRuntime& ai);

void SleepNPC(flecs::entity npc, BehaviorTreeRuntime& runtime) {
    auto* controller = npc.get_mut<AIController>();
    if (!controller) return;
    if (controller->brain != 0) {
        runtime.Sleep(controller->brain);   // recycled into the brain pool
        controller->brain = 0;
    }
    npc.disable<AIActive>();
}
```

* A target dying, becoming non-aggroable, rising in concealment beyond the detect radius, disconnecting or otherwise becoming invalid triggers target reevaluation.

* Leaving the leash boundary moves the NPC to ReturnHome instead of sleeping in place.

* After returning home and satisfying any Game reset rules, the brain is released to the pool.

* Unloading a region removes the entity from the simulation entirely; the AI runtime never keeps offline brains alive.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Data model|Data model]] · [[Events and perception pipeline|Events and perception pipeline]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Perception, wake, leash and sleep · exported 2026-11-03
