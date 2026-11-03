---
title: "Implementation order"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Implementation order"
created: "2026-10-14"
modified: "2026-10-30"
---

| Step | Deliverable |
| :---- | :---- |
| 1\. Contracts | AI components and tags, AIIntent, AIWorkingMemory, AIDefinition, event-view interfaces |
| 2\. Runtime shell | BehaviorTreeRuntime, BrainPool, basic node registration, Wake and Sleep, a tiny test tree |
| 3\. Perception lifecycle | Aggroable toggle, perception profiles from the light API, warn and detect wake, target validation, leash, return home, sleep |
| 4\. Command bridge | Intents translated into movement and combat commands and validated normally |
| 5\. Reactive combat | SkillStarted perception, IncomingThreat, reaction timer, ChooseDefense utility |
| 6\. Data assets | Tree loading, AIDefinition registry, personality and perception profiles, BasicMelee content |
| 7\. Instrumentation | Per-brain execution trace; event, memory, utility and intent diagnostics |
| 8\. AI editor MVP | [[Tools#RunicEditor\|RunicEditor]] dock, asset browser, GraphEdit canvas, palette, inspector, XML save and load |
| 9\. Runic-specific tools | NPC definition editor, personality editor, content-ID validation, live entity attachment |
| 10\. Scale tests | Thousands of loaded NPCs with controlled awake percentages; profile tree ticks, perception fan-out, spatial queries and allocations |

The steps map to work packages: steps 1 and 2 are [[AI-1|AI-1]], and steps 4 and 6 are [[AI-2|AI-2]] (slice [[Slice 32 AI brains|32]], AI brains); step 3 is [[AI-3|AI-3]] (slice [[Slice 33 Perception at night|33]], perception at night); step 5 is [[AI-4|AI-4]] and step 7 is [[AI-5|AI-5]] (slice [[Slice 34 Reactive combat|34]], reactive combat); steps 8 and 9 are [[GDT-11|GDT-11]] and [[GDT-12|GDT-12]] (slice [[Slice 35 AI editor|35]], AI editor); step 10 is [[AI-6|AI-6]] (slice [[Slice 38 Battle scale|38]], battle scale).

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Tests|Tests]] · [[Invariants|Invariants]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Implementation order · exported 2026-11-03
