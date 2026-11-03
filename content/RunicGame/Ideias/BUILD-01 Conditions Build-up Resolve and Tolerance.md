---
title: "BUILD-01 · Conditions, Build-up, Resolve and Tolerance"
aliases:
  - "BUILD-01"
  - "Conditions, Build-up, Resolve and Tolerance"
tags:
  - "runicgame"
  - "idea"
  - "status/in-game-vision"
id: "BUILD-01"
status: "In game vision"
game_vision: "Combat › Resolve: hard and light CC; Conditions, build-up and Tolerance"
source: "RunicGame — Ideias"
source_url: "https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit"
created: "2026-10-17"
modified: "2026-11-03"
---

**ID:** BUILD-01 · **Status:** In game vision · **Game vision:** [[Combat#Resolve hard and light CC|Combat › Resolve: hard and light CC]]; [[Combat#Conditions, build-up and Tolerance|Conditions, build-up and Tolerance]]

**Decided (2026-10-30):** conditions use build-up; the detailed rules can still change, but this is the best way found so far. Two limits: [[Combat#Resolve hard and light CC|Resolve]] covers hard CC, and [[Combat#Conditions, build-up and Tolerance|Tolerance]] covers condition build-up. A peak whose extra effect is a hard CC also goes through Resolve. Environment hazards go through Resolve and Tolerance too, unless their own entry says they ignore them (ex.: slips, [[HAZARD-01 Environmental Hazards|HAZARD-01]]).

**Hard CC** (Stun, Knockdown, Trip, Root and Stagger) is applied directly by the skill that declares it, with no build-up. Resolve, the CC immunity buff, limits it: the CC lands in full; when it ends, the target gets Resolve T1 for about 2 s, and a CC that lands during T1 drops one level (ex.: a Stun lands as a Stagger); when that lowered CC ends, Resolve resets to Resolve T2 for about 2 s, immune to every CC. If no CC lands during T1, Resolve expires.

* **Light CC:** a target can be slowed for at most about 10 s, then is immune to slows for about 5 s: the Resolve of light CC. The durations are examples.  
* **Effect gates:** a skill's effect can be gated by the skill's cooldown, an effect cooldown, an effect cost, or both ([[ATK-01 Basic Attacks and Bash|ATK-01]]).  
* **[[Defense Evasion Guard and armor#Guard|Guard]]:** no effect zeroes the Guard and takes away blocking at the same time; it's one or the other. A zeroed Guard regenerates normally.

**Condition build-up:** each attacker has their own internal bar for each condition on the target.

* **The bar is time:** each hit adds time up to the condition's cap, and the bar drains in real time while the condition is active. Each condition has its own build-up speed: Burn and Chill are fast, Acid and Madness are slow.  
* **One instance acts:** only the source with the highest % ticks, which is also the one that lasts longest. Three bars deal the same damage as one; the others wait underneath and take over if the top one ends.  
* **Damage:** condition damage doesn't change with attributes. *(proposal: a fixed value per level of the character who applied it.)*  
* **Credit:** every source gets an assist. A kill from a condition tick goes to the source with the highest %.  
* **Peak:** when a source's bar reaches 100%, the condition pops and gives its extra effect. No skill gives the extra effect directly. *(proposal: no single skill adds more than about 60% of a bar, so a peak always needs at least two applications.)*  
* **Tolerance:** per condition. It starts at once when a peak pops, or after the condition has been active for about 10 s in a row. It doesn't remove the active condition; for about 5 s that condition gains no time and no build-up on the target. The numbers are examples.  
* **Icon:** the bar is internal. The player sees a status icon with the condition, its time left, its % and the number of sources, showing the highest source. *(proposal: an attacker sees their own % on the enemy, to know how close their peak is.)*  
* **Cleanse:** removes build-up. Support classes have the cleanses, with the strongest and the group ones in Vitality; Tanks can have a self-cleanse. *(proposal: a cleanse removes every source of 1 or 2 conditions, highest % first; a potion cleanses 1 condition, with a cooldown.)*  
* **Sources:** skills that declare the condition, and basic attacks with an imbue ([[ATK-01 Basic Attacks and Bash|ATK-01]]). *(proposal: the amount per hit scales with the weapon's timing profile, so fast and slow weapons build at a similar rate.)*  
* *(proposal: **Guard and dodge:** a blocked hit adds half its build-up and a dodged hit adds none. **Resistance:** reduces what each hit adds; it comes from armor weight per piece, never from enchants. **Bosses:** they don't take hard CC; every CC adds to a Break bar, and a full Break knocks the boss down for a damage window.)*  
* **Data:** about 8 bytes per instance on the server (owner, condition, time); only apply and peak events go over the network, about 6 bytes each.

**Conditions** (who has it, build-up speed: while active → peak):

* **Burn** (any [[Weapon Class System#Disciplines|Discipline]], fast): damage over time → Ignite, a burst of damage.  
* **Chill** (any Discipline, fast): Slow → Frozen, a hard CC through Resolve; a heavy hit shatters it.  
* **Shock** (any Discipline, medium): a mark that combos read → Electrocute, a Stagger that interrupts.  
* **Poison** (any Discipline, medium): damage over time and less healing received → *(proposal: Wither, healing received −50% for a few seconds)*.  
* **Bleed** (War, only physical skills that declare it, medium): damage over time → Hemorrhage, damage based on max health.  
* **Curse** (Occultism, medium): the target takes more damage → *(proposal: Doom, a burst equal to part of the damage taken while cursed)*.  
* **Madness** (Occultism, slow): *(proposal: [[Defense Evasion Guard and armor#Evasion|Evasion]] charges recharge slower → Panic, about 1.5 s of lost control, through Resolve)*.  
* **Acid** (Arcane, slow): less armor → the Guard drops to zero and regenerates normally, and the target can still block. It adds to the other breaks (Concussion, Armor Break) and replaces none.

Elemental conditions are open to every Discipline. Arcane damage is exclusive to Arcane and has no build-up.

**NPC conditions:** some conditions exist only for NPCs, for dungeon mechanics. Ex.: Instant Death, whose build-up deals no damage and whose peak kills at once, so the healer has to watch and cleanse the allies' build-up, like Elden Ring's Deathblight. NPC conditions ignore Tolerance or take longer to trigger it. Player kits never have them; divine items can ([[GOD-01 Divine Items|GOD-01]]).

*Updated 2026-10-30: build-up decided (was: a concept test that could be removed); Resolve T1 and T2 and the light-CC slow cap (was: a proposed Resolve ladder with about 8 s of Stagger and 5 s of immunity); Tolerance per condition, about 10 s active then about 5 s, at once on a peak (was: about 8 s active and 3 s after).*

---

↑ [[Ideias|Ideias]]  
Source: [RunicGame — Ideias](https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit) · exported 2026-11-03
