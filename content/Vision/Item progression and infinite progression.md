---
title: "Item progression and infinite progression"
tags:
  - "vision"
  - "appendix/combat-review"
  - "appendix/design-compile"
  - "appendix/nodes-economy-exploration"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-11-16"
---

Any weapon can reach the power ceiling, about 20% above the base power of a level 50 with the reference weapon. The reference weapon sets the best-in-slot base against power creep and can be a crafted tier; there are many ways to get weapons, and the faction series gives a weapon recipe slightly above it. Raids and PvP shorten the path and give unique effects, but don't create a power gap: skill still matters more than gear.

### Anatomy of a weapon

| Part | What it does | How it evolves |
| :---- | :---- | :---- |
| Weapon type | Belongs to a loadout: its kit, Reach, timing profile, base damage and base Focus (Sword, Spear…) | Doesn't change |
| Implicit stats | From the item type: weapon damage; for armor, the armor pools, Guard and weight | Follow the item level |
| Item level | Base power and the size of the stat budget | Deterministic upgrade with materials and gold |
| Grade | A small power bonus and visuals | Improved through crafting, with no RNG |
| Quality | A bonus from the crafter's work | Set by crafting; any item, dropped or crafted, can be reworked by a crafter |
| Budget stats | Direct stats bought with the item's point budget (Health, Stamina, Mana, Powers, critical chance, armor…) | *Proposal: a reforge redistributes the budget and offers 3 distributions* |
| Unique effect | Adds or swaps tags of a skill, changes the element, adds an effect or a new skill | Awakens at certain grades; can be extracted into a gem |
| Gem socket | Holds one gem with an Infusion Rune | A gem from extraction or dismantling goes in |

**Stat budget.** Every item has a point budget per item level, and each stat has a point cost per unit (reloadable data tuned with telemetry), so any item can carry any stat, with many zeros. Negative stats are allowed (an accessory with a lot of damage and negative health): a negative point refunds 0.8 of a bought one, and stats can be bought in decimals. Zero stats are never shown. Extra rules sit on top of the budget:

* **Weapons** carry any stats but must have 1 or 2 Powers, never a third. The primary comes from the weapon type (martial weapons: Physical; magic weapons: Magical); the secondary comes from the item family. Concentrating Power is allowed with a loss (500 + 500 becomes about 700 to 800 in one).  
* **Families** set the mix, like ArcheAge's named sets: Physical + Magical, Physical + Healing, Magical + Healing (names to define). Healing Power is never a primary.  
* **Accessories** (a necklace, 2 earrings and 2 rings) have no mandatory stat and a limit of attributes (e.g. 3); only accessories can carry a single Power (e.g. pure Healing Power for a healer). The cloak works as an accessory; bracers maybe later.  
* **Armor** is freer: any stat set, and always some armor.  
* *Idea: players building their own items within the budget, once the system proves to have no holes.*  
* *Open: which stats are flat and which are %, and whether they affect only item bonuses or the base; armor sets and their budget.*

**Unique weapons.** Named weapons from specific bosses, PvP or rare recipes, with a fixed stat distribution and a unique effect. E.g. the Tide Spear, always Reach and Stagger; its effect makes the sweep pull targets. At the Epic and Mythic grades the effect awakens a second part and the visuals transform: a vertical upgrade, but in behavior, not in numbers.

**Unique effects and extraction**

* The effect of a unique weapon is flexible: it adds a tag to a skill, swaps tags, changes the element, adds an effect or adds a new skill.  
* Effects come from PvE and can also come from PvP; the ratio between the sources is a balance knob, and the system supports both. They work in PvE and PvP.  
* A weapon that adds a skill is stronger, and that is accepted.  
* **Extraction** is the same process as dismantling: it destroys the source item, and the effect becomes a gem. The gem holds an Infusion Rune; the rune is the item's descriptive flavor, with the same function. A gem goes into another weapon's socket (one per weapon), can be sold at the auction house, or can be crushed into another resource.

### Power budget

| Source of power | Range | Rule |
| :---- | :---- | :---- |
| Reference weapon | 100% | The best-in-slot base; can be a crafted tier |
| Item level up to the cap | up to \+10% | No RNG |
| Grade up to Mythic | up to \+5% | No RNG; grindy, with fixed costs |
| Quality | *Open* | Set by the crafter (*proposal: up to \+10%, replacing the item level axis*) |
| Weapon mastery passives, Inscription morphs and the stat budget | Inside the same ceiling | The sum of every source is tuned in playtests |
| Unique effect (or its gem) | \+0% in numbers | Behavior, including a new skill; an extra skill makes the weapon stronger, and that is accepted |
| BiS (item level cap \+ Mythic) | about \+15.5% | Within the ceiling of about 20%; future raises of the item level cap each add half of the previous one, without raising the level cap |

### Grades

The list of grades is data, not code: adding or removing a grade must not require a system change, and the ceiling stays the same.

| Grade | Cumulative bonus | Visuals |
| :---- | :---- | :---- |
| Common | 0% | No glow |
| Uncommon | \+0.5% | No glow |
| Rare | \+1% | Light outline |
| Heroic | \+1.5% | Light outline |
| Epic | \+2.5% | Glow |
| Legendary | \+3.5% | Particles |
| Celestial | \+4.5% | Aura |
| Mythic | \+5% | Visual transformation |

**No RNG in upgrades; RNG only in drops** (decided on 9 November)

* Grades in the style of ArcheAge stay, and quality is added. Grade and quality can be improved on any item: a crafted item through better materials, a dropped item by spending materials on it. An iron weapon could reach Mythic at maximum quality, even if it isn't a good use of materials.  
* Improvement is grindy but has no RNG: every step has a fixed, visible cost. Randomness exists only in what drops (items and materials).  
* Crafting sets the quality, and a dropped item's quality can be improved through crafting.  
* Weapons and armor come in categories: a crafted line that goes up through metals made from ores found in the world (tin, iron and on to mithril, adamantite and beyond); weapons dropped by bosses, which sit somewhere on the crafted tiers; and mixed items, where a dropped item gets a crafted part to become the final item, or where a blueprint drops.  
* Several materials don't correspond directly to a tier.

**Mythic Spark** (working name): a rare material needed to raise grades above Epic (Legendary, Celestial and Mythic). It comes from raids, ranked PvP, world bosses and the boss region; dungeons only go up to Epic.

### Where everything comes from

| Source | Starting item level | Starting grade | Unique effects | Materials it gives |
| :---- | :---- | :---- | :---- | :---- |
| Faction series | A weapon recipe slightly above the reference, with a special effect and hard or unique materials | By the crafter | Yes | — |
| Dungeons | 102 to 104% | Rare or Heroic | Yes, one per boss | Item level and grades up to Epic |
| Raids | 105 to 108% | Epic | Yes, the most striking ones | Mythic Spark and high grades |
| PvP (honor and ranking) | 104 to 106% | Heroic | Yes; the PvE to PvP ratio is a balance knob | Mythic Spark and high grades |
| World bosses and the boss region | 105 to 108% | Epic | Yes | Mythic Spark and high grades |
| Crafting | 100 to 106%, by materials | Set by the recipe | From rare recipes | — (the item carries the crafter's name) |

**Why this encourages variety**

* Each dungeon and raid has its own unique effects; collecting effects for different builds makes players move through the content.  
* High-grade materials come from raids, ranked PvP and the boss region: any of them works, and doing several is the fastest path. An incentive, not an obligation.  
* Since every weapon reaches the ceiling, the weapon with the effect the player likes never becomes obsolete within the expansion.  
* Updates never raise the number scale: each update's upgrade step closes half of the remaining headroom, through upgrade chains that dismantle the previous armor into parts of the new best-in-slot (see Infinite progression).

### Infinite progression

Progression has a ceiling (unlike RuneScape, which trades the ceiling for a huge grind), and is horizontal for most of the game, vertical only on gear. Decided on 6 to 12 November:

* **No WoW retail model.** The level cap (e.g. 50) never rises. Updates add content at every level (10, 25, 30 and 50 alike) and new regions, and can add a new continent for max-level players; the older continents, the neutral one included, stay relevant. New low-level content mostly serves leveling, alts and completionists, and that is accepted: a fun leveling makes alts appealing.  
* **The region is the content,** with its own mechanic, like the maps of Guild Wars 2: one needs a jumping mount, another a water mount or a glider, another is a war where players clear things and repair cannon stations.  
* **One number scale** for everything, from a level 1 mouse to the gods, set at launch and never raised. A new item brings a different function, effect or situational use, never bigger numbers. Growth is 4% per level, so a level 50 has 6.8 times the numbers of a level 1 and 2.2 times those of a level 30.  
* **Headroom:** at launch the maximum numbers sit below the top of the scale, and each update's upgrade step closes half of the remaining gap, so the headroom never runs out. Vertical progression is upgrading items inside the scale: the previous armor is dismantled into parts, which are components of the new best-in-slot.  
* **A pillar:** old content stays relevant, and there is no power creep.  
* **XP:** one base XP type from every source except professions, exploration included. Weapon mastery and Inscriptions receive it through conversion rates (e.g. 0.6 and 0.1), always in parallel: the whole XP goes to the level, and the conversions add on top. Only the equipped mastery levels.

| Track | How it repeats | Power ceiling |
| :---- | :---- | :---- |
| Ascensions (dungeon and raid) | Each level adds rotating modifier modules (e.g. a rising tide, enemies that explode on death) | Gives grade materials, cosmetics and titles; never goes past the ceiling |
| Inscriptions (skill levels) | The level after 50: 50 → Inscription 1, 2, 3… | Effects and morphs; costs grow exponentially |
| Exploration | Base XP; the exploration shop sells exploration gear, items and consumables, in the style of ArcheAge's Blue Salt Brotherhood | Horizontal only |
| Regional renown | Reputation per region | Recipes, discounts and cosmetics |
| The leveling run (New Game+) | A max-level character redoes the leveling, endlessly | Gold, titles, cosmetics, prestige and ranking; never power |
| Updates | New regions, continents, loadouts and Disciplines | The scale and the level cap never rise |

**Inscriptions** (working name; "Ascensions" stays for dungeons and raids, since Ascendancy is the old empire) are skill levels in the style of ArcheAge's ancestral levels: they add special effects to existing skills and improve them by level. Inscription X gives X morph slots, and morphs cost no skill points; only skills flagged as morphable get variants. Levels can be lost only in marked regions and moments (war time, the neutral continent and others), always announced: any death while the loss is active drops one level and removes the highest morph slot. Regaining the level brings the slot back empty, and the player chooses the morph again. The floor is level 50: Inscription 1 drops to 50, never below. It is a real grind, the endgame of the endgame: costs grow exponentially (the first levels about 3 to 4 hours), recovering a lost level costs the same, and the goal is casual players between 1 and 5 and hardcore ones between 5 and 10. Outside those regions the death penalty stays light and costs only experience, never items.

### The leveling run (New Game+)

A max-level character can redo the leveling from level 1, endlessly.

* **Two truths:** the character's real state is frozen during the run, and the run is a second layer with its own level, XP and quest progress. Technically it is a second progression profile; the simulation sees only the active one, and returning is one idempotent merge.  
* **Start and end:** a run starts at an Altar and can end at any time, which snaps the character back to its real state. Reaching max level ends it with a completion bonus.  
* **Reset:** the run starts with starting gear (gear has level requirements). Level, skill points, Discipline, level choices and professions reset; profession XP earned in the run counts toward points, so trade runs, Larceny and crafting are allowed. The Codex, map discovery, reputation, housing and cosmetics stay.  
* **Storage:** the bank and the house stay usable, but anything stored before the run is locked; only items deposited during the run can be taken out, and they stay in the bank on return.  
* **Quests:** a quest done on the real state can be replayed for run points, without quest points and without overwriting the original choice. Content done for the first time merges into the real state on return, with its quest points, rewards and choice. Each quest counts once per run, and content far below the run's level gives no points.  
* **Points** come from content (quests, events, dungeons, raids, bosses and profession XP). Gold counts only when earned from content, never from trades or the auction. Rewards are gold, titles, cosmetics, prestige levels and a ranking, never power.  
* **Teaching:** playing with someone doing content for the first time (counted per Lineage) gives a bonus to the run's rewards after the points are counted, so the ranking isn't affected.

New loadouts and Disciplines come in without rework: each brings its own skill pool, and role passives and item effects that read tags already work on them on launch day.
