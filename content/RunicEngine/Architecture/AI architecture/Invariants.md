---
title: "Invariants"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Invariants"
created: "2026-10-14"
modified: "2026-10-30"
---

* AI registers into the simulation-owned [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] world and never creates a competing authoritative world.

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

* The AI editor runs in the [[Tools#RunicEditor|RunicEditor]] on GraphEdit and edits shared assets; Groot2 is not embedded.

* Debugging exposes the chain event, memory, tree, utility, intent, command result.

* The Engine supplies reusable mechanics; RunicGame owns trees, personalities, perception values, encounters and game-specific nodes.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Implementation order|Implementation order]] · [[Example NPC lifecycle|Example NPC lifecycle]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Invariants · exported 2026-11-03
