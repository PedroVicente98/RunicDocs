---
title: "Weapon Class System"
tags:
  - "vision"
  - "appendix/combat-review"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-11-16"
---

The class is a weapon loadout plus a Discipline. There are ten fixed loadouts and five Disciplines, which make 50 named classes, each with a single role: Damage, Tank or Support (heals and buffs). There is no separate role choice: the role comes from the class. E.g. Sword \+ Shield \+ Defense \= Guardian (Tank); Sword \+ Shield \+ Vitality \= Paladin (Support); Sword \+ Shield \+ War \= Legionnaire (Damage).

Vertentes no longer exist, and there are no versatile weapons: each weapon is either one-handed or two-handed, and the only pairs are the loadouts below.

### The layers of the class

| Layer | What it defines | How it is obtained | When it changes |
| :---- | :---- | :---- | :---- |
| Weapon loadout | Basic actions, range and shape of the strikes (Reach), timing profile, base damage and base Focus | Chosen at the Altar | Only at the Altar reset |
| Weapon mastery | The weapon's base kit, its cheap ranged strike, and passives that change the kit or add base damage, defense or Focus | Mastery XP on the equipped weapon type; never reset | Passive choices reset at the Altar |
| Discipline | The main kit: a pool of skills with its own mechanic | Chosen at the Altar | Only at the Altar reset |
| Named class | Name, single role (Damage, Tank or Support), role kit and passive, class signature, one merged skill tree | Derived from the loadout plus the Discipline | Changes with the loadout or the Discipline |
| Skill points | Investment in the Discipline skills | Only by leveling | Redistributed at the Altar reset |

There is no weapon swap in combat, and no change of weapon type outside the Altar reset. Replacing a weapon with a better one of the same type happens out of combat, as usual.

### Choosing and resetting the class

* At an Altar the player picks the loadout and the Discipline, which locks the named class. Changing either needs the full reset at an Altar; every city has one.  
* The reset redistributes the skill points and clears every mastery passive choice. It is paid with in-game gold, and the first one can be free.  
* Why fixed loadouts: stronger identity, readability in PvP (the enemy knows what a class can do), a manageable number of classes and animations, and focus on the skill pools.

### Loadouts

| Loadout | Hands | Delivery | Signature mechanic |
| :---- | :---- | :---- | :---- |
| Sword \+ Shield | 1H \+ off hand | Melee | *Open since Riposte became a Discipline skill*; the shield gives free, directional Guard and the shield bash |
| Wand \+ Shield | 1H \+ off hand | Ranged magic | Fast projectiles and channeling; no bash of its own, so it uses the shield bash |
| Wand \+ Focus | 1H \+ off hand | Ranged magic | The Focus amplifies spells and gives a personal barrier; more evasion instead of a bash |
| Spear | 2H | Medium reach | A Stagger meter on the target; a sprint with frontal Guard as its alt action (Shift+RMB) |
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
* **Basic attacks** are LMB (light) and Shift+LMB (heavy), with RMB for Guard and Shift+RMB for the alt action. They have no cooldown, cost stamina and have a fixed damage type per weapon; the Quarterstaff is hybrid, physical and magical. Discipline passives can imbue basic attacks with an element: fire builds Burn, ice builds Chill and lightning builds Shock. Imbuing isn't exclusive to Arcane.  
* **The bash** has no cooldown, only cost and recovery, but its stun has its own effect cooldown, spent when the skill is used, hit or miss; the effect's cost is paid only on a hit. Any skill can gate its effect the same way. The bash is press only, with no hold version.

### Disciplines

Each Discipline exists because it creates a different play pattern, not just a different element. A Discipline is a pool of skills, a mask over the weapon kit: its tree has about 15 skills, but its full pool is larger, with skills exclusive to a weapon type (instrument, staff, shield…) and skills shared with other pools. Five Disciplines at launch:

| Discipline | Play pattern | Role | Exclusive |
| :---- | :---- | :---- | :---- |
| War | Physical techniques and Fury, with damage and life steal | Always Damage | Bleed |
| Defense | Shields, Guard and protection of allies | Always Tank, except on the Bow, where it is Support | *Proposal: absorb barriers, restoring Guard and reflect* |
| Vitality | Heals, buffs and cleanse, the largest support kit | Always Support | To define |
| Arcane | Rune magic: raw arcane damage that ignores part of magical armor, plus elemental spells such as fireball and meteor | Damage or Tank by loadout | Arcane damage, with no build-up, and Acid |
| Occultism | Stealth and teleports (skills paid with life are out for now) | Damage, Tank or Support by loadout | Curse and Madness |

* **Defense on the Bow** is Support: shield arrows damage the enemy and shield allies. The Vigilant (Defense) shields more and the Sacred Archer (Vitality) heals more. Mages tank with magic shields (Wand \+ Focus, Staff), and the Instrument with magic shields around it.  
* **Elemental conditions** (Burn, Chill, Shock, Poison) are open to every Discipline, because elemental is too wide to lock into one; each Discipline also has something exclusive.  
* **Removed Disciplines:** Song doesn't exist (instrument classes take damage, buff or healing kits from the other Disciplines), Elementalism merged into Arcane, and Shadow's stealth and teleports went to Occultism. Hunt (marks and traps) stays an expansion candidate. Ranged damage comes from the weapons, so it isn't a Discipline.  
* When the role passive and a Discipline effect give the same effect, they don't stack: the strongest wins (provisional).

### Skills, trees and points

* **The weapon kit comes from weapon mastery** (see below): light, heavy, Guard, the alt action and the cheap ranged strike, always available and outside the tree. The extra weapon skills of earlier versions (Thrust, Riposte, Charge…) are Discipline skills with a weapon requirement, and mastery passives can add effects to them.  
* **Discipline skills are the main kit.** They cost skill points. Pools belong only to the Disciplines; the weapon kit is in no pool.  
* **Skill library:** every skill is written once, with its pools, requirements (weapon parts such as blade, point, haft, shield or bow, and a minimum Focus) and a default tier, which a loadout can override (e.g. Vine Strike is tier 1 on the Quarterstaff and tier 2 on the Staff). Each class's tree is cooked from the library, with per-class pin, remove and move overrides for exceptions; a skill in several pools appears once.  
* **Tiers:** a tier opens by character level and by a number of points spent in the tier below (a different number per tier); passives count as picks. Between 5 and 10 tiers; 28 skill points at level 50 for now (it can become 25, 30…). Ultimates (capstones) sit at level 50, and a build takes only one. One pick per tier and the fully free ArcheAge form were both dropped.  
* **Skill types** (mediums): **martial** needs the weapon part; **infused** needs the weapon part and costs half stamina and half mana; a **spell** needs a minimum Focus and costs mana; an **innate** skill costs only mana and appears on every loadout of its Discipline. Focus comes only from weapon mastery (some loadouts have a base Focus and always cast spells; mastery passives raise it, so a Greatsword can reach a fireball). It is not an item stat. *Proposal: Focus 0 to 10 (Wand + Focus 10; Wand + Shield, Staff and Instrument 8; Quarterstaff 4; the rest 0), with spells needing 3, 6 or 9.* *To test: a spell from the Discipline pool appears in the skill list once the loadout's Focus reaches it.*  
* **Builds:** the unlock choices depend on how skills are categorized (melee, area, projectile, projectile with area; buff, heal, damage; weapon or magic; cast, cost, cooldown; morph; kit or Discipline). The same class must allow different builds.  
* **Discipline skills are filtered by the weapon,** so a skill that needs a shield is shared by Sword \+ Shield and Wand \+ Shield.  
* **Discipline skills follow the weapon.** Most Discipline skills are written against what every weapon has (light and heavy attack, the off-hand action, Guard, dodge, and tags like Blunt or Finisher), so they work with any loadout. E.g. Bastion (your next Guard within 2 s reflects 30%) works as the shield block, the quarterstaff timed Guard or the spear's Guard while sprinting. Variants by weapon exist only where the form really changes, and Discipline skills reuse the weapon's animations by default.  
* **Values per class:** the same skill can scale differently in different classes. *Proposal: requirement tags on each skill (e.g. needs an instrument); the named-class list is the allowlist; trees are generated at cook time, with nodes pinned, removed or moved by hand per class; the most specific value wins (class \+ PvP over class, over PvP, over base); per-class overrides stay exceptions.*  
* Combat skill points come only from leveling, and everyone at max level has the same total. Balance is through the points and the skill cap below, and each skill's power is capped.  
* **About 28 combat skill picks** at max level, close to ArcheAge's count. Auxiliary skills don't count: emotes, the context kit (mount, glider and wing) and other non-combat skills are separate categories. *Open: whether a skill added by an item's unique effect counts toward the 28.*  
* Weapons and effects that grant extra skills make the class stronger, and that is accepted.  
* **Tags as a contract.** Interactions are reusable conditions and modifiers, not hand-written pairs (see [[Skills by components]]).  
* **Freedom to author:** any number of skills can be created and spread across the weapons, added later to specific weapons, or used to replace provisional ones. Some skills are weapon-focused and others purely magic (a protective aura not tied to the sword and shield; a magic shield charge tied to the shield).  
* **Class signature.** Each named class has a small effect of its own: the per-class balance lever, used sparingly.

### Weapon mastery

Weapon mastery is separate from the character level and the Discipline. It is kept per weapon type (one per loadout) and never resets: moving from the Spear to the Instrument starts the Instrument at mastery 1, while level 50 and every Discipline point stay. Players who switch weapons at max level accept that cost.

* **Milestones:** mastery 1 gives the base kit, mastery 5 the cheap ranged strike, mastery 10 the first passive, then one passive choice every 10 levels. *Open: the format (50 levels with a passive every 10, or about 10 levels with something at each), the scope and the passive pool.*  
* **Passives:** one pool, filtered per weapon. Each passive has a minimum level, and a slot takes any passive at or below its own level (a level-10 passive fits the level-30 slot, not the reverse). A passive is a big stat with no effect, a big effect with no stat, or a smaller stat plus a lesser effect. Mastery gives mostly passives and base-kit changes, including base damage, defense or Focus.  
* **XP:** only the equipped mastery levels, through a conversion of the base XP (see [[Item progression and infinite progression#Infinite progression|Infinite progression]]). No catch-up: higher-level monsters give more XP, and switching at max level already levels faster.  
* **Impact:** mastery 1 against max mastery must be felt, neither too strong nor too weak; it can't be measured as a fixed % because it mixes stats and effects.  
* The level-35 element strike of earlier versions becomes a wider effect milestone.  
* The whole mastery framework can still change during development.

**Basic kit per loadout** (decided as a direction; the Bow and Dual Axes entries are open):

| Loadout | LMB light | Shift+LMB heavy | RMB Guard | Shift+RMB alt |
| :---- | :---- | :---- | :---- | :---- |
| Sword \+ Shield | Slash | Heavy slash | Shield block, free and directional | Shield bash |
| Wand \+ Shield | Fast bolt | Charged bolt | Shield block | Shield bash |
| Wand \+ Focus | Bolt | Heavy spell | Magic Guard | Focus personal barrier |
| Spear | Thrust (builds Stagger) | Sweep | Frontal brace, limited | Sprint with frontal Guard |
| Quarterstaff | Staff strike | Heavy staff | Timed Guard, then cooldown | Palm or kick (alternating builds Flow) |
| Staff | Bolt | Area spell | Magic Guard | Bash (stun and push) |
| Bow | Quick shot | Charged shot | Short deflect (open) | Kick-back (open) |
| Instrument | Note | Chord (Resonance) | Magic Guard | Bash (stun and push) |
| Greatsword | Slash | Charged strike (breaks Guard) | Parry Guard, limited | Side dash with frontal Guard |
| Dual Axes | Flurry | Cleave | Cross guard, limited | Open |

**Reach** is a fixed property of the weapon type: the hit shape (range, angle and width) and the projectile paths, the same for every weapon of that type and never an item stat. It changes only through passives and unique effects (possibly mastery). Range increases come only from outside sources such as ship stations, global to melee and ranged (melee possibly exempt). An effect around the weapon shows the real hit shape, even on basic attacks. A weapon's properties are its type, parts, timing profile, hit shapes, base damage and base Focus; an armor piece's are its weight (iframe share and condition resistance).

*Idea, not decided: Dual Axes as a hybrid mid-range weapon in the style of the Blades of Chaos, mostly physical but also magical, with strikes, chain throws and chain skills.*

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

* Each named class has a mount tree and an aerial tree, with their own points earned by level and separate from the combat tree, and 5 to 10 skills at most each. *Open: combos in the air.*  
* Mounted, on a glider or with a wing, the character uses only the context skills.  
* The mount, glider or wing can modify the kit. E.g. Run becomes a Dash with the same buff and an animation before it; a mount brings its own elemental skill.  
* The mount kit is the same on the ground and flying.

### Example: Sword + Shield

* **Loadout:** Sword \+ Shield. Basic kit from weapon mastery: light and heavy attack, block, shield bash and a flying slash. Thrust, Riposte and Charge are Discipline skills that need a sword or a shield.  
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
