---
title: "Scheduler integration"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Scheduler integration"
created: "2026-10-14"
modified: "2026-10-30"
---

| Domain and phase | AI responsibility | Result |
| :---- | :---- | :---- |
| 10 Hz maintenance | Wake scans, sleep and leash maintenance, low-priority idle and world AI | Activation changes and coarse intentions; no realtime combat |
| 20 Hz pre-realtime | Validate targets, advance memory, tick active trees, translate output into intents and commands | Commands ready for the next realtime phase |
| 30 Hz realtime | Apply commands, movement, combat timelines, [[Defense Evasion Guard and armor#Guard\|Guard]], dodge, abilities, [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] queries, hits, damage and effects | Authoritative results and gameplay facts |
| 20 Hz post-realtime | Consume relevant combat facts and update perception and memory | Knowledge ready for a later decision tick |

Within one 60 Hz master step: due 10 and 20 Hz producers validate targets, tick AI and emit intents; the 30 Hz realtime phase applies commands, runs movement, combat and Jolt and produces SkillStarted, Damage and Death facts; due 20 Hz consumers then update AI memory.

**Spatial locality:** aggro acquisition, threat fan-out and similar discovery always start from Runic cells and sectors, never “for every NPC, query every player” or “for every global event, tick every brain”. [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] filters then apply to an already small candidate set.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Reactive combat and personality|Reactive combat and personality]] · [[Intents become ordinary commands|Intents become ordinary commands]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Scheduler integration · exported 2026-11-03
