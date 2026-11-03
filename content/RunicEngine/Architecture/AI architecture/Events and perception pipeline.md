---
title: "Events and perception pipeline"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Events and perception pipeline"
created: "2026-10-14"
modified: "2026-10-30"
---

Behavior trees never subscribe to the whole global event stream. AI perception systems consume relevant facts, apply spatial and eligibility filters and update AIWorkingMemory; trees read that bounded memory.

| Simulation fact | Typical AI use |
| :---- | :---- |
| SkillStartedEvent | Create or refresh IncomingThreat for NPCs that are plausible targets or observers |
| DamageEvent | Wake a dormant NPC if appropriate; set or raise its combat target; remember the attacker |
| DeathEvent | Invalidate targets, change encounter state, react to ally or enemy death |
| StatusChangedEvent | Update knowledge relevant to choosing abilities or defenses |
| Encounter control event | Wake, sleep or phase changes for scripted content |

```cpp
struct SkillStartedEvent {
    EntityId caster = 0;
    AbilityId ability = 0;
    double startTime = 0.0;
    WorldPosition position {};
    Vec3 facing {};
};

// 20 Hz post-realtime phase.
void AIPerceptionSystem(flecs::world& world, const CombatEventBuffer& events,
                        const SpatialWorld& spatial, double now)
{
    for (const SkillStartedEvent& event : events.skillStarted) {
        const AbilityDefinition& ability = GetAbility(event.ability);

        SmallVector<EntityId, 32> candidates;
        spatial.QueryActorsSphere(event.position, ability.threatAwarenessRadius, candidates);

        for (EntityId id : candidates) {
            flecs::entity npc = world.entity(id);
            if (!npc.has<NPC>() || !npc.is_enabled<AIActive>()) continue;

            auto* memory = npc.get_mut<AIWorkingMemory>();
            const auto* personality = npc.get<CombatPersonality>();
            if (!memory || !personality) continue;
            if (!CouldThreatenNPC(event, ability, npc)) continue;

            const float reaction = RandomRange(personality->minReactionTime,
                                               personality->maxReactionTime);
            memory->incomingThreat = {
                .attacker = event.caster,
                .ability = event.ability,
                .perceivedAt = now,
                .reactAt = now + reaction,
                .estimatedTimeToImpact = EstimateImpactTime(event, ability, npc),
                .blockable = ability.HasTag("Blockable"),
                .dodgeable = ability.HasTag("Dodgeable"),
                .valid = true };
        }
    }
}
```

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Perception wake leash and sleep|Perception, wake, leash and sleep]] · [[Behavior-tree runtime|Behavior-tree runtime]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Events and perception pipeline · exported 2026-11-03
