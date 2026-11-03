---
title: "Engine gameplay APIs (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Engine gameplay APIs (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

The Engine provides generic, thread-safe building blocks for gameplay, grouped under the GameplayAPI umbrella: Runic::Gameplay (character state, movement, restrictions, interactions, items), Runic::Combat (abilities, hits, statuses, rules, damage, threat), Runic::GameplayFlow (scripted sequences) and Runic::Quest (the quest runtime). Each is its own module with its own boundary and tests. The Engine knows timelines, tags, statuses, rules, threat and perception, but not Stagger, [[Defense Evasion Guard and armor#Guard|Guard]] or any concrete rule.

| API | Module | What the Engine provides | What a game supplies |
| :---- | :---- | :---- | :---- |
| Ability toolkit | Combat | Timeline runner in DomainTickCount (startup, active, recovery, cancel windows); hit volumes and projectile queries; cooldowns; resource pools; one-slot input queue | Ability definitions, timings, costs, queue window |
| Hit timing | Combat | ServerTime and CappedRewind (with a per-character position history), chosen per ability | The choice per ability and the cap |
| Tags | Gameplay | Hierarchical, interned tags on abilities, statuses and entities | The vocabulary (Impact, Finisher, Opener…) |
| Status container | Combat | Timed statuses with stacking policy, duration, periodic tick and immunity windows | Every concrete status (Bleed, Stagger, Freeze) |
| Attributes and modifiers | Gameplay | Base values and modifier stacks (add, multiply, override) with caps | Stats and formulas |
| Rule pipeline | Combat | Registration of typed conditions and modifiers; evaluation in named stages; outputs to per-worker buffers; compilation into a resolved [[Weapon Class System#Loadouts\|loadout]] per character; value variants chosen by a per-hit context (e.g., PvE and PvP) | Stage order and every condition and modifier |
| Damage interception | Combat | Hooks before and after damage is applied; invulnerability windows | Guard, [[Defense Evasion Guard and armor#Evasion\|Evasion]], armor, the damage formula |
| Threat table | Combat | Per-NPC threat storage read by AI target selection | What generates threat; taunt; Challenge |
| Behavior registries | Combat | ID-to-C++ registration, parameter schemas, a fixed hook list, read-only context and output buffers | The behaviors |
| Restrictions | Gameplay | Source-owned restriction sets (input, movement, abilities, interactions, targeting, damage, external motion), release by source, command validation | Which skills, effects and sequences acquire which restrictions |
| Interactions | Gameplay | Interaction volumes, reach and permission checks, reservation, an interaction registry | Levers, rituals, gathering, cartography |
| Movement | Gameplay | CharacterVirtual integration; a movement-mode registry with walk, glide (reads Environment wind), flight inside flight-zone volumes, mount and vehicle modes; Water registers swimming (CharacterWaterMovement); prediction hooks; server validation | Speeds, dashes, mount, glider and wing stats |
| Item runtime | Gameplay | Runtime item instances and containers mirrored from services | Item definitions and rules |
| Scripted sequences | [[Scripted sequences GameplayFlow and restrictions\|GameplayFlow]] | Sequence runtime, trigger, condition and action registries, timers, termination path, [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] policies | Boss phases, cutscenes, dungeon and world-event scripts |
| Quests | Quest | Quest runtime and quest-creation API, generic triggers, conditions and actions, durable-fact bridge | Every quest, Game-specific triggers, conditions and actions |

## Contents

- [[Behavior registry contract|Behavior registry contract]]
- [[Light and perception|Light and perception]]
- [[Scripted sequences GameplayFlow and restrictions|Scripted sequences (GameplayFlow) and restrictions]]
- [[Quest runtime and the quest-creation API|Quest runtime and the quest-creation API]]

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Environment wind currents tides waves and weather|Environment: wind, currents, tides, waves and weather (Engine)]] · [[AI architecture|AI architecture (Engine, Game)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Engine gameplay APIs (Engine) · exported 2026-11-03
