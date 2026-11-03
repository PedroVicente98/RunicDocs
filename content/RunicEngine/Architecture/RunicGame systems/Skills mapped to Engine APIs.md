---
title: "Skills mapped to Engine APIs"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "RunicGame systems (Game) › Skills mapped to Engine APIs"
created: "2026-10-14"
modified: "2026-10-30"
---

| Skill component | Holds | Engine API used |
| :---- | :---- | :---- |
| Identity | ID, weapon, skill tree and slot, tags | Tags |
| Activation | Cost, cooldown, cast time, requirements | Ability toolkit |
| Timeline | Startup, active, recovery, cancel windows | Ability toolkit |
| Shape | Cone, circle, line, projectile; origin; range | Ability toolkit |
| Damage | Parts with domain, delivery and optional subtype or element | Attributes, rule pipeline |
| Effect | Conditions with build-up (Burn, Chill, Shock, Poison, Bleed, Curse, Madness, Acid) through [[Combat#Conditions, build-up and Tolerance\|Tolerance]], Armor Break, buffs | Status container |
| Control | Stagger, Trip, Knockdown, Stun, Root through [[Combat#Resolve hard and light CC\|Resolve]] (T1 and T2); slows capped by the light-CC Resolve | Status container, rule pipeline |
| Movement | Dash, leap, root while casting | Movement |
| Defense | [[Defense Evasion Guard and armor#Guard\|Guard]] or iframe granted by the skill | Damage interception |
| Threat and protection | Threat multiplier, Challenge | Threat table, damage interception |
| World utility | Light emitter, reveal | Light and perception |
| Hit timing | ServerTime or CappedRewind | Hit timing |
| Custom | Behavior ID and parameters | Behavior registries |
| Interactions | Condition → modifier rules | Rule pipeline |

* A damage type only selects defenses; effects and CC are always declared components.

* Weapon timing profiles (one per weapon; there are no versatile weapons) scale recovery.

* Role efficiency and per-component coefficients (PvE and PvP) are data tables reloadable at runtime. Every value has a base, and a skill, item or effect may declare its own PvE and/or PvP values (e.g., base 100, PvP 85, PvE 105); the rule pipeline’s per-hit context picks the variant. Proposal: the context is decided by the target of each hit.

$${D}_{final}={D}_{base}\times \prod\limits_{c\in C}^{}{k}_{c}\times {E}_{role}\times \left({1-min\left({{R}_{max}, \sum\limits_{c\in C}^{}{r}_{c}}\right)}\right)$$

---

↑ [[RunicGame systems|RunicGame systems (Game)]] · [[Resolver|Resolver]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › RunicGame systems (Game) › Skills mapped to Engine APIs · exported 2026-11-03
