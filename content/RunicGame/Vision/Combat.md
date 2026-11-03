---
title: "Combat"
tags:
  - "runicgame"
  - "vision"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
section: "Combat"
created: "2026-10-13"
modified: "2026-10-30"
---

Combat is spatial action with an authoritative server: execution and positioning as in TERA, skill interactions as in ArcheAge and a slower rhythm inspired by Crimson Desert, with long cooldowns and skills that matter. The base is a configurable skill bar, with basic attacks on the mouse buttons; key-sequence combos (Black Desert) or a chain key (TERA) are optional client upgrades that call the same skills.

| Mechanic | Rule |
| :---- | :---- |
| Offensive aim | Free aim with light aim assist; offensive projectiles don't home |
| Support aim | Heals and buffs use FriendlyLock and can home in on the ally |
| Dodge | Universal, with iframes; spends [[Defense Evasion Guard and armor#Evasion\|Evasion]] charges (see Defense) |
| [[Defense Evasion Guard and armor#Guard\|Guard]] | One resource; the shield gives free, directional blocking, and the other weapons use Guard in limited ways (see Defense) |
| Weapon swap | None in combat; the [[Weapon Class System#Loadouts\|loadout]] changes only at the [[Real exploration#Altars, death, respawn and teleports\|Altar]] reset |
| Combat state | Starts on the first hostile action and ends 30 s after the last one |
| Hard CC | Limited by Resolve: the CC lands in full, Resolve T1 lowers the next CC by a level, and Resolve T2 makes the target immune to every CC (see Resolve) |
| Light CC | Slows have a time limit, then a short slow immunity (see Resolve) |
| Conditions | Build-up per source, limited by Tolerance (see Conditions) |
| AoE | Decreasing damage per target and a separate target limit for CC |
| Tank in PvE | Threat plus a spatial Taunt; the boss still hits whoever is in the area |
| Tank in PvP | Challenge protects nearby allies by redirecting part of the damage to the Tank, without controlling the enemy |
| Naval | Boarding uses normal combat; the ship gives a slight range bonus to eligible skills |

**How the loadouts enter combat.** Each loadout brings a signature mechanic: the Spear builds Stagger, the Sword counters, the Greatsword breaks Guard, the Quarterstaff chains staff strikes, punches and magic, the Bow charges its shots and the Instrument builds chords. The layers talk through states: Frozen (the Chill peak) makes the Spear's Stagger become a Knockdown, and a Shock mark is read by combos.

**Scale.** The same rules apply from a duel to a 100 vs 100 war. In small fights you defend by reacting; in big ones, with formation, terrain and line of sight. Nobody has to dodge a whole army.

**PvE and PvP values.** Every value (damage, percentages, durations, cooldowns) has a base, and a skill, item or effect can declare its own PvE and/or PvP values. Ex.: base 100, PvP 85, PvE 105\. These values form the Balance Profile (Base, PvE or PvP). *Proposal: the profile is decided by the target of each hit.*

## Resolve: hard and light CC

Resolve is the CC immunity buff, so control never chains forever. Hard CC (Stun, Knockdown, Trip, Root and Stagger) is applied directly by the skill that declares it, with no build-up.

* **Full CC:** the first hard CC lands in full.  
* **Resolve T1:** when that CC ends, the target gets Resolve T1 for about 2 s. A CC that lands during T1 drops one level (ex.: a Stun lands as a Stagger).  
* **Resolve T2:** when the lowered CC ends, Resolve resets to Resolve T2 for about 2 s, and the target is immune to every CC. If no CC lands during T1, Resolve simply expires.  
* **Light CC:** a target can be slowed for at most about 10 s, then is immune to slows for about 5 s. This is the Resolve of light CC.  
* A condition peak whose extra effect is a hard CC (Frozen, Electrocute, Panic) also goes through Resolve.  
* Environment hazards go through Resolve and Tolerance too, unless their own rule says they ignore them (ex.: slips on wet ground).  
* **Effect gates:** a skill's effect can be gated by the skill's cooldown, an effect cooldown, an effect cost, or both.  
* **Guard:** no effect zeroes the Guard and takes away blocking at the same time; it is one or the other. A zeroed Guard regenerates normally.  
* *Proposal: bosses don't take hard CC; every CC adds to a Break bar, and a full Break knocks the boss down for a damage window.*  
* The durations (2 s, 10 s, 5 s) are examples for tuning.

## Conditions, build-up and Tolerance

Decided on 30 October: conditions use build-up. The detailed rules can still change, but this is the best way of working found so far. Two limits keep control fair: Resolve covers hard CC, and Tolerance covers condition build-up.

* **One bar per attacker:** each attacker has their own internal bar for each condition on the target.  
* **The bar is time:** each hit adds time up to the condition's cap, and the bar drains in real time while the condition is active. Each condition has its own build-up speed: Burn and Chill are fast; Acid and Madness are slow.  
* **One instance acts:** only the source with the highest % ticks, which is also the one that lasts longest. Three bars deal the same damage as one; the others wait underneath and take over if the top one ends.  
* **Damage:** condition damage doesn't change with attributes. *Proposal: a fixed value per level of the character who applied it.*  
* **Credit:** every source gets an assist. A kill from a condition tick goes to the source with the highest %.  
* **Peak:** when a source's bar reaches 100%, the condition pops and gives its extra effect. No skill gives the extra effect directly, so Frozen comes only from the Chill peak. *Proposal: no single skill adds more than about 60% of a bar, so a peak always needs at least two applications.*  
* **Tolerance:** per condition. It starts at once when a peak pops, or after the condition has been active for about 10 s in a row. It doesn't remove the active condition; for about 5 s that condition gains no time and no build-up on the target. The numbers are examples.  
* **Icon:** the bar is internal. The player sees a status icon with the condition, its time left, its % and the number of sources, showing the highest source. *Proposal: an attacker sees their own % on the enemy, to know how close their peak is.*  
* **Cleanse** removes build-up. Support classes have the cleanses, with the strongest and the group ones in Vitality; Tanks can have a self-cleanse. *Proposal: a cleanse removes every source of 1 or 2 conditions, highest % first; a potion cleanses 1 condition, with a cooldown.*  
* **Sources:** skills that declare the condition, and basic attacks with an imbue. *Proposal: the amount per hit scales with the weapon's timing profile, so fast and slow weapons build at a similar rate.*  
* *Proposal: a blocked hit adds half its build-up and a dodged hit adds none. Resistance reduces what each hit adds; it comes from armor weight per piece, never from enchants.*  
* **Data:** about 8 bytes per instance on the server (owner, condition, time); only apply and peak events go over the network, about 6 bytes each.

| Condition | Who has it | Build-up | While active | Peak |
| :---- | :---- | :---- | :---- | :---- |
| Burn | Any [[Weapon Class System#Disciplines\|Discipline]] | Fast | Damage over time | Ignite: a burst of damage |
| Chill | Any Discipline | Fast | Slow | Frozen: a hard CC through Resolve; a heavy hit shatters it |
| Shock | Any Discipline | Medium | A mark that combos read | Electrocute: a Stagger that interrupts |
| Poison | Any Discipline | Medium | Damage over time and less healing received | *Proposal: Wither, healing received −50% for a few seconds* |
| Bleed | War, only physical skills that declare it | Medium | Damage over time | Hemorrhage: damage based on max health |
| Curse | Occultism | Medium | The target takes more damage | *Proposal: Doom, a burst equal to part of the damage taken while cursed* |
| Madness | Occultism | Slow | *Proposal: Evasion charges recharge slower* | *Proposal: Panic, about 1.5 s of lost control, through Resolve* |
| Acid | Arcane | Slow | Less armor | The Guard drops to zero and regenerates normally; the target can still block |

* Acid adds to the other breaks (Concussion, Armor Break) and replaces none.  
* **NPC conditions** exist only for NPCs, for dungeon mechanics. Ex.: Instant Death, whose build-up deals no damage and whose peak kills at once, so the healer has to watch and cleanse the allies' build-up, like Elden Ring's Deathblight. NPC conditions ignore Tolerance or take longer to trigger it. Player kits never have them; divine items can.

---

↑ [[Vision|Vision]] · ← [[Races|Races]] · [[Defense Evasion Guard and armor|Defense: Evasion, Guard and armor]] →  
Source: [RunicGame — Complete MMORPG Vision](https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit) › Combat · exported 2026-11-03
