---
title: "Mental model"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Mental model"
created: "2026-10-14"
modified: "2026-10-30"
---

1. World truth ([[Simulation core Flecs and Jolt#Flecs rules|Flecs]], combat and spatial systems) publishes permitted facts and events.

2. AI perception filters them for each NPC.

3. AI working memory holds what that NPC knows.

4. The [[Behavior-tree runtime|behavior tree]] asks “what should I consider now?”.

5. Utility or policy choice asks “which valid response best fits this NPC?”.

6. An AI intent is emitted.

7. Normal gameplay command validation accepts or rejects it.

8. The authoritative result becomes new world truth.

| Layer | Owns | Example |
| :---- | :---- | :---- |
| World truth | Authoritative state and actual outcomes | The player started HeavySlash; the NPC has 24 [[Defense Evasion Guard and armor#Guard\|Guard]]; the NPC is committed to an attack |
| AI knowledge | What this NPC may know, and when | The NPC perceived a blockable incoming attack and may react after reactAt |
| AI desire | What the decision layer wants the actor to do | BeginDefense, Evade, UseAbility, MoveTo |

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Goals and non-goals|Goals and non-goals]] · [[Module boundaries|Module boundaries]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Mental model · exported 2026-11-03
