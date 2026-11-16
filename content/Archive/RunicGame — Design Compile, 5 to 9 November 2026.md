---
title: "RunicGame — Design Compile, 5 to 9 November 2026"
tags:
  - "archive"
  - "appendix"
  - "appendix/design-compile"
source: "RunicGame — Design Compile, 5 to 9 November 2026"
source_url: "https://docs.google.com/document/d/1mwKrN4OZidDuRU-AdFxlYmjvbd5TcrCQ2DXoTtj-du4/edit"
created: "2026-11-09"
modified: "2026-11-09"
---

## About this compile

This collects what was decided, proposed and left open in the design conversation of 5 to 9 November 2026, with the numbers. Decided means the decision was stated or confirmed. A proposal is a suggestion that hasn't been accepted yet. Open is a question still to answer. Every number is an example meant for data tables unless it says otherwise. The second part is a comparison of item systems in other games and a proposal for RunicGame's items.

### Where each part stands in the docs

| Update | Where | Status |
| :---- | :---- | :---- |
| Lore and Quest Design, Draft 3 | Google Docs in RunicMMOEngine | Done on 5 Nov |
| RunicWorld authoring vault | RunicGame repo, docs/RunicWorld | Pushed to main (2a4d4ae), then the Overhear trigger and quest kinds (387885d) |
| Housing: houses, basements, home functions | RunicDocs | Applied on 5 Nov (6158fa5) |
| 5 Nov decisions: quests, races, organizations, Inscriptions, professions, ships, region mechanics, monsters | RunicDocs prompt (RunicDocs-prompt-2026-11-05.md) | Not applied yet |
| Content growth and the fixed number scale | RunicDocs prompt (RunicDocs-prompt-progression-2026-11-06.md) | Not applied yet; apply after the 5 Nov prompt |
| Leveling run, PvP layer, scale anchors at 4%, items | This compile only | Not in any prompt yet |

## Quests and story

### Decided

* Quest items go to a special inventory tab. They are always character-bound and can never be stolen. Items have three binding levels: character-bound, account-bound and unbound.  
* Knowledge is gained automatically, in the style of Crimson Desert. Codex entries carry knowledge tags with tiers, in the style of EverQuest, and NPCs know things through their role, home and faction.  
* No exclamation marks over NPCs. At most a compass mark or a circle over a region. Secrets in the style of WoW and EverQuest are part of the design.  
* The game is non-linear, like RuneScape: series, quest lines and contained quests. A quest can be linear inside; the game isn't. No quest is mandatory, but the rewards draw players in.  
* There is no main story. The old main story (the faction's continent and the war) becomes one very long faction series of grandmaster complexity, which requires faction reputation, quest points and level. Low-level quests never involve the player in the big picture, and there is no world thread through every expansion.  
* Only series have quest prerequisites. Other quests can require level, reputation, professions, knowledge or quest points, never another quest.  
* Quest starts are spread evenly across the map, so every level has starts in several regions.  
* A quest that needs a profession item can be completed through a job contract. Profession quests are the exception: they can't be outsourced and give profession XP and their own currency.  
* Event quests are the only repeatable quests. Any event can be given as a quest.  
* Beginner quests stay inside each race's region; a series around levels 8 to 12 mixes the faction's three races. Visitors can do another race's quests, with the pronoun changed and an opening line about being a visitor. Their rewards stay useful later (inventory slots, the race's mount), and their difficulty comes from verbs, not combat.  
* Faction quests come in mirrored pairs: one structure, two settings, with small changes per faction. Organization quests are the same for everyone.  
* Rewards come in categories: access, travel, professions, housing, exploration, prestige, plus a special category. A quest never gives an item that can be lost for good, such as a weapon. Quests give recipes, consumables, currency, unlocks, experience, reputation and quest points.  
* Epic quests give at most epic recipes for combat, such as a weapon recipe with a special effect, and never combat skills. The faction series gives a weapon recipe that slightly beats the reference weapon, with a special effect and hard or unique materials.  
* Quest points have a regional part, which counts toward that region's reputation.  
* The NPC rune: an NPC with something new for this character (a quest, a hint, a vendor or knowledge) turns its head and shows a small rune on its nameplate, only within a few meters. It disappears once everything new has been heard. Secrets never show it unless the player carries what the NPC reacts to, and background NPCs never show it.  
* The quest helper keeps only hints, the knowledge linked to the quest, the timeline and, in some cases, the area around an object.  
* Overhear: a player who stays in an area for the zone's set time gets a knowledge entry or a lead, once per character. Requirements are optional, such as an active quest or a prior entry. It is a Game block built on the Engine's volume API.  
* Skill variants (morphs) from epic quests stay in Ideias.

### Open

* Organization allies and rivals in the style of EverQuest (acting against one organization moves its allies and rivals a little). Leaning yes.

### Numbers

* About 30 quests per faction and 140 shared, toward a goal of 250 or more, built a few at a time.  
* The mixed beginner series sits around levels 8 to 12.  
* Overhear dwell time per zone, for example 1, 2 or 3 seconds.

## Races, starts and organizations

### Decided

* Races: Human and Dragonkin in one faction, Elf and Orc in the other, and the Undead in both.  
* Each race, the Undead included, always starts at the same place in its own region. The random start and the tailored start were dropped. The Undead choose their faction at character creation, and each continent has an Undead region.  
* Governments and other groups are all organizations, each with its own reputation. Organizations are neutral; only the two factions are enemies.  
* Quests give a large and fixed amount of reputation. Repeated deeds and events raise it slowly, more at low standing and less at high standing. Acting against an organization loses reputation, and reputation never decays with time.  
* Some quests require a reputation level, and the faction series requires faction reputation.

## Inscriptions, death and weapons

### Decided

* Inscriptions (working name) are skill levels in the style of ArcheAge's ancestral levels: they add special effects to existing skills and improve them by level.  
* Inscription levels can be lost only in marked regions and moments (war time, the neutral continent and others), always announced. Any death while the loss is active drops one level, never below 1 once reached. Recovery is neither fast nor a giant grind.  
* Outside that, the death penalty stays light and costs only experience, never items.  
* Until there is a final name, write "Ascensions (dungeon and raid)" and "Inscriptions (skill levels)", since Ascendancy is the old empire.  
* The campaign weapon is removed. A reference weapon still sets the best-in-slot base against power creep, and it can be a crafted tier. There are many ways to get weapons.

### Proposal

* Inscriptions sit on the fixed number scale: their top level is set at launch, and new Inscriptions add effects, not higher levels.

## Professions

### Decided

* Professions have a max level, then a continued XP grind for small improvements. Unlocking every recipe and becoming a master takes a grind, but it is viable in two or three professions.  
* Reaching MAX needs a huge grind like RuneScape's. MAX gives a title, a mantle, a maker's mark and a small, capped efficiency in labor, time and resource cost, plus milestone rewards.  
* Machining is a new profession, which makes ship stations, with Metalwork and Carpentry as secondary professions.

### Numbers

* The curve numbers are temporary. Reference: in RuneScape, level 85 needs a quarter of level 99's XP.

## Ships

### Decided

* Two layers: ship parts (hull, sails, helm, keel) can be upgraded, and stations go in slots.  
* Every ship has at least one slot, and bigger ships have more. Slots are categorized by position: broadside, deck, hold, bow and stern, and each station lists the positions it fits. A cargo hold can't replace a cannon. A trader comes with trade pack slots that can be removed for something else.  
* Tonnage: every station and trade pack weighs something, each ship has a capacity, and more weight means less acceleration and turning.  
* There is no minimum crew, but one person can't sail a big ship efficiently.  
* A removed station becomes a crate that can go to another ship.

### Numbers (placeholders)

| Ship | Slots |
| :---- | :---- |
| Small boat | 1 deck |
| Clipper | 2 broadside, 1 deck, 1 hold |
| Trader | 2 broadside, 1 deck, 3 hold |
| Galleon | 8 broadside, 2 deck, 2 hold, plus bow and stern |

## Region mechanics and monsters

### Decided

* Every region mechanic is built from meters, conditions, effects and counter-measures, and more piece types can be added later.  
* PvP fairness rule: a region mechanic only adds noise. It never hides real information and never changes combat numbers.  
* Sanity in the dark is a new mechanic that exists only in its region. The other examples (cold, toxic swamp, altitude, sandstorm, magnetic region, rift distortion) stay as examples in Ideias.  
* Monsters get behavior modules with parameters and conditions (night, day, rain, light). The lurker and pack specs are defined during implementation.  
* Undiscovered stealth, whether a player or a mob, is never sent to clients.  
* The light query returns the overall luminosity at a point: the environment plus every light source.

### Proposal

* For undiscovered stealth, clients get only sound cues with a fuzzed position.

### Numbers

* Sanity has four tiers: whispers; false steps and shadows; hallucinations only you see, which do no damage; and at zero, a real shadow, only yours, until you reach light.

## Housing

### Decided

* Plots are only in the open world. There is no instanced housing.  
* House designs are models bought on the Market Isle, with two floors and balconies with covered space under them.  
* A house gives farming and husbandry on the plot, recall with a cost and a cooldown, crafting stations for some professions (the design needs that profession's mastery), and a packing bench and a resource-pack processing station for everyone.  
* No workers, laborers or dispatched expeditions. No bank and no commerce at the house.  
* Buffs come only from furniture given by rare rewards, and never affect combat.  
* Any crop grows anywhere; the node's climate sets how efficiently it grows. The exception is crops that only grow on the neutral continent.  
* The basement is an extra, not part of the first construction. It starts with an entrance (a trapdoor or a staircase), then grows one cell per expansion, horizontally up to the plot's area or vertically. Each expansion needs a new Market Isle design and is paid in resource packs.  
* The basement is a room like any other (chests, workbenches, trophies, furniture) and a cellar by default, for wine and aged delicacies.  
* Housing zones are built with the basement enabled from the start, and the basement dictates the ground. The construction approach: the cook cuts a hole in the heightfield under each zone and puts in a cooked tray with one sheltered volume; the hollow is a grid of cells; 4x4 m lids over the cells are the zone's ground; server and client build the walls and floors from the cell mask with the same rule.

### Proposals

* The home packing bench uses the recipes of the plot's region, and its packs take that region as their origin.  
* Recall uses the teleport rules (idle only, no pack or vehicle, cost by distance), so a house is never a cheap teleport anchor.  
* Home stations go to the professions fed by the land (Cooking, Alchemy, Tailoring, Leatherwork, Handicrafts); Metalwork, Weaponry and Machining stay in cities and nodes.  
* Each crop has a climate affinity (ideal, good or poor) that multiplies its growth time.  
* Furniture effects apply only on the plot: crop growth, stations, recall cooldown.  
* The packing bench and the processing station go under the balcony, since packs and carts stay at ground level; crafting stations go in the basement.  
* Cellar barrels and racks work only inside the sheltered volume, so the basement's size is its aging capacity. Aged packs age there too. Aging runs in real time, keeps its state in the Deed and yields the same in every climate.  
* A new basement level needs stairs or a trapdoor from the level above.

### Open

* The basement's vertical limit. It has to be set before housing zones are cooked, because the tray is cooked at the deepest level.  
* Which professions get home stations, and whether those stations get the specialty return of the plot's node.  
* What a chest placed in a house does, since personal storage is one global chest.  
* Which profession owns aging (Cooking is the likely one).

### Numbers

* Plots of 8x8, 16x16 and 32x32 m on the 8x8 slot grid; 32x32 m is the largest mapped size. Two plots per account, at most one 32x32 and at most one on the neutral continent.  
* Basement cells of 4x4 m, 3.5 m high per level: 4 per level on an 8x8 plot, 16 on a 16x16 and 64 on a 32x32.  
* Design measures: 4 m per floor, rooms on the 4 m module (4x8 or 8x8 m), U-shaped stairs of 4x4 m per floor, 36 small crops per 8x8 m (ArcheAge's density).

| Model (proposal) | Plot | House | Balcony and covered space | Rest of the plot |
| :---- | :---- | :---- | :---- | :---- |
| Garden annex | 8x8 | No two-floor house (the stairs would take half a floor) | None | About 36 small crops |
| Balcony house | 16x16 | 8x12 m, two floors, about 2 rooms and the stairs per floor | 4x8 m balcony over a 32 m² porch | 8x16 m strip, about 72 small crops |
| Farmhouse | 32x32 | 12x16 m, about 6 rooms per floor | 4x16 m balcony over a 64 m² porch | 32x16 m farm (about 288 small crops) and a 16x16 m yard or pen |
| Livestock house | 32x32 | 12x16 m in the style of a Minho house: animals and storage below, living upstairs with an outside stair and a veranda | Veranda over the animals' entrance | 32x16 m pasture |
| Courtyard manor | 32x32 | 28x28 m ring with 8 m wings and a 12x12 m courtyard, about 640 m² per floor | 2 m upper gallery over a covered arcade | Open 8x8 m courtyard; the farm goes on the second plot |

## Progression and the number scale

### Decided

* No WoW retail model. The level cap never rises. Updates add content at every level of the range (10, 25, 30, 50 alike) and new regions, and can add a new continent for max-level players. The older continents, the neutral one included, stay relevant.  
* One number scale for everything, from a level 1 mouse to the gods, set at launch. New content never raises it; a new item is a different function, effect or situational use.  
* The region is the content, with its own mechanic, like the maps of Guild Wars 2: one needs a jumping mount, another a water mount or a glider, another is a war where players clear things and repair cannon stations.  
* Vertical progression is upgrading items, inside the scale. The previous armor is dismantled into parts, and those parts are components of the new best-in-slot.  
* Headroom: at launch the maximum numbers sit below the top of the scale, and each update's upgrade step closes half of the remaining gap, so the headroom never runs out.  
* Growth of 4% per level.  
* New low-level content mostly serves leveling players, alts and completionists. That is accepted: leveling being fun is what makes alts appealing.  
* A design pillar: old content stays relevant, and there is no power creep.

### Proposals

* A top piece's recipe needs parts from the gear of the previous content step (the new continent's best-in-slot needs parts from neutral-continent gear), so older content keeps feeding the newest.  
* The scale is a data table; content declares its level, tier and role, and the content build rejects anything outside the scale.  
* The server stores damage and healing in hundredths and shows integers, with 1 as the visible floor. Single hits fit in int32; HP pools use int64.

### Open

* Where the top of the scale sits above the launch best-in-slot.  
* The level cap's value (50 is an example).

### Numbers

Headroom example, with the launch best-in-slot at +15.5% and the top of the scale at +25%: the steps land at about +20.3%, +22.6%, +23.8% and +24.4%.  
Anchors at 4% per level. At equal level a bite takes 10% of the character's HP, and about 7 basic hits kill a wolf.

| Anchor | HP | Typical hit | Reading |
| :---- | :---- | :---- | :---- |
| Damage floor | None | 1 | Every landed hit does at least 1, such as a level 1 rat on a level 50 in plate |
| Rat, level 1 | 20 | 3 | About 33 bites kill a level 1 character |
| Wolf, level 1 | 80 | 10 | 10 bites kill a level 1; a pack of 3 does it in about 7 s |
| Character, level 1 | 100 | Basic 12, skill 30 |  |
| Character, level 25 | About 256 | Basic about 31, skill about 77 |  |
| Character, level 50 | About 680 (cloth about 550, plate about 850) | Basic about 82, skill about 205 |  |
| Wolf, level 50 | About 550 | About 68 |  |
| Elite, level 50 | About 5,500 | About 140 | A small-group fight |
| Raid boss | About 1,300,000 | Telegraphed kill about 2,000 | About 7 minutes with 30 players at about 100 DPS each |
| A god | None | 30,000 or more | Beyond any player; divine items borrow this tier |

What 4% does across levels, before armor, compared with 7%:

| Fight | At 4% | At 7% |
| :---- | :---- | :---- |
| Level 30 wolf biting a level 50 | About 22 bites | About 39 |
| Level 10 wolf biting a level 50 | About 48 | About 150 |
| Level 50 killing a level 30 wolf | About 3 hits | 1 or 2 |

A level 50 has 6.8 times the numbers of a level 1, and 2.2 times those of a level 30. At one bite every 2 s, a pack of five level 30 wolves gets through 22 bites in about 9 s, or about 15 s with 40% damage reduction.

## The leveling run (New Game+)

### Decided

* A max-level character can redo the leveling from level 1, endlessly. The character keeps two truths: its real state is frozen during the run, and the run is a second layer with its own level, XP and quest progress.  
* A run starts at an Altar. It can be ended at any time, which snaps the character back to its real state; reaching max level ends it with a completion bonus. Ending early counts only what was done, which is little unless the run covered a lot of content.  
* The run starts with starting gear, and gear has level requirements.  
* Level, skill points, Discipline and level choices reset, and professions reset too. Profession XP earned in the run counts toward points, so trade runs, Larceny and crafting are all allowed.  
* The Codex, map discovery, reputation, housing and cosmetics stay.  
* The bank and the house stay usable, but anything stored before the run is locked. Only items deposited during the run can be taken out, and they stay in the bank on return.  
* A quest done on the real state can be replayed for run points, with no quest points again and without overwriting the original choice. A quest or content done for the first time merges into the real state on return, with its quest points, rewards and choice. Each quest counts once per run, and content far below the run's level gives no points.  
* Points come from content: quests, events, dungeons, raids, bosses and profession XP. Gold counts only when earned from content (quest and event rewards, deliveries, coin purses), never from trades or the auction.  
* Rewards: gold, titles, cosmetics, prestige levels and a ranking, never power.  
* Teaching: playing with a player who is doing content for the first time gives a bonus to the run's rewards, after the points are counted, so the ranking isn't affected. "First time" counts per Lineage, so a veteran's alt never counts as new.  
* Technically a run is a second progression profile per character; the simulation only sees the active one, and returning is one idempotent merge.

### Proposals

* On return, the run's inventory and gold join the original as well, since a player could deposit everything before ending anyway.  
* Nothing can be mailed or traded into the run from the same Lineage.  
* Labor is per Lineage, so the run spends the same pool as the alts.  
* Home stations stay usable at the run's profession level.  
* If the base game ends up free-to-play, a new player's account also needs some play time (for example 10 hours) before it triggers the teaching bonus.

### Open

* Crops and animals already on the plot when the run started: can the run harvest them? The proposed reading is that they keep growing but can't be harvested until the character returns, and the run harvests only what it plants or raises.

## PvP on the same scale

### Decided

* PvP numbers can differ from PvE, since each is balanced separately. At the current scale, characters do too much damage in PvP relative to other characters' health; PvE is fine.  
* PvP has to work for 1v1 and for 100v100 on the same scale.

### Proposals

* HP stays one pool, because in PvPvE a character is hit by mobs and players at the same time.  
* A PvP damage coefficient on hits against players sets the 1v1 time to kill.  
* Focus-fire pressure, PvP only: each extra attacker on the same target within a few seconds adds less, at times 0.85 per attacker, capped at about 6.7 times a single attacker. A 1v1 is untouched.  
* AoE falloff, already in the Vision (less damage per extra target and a separate cap for CC), handles AoE spam.  
* Healing on a player who was hit by another player in the last 10 s uses the PvP value, so healers can't out-heal everything once PvP damage drops.

### Open

* The coefficient: times 0.25 fits the slow, long-cooldown combat best; times 0.4 gives sharper PvP.

### Numbers

Level 50, with 40% physical reduction for plate and 15% for cloth. "Now" is the scale without a PvP layer. The focused rows use the pressure rule.

| Case | Now | PvP times 0.4 | PvP times 0.25 |
| :---- | :---- | :---- | :---- |
| One skill on cloth | 32% of HP | 13% | 8% |
| 1v1, killing cloth | About 6.5 s | About 16 s | About 26 s |
| 1v1, killing plate | About 14 s | About 35 s | About 57 s |
| Cloth focused by 5 | About 1.3 s | About 4.4 s | About 7 s |
| Cloth focused by 20 | About 0.3 s | About 2.5 s | About 4 s |

Without the pressure rule, 20 attackers would kill cloth in about 1.3 s even at times 0.25.

## Tools and authoring

* The RunicWorld vault (Obsidian) holds the world's content: quests, places, NPCs, knowledge, items and history, with templates, dashboards (Dataview) and a controlled vocabulary of knowledge tags, NPC roles, IDs, quest triggers and verbs. Structure comes first and dialogue later.  
* Quest kinds: series, arc, side, profession, epic, secret and event. Start guidance runs from 0 (secret) to 3 (a circle over the area).  
* The GIMP map owns positions and shapes, and the vault owns meaning: a layer's name is the ID it places. The map runs at 160 px per km (6.25 m per pixel), and build_placements.py turns the export and the notes into placements for the engine.  
* Lore and Quest Design stay as Google Docs for now; Vision, Architecture and Ideias changes go through a dedicated docs session that gets a prompt.

## Items: other games and a proposal

### Decided on 9 November

* Grades in the style of ArcheAge, from Common to Mythic, stay, and quality is added.  
* Weapons and armor come in categories: a crafted line that goes up through metals made from ores found in the world (tin, iron and on to mithril, adamantite and beyond); weapons dropped by bosses, which sit somewhere on the crafted tiers; and mixed items, where a dropped item gets a crafted part to become the final item, or where a blueprint drops.  
* Crafting sets the quality, and a dropped item's quality can be improved through crafting.  
* Grade can be improved through crafting: for crafted items by improving the materials, and for dropped items by spending materials on them.  
* Improvement is grindy but has no RNG. Randomness exists only in what drops (items and materials).  
* Several materials don't correspond directly to a tier.  
* Grade and quality can be improved on any item. An iron weapon could reach Mythic at max quality, even if it isn't a good use of materials.

### How other games do it

| Game | How items are built | How they improve | Randomness |
| :---- | :---- | :---- | :---- |
| RuneScape 3 | Metal tiers every 10 Smithing levels, from bronze (1) to elder rune (90); masterwork armour at 99 | Each upgrade from +1 to +5 takes the previous version plus bars and raises the tier by 1. Masterwork is very slow, and can be trimmed with components from boss armour (Torva, Malevolent) | None in upgrades |
| WoW (The War Within) | Items sit on upgrade tracks by source (Explorer, Adventurer, Veteran, Champion, Hero, Myth); crafted gear has quality ranks | Fixed-cost upgrades paid with Valorstones and crests, cheaper once a higher item level is owned in that slot. Crafting quality comes from skill, gear and reagent quality, and Concentration, a regenerating resource, lifts a craft to the next quality | None in upgrades. Inspiration, a random quality proc, was removed for being too random |
| ArcheAge | Grades from Basic to Mythic, and gear lines (Hiram, Library, Erenor) | Regrade scrolls; failures past Celestial can crystallize the item, and anchoring charms are needed past Divine. Erenor gear is fed with Ayanad gear | High: regrades and tempering can fail |
| Albion Online | Tiers and enchantments (.1 to .4) each add 100 item power; quality from Normal to Masterpiece adds 0, 20, 40, 60 or 100; artifact items need a dropped artifact plus resources | Craft or buy a higher tier or enchantment | Quality is rolled when crafting, with better odds from specialization |
| Guild Wars 2 | Rarities up to Ascended, about 6% over Exotic; Legendary has the same stats as Ascended | Legendary adds stat swapping, free removal of upgrades and account-wide sharing, never more power | Drops only |
| Elder Scrolls Online | Quality from Normal to Legendary, with one temper per step (Honing Stone, Dwarven Oil, Grain Solvent, Tempering Alloy); the gear level has stayed at CP160 for years | The same tempers work on any item level; new content adds item sets instead of higher levels | Improvement attempts are chance-based |

### What fits RunicGame

* From RuneScape: upgrades that consume the previous item (the same idea as the upgrade chain), and boss components that finish a crafted top piece, which is the mixed category.  
* From WoW: fixed, visible upgrade costs, a discount for alts once a higher item exists, and crafting quality decided by skill and materials, with a spendable resource to push one step. Labor can play the role of Concentration.  
* From ESO: improvement materials that work on every level (materials that don't correspond to a tier), and a gear cap that never moves while new content adds sets.  
* From Guild Wars 2: the top tier stays fixed, and prestige items add convenience and looks, not power.  
* From Albion: simple additive power math across the axes, and artifacts as mixed items that change abilities rather than numbers.  
* From ArcheAge: the grade names and the visual progression. Its failures, crystallization and breakage are what to avoid.

### Proposal: four axes

| Axis | What it sets | Where it comes from | Range (example) |
| :---- | :---- | :---- | :---- |
| Tier | The base numbers, from the item's level band on the scale | The material (crafted) or the drop's placement | 8 tiers, one every 7 levels |
| Grade | A small bonus, the visuals, and effect awakening at Epic and Mythic | Grade materials, one kind per step, usable on any tier | Common to Mythic, up to +5% |
| Quality | A bonus from the crafter's work | Crafting, or a crafter reworking an existing item | 5 steps, up to +10% |
| Unique effect | Behavior, never numbers | Drops, mixed items, rare recipes and blueprints | No numbers |

Grade and quality multiply: 1.05 times 1.10 is 1.155, so a fully improved item is +15.5% over its tier. That matches the launch best-in-slot budget already in the Vision (the reference weapon plus about 15.5%), with quality taking the place of the old item level axis.

### Proposal: categories

| Category | How it's made | Tier | Grade | Quality | Effect |
| :---- | :---- | :---- | :---- | :---- | :---- |
| Crafted line | Ore, wood, hide and fiber of the tier | The material's tier | Grade materials, at the craft or later | Set by the crafter | Only from rare recipes |
| Boss drop | Dropped by a boss | Placed on a crafted tier | Arrives at the source's grade, raised with grade materials | Arrives at a set quality; a crafter can rework it | Yes |
| Mixed | A dropped core plus crafted parts, such as a fang made into a blade with a mithril hilt | The core's tier | As crafted | Set by the crafter who finishes it | The core's |
| Blueprint | A dropped design, crafted with normal materials | The design's tier | As crafted | Set by the crafter | The design's |
| Upgrade chain piece | Parts from dismantled previous gear plus new materials | The top tier | As crafted | Set by the crafter | Can carry one |

### Proposal: tiers

The metal names other than tin, iron, mithril and adamantite are examples, and leather, cloth and wood need lines of their own with the same levels. New materials added later sit on an existing tier with a different profile, never above the top.

| Tier | Level | Metal (example) | Numbers vs tier 1 |
| :---- | :---- | :---- | :---- |
| 1 | 1 | Tin | 1.00 |
| 2 | 8 | Copper | 1.32 |
| 3 | 15 | Iron | 1.73 |
| 4 | 22 | Steel | 2.28 |
| 5 | 29 | Name open | 3.00 |
| 6 | 36 | Mithril | 3.95 |
| 7 | 43 | Adamantite | 5.19 |
| 8 | 50 | Name open | 6.83 |

Each tier is 1.32 times the one before it (4% per level over 7 levels). A fully improved item is 1.155 times its tier, so it always stays about 12% below the next tier's plain item: an iron weapon at Mythic and Masterwork comes to about 2.00, while plain steel is 2.28. Improving an old item is possible but never worth more than moving up a tier.

### Proposal: quality

| Quality | Bonus | Note |
| :---- | :---- | :---- |
| Normal | 0% | Batch mode, which skips the minigame, gives this |
| Fine | +2.5% |  |
| Superior | +5% |  |
| Exquisite | +7.5% |  |
| Masterwork | +10% | Needs the profession's mastery |

* No luck: the crafter's level against the recipe's difficulty sets the highest quality reachable, and the crafting minigame places the result within it.  
* A crafter can spend extra labor to push a craft one step, the way WoW's Concentration works.  
* Reworking an existing item, dropped or crafted, raises its quality one step at a time, paid with materials of the item's tier and labor. The item records who reworked it.

### Proposal: grade without RNG

| Step | Bonus (cumulative) | Material (working name) | Units | Source |
| :---- | :---- | :---- | :---- | :---- |
| Uncommon | +0.5% | Flux | 1 | Mining and refining |
| Rare | +1% | Polish | 2 | Gathering and world mobs |
| Heroic | +1.5% | Tempering salt | 4 | World mobs and coin purses |
| Epic | +2.5% | Ember oil | 8 | Dungeons |
| Legendary | +3.5% | Starglass | 16 | Dungeon Ascensions and world events |
| Celestial | +4.5% | Celestial dust | 32 | Raids, ranked PvP and world bosses |
| Mythic | +5% | Mythic Spark | 64 | Raids, ranked PvP, world bosses and the boss region |

* Every step has a fixed cost, 127 units in all from Common to Mythic. The only luck is in getting the materials to drop.  
* The same cost on every tier. That makes a low-tier Mythic as expensive as a top-tier one, which is why it is possible but not recommended.  
* Crafting an item at a grade costs the same grade materials as upgrading it afterwards, so neither path is cheaper.  
* The bonuses and visuals are the ones already in the Vision; effects still awaken at Epic and Mythic.

### Proposal: where items start at level 50

| Source | Tier | Starting grade | Starting quality | Effect |
| :---- | :---- | :---- | :---- | :---- |
| Crafting | By material | From grade materials | By the crafter | Rare recipes |
| Dungeons | Top | Rare or Heroic | Fine | One per boss |
| PvP | Top | Heroic | Fine | Yes |
| Raids | Top | Epic | Superior | The most striking ones |
| World bosses and the boss region | Top | Epic | Superior | Yes |

A raid drop starts at about +7.6% (Epic and Superior), a head start rather than a power gap. The reference weapon is the top tier at Common and Normal (100%), and the launch best-in-slot is the top tier at Mythic and Masterwork (+15.5%). Later updates spend the headroom through upgrade chain pieces.

### What this changes in the Vision

* The grade table loses its chance and guarantee columns, and "RNG without oppression" becomes "no RNG in upgrades; RNG only in drops". Mythic Spark stays as a drop.  
* The item level row gives way to tier and quality.  
* In the power budget, "item level up to the cap, up to +10%" becomes "quality up to Masterwork, up to +10%".  
* "Where everything comes from" lists a starting tier, grade and quality instead of an item level.

### Open

* Tier spacing: 8 tiers every 7 levels, or 10 every 5 levels (1.22 times per tier). Also the names after adamantite and the leather, cloth and wood lines.  
* Grade on crafted items: does it come from graded materials made by refiners (bars, planks and leather that carry a grade), or from grade materials added at the craft? Either way it must cost the same as upgrading later.  
* Whether grade costs stay flat across tiers or grow with the tier.  
* How many quality steps, and their names.

## Sources

* [RuneScape Wiki: Mining and Smithing rework](https://runescape.wiki/w/Mining_and_Smithing_rework)  
* [Icy Veins: World of Warcraft gear upgrading guide](https://www.icy-veins.com/wow/world-of-warcraft-gear-upgrading-guide)  
* [Warcraft Tavern: Concentration in The War Within](https://www.warcrafttavern.com/wow/news/new-concentration-system-for-professions-in-the-war-within/)  
* [ArcheAge Unchained: upgrading gear](https://www.magicgameworld.com/archeage-unchained-upgrading-gear/)  
* [Albion Free Market: understanding item power](https://albionfreemarket.com/articles/view/understanding-item-power-in-albion-online)  
* [GuildOrder: Albion crafting and gathering](https://guildorder.com/games/albion/wiki/crafting-and-gathering)  
* [MMOs.com: Albion Online's artifact system](https://mmos.com/news/albion-onlines-artifact-system-detailed)  
* [Hardstuck: Guild Wars 2 equipment basics](https://hardstuck.gg/gw2/guides/general/equipment-basics)  
* [GamingBolt: Guild Wars 2 and the Ascended gear treadmill](https://gamingbolt.com/guild-wars-2-dev-on-ascended-gear-backlash-our-goal-is-not-to-create-a-gear-treadmill)  
* [ESO Wiki: tempers](https://elderscrollsonline.wiki.fextralife.com/tempers)
