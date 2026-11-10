---
title: "Engine gameplay APIs (Engine)"
tags:
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-10"
---

The Engine provides generic, thread-safe building blocks for gameplay, grouped under the GameplayAPI umbrella: Runic::Gameplay (character state, movement, restrictions, interactions, items), Runic::Combat (abilities, hits, statuses, rules, damage, threat), Runic::GameplayFlow (scripted sequences) and Runic::Quest (the quest runtime). Each is its own module with its own boundary and tests. The Engine knows timelines, tags, statuses, rules, threat and perception, but not Stagger, Guard or any concrete rule.

| API | Module | What the Engine provides | What a game supplies |
| :---- | :---- | :---- | :---- |
| Ability toolkit | Combat | Timeline runner in DomainTickCount (startup, active, recovery, cancel windows); hit volumes and projectile queries; cooldowns; resource pools; one-slot input queue | Ability definitions, timings, costs, queue window |
| Hit timing | Combat | ServerTime and CappedRewind (with a per-character position history), chosen per ability | The choice per ability and the cap |
| Tags | Gameplay | Hierarchical, interned tags on abilities, statuses and entities | The vocabulary (Impact, Finisher, Opener…) |
| Status container | Combat | Timed statuses with stacking policy, duration, periodic tick and immunity windows | Every concrete status (Bleed, Stagger, Freeze) |
| Attributes and modifiers | Gameplay | Base values and modifier stacks (add, multiply, override) with caps | Stats and formulas |
| Rule pipeline | Combat | Registration of typed conditions and modifiers; evaluation in named stages; outputs to per-worker buffers; compilation into a resolved loadout per character; value variants chosen by a per-hit context (e.g., PvE and PvP) | Stage order and every condition and modifier |
| Damage interception | Combat | Hooks before and after damage is applied; invulnerability windows | Guard, Evasion, armor, the damage formula |
| Threat table | Combat | Per-NPC threat storage read by AI target selection | What generates threat; taunt; Challenge |
| Behavior registries | Combat | ID-to-C++ registration, parameter schemas, a fixed hook list, read-only context and output buffers | The behaviors |
| Restrictions | Gameplay | Source-owned restriction sets (input, movement, abilities, interactions, targeting, damage, external motion), release by source, command validation | Which skills, effects and sequences acquire which restrictions |
| Interactions | Gameplay | Interaction volumes, reach and permission checks, reservation, an interaction registry | Levers, rituals, gathering, cartography |
| Movement | Gameplay | CharacterVirtual integration; a movement-mode registry with walk, glide (reads Environment wind), flight inside flight-zone volumes, mount and vehicle modes; Water registers swimming (CharacterWaterMovement); prediction hooks; server validation | Speeds, dashes, mount, glider and wing stats |
| Item runtime | Gameplay | Runtime item instances and containers mirrored from services | Item definitions and rules |
| Scripted sequences | GameplayFlow | Sequence runtime, trigger, condition and action registries, timers, termination path, handoff policies | Boss phases, cutscenes, dungeon and world-event scripts |
| Quests | Quest | Quest runtime and quest-creation API, generic triggers, conditions and actions, durable-fact bridge | Every quest, Game-specific triggers, conditions and actions |

### Behavior registry contract

| Rule | Why |
| :---- | :---- |
| Behaviors are registered by ID; data refers to the ID | Content stays data; an unknown ID fails at load, not mid-fight |
| Parameters have a schema checked at load | Typos are caught by the Cooker, not by players |
| Hooks are a fixed list: OnActivate, OnPhaseChange, OnHitCandidate, OnHit, OnEffectTick, OnEffectExpire, OnKill, OnInteract | The engine knows exactly when custom code runs |
| A behavior subscribes only to the hooks it uses | Abilities without custom code cost nothing |
| Behaviors read a context and write an output buffer | Safe in parallel phases; outputs merge in a fixed order |
| Behaviors are stateless; per-instance state lives in components | Inspection and data reload stay simple |
| The same registry serves abilities, item effects, AI nodes and interactions | One extension model for any game |
| Data reloads live; changed C++ needs a restart | A scripting language can be added later behind the same registry |

### Light and perception

Light scales how far mobs notice entities and how far players see each other; it never changes how a hit is resolved.

| Element | What it is | What a game supplies |
| :---- | :---- | :---- |
| AmbientLightProfile | Light level per region and volume over time of day and weather, with a floor (“skylight”) | Curves per region, volume and weather |
| LightEmitter | Radius, intensity and duration on an entity or area | Torches, lanterns, lit abilities, items, area lights |
| Luminosity | Effective light on an entity: the brighter of ambient light and emitters reaching it | Nothing; computed |
| Concealment | Multiplier on how far others detect or see the entity | Stealth, invisibility, gear values |
| PerceptionProfile | Warn and detect base radii, minimum and maximum, light curve, dark vision | Per mob definition |
| VisibilityProfile | Maximum visible range, silhouette range, light curve | Global or per region |

* Emitters are indexed in cells, so luminosity is a few lookups in neighboring cells. It updates at 10 Hz for players and for mobs awake or near players; lighting a torch updates it at once.

* Mob radius \= base × light curve (target luminosity) × target concealment, clamped to the profile’s minimum and maximum. The minimum guarantees detection in total darkness.

* Inside the warn radius a mob investigates; inside the detect radius it engages. A game that sets warn at or below detect never uses warn.

* Stealth and invisibility are concealment values; zero means undetectable. A separate Aggroable toggle covers non-perception cases (dead, GM, protected).

### Scripted sequences (GameplayFlow) and restrictions

GameplayFlow is the one authoritative runtime for scripted gameplay. Quests, boss phases, dungeons, cutscenes, escorts, tutorials and world events all run on it instead of each inventing its own timers and state machines. It belongs to the GameplayAPI group; the Game supplies every concrete sequence.

**Model.** A sequence is a graph of steps. Each step waits for a trigger, checks conditions, runs actions and moves to the next state:

TRIGGER → CONDITIONS → ACTIONS → STATE TRANSITION

Triggers and conditions read authoritative facts and state. Actions change the world only through Simulation commands and Gameplay APIs, the same doors players and AI use: starting an ability is a UseAbility command, changing an NPC’s behavior is an AI profile command. GameplayFlow never calls Combat or AI internals. Sequences run on the simulation thread at phase boundaries, and their timers use simulation time, never wall-clock time.

| Category | Generic actions |
| :---- | :---- |
| Entity | Spawn, despawn, enable, disable |
| State | Set a tag, state or value; set an objective or sequence variable |
| Movement | Move an entity, follow a path, teleport where explicitly legal |
| Interaction | Enable or disable an interaction; reserve or release a target |
| Combat | Request an ability through a command; apply an approved effect; end an encounter state |
| AI | Change a behavior profile or state through AI commands |
| World | Open or close a door, activate an object, set a world-state value |
| Timing | Delay, timeout, wait until a simulation time |
| Sequence | Start, stop or wait for a nested sequence |
| Event | Wait for or emit an authoritative fact |
| Restriction | Acquire or release input, movement, ability, interaction, targeting or damage restrictions |
| Presentation | Start dialogue or emit a presentation cue for clients |
| Service | Submit an asynchronous durable operation and wait for its accepted result |
| Branching | If, switch, random choice with an explicit seed |
| Synchronization | Wait for an entity, party, event or encounter condition |

The Engine provides these built-ins under engine: IDs. The Game registers its own actions and conditions under game: IDs for mechanics that are not reusable.

```cpp
// Illustrative
actions.Register("engine:spawn_entity", SpawnEntityAction{});
actions.Register("engine:start_sequence", StartSequenceAction{});

// RunicGame, server only
actions.Register("game:set_trade_route_state", SetTradeRouteStateAction{});

Sequence: BossPhase2
  Wait:     Boss.Health <= 70%
  Actions:  SetBossPhase(2)
            LockArenaDoors
            AcquireRestriction(Boss, DamageImmune)
            PresentationCue("game:dragon_phase_2")
            SpawnAdds
            WaitFor(AllAddsDead)
            ReleaseRestriction(Boss)
            RequestAbility("game:dragon_firestorm")
```

The phase, the adds, the cue and the ability are Game content. The waits, the cleanup, the fact handling and the calls into Engine APIs are Engine behavior.

**Cutscenes are server sequences with client presentation.** The server runs the sequence, acquires restrictions and emits presentation cues. The client plays camera, animation, dialogue, music and UI from the Game’s presentation definition and disables local controls for feel. The server keeps validating and rejecting blocked commands, so a modified client gains nothing.

**Source-owned restrictions.** No scattered flags such as invulnerable \= true. A sequence, a skill or an effect acquires a restriction set under its own source ID, and every exit path releases everything held by that source in one call.

```cpp
// Illustrative
RestrictionHandle handle = restrictions.Acquire(player, RestrictionSet{
    .input = Blocked, .movement = Blocked, .abilities = Blocked,
    .interactions = Blocked, .targeting = Untargetable,
    .damage = Immune, .externalMotion = Immune }, sequenceInstanceId);
```

restrictions.ReleaseAllFromSource(sequenceInstanceId);   // on every terminal path

Intangible during a cutscene is several separate policies (input, movement, abilities, interactions, targeting, damage, external motion, optional collision), so other systems can hold their own restrictions at the same time. Restrictions live in Runic::Gameplay; dodge invulnerability windows use the same mechanism.

**One termination path.** Complete, abort, cancel, timeout, disconnect, owner destruction, quest abandon, shutdown and transfer failure all converge on one routine. It cancels timers, releases the sequence’s restrictions and reservations, clears sequence-owned control and emits SequenceEnded or SequenceAborted. Temporary restrictions also carry an expiry and a watchdog diagnostic, so no fault can leave a player permanently invulnerable.

**Handoff policy.** Each sequence declares what happens when its owner’s authority moves to another simulation.

enum class HandoffPolicy { Transferable, PinAuthority, AbortOnTransfer };

A Transferable sequence travels in the final transfer snapshot with its step, its timers relative to simulation time, its restriction source IDs and its quest or encounter context. PinAuthority delays the transfer until a short, critical sequence ends. AbortOnTransfer runs the termination path first.

### Quest runtime and the quest-creation API

The quest runtime (Runic::Quest) runs inside the simulation on top of GameplayFlow, so a kill or an interaction advances a quest in the same tick that produced the fact. Durable progress lives in the Game’s Go Quest service. The Engine owns the runtime and the API; the Game owns every quest.

The quest-creation API is how the Game makes quests:

* **Definitions are data.** A quest is an ID, its states and objectives, and for each transition a trigger, conditions, actions and the next state. Designers write them without C++, and the Cooker validates them.

* **Registries extend the vocabulary.** The Engine ships generic triggers (entity killed, item acquired, interaction completed, area entered, state entered, sequence ended), conditions (quest state, has item, has state, entity alive, time window) and actions (set objective, start sequence, request an item grant or removal through a service, spawn). The Game registers game: triggers, conditions and actions in C++ for anything specific to RunicGame. They are items of the Runic API’s vocabulary (see [[Simulation core Flecs and Jolt (Engine)#The Runic API over Flecs and Jolt|The Runic API over Flecs and Jolt]]).

* **A builder for code.** The same definitions can be built in C++ for tests and generated content; data and code end in the same registry.

* **Triggers are facts, conditions are states.** “When the player mounts” is a trigger: an instant fact. “The player must be mounted” is a condition: a lasting state. Only observable states can be triggers, and the Cooker rejects a trigger on any other state.

* **WhenState fires once either way.** A state trigger fires when the state changes or, if the state already holds, when the quest enters that step, so a player who is already mounted is never stuck waiting for a change.

* **A quest never writes a state it does not own.** It requests the owner’s action: Mount, never Set(Mounted). The Cooker rejects a quest that writes another owner’s state.

* **Waiting belongs to the sequence.** An NPC that waits for the player is a WaitUntil(condition, timeout) step in GameplayFlow or in the NPC’s AI, not a quest state.

```cpp
Quest: game:the_stablemasters_test
  State WaitForMount
    Trigger:     WhenState(engine:mounted)
    Conditions:  InVolume(game:stable_yard)
                 Near(game:npc_stablemaster, 10 m)
    Actions:     StartSequence(game:ride_with_stablemaster)
    Next:        RideToVillage
```

```cpp
Quest: game:rescue_the_prisoner
  State OpenCell
    Trigger:     InteractionCompleted(game:prison_door)
    Conditions:  HasItem(game:cell_key), EntityAlive(game:prisoner)
    Actions:     OpenDoor(game:prison_door)
                 RemoveItem(game:cell_key)
                 StartSequence(game:prisoner_escape)
                 SetObjective(EscapeCastle)
    Next:        EscapeCastle

// Illustrative
QuestDefinition quest = QuestBuilder("game:rescue_the_prisoner")
    .State("OpenCell")
        .On(Trigger::InteractionCompleted("game:prison_door"))
        .If(Condition::HasItem("game:cell_key"))
        .If(Condition::EntityAlive("game:prisoner"))
        .Do(Action::StartSequence("game:prisoner_escape"))
        .Do(Action::SetObjective("EscapeCastle"))
        .GoTo("EscapeCastle")
    .Build();

quests.Register(std::move(quest));   // the same path loaded data takes
conditions.Register("game:faction_standing_at_least", FactionStandingCondition{});
```

The durable path:

1. Combat emits EntityKilled once, with a stable event ID.

2. The quest runtime consumes the fact, advances its local state and may start a sequence.

3. The fact leaves through the Simulation’s service port, and the Platform’s services-bridge layer carries it to the Quest service, asynchronously.

4. The service validates the source, deduplicates by event ID, updates progress and commits rewards in one transaction.

5. The accepted result returns to the simulation and is applied at a later safe tick; a service callback never touches Flecs directly.

6. Replaying the same fact changes nothing.

On login the character’s quest state loads from the service into the runtime. On handoff, quest instances travel in the transfer snapshot with the rest of the player’s state.
