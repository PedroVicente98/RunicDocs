---
title: "Weapon Class System"
tags:
  - "vision"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-11-04"
---

The class is a weapon loadout plus a Discipline. There are ten fixed loadouts and five Disciplines, which make 50 named classes, each with a single role: Damage, Tank or Support (heals and buffs). There is no separate role choice: the role comes from the class. E.g. Sword \+ Shield \+ Defense \= Guardian (Tank); Sword \+ Shield \+ Vitality \= Paladin (Support); Sword \+ Shield \+ War \= Legionnaire (Damage).

Vertentes no longer exist, and there are no versatile weapons: each weapon is either one-handed or two-handed, and the only pairs are the loadouts below.

### The layers of the class

| Layer | What it defines | How it is obtained | When it changes |
| :---- | :---- | :---- | :---- |
| Weapon loadout | Basic actions, the weapon's basic kit of skills, range and shape of the strikes, timing profile | Chosen at the Altar | Only at the Altar reset |
| Discipline | The main kit: a pool of skills with its own mechanic | Chosen at the Altar | Only at the Altar reset |
| Named class | Name, single role (Damage, Tank or Support), role kit and passive, class signature, one merged skill tree | Derived from the loadout plus the Discipline | Changes with the loadout or the Discipline |
| Skill points | Investment in the Discipline skills | Only by leveling | Redistributed at the Altar reset |
| Level choices | Some levels offer a choice of weapon skill (e.g. level 35: flame, ice or lightning strike) | By level | Only at the Altar reset |

There is no weapon swap in combat, and no change of weapon type outside the Altar reset. Replacing a weapon with a better one of the same type happens out of combat, as usual.

### Choosing and resetting the class

* At an Altar the player picks the loadout and the Discipline, which locks the named class. Changing either needs the full reset at an Altar; every city has one.  
* The reset redistributes the skill points and the level choices. It is paid with in-game gold, and the first one can be free.  
* Why fixed loadouts: stronger identity, readability in PvP (the enemy knows what a class can do), a manageable number of classes and animations, and focus on the skill pools.

### Loadouts

| Loadout | Hands | Delivery | Signature mechanic |
| :---- | :---- | :---- | :---- |
| Sword \+ Shield | 1H \+ off hand | Melee | Sword riposte: a short parry that opens a counterattack; the shield gives free, directional Guard and the shield bash |
| Wand \+ Shield | 1H \+ off hand | Ranged magic | Fast projectiles and channeling; no bash of its own, so it uses the shield bash |
| Wand \+ Focus | 1H \+ off hand | Ranged magic | The Focus amplifies spells and gives a personal barrier; more evasion instead of a bash |
| Spear | 2H | Medium reach | A Stagger meter on the target; a sprint with frontal Guard as its own skill |
| Quarterstaff | 2H | Monk: staff, punches and kicks; hybrid physical and magical | Flow: alternating staff and empty hand empowers the next spell |
| Staff | 2H | Ranged magic | Area and long casts; a melee bash that stuns and pushes away |
| Bow | 2H | Physical ranged (the only one) | Charged shots, with no homing |
| Instrument (Lute, Harp, Flute, Drum and others) | 2H | Ranged sound magic | Resonance: notes add up into chords of damage or buffs; a melee bash that stuns and pushes away |
| Greatsword | 2H | Melee | Charged strikes that break Guard; a side dash with frontal Guard |
| Dual Axes | 1H \+ 1H | Melee | To define in the class design (the old axe bleed went to War, which owns Bleed) |

* **Removed:** Mace, Dagger, War Axe, the one-handed Axe as its own loadout, and hand instruments as off hands. Axes exist only as Dual Axes, and the Instrument is two-handed.  
* **Katana:** not added; its animation style is too different from the Greatsword's.  
* **Expansion candidates:** a hand crossbow (pirates), a harpoon for naval combat and gauntlets.  
* **No ranged slot.** The Bow is a loadout you choose, and every melee loadout also has a few cheap long-range skills at the root of its kit (flying slash, air ball, air pierce).  
* **Basic attacks** use the left and right mouse buttons, have no cooldown and have a fixed damage type per weapon; the Quarterstaff is hybrid, physical and magical. Discipline passives can imbue basic attacks with an element: fire builds Burn, ice builds Chill and lightning builds Shock. Imbuing isn't exclusive to Arcane.  
* **The bash** has no cooldown, only cost and recovery, but its stun has its own effect cooldown, spent when the skill is used, hit or miss; the effect's cost is paid only on a hit. Any skill can gate its effect the same way. *Proposal: holding the button uses the version with the effect, with a heavier animation, and a tap is the plain bash, so a filler bash never spends the stun by accident.*

### Disciplines

Each Discipline exists because it creates a different play pattern, not just a different element. A Discipline is a pool of skills, a mask over the weapon kit: its tree has about 15 skills, but its full pool is larger, with skills exclusive to a weapon type (instrument, staff, shield…) and skills shared with other pools. Five Disciplines at launch:

| Discipline | Play pattern | Role | Exclusive |
| :---- | :---- | :---- | :---- |
| War | Physical techniques and Fury, with damage and life steal | Always Damage | Bleed |
| Defense | Shields, Guard and protection of allies | Always Tank, except on the Bow, where it is Support | *Proposal: absorb barriers, restoring Guard and reflect* |
| Vitality | Heals, buffs and cleanse, the largest support kit | Always Support | To define |
| Arcane | Rune magic: raw arcane damage that ignores part of magical armor, plus elemental spells such as fireball and meteor | Damage or Tank by loadout | Arcane damage, with no build-up, and Acid |
| Occultism | Skills paid with life, stealth and teleports | Damage, Tank or Support by loadout | Curse and Madness |

* **Defense on the Bow** is Support: shield arrows damage the enemy and shield allies. The Vigilant (Defense) shields more and the Sacred Archer (Vitality) heals more. Mages tank with magic shields (Wand \+ Focus, Staff), and the Instrument with magic shields around it.  
* **Elemental conditions** (Burn, Chill, Shock, Poison) are open to every Discipline, because elemental is too wide to lock into one; each Discipline also has something exclusive.  
* **Removed Disciplines:** Song doesn't exist (instrument classes take damage, buff or healing kits from the other Disciplines), Elementalism merged into Arcane, and Shadow's stealth and teleports went to Occultism. Hunt (marks and traps) stays an expansion candidate. Ranged damage comes from the weapons, so it isn't a Discipline.  
* When the role passive and a Discipline effect give the same effect, they don't stack: the strongest wins (provisional).

### Skills, trees and points

* **Weapon skills are the basic kit:** light, heavy, the off-hand action and the cheap ranged strike, always available. More unlock automatically by level, with no point cost. Some levels offer a choice (e.g. level 35: flame, ice or lightning strike), changed only at the Altar reset.  
* **Discipline skills are the main kit.** They cost skill points and are tiered: a pick in one tier unlocks the next.  
* **One merged tree per named class:** the merge of the weapon and Discipline skills whose requirements match the equipped weapons; a skill in several pools appears once. Discipline skills are filtered by the weapon, so a skill that needs a shield is shared by Sword \+ Shield and Wand \+ Shield.  
* **Discipline skills follow the weapon.** Most Discipline skills are written against what every weapon has (light and heavy attack, the off-hand action, Guard, dodge, and tags like Blunt or Finisher), so they work with any loadout. E.g. Bastion (your next Guard within 2 s reflects 30%) works as the shield block, the quarterstaff timed Guard or the spear's Guard while sprinting. Variants by weapon exist only where the form really changes, and Discipline skills reuse the weapon's animations by default.  
* **Values per class:** the same skill can scale differently in different classes. *Proposal: requirement tags on each skill (e.g. needs an instrument); the named-class list is the allowlist; trees are generated at cook time, with nodes pinned, removed or moved by hand per class; the most specific value wins (class \+ PvP over class, over PvP, over base); per-class overrides stay exceptions.*  
* Combat skill points come only from leveling, and everyone at max level has the same total. Balance is through the points and the skill cap below, and each skill's power is capped.  
* **At most 28 combat skills.** A character's weapon skills and Discipline skills together add up to at most 28 skills usable in combat, close to ArcheAge's count. Auxiliary skills don't count: emotes, the context kit (mount, glider and wing) and other non-combat skills are separate categories. *Open: whether a skill added by an item's unique effect counts toward the 28.*  
* Weapons and effects that grant extra skills make the class stronger, and that is accepted.  
* **Tags as a contract.** Interactions are reusable conditions and modifiers, not hand-written pairs (see [[Skills by components]]).  
* **Class signature.** Each named class has a small effect of its own: the per-class balance lever, used sparingly.

### Roles

The role comes from the named class: each loadout and Discipline combination has one role, set in the class design. The role sets the ceiling of what the class does well, the role kit and passive, and the dodge charges. The three roles come in similar numbers: 18 Damage, 15 Tank and 17 Support among the 50 classes. War is always Damage, Defense is always Tank (Support on the Bow) and Vitality is always Support; Arcane and Occultism change by loadout.

| Role | Role kit (examples) | Passive by tag | Dodge charges |
| :---- | :---- | :---- | :---- |
| Tank | Taunt (PvE), Challenge with area protection (PvP), Unbreakable Guard | Blunt skills generate threat and restore Guard | 3 |
| Support | Heals and buffs with FriendlyLock, resurrection, cleanse | Finishers heal the most wounded ally nearby | 4 |
| Damage | Execution, burst window | Openers and Finishers get a positional bonus | 4 |

Efficiency per role applies to everything the character produces, from the weapon kit or the Discipline. These values are the starting point for playtests:

| Role | Damage | Healing | Mitigation | Buffs |
| :---- | :---- | :---- | :---- | :---- |
| Tank | 55% | 45% | 100% | 70% |
| Support | 45% | 100% | 50% | 85% |
| Damage | 100% | 35% | 40% | 70% |

### Context kit: mount, glider and wing

**Being defined.** The open point is balancing how easy it is to create new skills with the quality of aerial combat.

* Each named class has a mount tree and an aerial tree, with their own points earned by level and separate from the combat tree.  
* Mounted, on a glider or with a wing, the character uses only the context skills.  
* The mount, glider or wing can modify the kit. E.g. Run becomes a Dash with the same buff and an animation before it; a mount brings its own elemental skill.  
* The mount kit is the same on the ground and flying.

### Example: Sword + Shield

* **Loadout:** Sword \+ Shield. Basic kit: light and heavy attack, block, shield bash and a flying slash; more weapon skills unlock by level (Thrust, Riposte, Charge…).  
* **With Defense** it is the Guardian, a Tank. The skill points go into Defense skills (Bastion, Wall…), and the Tank kit adds Taunt, Challenge and Unbreakable Guard; Blunt skills restore Guard.  
* **With Vitality** it is the Paladin, a Support, with Radiant Heal, Blessing and Purify.  
* **With War** it is the Legionnaire, a Damage class; with Arcane, the Rune Knight (Tank); with Occultism, the Blood Knight (Tank).  
* Changing the Discipline needs the Altar reset, which redistributes the points.

### Named classes

Fifty classes, ten loadouts × five Disciplines. War is Damage, Defense is Tank and Vitality is Support unless the table says otherwise; the role is shown where it varies.

| Loadout | War | Defense | Vitality | Arcane | Occultism |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Sword \+ Shield | Legionnaire | Guardian | Paladin | Rune Knight (Tank) | Blood Knight (Tank) |
| Wand \+ Shield | Battlemage | Spellwarden | Chaplain | Runeguard (Tank) | Pactbinder (Support) |
| Wand \+ Focus | Warcaster | Shieldweaver | Priest | Arcanist (Damage) | Warlock (Support) |
| Spear | Lancer | Phalanx | Valkyrie | Stormlancer (Damage) | Impaler (Tank) |
| Quarterstaff | Monk | Forest Guardian | Druid | Earthshaper (Tank) | Bog Witch (Support) |
| Staff | Devastator | Veilwarden | Oracle | Archmage (Damage) | Necromancer (Damage) |
| Bow | Ranger | Vigilant (Support) | Sacred Archer | Arcane Archer (Damage) | Plaguebow (Support) |
| Instrument | Skald | Songshield | Bard | Stormsinger (Damage) | Enchanter (Support) |
| Greatsword | Champion | Sentinel | Crusader | Spellblade (Damage) | Revenant (Tank) |
| Dual Axes | Berserker | Juggernaut | Shaman | Flamereaver (Damage) | Blood Shaman (Support) |

### Why this is easier to balance

Ten loadouts and five Disciplines give 50 named classes at launch, each with one role. Balance deals with the basic kits of 10 loadouts, the pools of 5 Disciplines, the 3 roles and the signatures.

1. At max level everyone has the same points, and each skill's power has a ceiling.  
2. Roles set the ceiling through the efficiency table.  
3. Loadout kits are compared with each other under the same role.  
4. Per-class values and the class signature are the per-class adjustment, used as a last resort.  
5. Telemetry per axis: usage and performance per loadout, per Discipline and per class.
