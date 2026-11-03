---
title: "Defense and threat"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "RunicGame systems (Game) › Defense and threat"
created: "2026-10-14"
modified: "2026-10-30"
---

| Game system | Holds | Built on |
| :---- | :---- | :---- |
| Evasion | Charges by the class’s role, dodge form by [[Weapon Class System#Disciplines\|Discipline]], iframe length by armor, minimum recovery | Resource pools, invulnerability windows |
| [[Defense Evasion Guard and armor#Guard\|Guard]] | One resource; modes Free (shield arc), Timed (the Quarterstaff), DuringMovement (greatsword dash, spear run), Filtered (mage, by damage domain and delivery) | Damage interception |
| [[Combat#Resolve hard and light CC\|Resolve]] | CC immunity buff: full CC, then Resolve T1 (about 2 s; a CC during it drops one level), then Resolve T2 (about 2 s, immune to every CC); slows last at most about 10 s, then about 5 s of slow immunity. [[Combat#Conditions, build-up and Tolerance\|Tolerance]], per condition: after about 10 s active, or at once on a peak, about 5 s with no added time or build-up | Status container |
| Threat and taunt | Threat values per action; spatial taunt | Threat table |
| Challenge | PvP protection: a share of damage redirected to the Tank, non-stacking | Damage interception |

---

↑ [[RunicGame systems|RunicGame systems (Game)]] · ← [[Custom behaviors|Custom behaviors]] · [[Items progression and inventory|Items, progression and inventory]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › RunicGame systems (Game) › Defense and threat · exported 2026-11-03
