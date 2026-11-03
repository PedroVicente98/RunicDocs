---
title: "Quest runtime and the quest-creation API"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Engine gameplay APIs (Engine) › Quest runtime and the quest-creation API"
created: "2026-10-14"
modified: "2026-10-30"
---

The quest runtime (Runic::Quest) runs inside the simulation on top of [[Scripted sequences GameplayFlow and restrictions|GameplayFlow]], so a kill or an interaction advances a quest in the same tick that produced the fact. Durable progress lives in the Game’s Go Quest service. The Engine owns the runtime and the API; the Game owns every quest.

The quest-creation API is how the Game makes quests:

* **Definitions are data.** A quest is an ID, its states and objectives, and for each transition a trigger, conditions, actions and the next state. Designers write them without C++, and [[Cooker|the Cooker]] validates them.

* **Registries extend the vocabulary.** The Engine ships generic triggers (entity killed, item acquired, interaction completed, area entered, sequence ended), conditions (quest state, has item, entity alive, time window) and actions (set objective, start sequence, request an item grant or removal through a service, spawn). The Game registers game: triggers, conditions and actions in C++ for anything specific to RunicGame.

* **A builder for code.** The same definitions can be built in C++ for tests and generated content; data and code end in the same registry.

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

5. The accepted result returns to the simulation and is applied at a later safe tick; a service callback never touches [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] directly.

6. Replaying the same fact changes nothing.

On login the character’s quest state loads from the service into the runtime. On [[Networking replication interest and handoff#Simulations, handoff and ghosts|handoff]], quest instances travel in the transfer snapshot with the rest of the player’s state.

---

↑ [[Engine gameplay APIs|Engine gameplay APIs (Engine)]] · ← [[Scripted sequences GameplayFlow and restrictions|Scripted sequences (GameplayFlow) and restrictions]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Engine gameplay APIs (Engine) › Quest runtime and the quest-creation API · exported 2026-11-03
