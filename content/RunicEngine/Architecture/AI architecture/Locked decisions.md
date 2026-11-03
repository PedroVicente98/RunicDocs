---
title: "Locked decisions"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Locked decisions"
created: "2026-10-14"
modified: "2026-10-30"
---

| Decision | Direction |
| :---- | :---- |
| AI ownership | AI is an Engine gameplay module that registers components and systems into the simulation-owned [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] world; it never owns a separate world |
| Decision runtime | BehaviorTree.CPP, behind a Runic adapter |
| Communication | AI consumes authoritative Flecs state and event buffers and emits intents. Nodes never mutate combat, movement, physics or persistent state |
| Reactive combat | NPCs respond to perceived player actions. Imperfection comes from reaction time, action commitment, resources, positioning, knowledge limits and small utility noise |
| Perception | Warn and detect radii come from the light and perception API: base × light curve × concealment, clamped to a minimum and maximum. Stealth and invisibility are concealment values (zero means undetectable). There is no line-of-sight vision simulation. The Aggroable toggle remains for reasons unrelated to perception: dead, GM, protected |
| Wake and sleep | Brains are active only when relevant: warn or detect, damage, encounter or script activation, or another explicit wake source. Dormant and unloaded NPCs never tick full trees |
| Scheduler | Decisions and perception at 20 Hz, maintenance at 10 Hz, movement, combat and physics at 30 Hz |
| Editor | No embedded Groot2: a native Runic editor inside the [[Tools#RunicEditor\|RunicEditor]] on Godot’s GraphEdit, using the same assets as the runtime |
| Editor dependency | Runic::AI knows nothing about editor or UI code; the AI docks in GodotTools depend on AI contracts and editor services, never the reverse |
| Game boundary | The Engine provides generic mechanisms and nodes; RunicGame supplies concrete trees, personalities, content definitions and game-specific nodes |

**Rule:** the [[Behavior-tree runtime|behavior tree]] decides what an NPC wants to attempt; the authoritative simulation decides whether that action is legal and what actually happens.

**Outside this section:** navigation internals beyond the MoveTo and MoveGoal contract; final balance values (reaction times, radii, utility weights, leash distances); RunicGame content such as species, encounters and boss trees; persistent offline simulation.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Ownership (AI architecture)|Ownership (AI architecture)]] · [[Goals and non-goals|Goals and non-goals]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Locked decisions · exported 2026-11-03
