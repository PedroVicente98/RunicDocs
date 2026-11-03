---
title: "Resolver"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "RunicGame systems (Game) › Resolver"
created: "2026-10-14"
modified: "2026-10-30"
---

The resolver is RunicGame’s configuration of the Engine rule pipeline: two stages and a fixed order.

| Stage | Reads | May change |
| :---- | :---- | :---- |
| Activation | Caster state, previous skill and its window, resources, position | Cost, cast time, variant |
| Hit | Target state and position | Control swap, added effects, values |

* Order inside each stage: component swaps, then additions, then value changes (summed per category, capped), then defenses. Identical effects from the role passive and the [[Weapon Class System#Disciplines|Discipline]] do not stack: the stronger applies (provisional; confirm with the skill trees).

* Rules come from five sources — the skill and the choices in its tree, the role passive of the named class, item effects (including extracted ones), the mount, glider or wing modifications of the context kit, and the class signature. They compile into one resolved [[Weapon Class System#Loadouts|loadout]] per character, rebuilt only when equipment, class, tree choices or the context (on foot, mounted, gliding, winged) change, so no hit searches for rules.

* Hit timing is chosen per skill: ServerTime by default, CappedRewind (e.g., ≤ 100 ms) only on skills flagged after playtests. Full rewind is not offered.

---

↑ [[RunicGame systems|RunicGame systems (Game)]] · ← [[Skills mapped to Engine APIs|Skills mapped to Engine APIs]] · [[Custom behaviors|Custom behaviors]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › RunicGame systems (Game) › Resolver · exported 2026-11-03
