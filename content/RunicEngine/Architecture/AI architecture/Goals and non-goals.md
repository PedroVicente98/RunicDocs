---
title: "Goals and non-goals"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Goals and non-goals"
created: "2026-10-14"
modified: "2026-10-30"
---

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

* Gameplay truth stored in BehaviorTree.CPP blackboards instead of [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] components.

* Tree nodes that bypass combat, movement, cooldown, [[Defense Evasion Guard and armor#Guard|Guard]], dodge or ability validation.

* One heavyweight tree instance for every dormant NPC in the world.

* Line-of-sight or realistic stealth vision; perception is radii scaled by light and concealment.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Locked decisions|Locked decisions]] · [[Mental model|Mental model]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Goals and non-goals · exported 2026-11-03
