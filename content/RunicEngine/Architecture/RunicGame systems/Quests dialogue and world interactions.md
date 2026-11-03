---
title: "Quests, dialogue and world interactions"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "RunicGame systems (Game) › Quests, dialogue and world interactions"
created: "2026-10-14"
modified: "2026-10-30"
---

* Quests are made with the Engine’s quest-creation API: definitions are data (states, objectives, triggers, conditions, actions), and Game-only triggers, conditions and actions are C++ registered under game:. The quest runtime runs inside the simulation, so a kill or an interaction advances a quest in the same tick.

* The Go Quest service stores progress, deduplicates quest facts by their stable IDs and commits rewards; the simulation never waits for it.

* Dialogue graphs are data whose conditions read quest and character state. Scripted scenes (escorts, boss phases, cutscenes) run on [[Scripted sequences GameplayFlow and restrictions|GameplayFlow]].

* Physical interactions (levers, escorts, gathering, rituals, the cartography table) are C++ behaviors registered on the Engine interaction framework.

* Flow: client intent, then the simulation checks reach, state and permissions, executes and emits a fact; the quest runtime advances the quest in the same tick; the fact travels with its stable ID to the Quest service, which stores progress idempotently and commits rewards; the accepted result returns at a later safe tick.

---

↑ [[RunicGame systems|RunicGame systems (Game)]] · ← [[Items progression and inventory|Items, progression and inventory]] · [[Map knowledge altars factions and progression|Map knowledge, altars, factions and progression]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › RunicGame systems (Game) › Quests, dialogue and world interactions · exported 2026-11-03
