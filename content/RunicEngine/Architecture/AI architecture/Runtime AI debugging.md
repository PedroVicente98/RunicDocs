---
title: "Runtime AI debugging"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Runtime AI debugging"
created: "2026-10-14"
modified: "2026-10-30"
---

The [[Tools#RunicEditor|RunicEditor]] attaches to development and staging servers through the GameServer’s Diagnostics layer and shows:

| Debug view | Minimum information |
| :---- | :---- |
| Brain summary | Entity, AIDefinition, tree asset, BrainHandle, active or sleeping, current target |
| Tree execution | Running, succeeded and failed nodes for the current or previous tick, with the subtree path |
| Working memory | IncomingThreat, reactAt, target, last combat time, alert position, leash and home state, Game-exposed values |
| Utility trace | Candidates, base scores, major modifiers, decision noise, selected result |
| Event trace | Recent facts this NPC’s perception consumed |
| Intent trace | Recent intents and whether the resulting command was accepted or rejected |
| Spatial debug | Warn, detect and leash radii, navigation goal, target marker |

Explainability is an engineering feature: a developer can answer “why did this NPC block?”, “why did it ignore that attack?”, “why is it still awake?” or “why did the command fail?” by following event, memory, tree branch, utility choice, intent and validation result — without stepping through library internals.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[AI editor inside the RunicEditor|AI editor (inside the RunicEditor)]] · [[Repository layout|Repository layout]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Runtime AI debugging · exported 2026-11-03
