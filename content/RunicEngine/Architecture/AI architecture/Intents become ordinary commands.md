---
title: "Intents become ordinary commands"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Intents become ordinary commands"
created: "2026-10-14"
modified: "2026-10-30"
---

```cpp
// Defensive actions are game-registered IDs; RunicGame maps them to its own rules.
enum class AIIntentType { MoveTo, FaceTarget, UseAbility, BeginDefense, EndDefense,
                          Evade, ClearTarget, ReturnHome, Investigate };

struct AIIntent {
    EntityId actor = 0;
    AIIntentType type {};
    EntityId target = 0;
    AbilityId ability = 0;
    DefenseId defense = 0;        // a game-registered defensive action
    WorldPosition position {};
};

class AIIntentBuffer {                // one per worker
public:
    void Push(const AIIntent& intent) { m_Intents.push_back(intent); }
    std::span<const AIIntent> Intents() const { return m_Intents; }
    void Clear() { m_Intents.clear(); }
private:
    std::vector<AIIntent> m_Intents;
};

BT::NodeStatus ChooseDefense(BT::TreeNode& node) {
    auto* context = node.config().blackboard->get<AIBrainContext*>("RunicContext");
    flecs::entity self = context->world->entity(context->self);
    const auto* personality = self.get<CombatPersonality>();
    const auto* memory = self.get<AIWorkingMemory>();
    if (!personality || !memory) return BT::NodeStatus::FAILURE;

    AIIntent intent {};
    intent.actor = context->self;
    const DefenseChoice choice = context->defenses->Choose(*personality, memory->incomingThreat, *context->random);
    switch (choice.kind) {            // the Game's registered defense chooser fills the choice
        case DefenseKind::Hold:    intent.type = AIIntentType::BeginDefense; intent.defense = choice.defense; break;
        case DefenseKind::Evade:   intent.type = AIIntentType::Evade;        intent.defense = choice.defense; break;
        case DefenseKind::Counter: intent.type = AIIntentType::UseAbility;   intent.ability = choice.ability; break;
        case DefenseKind::Ignore:  return BT::NodeStatus::SUCCESS;
    }
    context->intents->Push(intent);   // decide, never execute
    return BT::NodeStatus::SUCCESS;
}

// At the barrier, in a fixed worker order.
void ApplyAIIntents(AIIntentBuffers& buffers, SimulationCommandBuffer& commands) {
    for (AIIntentBuffer& intents : buffers) {
        for (const AIIntent& intent : intents.Intents()) {
            switch (intent.type) {
                case AIIntentType::BeginDefense: commands.Push(DefenseCommand{ .actor = intent.actor,
                                                     .defense = intent.defense, .active = true }); break;
                case AIIntentType::Evade:        commands.Push(DefenseCommand{ .actor = intent.actor,
                                                     .defense = intent.defense, .active = true }); break;
                case AIIntentType::UseAbility:   commands.Push(UseAbilityCommand{ .actor = intent.actor,
                                                     .ability = intent.ability, .target = intent.target }); break;
                case AIIntentType::MoveTo:
                case AIIntentType::Investigate:  commands.Push(MoveGoalCommand{ .actor = intent.actor,
                                                     .destination = intent.position }); break;
                default: break;
            }
        }
        intents.Clear();
    }
}
```

**Shared-command principle:** when an AI action means the same as a player action, it goes through the same validation and execution path, which automatically keeps cooldowns, action commitment, [[Defense Evasion Guard and armor#Guard|Guard]] rules, dodge resources, CC restrictions and the input queue authoritative. Defensive actions are game-registered IDs: the Engine emits BeginDefense, EndDefense or Evade with an ID, and RunicGame maps them to its Guard and Dodge rules.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Scheduler integration|Scheduler integration]] · [[Behavior-tree assets|Behavior-tree assets]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Intents become ordinary commands · exported 2026-11-03
