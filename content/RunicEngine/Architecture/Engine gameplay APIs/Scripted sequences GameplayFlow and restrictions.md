---
title: "Scripted sequences (GameplayFlow) and restrictions"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Engine gameplay APIs (Engine) › Scripted sequences (GameplayFlow) and restrictions"
created: "2026-10-14"
modified: "2026-10-30"
---

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

---

↑ [[Engine gameplay APIs|Engine gameplay APIs (Engine)]] · ← [[Light and perception|Light and perception]] · [[Quest runtime and the quest-creation API|Quest runtime and the quest-creation API]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Engine gameplay APIs (Engine) › Scripted sequences (GameplayFlow) and restrictions · exported 2026-11-03
