---
title: "Reactive combat and personality"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Reactive combat and personality"
created: "2026-10-14"
modified: "2026-10-30"
---

A rule like “30% chance to block” produces arbitrary-looking successes and failures. Instead, the NPC reasons about valid responses, and imperfection comes from when it perceives the threat, when it may react, its resources and position, whether it is already committed, and small controlled variation between close choices.

```cpp
BT::NodeStatus HasReactableThreat(BT::TreeNode& node) {
    auto* context = node.config().blackboard->get<AIBrainContext*>("RunicContext");
    flecs::entity self = context->world->entity(context->self);
    const auto* memory = self.get<AIWorkingMemory>();

    if (!memory || !memory->incomingThreat.valid) return BT::NodeStatus::FAILURE;
    if (context->simulationTime < memory->incomingThreat.reactAt) return BT::NodeStatus::FAILURE;
    return BT::NodeStatus::SUCCESS;
}

enum class DefensiveAction { Ignore, Block, Dodge, Counter };

DefensiveAction ChooseDefensiveAction(const CombatPersonality& p, const CombatState& combat,
                                      const IncomingThreat& threat, RandomStream& random)
{
    struct Candidate { DefensiveAction action; float score; };
    Candidate candidates[] = {
        { DefensiveAction::Ignore,  0.20f + p.aggression * 0.70f },
        { DefensiveAction::Block,   threat.blockable
                                      ? 0.40f + p.blockBias + p.caution * 0.40f : -1000.0f },
        { DefensiveAction::Dodge,   threat.dodgeable && combat.evasionCharges > 0
                                      ? 0.40f + p.dodgeBias + p.caution * 0.30f : -1000.0f },
        { DefensiveAction::Counter, combat.canCounter
                                      ? 0.30f + p.counterBias + p.aggression * 0.50f : -1000.0f }
    };
    for (Candidate& c : candidates)
        c.score += random.Range(-p.decisionNoise, p.decisionNoise);
    return MaxScore(candidates).action;
}
```

**Action commitment is the main source of believable failure.** The player starts HeavySlash; the NPC perceives it; the reaction timer expires; the tree chooses BeginDefense; the command reaches the defense rule the Game registered (in RunicGame, [[Defense Evasion Guard and armor#Guard|Guard]]). If the rule accepts it, the defense starts. If the NPC is committed, stunned or out of the defense resource, the command is rejected and the NPC may be hit. The NPC made the right decision and still failed, because it reacted too late or was already committed — which is better than making it randomly stupid.

| Archetype direction | Aggression | Caution | Block bias | Dodge bias | Counter bias |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Defensive guard | Lower | High | High | Low | Medium |
| Mobile rogue | Medium-high | Medium | None or low | High | High |
| Berserker | High | Low | Low | Low-medium | Medium-high |

These are personality dimensions, not balance; RunicGame authors the actual profiles, and all three reuse the same tree.

**Bosses use the same contract at greater complexity:** a root that checks critical mechanics, then reacting to threats, then phase behavior (phase one, two, three), then positioning, then default combat. A boss may weigh tank Guard, a Support starting a long cast, a rogue moving behind it or a dangerous ground cast; the tree decides which concern wins, and the boss still emits ordinary intents under the same authoritative combat rules.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Behavior-tree runtime|Behavior-tree runtime]] · [[Scheduler integration|Scheduler integration]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Reactive combat and personality · exported 2026-11-03
