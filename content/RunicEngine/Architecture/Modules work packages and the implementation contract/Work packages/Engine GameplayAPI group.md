---
title: "Engine: GameplayAPI group"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: GameplayAPI group"
created: "2026-10-14"
modified: "2026-10-30"
---

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| [[GPL-1\|GPL-1]] | Movement-mode registry and modes (walk, sprint, dash hook, glide, mount; Water registers swimming) with movement parameters from data; gliding reads wind once [[ENV-2\|ENV-2]] provides it | Modes switch without teleporting; parameters come from Game data | [[PHYS-2\|PHYS-2]] | [[Slice 14 Prediction\|14]] |
| [[GPL-2\|GPL-2]] | Attributes, modifiers, resources and tags; death and kill facts when a vital resource reaches zero (Combat fills in the source) | Modifier order is deterministic; resources clamp | [[SIM-2\|SIM-2]], [[CNT-1\|CNT-1]] | [[Slice 15 Character state\|15]] |
| [[GPL-3\|GPL-3]] | Restrictions: source-owned restriction sets, acquire and release by source, command-validation hooks | Blocked commands are rejected on the server; releasing a source clears everything it held | [[GPL-2\|GPL-2]] | [[Slice 18 Defense\|18]] |
| [[GPL-4\|GPL-4]] | Item and equipment runtime that mirrors ledger containers | Equipping changes modifiers; the mirror matches the ledger after a reload | [[GPL-2\|GPL-2]] | [[Slice 28 Persistence\|28]] |
| [[GPL-5\|GPL-5]] | Interaction framework: interactables, reservation, interaction facts | Two players cannot reserve the same target | [[GPL-2\|GPL-2]], [[EVT-1\|EVT-1]] | [[Slice 29 Scripted sequences\|29]] |
| [[GPL-6\|GPL-6]] | Factions and spawn primitives, including spawn areas driven by rule data over cooked candidate points | A spawner keeps its population; a spawn area keeps its rule’s count and refills by elapsed time when its cell loads; faction checks drive hostility | [[GPL-2\|GPL-2]], [[COOK-3\|COOK-3]] | [[Slice 31 Navigation and spawning\|31]] |
| [[GPL-7\|GPL-7]] | Flight and climbing movement modes: flight inside flight-zone volumes with an altitude ceiling above which only gliding works, glide and flight as separate mount capabilities, flying vehicles, climbing mounts; restrictions can forbid flight and gliding | Above the ceiling flight stops and gliding takes over; outside a flight zone a flying mount only glides; a restriction blocks both; a mount climbs a marked wall | [[GPL-1\|GPL-1]], [[GPL-3\|GPL-3]], [[WORLD-2\|WORLD-2]], [[ENV-2\|ENV-2]] | [[Slice 44 Expansion\|44+]] |
| [[GPL-8\|GPL-8]] | Routine spawning: when a cell activates, routine entities (escorts, caravans, ships, mob routines) spawn where their routine puts them; stored exceptions override the routine and fade back into it | A caravan appears at the right point of its route when a player arrives; a delayed escort rejoins its routine over time | [[GPL-6\|GPL-6]], [[ENV-6\|ENV-6]], [[WORLD-3\|WORLD-3]] | [[Slice 43a Living world\|43a]] |
| [[CMB-1\|CMB-1]] | Ability toolkit: timelines and hit timing per skill (ServerTime, CappedRewind) | Timeline phases fire on exact ticks | [[GPL-2\|GPL-2]], [[CNT-1\|CNT-1]] | [[Slice 16 Ability toolkit\|16]] |
| [[CMB-2\|CMB-2]] | Targeting modes (free aim, FriendlyLock, light aim-assist hooks), combat volumes and hit detection over Physics queries | A melee arc and a projectile each hit a dummy exactly once; FriendlyLock never selects a hostile | [[CMB-1\|CMB-1]], [[PHYS-5\|PHYS-5]] | [[Slice 16 Ability toolkit\|16]] |
| [[CMB-3\|CMB-3]] | Statuses and effects, cooldowns, resource costs | Durations, stacks and cooldowns expire on the right tick | [[CMB-1\|CMB-1]] | [[Slice 17 Statuses and rules\|17]] |
| [[CMB-4\|CMB-4]] | Rule pipeline and behavior registries (fixed hooks for Game code); value variants selected by a per-hit context the Game defines | A test rule and a test behavior run in order; a value with a base and a contextual variant resolves by the hit context; the Engine holds no game rule | [[CMB-3\|CMB-3]] | [[Slice 17 Statuses and rules\|17]] |
| [[CMB-5\|CMB-5]] | Damage pipeline, interception hooks, invulnerability windows | Interception follows hook order; invulnerability blocks hits | [[CMB-4\|CMB-4]], [[GPL-3\|GPL-3]] | [[Slice 18 Defense\|18]] |
| [[CMB-6\|CMB-6]] | Threat table and crowd control (target cap, immunity windows) | A CC chain and its immunity follow the test data | [[CMB-5\|CMB-5]] | [[Slice 19 Combat prototype\|19]] |
| [[CMB-7\|CMB-7]] | Input queue: one queued action per character inside the game-set window, started on the first legal tick; game-named priority inputs skip it when the cancel window allows | An early input fires on the first legal tick; a stun in between cancels it | [[CMB-1\|CMB-1]], [[SIM-4\|SIM-4]] | [[Slice 19 Combat prototype\|19]] |
| [[CMB-8\|CMB-8]] | Foreign combat: volumes crossing an authority border become requests to the owner | The target is damaged exactly once, by its owner | [[CMB-5\|CMB-5]], [[DSIM-4\|DSIM-4]] | [[Slice 37 Cross-border combat\|37]] |
| [[FLOW-1\|FLOW-1]] | Sequence runtime: trigger, condition and action registries, scheduler, timers on simulation time | A sequence waits, branches and acts only through commands and Gameplay APIs | [[GPL-5\|GPL-5]] | [[Slice 29 Scripted sequences\|29]] |
| [[FLOW-2\|FLOW-2]] | Termination path, restriction ownership, watchdog, presentation cues | Complete, abort, timeout, disconnect and shutdown all release everything the sequence held | [[FLOW-1\|FLOW-1]], [[GPL-3\|GPL-3]] | [[Slice 29 Scripted sequences\|29]] |
| [[FLOW-3\|FLOW-3]] | Handoff policies and sequence state in the transfer snapshot | Transferable keeps its timers; PinAuthority blocks transfer; AbortOnTransfer cleans up | [[FLOW-2\|FLOW-2]], [[DSIM-3\|DSIM-3]] | [[Slice 37 Cross-border combat\|37]] |
| [[QST-1\|QST-1]] | Quest runtime and quest-creation API: definitions, objectives, triggers from facts, instances | A quest defined only in data advances from kill and interaction facts | [[FLOW-1\|FLOW-1]] | [[Slice 30 Quests\|30]] |
| [[QST-2\|QST-2]] | Durable bridge: outgoing quest facts with stable IDs through the service port; accepted results applied at safe ticks | A replayed fact never doubles progress; no service callback touches [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] | [[QST-1\|QST-1]], [[SIM-5\|SIM-5]] | [[Slice 30 Quests\|30]] |
| [[QST-3\|QST-3]] | Quest instances registered as a transfer-snapshot contributor | A quest in progress crosses a simulation border with its objectives and timers intact | [[QST-1\|QST-1]], [[DSIM-3\|DSIM-3]] | [[Slice 37 Cross-border combat\|37]] |

---

↑ [[Work packages|Work packages]] · ← [[Engine simulation core|Engine: simulation core]] · [[Engine world systems|Engine: world systems]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: GameplayAPI group · exported 2026-11-03
