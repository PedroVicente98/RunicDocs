---
title: "AI architecture (Engine, Game)"
tags:
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-12"
---

AI is reasoning, not authority. The Engine’s AI module reads permitted facts, keeps bounded working memory, ticks behavior trees and emits intents; the simulation validates and executes those intents exactly like player commands. RunicGame supplies the trees, personalities, perception values and game-specific nodes.

### Ownership

| Part | Owner | Contains |
| :---- | :---- | :---- |
| Runic::AI | Engine | Flecs components, wake, perception, think, target and sleep systems, BehaviorTreeRuntime (the BehaviorTree.CPP adapter), brain pool, intent buffers, generic nodes |
| Runic::GodotTools (AI docks) | Engine (tool) | Behavior-tree editor on Godot’s GraphEdit, AI asset browser, inspectors, personality editor, validation, live debugger |
| Light and perception API | Engine | Warn and detect radii from light and concealment (see [[Engine gameplay APIs (Engine)\|Engine gameplay APIs]]) |
| Runic::Navigation | Engine | Detour runtime behind the MoveTo and MoveGoal contract |
| Perception values | Game | PerceptionProfiles, light curves, concealment values |
| Trees, personalities, NPC definitions | Game | XML behavior trees, CombatPersonality profiles, AIDefinitions |
| Game-specific nodes | Game | Boss mechanics, naval boarding decisions, world-boss contribution logic, named encounter phases |

### Locked decisions

| Decision | Direction |
| :---- | :---- |
| AI ownership | AI is an Engine gameplay module that registers components and systems into the simulation-owned Flecs world; it never owns a separate world |
| Decision runtime | BehaviorTree.CPP, behind a Runic adapter |
| Communication | AI consumes authoritative Flecs state and event buffers and emits intents. Nodes never mutate combat, movement, physics or persistent state |
| Reactive combat | NPCs respond to perceived player actions. Imperfection comes from reaction time, action commitment, resources, positioning, knowledge limits and small utility noise |
| Perception | Warn and detect radii come from the light and perception API: base × light curve × concealment, clamped to a minimum and maximum. Stealth and invisibility are concealment values (zero means undetectable). There is no line-of-sight vision simulation. The Aggroable toggle remains for reasons unrelated to perception: dead, GM, protected |
| Wake and sleep | Brains are active only when relevant: warn or detect, damage, encounter or script activation, or another explicit wake source. Dormant and unloaded NPCs never tick full trees |
| Scheduler | Decisions and perception at 20 Hz, maintenance at 10 Hz, movement, combat and physics at 30 Hz |
| Editor | No embedded Groot2: a native Runic editor inside the RunicEditor on Godot’s GraphEdit, using the same assets as the runtime |
| Editor dependency | Runic::AI knows nothing about editor or UI code; the AI docks in GodotTools depend on AI contracts and editor services, never the reverse |
| Game boundary | The Engine provides generic mechanisms and nodes; RunicGame supplies concrete trees, personalities, content definitions and game-specific nodes |

**Rule:** the behavior tree decides what an NPC wants to attempt; the authoritative simulation decides whether that action is legal and what actually happens.

**Outside this section:** navigation internals beyond the MoveTo and MoveGoal contract; final balance values (reaction times, radii, utility weights, leash distances); RunicGame content such as species, encounters and boss trees; persistent offline simulation.

### Goals and non-goals

**Goals**

* Reactive rather than rotation-only behavior: NPCs respond to player actions and changing combat facts.

* Cheap enough for an MMORPG: expensive thinking only for active, relevant NPCs, with spatial candidate sets.

* Data-driven tree authoring, so ordinary behavior changes need no engine recompile.

* One command path for humans and AI wherever practical: AI output becomes the same validated gameplay commands.

* Composable behavior: a small melee NPC, a dungeon elite, a search behavior, a companion and a raid boss share one runtime contract with different tree complexity.

* Observable behavior: developers can inspect current nodes, memory, utility scores, targets, reaction timers, event inputs and emitted intents.

* A headless-safe runtime with no Godot, window or editor dependency.

**Non-goals**

* A perfect combat bot that reads hidden player inputs or reacts with zero latency.

* Gameplay truth stored in BehaviorTree.CPP blackboards instead of Flecs components.

* Tree nodes that bypass combat, movement, cooldown, Guard, dodge or ability validation.

* One heavyweight tree instance for every dormant NPC in the world.

* Line-of-sight or realistic stealth vision; perception is radii scaled by light and concealment.

### Mental model

1. World truth (Flecs, combat and spatial systems) publishes permitted facts and events.

2. AI perception filters them for each NPC.

3. AI working memory holds what that NPC knows.

4. The behavior tree asks “what should I consider now?”.

5. Utility or policy choice asks “which valid response best fits this NPC?”.

6. An AI intent is emitted.

7. Normal gameplay command validation accepts or rejects it.

8. The authoritative result becomes new world truth.

| Layer | Owns | Example |
| :---- | :---- | :---- |
| World truth | Authoritative state and actual outcomes | The player started HeavySlash; the NPC has 24 Guard; the NPC is committed to an attack |
| AI knowledge | What this NPC may know, and when | The NPC perceived a blockable incoming attack and may react after reactAt |
| AI desire | What the decision layer wants the actor to do | BeginDefense, Evade, UseAbility, MoveTo |

### Module boundaries

```cpp
class AIModule {
public:
    void Register(flecs::world& world);
private:
    BehaviorTreeRuntime m_BehaviorTrees;
    AIIntentBuffers     m_Intents;      // one buffer per worker
};

void AIModule::Register(flecs::world& world) {
    RegisterAIComponents(world);
    RegisterAggroSystem(world);
    RegisterPerceptionSystem(world);
    RegisterThinkSystem(world);
    RegisterTargetSystem(world);
    RegisterSleepSystem(world);
}
```

Runic::AI is a Flecs-integrated module, not a second simulation engine: the SimulationRuntime owns the Flecs world, and AI registers data and work into it, owning only AI-specific runtime objects such as brain instances and intent buffers.

| Module | May depend on | Must not depend on |
| :---- | :---- | :---- |
| Runic::AI | Core and runtime contracts, Flecs, gameplay command and event contracts, Perception, Navigation, BehaviorTree.CPP | Godot, editor docks, client presentation |
| Runic::GodotTools (AI docks) | Runic::AI definitions and contracts, GodotTools, Godot’s GraphEdit | Authoritative simulation ownership; direct mutation of live combat state |
| RunicGame AI content | The public Runic AI extension API, game ability and content registries | Internal BehaviorTreeRuntime details where avoidable |

### Data model

```cpp
// Illustrative contract, not a frozen API.
using EntityId       = uint64_t;
using AbilityId      = uint32_t;
using AIDefinitionId = uint32_t;
using BrainHandle    = uint32_t;

struct NPC {};
struct Player {};
struct Aggroable {};          // toggle: off when dead, GM or protected

struct AggroSensor {
    PerceptionProfileId perception;   // warn/detect radii, min/max, light curve
    float leashRadius = 30.0f;
};

struct AIController {
    AIDefinitionId definition = 0;
    BrainHandle brain = 0;            // 0 while sleeping
};
```

struct AIActive {};           // toggle (CanToggle): active decision brain

```cpp
struct CombatPersonality {
    float aggression = 0.5f, caution = 0.5f;
    float blockBias = 0.5f, dodgeBias = 0.5f, counterBias = 0.5f;
    float minReactionTime = 0.20f, maxReactionTime = 0.40f;
    float decisionNoise = 0.10f;
};

struct IncomingThreat {
    EntityId attacker = 0;
    AbilityId ability = 0;
    double perceivedAt = 0.0, reactAt = 0.0;
    float estimatedTimeToImpact = 0.0f;
    bool blockable = false, dodgeable = false, valid = false;
};

struct AIWorkingMemory {
    EntityId combatTarget = 0;
    IncomingThreat incomingThreat;
    double lastEnemySeenTime = 0.0, lastCombatTime = 0.0;
    bool hasTarget = false;
    bool alerted = false;             // warn radius reached; investigating
    WorldPosition alertPosition {};
};

struct AIDefinition {                 // shared content; many NPCs reference one
    AIDefinitionId id = 0;
    std::string behaviorTreeName;
    CombatPersonality defaultPersonality;
    PerceptionProfileId defaultPerception;
    float defaultLeashRadius = 30.0f;
};
```

BehaviorTree.CPP tree instances, nodes, blackboards, allocators and library-owned objects stay in the AI runtime; Flecs stores only a lightweight BrainHandle that refers to the runtime-owned brain.

| Stored in Flecs | Stored in the AI runtime |
| :---- | :---- |
| AIController, AIActive, AIWorkingMemory, CombatPersonality, target IDs, timers, aggro and leash state | BT::Tree instances, blackboards, node factories, per-brain random stream, tree-debug instrumentation |
| State other systems need or tools inspect | Implementation details needed to execute trees |

### Perception, wake, leash and sleep

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

### Events and perception pipeline

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

### Behavior-tree runtime

```cpp
class BehaviorTreeRuntime {
public:
    BehaviorTreeRuntime(flecs::world& world, AIIntentBuffers& intents);

    void        RegisterTree(AIDefinitionId definition, std::string_view xml);
    BrainHandle Wake(EntityId entity, AIDefinitionId definition);   // barrier only
    void        Sleep(BrainHandle brain);                            // barrier only
    void        Tick(BrainHandle brain, double simulationTime, WorkerIndex worker);

private:
    flecs::world&           m_World;
    BT::BehaviorTreeFactory m_Factory;
    BrainPool               m_Brains;
    AIIntentBuffers&        m_Intents;
};

struct AIBrainContext {
    EntityId          self = 0;
    flecs::world*     world = nullptr;
    AIIntentBuffer*   intents = nullptr;   // the ticking worker's buffer
    RandomStream*     random = nullptr;    // per brain, seeded: decisions are reproducible
    double            simulationTime = 0.0;
};

BrainHandle BehaviorTreeRuntime::Wake(EntityId entity, AIDefinitionId definition) {
    const auto& def = m_Definitions.Get(definition);
    auto blackboard = BT::Blackboard::create();
    BrainHandle handle = m_Brains.Create();
    BrainInstance& brain = m_Brains.Get(handle);

    brain.context.self   = entity;
    brain.context.world  = &m_World;
    brain.context.random = &brain.random;
    blackboard->set("RunicContext", &brain.context);

    brain.tree = m_Factory.createTree(def.behaviorTreeName, blackboard);
    return handle;
}

// 20 Hz pre-realtime phase, in parallel by NPC.
void AIThinkSystem(flecs::world& world, BehaviorTreeRuntime& runtime, double now) {
    auto query = world.query_builder<AIController, AIWorkingMemory>()
        .with<NPC>().with<AIActive>().build();
    query.each([&](flecs::iter& it, size_t, AIController& controller, AIWorkingMemory&) {
        if (controller.brain != 0)
            runtime.Tick(controller.brain, now, it.world().get_stage_id());
    });
}

void BehaviorTreeRuntime::Tick(BrainHandle handle, double now, WorkerIndex worker) {
    BrainInstance& brain = m_Brains.Get(handle);
    brain.context.simulationTime = now;
    brain.context.intents = &m_Intents.ForWorker(worker);
    brain.tree.tickOnce();
}

BehaviorTreeRuntime::BehaviorTreeRuntime(flecs::world& world, AIIntentBuffers& intents)
    : m_World(world), m_Intents(intents)
{
    m_Factory.registerSimpleCondition("HasReactableThreat", HasReactableThreat);
    m_Factory.registerSimpleCondition("HasCombatTarget",    HasCombatTarget);
    m_Factory.registerSimpleCondition("CanAttackTarget",    CanAttackTarget);
    m_Factory.registerSimpleCondition("IsAlerted",          IsAlerted);
    m_Factory.registerSimpleAction("ChooseDefense",   ChooseDefense);
    m_Factory.registerSimpleAction("ChooseAttack",    ChooseAttack);
    m_Factory.registerSimpleAction("ApproachTarget",  ApproachTarget);
    m_Factory.registerSimpleAction("InvestigateAlert", InvestigateAlert);
    m_Factory.registerSimpleAction("Idle",            Idle);
}
```

Threading follows the simulation’s rules: brains tick in parallel, each worker writes intents into its own buffer, and brain creation or release happens only at the barrier.

### Reactive combat and personality

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

**Action commitment is the main source of believable failure.** The player starts HeavySlash; the NPC perceives it; the reaction timer expires; the tree chooses BeginDefense; the command reaches the defense rule the Game registered (in RunicGame, Guard). If the rule accepts it, the defense starts. If the NPC is committed, stunned or out of the defense resource, the command is rejected and the NPC may be hit. The NPC made the right decision and still failed, because it reacted too late or was already committed — which is better than making it randomly stupid.

| Archetype direction | Aggression | Caution | Block bias | Dodge bias | Counter bias |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Defensive guard | Lower | High | High | Low | Medium |
| Mobile rogue | Medium-high | Medium | None or low | High | High |
| Berserker | High | Low | Low | Low-medium | Medium-high |

These are personality dimensions, not balance; RunicGame authors the actual profiles, and all three reuse the same tree. The defensive actions in the example (Block, Dodge, Counter) are RunicGame’s list; the Engine provides threat perception, the reaction timer and the scoring helper.

**Bosses use the same contract at greater complexity:** a root that checks critical mechanics, then reacting to threats, then phase behavior (phase one, two, three), then positioning, then default combat. A boss may weigh tank Guard, a Support starting a long cast, a rogue moving behind it or a dangerous ground cast; the tree decides which concern wins, and the boss still emits ordinary intents under the same authoritative combat rules.

### Scheduler integration

| Domain and phase | AI responsibility | Result |
| :---- | :---- | :---- |
| 10 Hz maintenance | Wake scans, sleep and leash maintenance, low-priority idle and world AI | Activation changes and coarse intentions; no realtime combat |
| 20 Hz pre-realtime | Validate targets, advance memory, tick active trees, translate output into intents and commands | Commands ready for the next realtime phase |
| 30 Hz realtime | Apply commands, movement, combat timelines, Guard, dodge, abilities, Jolt queries, hits, damage and effects | Authoritative results and gameplay facts |
| 20 Hz post-realtime | Consume relevant combat facts and update perception and memory | Knowledge ready for a later decision tick |

Within one 60 Hz master step: due 10 and 20 Hz producers validate targets, tick AI and emit intents; the 30 Hz realtime phase applies commands, runs movement, combat and Jolt and produces SkillStarted, Damage and Death facts; due 20 Hz consumers then update AI memory.

**Spatial locality:** aggro acquisition, threat fan-out and similar discovery always start from Runic cells and sectors, never “for every NPC, query every player” or “for every global event, tick every brain”. Flecs filters then apply to an already small candidate set.

### Intents become ordinary commands

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

**Shared-command principle:** when an AI action means the same as a player action, it goes through the same validation and execution path, which automatically keeps cooldowns, action commitment, Guard rules, dodge resources, CC restrictions and the input queue authoritative. Defensive actions are game-registered IDs: the Engine emits BeginDefense, EndDefense or Evade with an ID, and RunicGame maps them to its Guard and Dodge rules.

### Behavior-tree assets

```xml
<root BTCPP_format="4">
  <BehaviorTree ID="BasicMelee">
    <ReactiveFallback>
      <Sequence>
        <HasReactableThreat/>
        <ChooseDefense/>
      </Sequence>
      <Sequence>
        <HasCombatTarget/>
        <Fallback>
          <Sequence>
            <CanAttackTarget/>
            <ChooseAttack/>
          </Sequence>
          <ApproachTarget/>
        </Fallback>
      </Sequence>
      <Sequence>
        <IsAlerted/>
        <InvestigateAlert/>
      </Sequence>
      <Idle/>
    </ReactiveFallback>
  </BehaviorTree>
</root>
```

| Node | Responsibility |
| :---- | :---- |
| HasReactableThreat | Reads AIWorkingMemory and reaction timing; never discovers global events itself |
| ChooseDefense | Scores legal, meaningful defense families and emits one intent |
| HasCombatTarget | Checks that memory holds a current target |
| CanAttackTarget | Checks a coarse attack opportunity; final legality stays with command validation |
| ChooseAttack | Utility or priority choice among available abilities; emits UseAbility |
| ApproachTarget | Emits a movement goal through navigation and movement |
| IsAlerted, InvestigateAlert | The warn-radius behavior: walk to the sensed position, look around, give up after a Game-defined time |
| Idle | No expensive world scan; maintenance systems own wake conditions |

| Engine reusable nodes | Game content-specific nodes |
| :---- | :---- |
| HasCombatTarget, HasReactableThreat, TargetInRange, HealthBelow, IsAlerted, ChooseDefense, ApproachTarget, InvestigateAlert, ReturnHome | DragonWingSweepPolicy, NavalBoardingDecision, WorldBossContributionMechanic, named encounter phase logic |
| Generic ability-selection hooks and utility helpers | Actual skill IDs, encounter priorities, faction and game rules, boss mechanics |

### AI editor (inside the RunicEditor)

Runic builds its own editor inside the RunicEditor, on Godot’s GraphEdit, instead of embedding the standalone BehaviorTree.CPP editor. The library remains the executor; Runic owns the authoring experience so trees, NPC definitions, personalities, validation, asset management, world selection, Flecs inspection and live debugging live in one tool.

| Runic::AI (server-safe runtime) | Runic::GodotTools, AI docks (editor only) |
| :---- | :---- |
| AI components, definitions and contracts | GraphEdit behavior-tree canvas |
| BehaviorTreeRuntime | Node palette |
| Perception and think systems | Asset browser |
| Event consumers | Node and property inspector |
| Intent producer | Personality editor, validation, runtime debugger, selected-NPC inspection |

Runic::AI never includes or links Godot or editor code; the AI docks use the public AI definition and debug interfaces to author and inspect.

```cpp
struct BehaviorTreeAsset {
    AssetId id;
    std::string name;
    std::string xml;
};

runtime.Load(treeAsset);   // runtime
editor.Open(treeAsset);    // editor: edits and saves the asset, never a live BT::Tree

struct AINodeMetadata {
    std::string_view name;
    std::string_view category;
    std::string_view description;
    bool engineNode = true;
};

// One registration feeds both execution and editor discovery.
template <class T>
void RegisterAINode(BT::BehaviorTreeFactory& factory, AIEditorRegistry& editorRegistry,
                    AINodeMetadata metadata) {
    factory.registerNodeType<T>(std::string(metadata.name));
    editorRegistry.Register<T>(metadata);   // category, docs, ownership, icons, allowed contexts
}
```

| Panel | Purpose |
| :---- | :---- |
| AI Assets | Create, duplicate, rename, organize, open and delete trees; browse NPC definitions and personality profiles |
| Behavior Tree Canvas | Create, select and connect nodes; arrange, zoom and pan; validate structure; edit subtrees |
| Inspector | Node ports and properties plus Runic metadata and documentation |
| NPC Definition Inspector | Assign tree, personality, perception profile, leash defaults and Game AI profile fields |
| Runtime Debug | The selected live NPC: active node path, working memory, target, reaction timer, utility scores, last events, last intent |
| Validation and Problems | Missing nodes, invalid ports, unknown ability or content IDs, unreachable branches, forbidden dependencies |

**Editor actions**

* New tree from a template: Empty, Basic Melee, Ranged, Companion, Boss Phase Skeleton.

* Create or edit CombatPersonality profiles and preview how biases change utility.

* Assign a tree to an NPC archetype and jump from the NPC inspector straight to its tree.

* Validate referenced abilities, statuses, factions and RunicGame content IDs against the loaded registries.

* Open a live entity from the Flecs inspector and attach the AI debugger to its BrainHandle.

* Visualize wake or sleep state, warn, detect and leash radii, target and last perception facts in the viewport with the debug layers.

* Save trees independently of the live simulation; hot reload only through a development-only safe-point operation.

**Interaction rules**

* Graph editing is editor state, not simulation state.

* Runtime highlights are read-only overlays unless a specific debug command is implemented.

* Live tree replacement happens only at an explicit safe point; a tree is never destroyed or replaced while it ticks.

* The editor’s node list comes from the runtime’s registration plus editor metadata, never a second hard-coded list.

### Runtime AI debugging

The RunicEditor attaches to development and staging servers through the GameServer’s Diagnostics layer and shows:

| Debug view | Minimum information |
| :---- | :---- |
| Brain summary | Entity, AIDefinition, tree asset, BrainHandle, active or sleeping, current target |
| Tree execution | Running, succeeded and failed nodes for the current or previous tick, with the subtree path |
| Working memory | IncomingThreat, reactAt, target, last combat time, alert position, leash and home state, Game-exposed values |
| Utility trace | Candidates, base scores, major modifiers, decision noise, selected result |
| Event trace | Recent facts this NPC’s perception consumed |
| Intent trace | Recent intents and whether the resulting command was accepted or rejected |
| Spatial debug | Warn, detect and leash radii, navigation goal, target marker |

Explainability is an engineering feature: a developer can answer “why did this NPC block?”, “why did it ignore that attack?”, “why is it still awake?” or “why did the command fail?” by following event, memory, tree branch, utility choice, intent and validation result — without stepping through library internals.

### Repository layout

```text
RunicEngine/
  Engine/
    WorldSystems/AI/
      Public/   AIModule.hpp  AIComponents.hpp  AIDefinition.hpp  AIIntent.hpp
      Source/
        Runtime/        BehaviorTreeRuntime.cpp  BrainPool.cpp
        BehaviorTree/   Conditions.cpp  Actions.cpp  UtilityDecision.cpp
        Systems/        AggroSystem.cpp  AIPerceptionSystem.cpp  AIThinkSystem.cpp
                        AITargetSystem.cpp  AISleepSystem.cpp
      Tests/
    Tools/GodotTools/
      Source/AI/  AIDocks.cpp  BehaviorTreeGraph.cpp  NodePalette.cpp  TreeInspector.cpp
                  PersonalityEditor.cpp  RuntimeAIDebugger.cpp  AIValidation.cpp

RunicGame/
  Data/AI/
    basic_melee.xml  basic_archer.xml  personalities/  perception/  bosses/
  Source/Server/AI/
    GameSpecificAINodes.cpp
```

| Target | Content | Shipped in |
| :---- | :---- | :---- |
| Runic::AI | Generic runtime AI, Flecs systems, tree adapter, definitions, intents and events | GameServer; GameClient only if client-side AI is ever needed |
| Runic::GodotTools (AI docks) | GraphEdit tree editor, inspectors, debug tools | RunicEditor only |
| RunicGame AI | Trees, personalities, perception profiles, game-specific nodes and rules | Game content and RunicGame::Server |

### Performance and scaling

| NPC state | AI cost |
| :---- | :---- |
| Unloaded | Zero |
| Loaded, dormant | No live tree; cheap structural presence and the 10 Hz wake scan only |
| Awake nearby (alerted or engaged) | Active brain; 20 Hz decisions and perception |
| In combat | Active brain plus event-driven memory updates |
| Boss or elite | More complex tree, utility and encounter state behind the same contract |

* No tree ticks for dormant or unloaded NPCs.

* Spatial cells and sectors produce the candidates for wake scans and threat perception.

* Hot combat facts travel in event buffers, not through Flecs observers.

* Hot mutable AI state stays compact in Flecs; BehaviorTree.CPP object graphs stay in the runtime.

* Shared definitions and tree assets; per-entity state holds only what is truly mutable.

* No structural add and remove churn in hot paths; AIActive and Aggroable are toggles.

* Profile brain count, average and p95 tree tick time, event fan-out, candidate counts, intent counts and rejected-command rates.

* If per-brain BehaviorTree.CPP cost becomes material at very high counts, keep the public Runic AI contracts and consider a data-oriented Runic executor later — only after profiling.

### Tests

| Area | Representative tests |
| :---- | :---- |
| Perception | A hostile entering detect radius wakes the NPC engaged; entering only warn radius wakes it alerted; high concealment shrinks the radii; the minimum radius still detects in total darkness; damage wakes from outside both radii |
| Target validity | Death, concealment beyond detect range or leash break invalidates or changes behavior according to policy |
| Reaction timing | A threat before reactAt fails HasReactableThreat; the same threat after reactAt succeeds |
| Utility | Unavailable actions score invalid; personality biases change ordering; a fixed seed reproduces a choice |
| Intent boundary | A tree action emits the expected intent and never changes CombatState directly |
| Command rejection | Choosing a defensive action while committed is rejected; AI never bypasses combat rules |
| Wake and sleep | A BrainHandle is created on wake and recycled on sleep; dormant entities never tick a tree |
| Editor validation | Unknown nodes, ports or content IDs are reported; valid assets round-trip without loss |

**Integration tests**

1. An NPC detects a player, approaches, attacks, reacts to a telegraphed attack and returns home after a leash break.

2. At night an unlit player passes outside the reduced detect radius unnoticed, while a player carrying a torch is detected from farther away.

3. A player raises concealment while engaged; the target is dropped according to Game policy, and lowering it makes the player detectable again.

4. An NPC chooses a defense after its action became non-cancellable and correctly fails to execute it.

5. A SkillStarted fact produced in the realtime phase reaches AI memory only in the post-realtime phase and is acted on in a later pre-realtime tick.

6. Runic::AI builds and runs headless with no Godot or editor dependency.

7. Selecting a live NPC in the RunicEditor shows the same BrainHandle, tree, memory and intents the runtime instrumentation records.

### Implementation order

| Step | Deliverable |
| :---- | :---- |
| 1\. Contracts | AI components and tags, AIIntent, AIWorkingMemory, AIDefinition, event-view interfaces |
| 2\. Runtime shell | BehaviorTreeRuntime, BrainPool, basic node registration, Wake and Sleep, a tiny test tree |
| 3\. Perception lifecycle | Aggroable toggle, perception profiles from the light API, warn and detect wake, target validation, leash, return home, sleep |
| 4\. Command bridge | Intents translated into movement and combat commands and validated normally |
| 5\. Reactive combat | SkillStarted perception, IncomingThreat, reaction timer, ChooseDefense utility |
| 6\. Data assets | Tree loading, AIDefinition registry, personality and perception profiles, BasicMelee content |
| 7\. Instrumentation | Per-brain execution trace; event, memory, utility and intent diagnostics |
| 8\. AI editor MVP | RunicEditor dock, asset browser, GraphEdit canvas, palette, inspector, XML save and load |
| 9\. Runic-specific tools | NPC definition editor, personality editor, content-ID validation, live entity attachment |
| 10\. Scale tests | Thousands of loaded NPCs with controlled awake percentages; profile tree ticks, perception fan-out, spatial queries and allocations |

The steps map to work packages: steps 1 and 2 are AI-1, and steps 4 and 6 are AI-2 (slice 32, AI brains); step 3 is AI-3 (slice 33, perception at night); step 5 is AI-4 and step 7 is AI-5 (slice 34, reactive combat); steps 8 and 9 are GDT-11 and GDT-12 (slice 35, AI editor); step 10 is AI-6 (slice 38, battle scale).

### Invariants

* AI registers into the simulation-owned Flecs world and never creates a competing authoritative world.

* BehaviorTree.CPP stays isolated behind Runic::AI interfaces, apart from the approved node base types for custom nodes, and Flecs components never expose its types as gameplay state.

* AI reads filtered facts, events and Flecs state; trees never scan global systems directly.

* AI outputs intents only; combat, movement and navigation execute through their normal authoritative paths.

* Perception uses warn and detect radii from light and concealment, with a guaranteed minimum; there is no line-of-sight vision model.

* Dormant NPCs never keep live tree instances.

* Spatial candidate lookup always comes before perception filtering.

* Reaction time, resources, commitment and positioning create believable imperfection; a raw defense chance is never the main model.

* 20 Hz is the decision and perception domain; 30 Hz stays the authoritative realtime domain.

* Brains tick in parallel with per-worker intent buffers; wakes and sleeps happen at barriers.

* Editor code is a separate target and never required by a headless server.

* The AI editor runs in the RunicEditor on GraphEdit and edits shared assets; Groot2 is not embedded.

* Debugging exposes the chain event, memory, tree, utility, intent, command result.

* The Engine supplies reusable mechanics; RunicGame owns trees, personalities, perception values, encounters and game-specific nodes.

### Example NPC lifecycle

1. **Spawned or region loaded:** a dormant Flecs entity with NPC, AIController, AggroSensor, personality and memory, and no live BrainHandle.

2. **Warn radius reached:** wake alerted; the tree investigates the sensed position and, finding nothing, returns to dormancy.

3. **Detect radius reached or damage taken:** wake engaged; a tree instance is created, AIActive is enabled and the target is set.

4. **20 Hz decision loop:** the tree emits MoveTo, UseAbility, BeginDefense or Evade; commands are validated; the 30 Hz phase runs movement, combat and Jolt; resulting facts update perception; the loop repeats.

5. **Target invalid or leash broken:** ReturnHome.

6. **Reset:** eligible combat state is reset by Game rules.

7. **Sleep:** the BrainHandle is released to the pool and AIActive is disabled; the NPC is dormant again.
