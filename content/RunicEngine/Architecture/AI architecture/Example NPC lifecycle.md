---
title: "Example NPC lifecycle"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Example NPC lifecycle"
created: "2026-10-14"
modified: "2026-10-30"
---

1. **Spawned or region loaded:** a dormant [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] entity with NPC, AIController, AggroSensor, personality and memory, and no live BrainHandle.

2. **Warn radius reached:** wake alerted; the tree investigates the sensed position and, finding nothing, returns to dormancy.

3. **Detect radius reached or damage taken:** wake engaged; a tree instance is created, AIActive is enabled and the target is set.

4. **20 Hz decision loop:** the tree emits MoveTo, UseAbility, BeginDefense or Evade; commands are validated; the 30 Hz phase runs movement, combat and [[Simulation core Flecs and Jolt#Jolt rules|Jolt]]; resulting facts update perception; the loop repeats.

5. **Target invalid or leash broken:** ReturnHome.

6. **Reset:** eligible combat state is reset by Game rules.

7. **Sleep:** the BrainHandle is released to the pool and AIActive is disabled; the NPC is dormant again.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Invariants|Invariants]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Example NPC lifecycle · exported 2026-11-03
