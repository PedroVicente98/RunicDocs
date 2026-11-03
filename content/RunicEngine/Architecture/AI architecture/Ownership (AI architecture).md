---
title: "Ownership (AI architecture)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Ownership"
created: "2026-10-14"
modified: "2026-10-30"
---

| Part | Owner | Contains |
| :---- | :---- | :---- |
| Runic::AI | Engine | [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] components, wake, perception, think, target and sleep systems, BehaviorTreeRuntime (the BehaviorTree.CPP adapter), brain pool, intent buffers, generic nodes |
| Runic::GodotTools (AI docks) | Engine (tool) | Behavior-tree editor on Godot’s GraphEdit, AI asset browser, inspectors, personality editor, validation, live debugger |
| Light and perception API | Engine | Warn and detect radii from light and concealment (see Engine gameplay APIs) |
| Runic::Navigation | Engine | Detour runtime behind the MoveTo and MoveGoal contract |
| Perception values | Game | PerceptionProfiles, light curves, concealment values |
| Trees, personalities, NPC definitions | Game | XML [[Behavior-tree runtime\|behavior trees]], CombatPersonality profiles, AIDefinitions |
| Game-specific nodes | Game | Boss mechanics, naval boarding decisions, world-boss contribution logic, named encounter phases |

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · [[Locked decisions|Locked decisions]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Ownership · exported 2026-11-03
