---
title: "AI architecture (Engine, Game)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game)"
created: "2026-10-14"
modified: "2026-10-30"
---

AI is reasoning, not authority. The Engine’s AI module reads permitted facts, keeps bounded working memory, ticks [[Behavior-tree runtime|behavior trees]] and emits intents; the simulation validates and executes those intents exactly like player commands. RunicGame supplies the trees, personalities, perception values and game-specific nodes.

## Contents

- [[Ownership (AI architecture)|Ownership]]
- [[Locked decisions|Locked decisions]]
- [[Goals and non-goals|Goals and non-goals]]
- [[Mental model|Mental model]]
- [[Module boundaries|Module boundaries]]
- [[Data model|Data model]]
- [[Perception wake leash and sleep|Perception, wake, leash and sleep]]
- [[Events and perception pipeline|Events and perception pipeline]]
- [[Behavior-tree runtime|Behavior-tree runtime]]
- [[Reactive combat and personality|Reactive combat and personality]]
- [[Scheduler integration|Scheduler integration]]
- [[Intents become ordinary commands|Intents become ordinary commands]]
- [[Behavior-tree assets|Behavior-tree assets]]
- [[AI editor inside the RunicEditor|AI editor (inside the RunicEditor)]]
- [[Runtime AI debugging|Runtime AI debugging]]
- [[Repository layout|Repository layout]]
- [[Performance and scaling|Performance and scaling]]
- [[Tests|Tests]]
- [[Implementation order|Implementation order]]
- [[Invariants|Invariants]]
- [[Example NPC lifecycle|Example NPC lifecycle]]

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Engine gameplay APIs|Engine gameplay APIs (Engine)]] · [[RunicGame systems|RunicGame systems (Game)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) · exported 2026-11-03
