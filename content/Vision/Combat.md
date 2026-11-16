---
title: "Combat"
tags:
  - "vision"
  - "appendix/combat-review"
  - "appendix/nodes-economy-exploration"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-11-16"
---

Combat is spatial action with an authoritative server: execution and positioning as in TERA, skill interactions as in ArcheAge and a slower rhythm inspired by Crimson Desert, with long cooldowns and skills that matter. Players place their skills on a command board, with Black Desert-style combos (a direction or Shift plus a key), or on an ArcheAge-style skill bar; both are layouts of the same skills. Basic attacks, Guard and the weapon's alt action are on the mouse (see [[Controls, targeting and skill delivery]]).

| Mechanic | Rule |
| :---- | :---- |
| Offensive aim | Free aim with light aim assist; offensive projectiles don't home |
| Support aim | Heals and buffs snap to an ally in a generous cone (FriendlyLock) or go to the Ward (see [[Controls, targeting and skill delivery#Targeting\|Targeting]]) |
| Dodge | Universal, with iframes; spends Evasion charges (see [[Defense Evasion, Guard and armor\|Defense]]). Skills have no iframes: iframes exist only on the dodge |
| Guard | One resource; the shield gives free, directional blocking, and the other weapons use Guard in limited ways (see [[Defense Evasion, Guard and armor\|Defense]]) |
| Weapon swap | None in combat; the loadout changes only at the Altar reset |
| Combat state | Starts on the first hostile action and ends 30 s after the last one |
| Hard CC | Limited by Resolve: the CC lands in full, Resolve T1 lowers the next CC by a level, and Resolve T2 makes the target immune to every CC (see [[Combat#Resolve hard and light CC\|Resolve]]) |
| Light CC | Slows have a time limit, then a short slow immunity (see [[Combat#Resolve hard and light CC\|Resolve]]) |
| Conditions | Build-up per source, limited by Tolerance (see [[Combat#Conditions, build-up and Tolerance\|Conditions]]) |
| AoE | Decreasing damage per target and a separate target limit for CC |
| Tank in PvE | Threat plus a spatial Taunt; the boss still hits whoever is in the area |
| Tank in PvP | Challenge protects nearby allies by redirecting part of the damage to the Tank, without controlling the enemy |
| Naval | Boarding uses normal combat; the ship gives a slight range bonus to eligible skills |

**How the loadouts enter combat.** Each loadout brings a signature mechanic: the Spear builds Stagger, the Greatsword breaks Guard, the Quarterstaff chains staff strikes, punches and magic, the Bow charges its shots and the Instrument builds chords. *Open: the Sword + Shield's signature, now that Riposte is a Discipline skill (it looks more like a passive, such as a very fast counter with no cast and no recovery), and how charged shots and strikes work with press-only input.* The layers talk through states: Frozen (the Chill peak) makes the Spear's Stagger become a Knockdown, and a Shock mark is read by combos.

**Scale.** The same rules apply from a duel to a 100 vs 100 war. In small fights you defend by reacting; in big ones, with formation, terrain and line of sight. Nobody has to dodge a whole army.

**PvE and PvP values.** Every value (damage, percentages, durations, cooldowns) has a base, and a skill, item or effect can declare its own PvE and/or PvP values. E.g. base 100, PvP 85, PvE 105\. These values form the Balance Profile (Base, PvE or PvP). *Proposal: the profile is decided by the target of each hit.*

### Resolve: hard and light CC

Resolve is the CC immunity buff, so control never chains forever. Hard CC (Stun, Knockdown, Trip, Root and Stagger) is applied directly by the skill that declares it, with no build-up.

* **Full CC:** the first hard CC lands in full. Stagger is a hard CC, never a build-up or a condition.  
* **Resolve T1:** when that CC ends, the target gets Resolve T1 for about 2 s. A CC that lands during T1 drops one level (e.g. a Stun lands as a Stagger).  
* **Resolve T2:** when the lowered CC ends, Resolve resets to Resolve T2 for about 2 s, and the target is immune to every CC. If no CC lands during T1, Resolve simply expires.  
* **Light CC:** a target can be slowed for at most about 10 s, then is immune to slows for about 5 s. This is the Resolve of light CC.  
* **Skill-granted CC immunity** (Super Armor, working name) is a separate buff: it blocks CC and never starts or advances the natural Resolve chain. *Open: whether the T1/T2 chain with about 2 s of full immunity and no cooldown stays viable.* *Proposal: it blocks CC only (damage, conditions and Concussion still land), starts on a set tick and ends if the skill is cancelled, so starting and cancelling never gives free immunity; a PvP uptime cap (e.g. 20 to 25%) is checked when skills are cooked.*  
* **Grabs** never ignore Resolve or Super Armor (e.g. the spear's skewer-and-throw is blocked by them). *Proposal: against Resolve, a grab becomes Stagger build-up, so the skill still does something.*  
* A condition peak whose extra effect is a hard CC (Frozen, Electrocute, Panic) also goes through Resolve.  
* Environment hazards go through Resolve and Tolerance too, unless their own rule says they ignore them (e.g. slips on wet ground).  
* **Effect gates:** a skill's effect can be gated by the skill's cooldown, an effect cooldown, an effect cost, or both.  
* **Guard:** no effect zeroes the Guard and takes away blocking at the same time; it is one or the other. A zeroed Guard regenerates normally.  
* *Proposal: bosses don't take hard CC; every CC adds to a Break bar, and a full Break knocks the boss down for a damage window.*  
* The durations (2 s, 10 s, 5 s) are examples for tuning.

### Resources

Six resources: Health, Mana, Stamina, Evasion (charges), Guard and Shield. Health, mana and stamina come mostly from items, plus Discipline and mastery passives.

* **One stamina bar,** Dark Souls style, for attacks, sprinting, climbing, swimming and heavy objects. Costs are flat, the same in and out of combat; consumption and regeneration are fast. Maximum stamina and stamina regeneration are separate stats.  
* **Costs by skill type:** martial skills cost stamina, spells and innate skills cost mana, and infused skills cost half of each (10 + 10 instead of 20). Basic attacks cost stamina on every loadout; the alt action and the weapon's ranged strike can cost mana (e.g. the sword's ranged strike, the instrument's secondaries). Every class spends mana.  
* **Other resources:** Fury stays a passive and is never paid with life. Skills paid with life are out for now; they can come back or change.  
* **Evasion and Guard** keep their own charges and pool, never stamina.  
* **Climbing:** a hit while climbing costs normal damage plus a share of max stamina; climbing skill and gear lower that share and the climbing drain.  
* **Shields** sit on the health bar, temporary or until broken; passive shields rebuild after a cooldown. Shields stack up to 50% of max health without merging: damage takes the newest first (a passive shield of 50 plus a new one of 60: a hit of 50 leaves the passive's untouched, a hit of 51 takes 1 from it). "Breaks Shields" deals double damage to shields instead of erasing them; "ignores Shields" goes straight to health. Each condition defines its relation to shields (Bleed goes to health, Burn hits the shield first). Skill shields scale with the caster's Healing Power.  
* *Proposal (numbers): base 100 stamina and 100 mana; stamina regenerates 40/s after a 0.4 s pause, mana 20/s after 0.5 s; light attack 8, heavy 15, martial skill 20 to 30, sprint 10/s; spells 15 to 35.*

### Conditions, build-up and Tolerance

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
| Burn | Any Discipline | Fast | Damage over time | Ignite: a burst of damage |
| Chill | Any Discipline | Fast | Slow | Frozen: a hard CC through Resolve; a heavy hit shatters it |
| Shock | Any Discipline | Medium | A mark that combos read | Electrocute: a Stagger that interrupts |
| Poison | Any Discipline | Medium | Damage over time and less healing received | *Proposal: Wither, healing received −50% for a few seconds* |
| Bleed | War, only physical skills that declare it | Medium | Damage over time | Hemorrhage: damage based on max health |
| Curse | Occultism | Medium | The target takes more damage | *Proposal: Doom, a burst equal to part of the damage taken while cursed* |
| Madness | Occultism | Slow | *Proposal: Evasion charges recharge slower* | *Proposal: Panic, about 1.5 s of lost control, through Resolve* |
| Acid | Arcane | Slow | Less armor | The Guard drops to zero and regenerates normally; the target can still block |

* Acid adds to the other breaks (Concussion, Armor Break) and replaces none.  
* **NPC conditions** exist only for NPCs, for dungeon mechanics. E.g. Instant Death, whose build-up deals no damage and whose peak kills at once, so the healer has to watch and cleanse the allies' build-up, like Elden Ring's Deathblight. NPC conditions ignore Tolerance or take longer to trigger it. Player kits never have them; divine items can.
