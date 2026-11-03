---
title: "Performance and scaling"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Performance and scaling"
created: "2026-10-14"
modified: "2026-10-30"
---

| NPC state | AI cost |
| :---- | :---- |
| Unloaded | Zero |
| Loaded, dormant | No live tree; cheap structural presence and the 10 Hz wake scan only |
| Awake nearby (alerted or engaged) | Active brain; 20 Hz decisions and perception |
| In combat | Active brain plus event-driven memory updates |
| Boss or elite | More complex tree, utility and encounter state behind the same contract |

* No tree ticks for dormant or unloaded NPCs.

* Spatial cells and sectors produce the candidates for wake scans and threat perception.

* Hot combat facts travel in event buffers, not through [[Simulation core Flecs and Jolt#Flecs rules|Flecs]] observers.

* Hot mutable AI state stays compact in Flecs; BehaviorTree.CPP object graphs stay in the runtime.

* Shared definitions and tree assets; per-entity state holds only what is truly mutable.

* No structural add and remove churn in hot paths; AIActive and Aggroable are toggles.

* Profile brain count, average and p95 tree tick time, event fan-out, candidate counts, intent counts and rejected-command rates.

* If per-brain BehaviorTree.CPP cost becomes material at very high counts, keep the public Runic AI contracts and consider a data-oriented Runic executor later — only after profiling.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Repository layout|Repository layout]] · [[Tests|Tests]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Performance and scaling · exported 2026-11-03
