---
title: "Defense: Evasion, Guard and armor"
tags:
  - "runicgame"
  - "vision"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
section: "Defense: Evasion, Guard and armor"
created: "2026-10-13"
modified: "2026-10-30"
---

Everyone defends with two resources: Evasion charges to dodge and Guard to block. The class role, the [[Weapon Class System#Disciplines|Discipline]], the weapons and the armor change how each one works, but the resources are the same for all.

## Evasion

Evasion charges recharge over time; each charge pays a dodge with iframes. The role sets how many charges exist and an effect at the end of the iframe, the Discipline sets the dodge shape, and the armor changes the iframe duration. Only one dodge shape applies at a time.

* Charges recharge one at a time, at a fixed interval.  
* There is a minimum recovery between dodges, even when a skill zeroes the charge cost.  
* The iframe is short and readable; attributes only extend it with diminishing returns and a cap.  
* Special mobility (Blink, shadow step) spends the same charge, never a separate pool.

| Role | Charges | Effect at the end of the iframe |
| :---- | :---- | :---- |
| Tank | 3 | Steadiness: brief damage reduction right after the dodge |
| Support | 4 | Slightly faster charge recharge |
| Damage | 4 | Momentum: the next light attack comes out faster |

| Discipline | Dodge shape | Effect |
| :---- | :---- | :---- |
| War | Combat Roll | Escaping a strike with the dodge generates Fury |
| Defense | To define | To define |
| Vitality | Rescue Step | Dodging toward an ally with FriendlyLock gives them a small shield |
| Arcane | Blink *(proposal, from Elementalismo)* | A short teleport that spends a charge plus mana and leaves a trail of the active element |
| Occultism | Blood Escape and Shadow Step *(proposal, Shadow Step from Sombra)* | With the charges at zero, dodge by paying life, once per recharge cycle; Shadow Step extends the iframe and passes through enemies |

## Guard

Guard is a single resource, modified by the weapons and the Disciplines. Only the shield holds Guard freely; the other weapons have limited Guard and trade defensive versatility for damage. That is how a Tank without a shield exists.

| Weapon or style | How Guard works |
| :---- | :---- |
| Shield | Free, directional blocking while there is Guard; Tanks have much more Guard |
| Quarterstaff | Holds Guard for a limited time, then goes on cooldown |
| Greatsword | A side dash with frontal Guard during the dash |
| Spear | A sprint with frontal Guard, as its own skill; this skill costs no [[Stamina and climbing#Stamina\|stamina]] |
| Mages without a shield (Wand \+ Focus, Staff, Instrument) | Magic Guard: effective against magical damage, reduced against ranged, much reduced against melee; with Defense they tank with magic shields |
| Other [[Weapon Class System#Loadouts\|loadouts]] | Each kit defines its form (ex.: the Sword riposte) during development |

Magic Guard reads the damage components of the hit (domain and delivery), so it uses the same logic as the defenses in Skills by components.

## Armor

* Five armor pieces: head, chest, hands, legs and feet, with no waist or wrist.  
* **Iframe:** the iframe duration blends by the armor type of each piece, each piece counting 1/5. *Proposal: cloth has the longest iframe and plate the shortest.*  
* **Guard:** the Guard is the sum of every piece's Guard stat, which grows with quality; cloth gives little but still adds.  
* **Two armor pools**, physical and magical, each blended per piece: plate is the best against physical damage and great against magical; leather is good against both, below plate on both; cloth is great against magical damage and low against physical.  
* **Reduction:** total armor reduces damage through a curve that never reaches 100%. *Proposal: reduction \= A ÷ (A \+ K); with K \= 1,000, 500 armor gives 33%, 1,000 gives 50%, 2,000 gives 67% and 4,000 gives 80%.*

---

↑ [[Vision|Vision]] · ← [[Combat|Combat]] · [[Skills by components|Skills by components]] →  
Source: [RunicGame — Complete MMORPG Vision](https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit) › Defense: Evasion, Guard and armor · exported 2026-11-03
