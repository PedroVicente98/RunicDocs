---
title: "RunicGame — Combat Systems Review"
tags:
  - "archive"
  - "appendix"
  - "appendix/combat-review"
source: "RunicGame — Combat Systems Review"
source_url: "https://docs.google.com/document/d/1UM0JYOjUUx-AZXnadCTvmGhDv7a0KH6ZjFvFl4M8qG0/edit"
created: "2026-11-12"
modified: "2026-11-12"
---

Compiled on 11 November 2026 from the combat conversation of 10–11 November (BDO and ArcheAge study, controls, targeting, skills, mastery, resources, stats and items). Compared with RunicGame — Complete MMORPG Vision (30 October), RunicGame — Appendix: Ping Resolution (21 October) and the progression notes. This is a review document: nothing here is merged into the Vision yet.  
**Status legend.** **Decided**: stated by the owner. **Proposal**: suggested in the conversation, not confirmed. **Open**: still needs a decision. **To test**: decide by prototype or playtest. **Dropped**: considered and rejected. Numbers are examples for tuning.  
**Structure.** Part 1 lists every item by topic with its status. Part 2 lists what changes compared with the Vision. Part 3 lists what agrees with it. Part 4 is the open checklist. Part 5 lists gaps noticed while compiling.

## Part 1. Items by topic

### 1. References: BDO and ArcheAge

| Item | Status | Detail |
| :---- | :---- | :---- |
| Take from Black Desert | Decided | Command combos (direction or Shift + key) and follow-up links between skills |
| Reject from Black Desert | Decided | Fast pace, animation cancelling as a damage technique, iframes inside attack skills, grabs that ignore super armor |
| Take from ArcheAge | Decided | About 28 skill picks at max level, status-conditional combos, combos between players, ancestral-style morphs (as Inscriptions) |
| Reject from ArcheAge | Decided | Tab target in combat and free three-tree class combinatorics |

### 2. Controls and input

| Item | Status | Detail |
| :---- | :---- | :---- |
| WASD | Decided | Movement. A and D only steer; they are never part of a command |
| Sprint | Decided | Shift+W alone starts sprint. Sprint is a state: it continues while W is held, even after Shift is released |
| Sprint end | Proposal | Ends on releasing W, running out of stamina, or using a skill, dodge or Guard. Pressing Shift with W held restarts it |
| Shift + key | Decided | Fires that key's Shift skill and ignores W. No Shift+W+ or Shift+S+ contexts. Shift+Space removed: Space always jumps, including the sprint-jump |
| Space and Ctrl | Decided | Jump and dodge; players can swap them in settings |
| LMB and Shift+LMB | Decided | Light and heavy attack on every weapon |
| RMB (hold) | Decided | Guard on every weapon; its form depends on the weapon |
| Shift+RMB | Decided | The weapon's alt action, almost always with a movement component (dash, forward or backward) |
| Shift+RMB rules | Proposal | Direction comes from WASD as a parameter, with a default per weapon. No iframe and no Evasion charge, only the weapon's own Guard and a cooldown, so it never becomes a second dodge |
| Q | Decided | A tap key; default home of grabs and other control skills |
| Skill keys | Decided (tweaks possible) | Q, E, F, C: plain, W+, S+, Shift+. X, Z, V: plain and Shift+ |
| Extra combinations | To test | W+V, Shift+V and similar |
| Mouse | Decided | Three buttons only (LMB, MMB, RMB) and the wheel; no side buttons by default |
| MMB and wheel | Decided | Ward control (see Targeting) |
| Hotbar | Decided | 1–5 and Shift+1–5 |
| R | Decided | Tap interacts; hold opens a radial menu, picked with a mouse tether |
| T | Decided | Auto-walk forward only (cruise mode) |
| Tab | Decided | Cursor mode |
| UI windows | Decided | I inventory, P character, K skills, J journal and so on; UI windows never use skill keys |
| Input budget | Decided | 22 commands (16 on Q, E, F, C; 6 on X, Z, V) plus 10 hotbar keys = 32 |
| Press only | Decided | Every skill fires on press; no hold variants and no charged versions. Holding exists only for Guard and the R menu |
| Double-tap | Decided | Never used for anything (too error-prone) |
| Input resolution | Proposal | Most specific match first: Shift+key, then direction+key, then the key alone. A combination with no skill falls through to the next. Dodge and Guard always win |
| Action floor | Open | The Vision says 0.25 s between discrete actions; earlier notes say 0.5 s. Proposal: the floor is per action type, so starting a sprint never blocks a skill pressed right after |
| Skill bar mode | Open | An ArcheAge-style bar as an alternative layout of the same skills |

### 3. Command board

| Item | Status | Detail |
| :---- | :---- | :---- |
| Board | Decided | Players place their active skills freely in a grid of keys × contexts. Any skill can go in any cell; even fixed skills have configurable commands |
| Auto-placement | Proposal | When a skill is learned, it goes to a suggested cell derived from its components: Control → Q row; advance or leap → W+; step back or defense → S+; long cooldown or high cost → Shift+; buffs, cleanse and resurrection → X, Z, V. It never moves a skill the player placed |
| Context meaning | Proposal | A shared meaning used as placement hints for all 50 classes: plain = core skill, W+ = engage, S+ = defensive, Shift+ = empowered |
| Presets | Proposal | Default layouts per class; layouts saved per class and per skill preset; an Altar reset keeps the cells of skills that remain |
| Combos follow skills | Decided | Links and highlights point to the skill, not the key. The client decodes keys and the server only receives skill IDs |
| Reading enemies | Decided | From animations and telegraphs, not from keys |

### 4. Timeline and cancelling

| Item | Status | Detail |
| :---- | :---- | :---- |
| Timeline | Decided | Startup (shown to the player as the cast bar) → active → recovery. Cast time and startup are one phase |
| Commit | Decided | Pressing another skill never cancels a skill's startup, and Guard doesn't either. Only dodge cancels a startup, and the skill's cooldown applies |
| Active frames | Decided | Nothing cancels them |
| Recovery | Decided | Guard or dodge skips it. Another skill starts at once, with the leftover recovery added to its startup, so no time is saved |
| Dodge | Decided | Can't be cancelled; startup under 100 ms; a long iframe; a cancel never extends the iframe |
| Guard | Decided | Has its own startup before it is active; ends on release or when any skill is used, like a recovery |
| Fast attacks | Decided | Basic attacks and fast skills deal less damage and are naturally hard to dodge |
| Reaction numbers | Proposal | Dodge startup 2–3 ticks; Guard startup 3–4 ticks. Attacks meant to be reacted to have windups of at least 400–450 ms (the Ping appendix's 350–400 ms plus defense startup). At 100 ms ping with the latency helpers, a 300 ms windup leaves about 185 ms to react (a guess) and a 400 ms windup about 285 ms |

### 5. Resolve, grabs and protections

| Item | Status | Detail |
| :---- | :---- | :---- |
| Skill iframes | Decided | None. Iframes exist only on the dodge |
| Resolve as super armor | Decided | Skills can grant Resolve, which works as super armor |
| Grabs | Decided | Grabs never ignore Resolve. Example: the spear's skewer-and-throw is blocked by it |
| Skill-granted Resolve rules | Proposal | Blocks CC only (damage, conditions and Concussion still land). A separate flag that never starts or advances the T1/T2 chain. Starts on a set tick and ends if the skill is cancelled, so "start and cancel" is never a free immunity |
| Uptime budget | Proposal | A PvP cap on Resolve uptime (example 20–25%) checked by a cook-time validator |
| Fallback against Resolve | Proposal | Interaction rule: if the target has Resolve, the grab becomes Stagger build-up, so the skill still does something |

### 6. Targeting

| Item | Status | Detail |
| :---- | :---- | :---- |
| Combat | Decided | 100% action. No tab target on enemies. Hostile skills always follow the crosshair |
| Two target slots | Decided | Action target and Ward |
| Action target | Decided | Any entity, enemy or ally. The exact entity under the crosshair; if none, the closest one within a radius, after a short dwell. Faint outline. Feeds the info frame and the light aim assist |
| Action target numbers | To test | Radius about 5°; dwell about 100 ms on a direct hit and 250 ms on a closest guess; the frame lingers about 2 s after the crosshair leaves |
| Ward | Decided | An ally or yourself. Clear outline, with an optional arrow over the head |
| Ward control (variant 2) | Decided (to test) | MMB tap on an ally pins them; MMB tap on nothing unpins (automatic); MMB hold (about 300 ms) pins yourself; the wheel cycles your group. No modes to remember |
| Cycle group | Decided | Party, team or another predetermined group. Neutral allies enter only by tapping MMB on them |
| Wheel default | Decided | Cycles only once a Ward is set; a setting makes it always active |
| No Ward | Decided | A target skill goes to the ally closest to the crosshair (default) or to yourself (setting) |
| Fallback pinning | Proposal | The fallback is one-shot: it never pins, so aiming still matters until the player pins |
| Two allies at once | Decided | Crosshair on ally A (action target) and Ward on ally B is legal; target skills go to B, action skills go where the player aims |
| Frames | Decided | The action target and the Ward each show a frame like a tab-target MMO: health, mana, Resolve, buffs, debuffs and conditions |
| Highlights | Decided | Allies that would benefit from a skill are highlighted; when cycling, the board cells of skills that would combo on the Ward glow |
| Data | Proposal | Everyone in view: health and a status bitmask (about 8 bytes per change). The two targeted entities: full detail (about 50–100 bytes per change). Never reveals what the player couldn't see |
| Settings | Decided | Wheel behavior, cycle group, no-Ward fallback, hold time (about 300 ms, 200–500), Ward outline and arrow, action-target outline strength |
| Targeting Lab | Open | A browser prototype to test the variant, dwell times, fallback and cycle order (offered, not built) |
| Variant 1 (two modes) | Dropped | MMB toggling between Action mode and Ward mode |
| Triage mode | Dropped | Ctrl with mouse-over casting on party frames; replaced by the Ward |

### 7. Skill delivery and casting

| Item | Status | Detail |
| :---- | :---- | :---- |
| Delivery types | Decided | Action, Placed area, Target (Ward), Target-centered area, Dual-use, Self |
| Action | Decided | The crosshair sets direction and path; the action target never makes a skill home |
| Placed area | Decided | Shown while casting and placed where the crosshair is when the cast ends. Not necessarily a projectile: the area can spawn directly |
| Projectiles | Decided | No path is shown. An area left on impact (fire left by a fireball) appears where it hits |
| Target-centered area | Decided | A circle centered on the Ward (example: an area heal); each skill locks in place or follows the Ward |
| Dual-use | Decided | A projectile, beam or area that hits the first entity or everything in its path, depending on the skill. The effect depends on whether each one is an ally or an enemy (like Moira's beam). It never depends on any mode |
| Damaging areas | Proposal | Enemies see the area once it locks, and it fills for about 400 ms before dealing damage. Heals apply at once |
| Movement while casting | Decided | Rooted (default), Slowed (speed set per skill) and Free (mostly basic attacks and the main kit). No automatic penalty: balance lives inside each skill. Applies to the startup and to channels |

### 8. Supports and combos

| Item | Status | Detail |
| :---- | :---- | :---- |
| Friendly aim | Decided | Friendly skills snap to the ally in a generous cone |
| Self-cast | Decided | Through the Ward (hold MMB) |
| Support damage | Decided | Supports' few damage skills are mostly dual-use |
| Healer styles | Proposal | Melee healers heal through hits and auras; ranged healers through dual-use arrows; mage healers through Ward-targeted spells |
| Combos | Decided | ArcheAge-style status combos plus links ("after skill X within N ticks"), both through the Vision's interaction framework |
| Combos between players | Decided | Combos read the target's state, whoever applied it |
| Payoffs consume | Proposal | Big payoffs consume the state, so only the first player cashes in; small bonuses don't consume |
| Combo roles | Decided | Opener, Setter, Payoff, Link, Finisher and Answer are a design checklist only, not in-game tags (Opener and Finisher remain real tags) |
| Combo hint | Proposal | A hint near the crosshair shows the player's own key for a skill that would combo now |

### 9. Skill structure

| Item | Status | Detail |
| :---- | :---- | :---- |
| Skill library | Decided | Every skill is written once, with pools, requirements and tier. Each class's tree is cooked from it, with per-class pin, remove and move overrides for exceptions |
| Pools | Decided | Disciplines only. The weapon kit is not in any pool |
| Requirements | Decided | Weapon parts (blade, point, haft, shield, bow…) and a minimum Focus |
| Tier | Decided | A default tier per skill, overridable per loadout (Vine Strike: tier 1 by default, tier 2 on the Staff) |
| Gate | Decided | Opening tier N needs X picks in each tier below. Passives count as picks |
| Capstones | Decided | Ultimates at level 50, only one per build |
| Mediums | Decided | Martial: needs the weapon part. Infused: weapon part plus half stamina and half mana. Spell: minimum Focus plus mana. Innate: mana only, and appears on every loadout of its Discipline |
| Extra weapon skills | Decided | Thrust, Riposte, Charge and similar move into Discipline pools with weapon requirements; mastery passives can add effects to them |
| Tree numbers | Open | Number of tiers, X, total skill points (28 as the ArcheAge reference) and whether tiers also open by character level |
| Morphs | Decided | Through Inscriptions (see section 11); only skills flagged as morphable get variants |
| Focus | Decided | Mastery only (loadout base plus mastery passives). A threshold that unlocks spells. Not an item stat and no speed role |
| Focus scale | Proposal | 0–10. Base: Wand + Focus 10; Wand + Shield, Staff and Instrument 8; Quarterstaff 4; other loadouts 0. Spells need 3 (simple), 6 (core) or 9 (big) |
| Spell unlock | To test | A spell from the Discipline pool appears in the skill list once the loadout's Focus reaches it. Since Focus no longer comes from items, swapping weapons of the same type never makes a spell dormant |
| Skill anatomy in the docs | Decided | Add medium, requirements, pools, tier with overrides, capstone flag, morph flag, cast mobility and a one-sentence fantasy line (design only) |
| Skill tree with one pick per tier | Dropped | Rejected along with full free form |
| Hold extensions | Dropped | Press only |

### 10. Weapon mastery

| Item | Status | Detail |
| :---- | :---- | :---- |
| Mastery | Decided | Separate from character level and Discipline. Kept per weapon type and never reset: moving from Spear to Instrument starts the Instrument at mastery 1, while level 50 and every skill point stay |
| Milestones | Decided | 1: base kit. 5: cheap ranged strike. 10: first passive. Then one passive choice every 10 levels |
| Max level | Proposal | 50, giving 5 passive slots (10, 20, 30, 40, 50) |
| Scope | Proposal | One mastery per loadout (10 in total), per character |
| Passive pool | Decided | One pool, filtered per weapon. Each passive has a minimum level; a slot takes any passive at or below its own level, so a level-10 passive in a level-30 slot is legal |
| Passive shapes | Decided | Big stat with no effect, big effect with no stat, or hybrid (smaller stat plus a lesser effect). Mastery gives mostly passives and base-kit changes, including base damage, defense and Focus |
| Pool rules | Proposal | No duplicates of the same passive; similar passives stack with a cap per stat; a passive's budget grows with its minimum level |
| Altar | Decided | The reset clears every mastery choice |
| Mastery XP | Decided | Only the equipped mastery levels. No catch-up mechanic |
| Impact | Decided (target) | Mastery 1 vs 50 should be felt, not too hard and not too soft |
| Impact measure | Proposal | In a mirror duel with equal gear and skill, mastery 50 wins about 60–65% of the time; each slot carries about a fifth of that; checked with bot duels and telemetry |
| Level-35 element strike | Proposal | Becomes a mastery passive that imbues the base kit with flame, ice or lightning |

### 11. XP, Inscriptions and morphs

| Item | Status | Detail |
| :---- | :---- | :---- |
| Base XP | Decided | One XP type from every source except professions. Exploration gives base XP |
| Conversion | Decided | Mastery and Inscription receive XP through conversion rates (examples: 0.6 and 0.1), which are the balancing knobs |
| Parallel or split | Open (proposal: parallel) | Parallel: every XP event feeds every active track at its own rate, as in ArcheAge, ESO and Old School RuneScape. Split: for example 40% level and 60% mastery, which slows leveling unless XP values rise |
| Mastery curve | Open | One curve serves both the first weapon and later switches. Example with 100 h of leveling: a mastery cost of 75% of leveling XP maxes the first mastery about 25 h after level 50 but makes a switch take about 125 h. Endgame content paying more base XP per hour shortens switches |
| Inscription | Decided | The level after 50: 50 → Inscription 1, 2, 3… |
| Morph slots | Decided | Inscription X gives X morph slots; morphs cost no skill points |
| Loss | Decided | A death with loss active drops one Inscription level and removes the highest morph slot. Regaining the level brings the slot back empty: the player chooses the morph again |
| Floor | Proposal (leaning) | Can drop back to level 50, after which nothing more is lost (replaces "never below Inscription 1") |
| Inscription pace | Proposal | Example: about 3 h per Inscription level at a 0.1 rate |

### 12. Resources

| Item | Status | Detail |
| :---- | :---- | :---- |
| Resources | Decided | Health, Mana, Stamina, Evasion (charges), Guard and Shield |
| One stamina bar | Decided | Sprint, climbing, swimming, heavy objects and attacks share one bar (Dark Souls style) |
| Costs by medium | Decided | Martial skills cost stamina; Spells and Innate skills cost mana; Infused skills cost half of each (10 + 10 instead of 20) |
| Basic attacks | Proposal | Cost stamina on every loadout, so mana stays purely magic |
| Flat costs | Decided | The same costs in and out of combat; players upgrade the bars through stats |
| Pace | Decided | Fast consumption and fast regeneration |
| Numbers | Proposal | Base 100 stamina and 100 mana. Stamina regenerates 40/s after a 0.4 s pause; mana 20/s after 0.5 s. Light attack 8, heavy 15, martial skill 20–30, sprint 10/s; spells 15–35 |
| Max and regeneration | Proposal | Separate stats, so a bigger bar doesn't also refill faster |
| Climbing hits | Decided | A hit while climbing removes a share of max stamina; climbing skill and gear reduce that share |
| Exploration | Decided | Gives no stamina |
| Sources | Decided | Mostly items, plus Discipline and mastery passives |
| Defense resources | Decided | Evasion and Guard keep their own charges and pool, never stamina |
| Shields | Decided | Sit on the health bar; temporary or until broken; passive shields rebuild after a cooldown; can stack; some attacks ignore or break them (ultimates and rare attacks) |
| Shield rules | Proposal | Newest absorbs first; total capped (example 50% of max health); "ignores Shields" and "breaks Shields" as damage components; skill shields scale with Healing Power |
| Armor weight lean | Open | Cloth leaning to mana, leather to stamina, plate to health and Guard. May conflict with "armor is freer" (section 14) |

### 13. Stats and damage formula

| Item | Status | Detail |
| :---- | :---- | :---- |
| Model | Decided | Direct stats: no attributes (Strength, Intelligence…) and no player stat points. Changing gear is the respec |
| Character sheet | Decided | Resources: Health, Stamina, Mana, Stamina regen, Mana regen. Offense: Physical Power, Magical Power, Healing Power, Crit chance, Crit damage, Cast Time Reduction, Recovery Reduction. Defense: Physical armor, Magical armor, Guard. Efficiency: Stamina cost reduction, Mana cost reduction. Utility: Focus (mastery only) |
| Damage | Decided | Weapon damage × skill coefficient × (1 + Power bonus of the part's domain) × the rest of the Vision formula (role efficiency, armor, subtype). Each damage part reads its own Power |
| Healing | Decided | Weapon damage × healing coefficient × (1 + Healing Power bonus) |
| Power curve | Decided | Diminishing returns: bonus = P ÷ (P + K). Example K = 400: 100 → +20%, 400 → +50%, 1,200 → +75%. Splitting points pays off for hybrid skills |
| Mixed damage | Decided | No class is 100% one damage type; every class has some physical and some magical |
| Caps | Decided | Every % stat has a hard cap in the base data |
| Critical damage | Decided | Base 150%, cap 200% for all content (no PvP/PvE split) |
| Crit chance | Proposal | Base 5%, cap 40%. At both caps the average multiplier is 1 + 0.40 × 1.0 = 1.4× |
| Accessory values | Decided | No single accessory maxes a stat; reaching a cap means specializing in it |
| Cast Time Reduction | Decided | Shortens the startup only above a 0.5 s floor: new = 0.5 + (base − 0.5) × (1 − r). Cap 30%. Examples at the cap: 1 s → 0.85 s; 3 s → 2.25 s |
| Recovery Reduction | Decided | The same formula with a 150 ms floor; cap 40%, provisional until the recovery table exists |
| Ticks | Decided | Results round to 30 Hz ticks (33 ms); reductions under one tick have no effect |
| Telegraph safety | Decided | The 0.5 s cast floor keeps reactable attacks dodgeable (Ping appendix rule) |
| Effects | Decided | Stun duration, build-up, threat and similar stay on skills and passives, never as character stats |

### 14. Items

| Item | Status | Detail |
| :---- | :---- | :---- |
| Two layers | Decided | Implicit stats from the item type (weapon damage; armor pools, Guard and weight) plus budget stats |
| Budget | Proposal | Item level × slot weight × grade; the Vision's grades become a 1.00–1.05 multiplier |
| Point costs | Decided (concept) | Each stat has a point cost per unit, so the mix for any item level is known. Rates are reloadable data tuned by telemetry |
| Example rates | Proposal | 1 point buys 20 Health, 2 Stamina or Mana, 0.5/s regen, 1 Power, 8 armor, 5 Guard, 0.2% Crit or 0.25% cost reduction |
| Negative stats | Decided (concept) | Allowed: big damage with negative health. Zero stats are never shown |
| Negative rules | Proposal | A refund of 0.8 per point; one negative stat per item, down to minus half the budget; items never push Health below about 50% of the base |
| Powers on weapons | Decided | At most 2. The primary comes from the weapon type (martial weapons: Physical; magic weapons: Magical); the secondary comes from the item family |
| Families | Decided | Item families (like ArcheAge's named sets) set the mix: Physical + Magical, Physical + Healing, Magical + Healing. Names to define |
| Healing Power | Decided | Separate from Magical Power (a melee healer like the Paladin shouldn't need caster stats); never a primary |
| Upgrade | Proposal | An upgrade can swap the secondary power, never add a third |
| Accessories | Decided | Necklace, 2 earrings, 2 rings. One or two powers; only accessories may carry a single power |
| Concentrated power | Open | Whether a weapon can trade its second power for more of the first (500 + 500 → 1,000) |
| Armor | Decided | Freer than weapons and accessories: any stat sets, possibly powers. Trading defense for damage (glass cannon) is a valid build |
| Armor sets | Open | Set bonuses and how they are budgeted |
| Reforge and crafting | Proposal | Reforge redistributes the budget and offers 3 distributions; unique weapons keep a fixed distribution; crafting picks from named templates (Bruiser, Climber, Glass…) |
| Cloak | Open | Whether the cloak carries budget stats |

### 15. Reach and weapon properties

| Item | Status | Detail |
| :---- | :---- | :---- |
| Reach | Decided | A fixed property of the weapon type: the hit shape (range, angle, width) and projectile paths. Every weapon of a type has the same reach. Not an item stat |
| Changes | Decided | Only through passives and unique effects (possibly mastery) |
| Range buffs | Decided | Only from outside sources such as ship stations; global to melee and ranged, with melee possibly exempt |
| Visuals | Decided | An effect around the weapon shows the real hit shape, even on basic attacks |
| Weapon properties | Decided | Type, parts, timing profile, hit shapes, base damage and base Focus |
| Armor properties | Decided | Weight: iframe share and condition resistance |

### 16. Basic kit per loadout

| Loadout | LMB light | Shift+LMB heavy | RMB Guard | Shift+RMB alt |
| :---- | :---- | :---- | :---- | :---- |
| Sword + Shield | Slash | Heavy slash | Shield block, free and directional | Shield bash |
| Wand + Shield | Fast bolt | Charged bolt | Shield block | Shield bash |
| Wand + Focus | Bolt | Heavy spell | Magic Guard | Focus personal barrier |
| Spear | Thrust (builds Stagger) | Sweep | Frontal brace, limited | Sprint with frontal Guard |
| Quarterstaff | Staff strike | Heavy staff | Timed Guard, then cooldown | Palm or kick (alternating builds Flow) |
| Staff | Bolt | Area spell | Magic Guard | Bash (stun and push) |
| Bow | Quick shot | Charged shot | Short deflect (Open) | Kick-back (Open) |
| Instrument | Note | Chord (Resonance) | Magic Guard | Bash (stun and push) |
| Greatsword | Slash | Charged strike (breaks Guard) | Parry Guard, limited | Side dash with frontal Guard |
| Dual Axes | Flurry | Cleave | Cross guard, limited | Open |

Status: Decided as a direction, with the Bow and Dual Axes entries open. "Shift+LMB heavy" with charged shots or charged strikes now means press-only versions, since holds were dropped.

### 17. Configurability

| Item | Status | Detail |
| :---- | :---- | :---- |
| Rule | Decided | If something can be configurable, it should be |
| Limit | Proposal | Everything about input and display is configurable; nothing changes what one press does: no macros, no sequence on one key, no auto-chaining, no aim help beyond the game's own light assist. Protects PvP fairness and keeps bot detection simple |

## Part 2. What changes compared with the Vision

| Topic | Vision or appendix today | Conversation |
| :---- | :---- | :---- |
| Main input | A configurable skill bar is the base; Black Desert key-sequence combos are an optional client upgrade | The command board is the main input; an ArcheAge-style bar is an optional layout (open) |
| Basic attacks | On the left and right mouse buttons | LMB light and Shift+LMB heavy; RMB is Guard; Shift+RMB is the alt action |
| Shield bash | Proposal: hold for the version with the stun | Press only; no hold variants |
| Cancelling | No animation lock; players cancel their own attacks and the cooldown applies. Ping appendix proposal: cancel during the windup into dodge or Guard; a cancelled basic attack costs 100–150 ms | Commit: only dodge cancels a startup; Guard only skips recovery; another skill inherits the leftover recovery |
| Timeline | Two values: public cast time and hidden startup ticks | One phase: startup is the cast |
| Weapon kit | Weapon skills unlock by character level (Thrust, Riposte, Charge…), with level choices such as the level-35 element strike | The base kit and passives come from weapon mastery; extra weapon skills move to Discipline pools; the element strike becomes a mastery passive (proposal) |
| Sword + Shield signature | The sword riposte is part of the loadout's signature mechanic | Riposte moves to the Discipline pools; the signature needs a new definition (see Part 5) |
| Class tree | One merged tree of weapon and Discipline skills | The weapon kit is outside the tree; the tree is the Discipline pool filtered by requirements |
| Tiers | A pick in one tier unlocks the next | X picks in each tier below; ultimates at level 50, one per build |
| Stamina | Combat skills never cost stamina; in-combat costs are a % of the maximum; regeneration is a % of the maximum; the maximum is raised in the exploration shop | Attacks and martial skills cost stamina; flat costs everywhere; regeneration as its own stat (proposal); exploration gives no stamina |
| Spear Guard sprint | A skill that costs no stamina | Becomes the Spear's Shift+RMB alt; its cost under the stamina model needs checking |
| Exploration XP | Separate exploration XP spent in an exploration shop (adventurer abilities, resources, maximum stamina) | Exploration gives base XP; the shop's future is open |
| Weapon stats | Secondary stats on weapons (critical, speed, Guard, reach) with a 3-option reforge | An item budget of direct stats; Reach is a fixed property; reforge redistributes the budget (proposal) |
| Damage formula | D_base is the skill's Balance Profile value | Weapon damage × skill coefficient × Power bonus × the rest of the formula; the skill data's "base" becomes a coefficient |
| Power budget | Weapon power comes from item level (up to +10%) and grade (up to +5%), BiS about +15.5% | Mastery passives and the item stat budget add power sources that must fit the same ceiling (open) |
| Inscription floor | Never below Inscription 1 once reached (progression notes) | Can drop back to level 50 (leaning) |
| Action floor | 0.25 s between discrete actions (Vision); 0.5 s in earlier notes | Open; proposal per action type |

## Part 3. What agrees with the Vision

* Free aim with light aim assist; offensive projectiles don't home (the action target feeds the assist).  
* FriendlyLock for heals and buffs, now extended by the Ward.  
* Universal dodge with iframes and Evasion charges per role; Guard as one resource with forms per weapon.  
* Resolve T1/T2 for hard CC; grabs go through Resolve (Ping appendix proposal), now with skills able to grant Resolve.  
* Conditions with build-up and Tolerance, unchanged.  
* The interaction framework (condition → modifier → scope) carries both ArcheAge-style combos and Black Desert-style links; tags as a contract.  
* Same skill points for everyone, no limit on active skills, actives vs passives as the player's choice.  
* Base values with PvE and PvP variants (critical damage decided without a split).  
* Roles and the efficiency table; the Support passive where Finishers heal.  
* No weapon swap in combat; loadouts change only at the Altar reset (which now also clears mastery choices).  
* Requirement tags on skills and trees generated at cook time.  
* Armor: five pieces, iframe by weight, physical and magical pools with A ÷ (A + K).  
* Equipment: necklace, 2 rings, 2 earrings.  
* Latency rules: reactable windups of at least 350–400 ms, prediction, defender grace; the 0.5 s cast floor respects them.  
* No macros or automation; one player action per input.

## Part 4. Open checklist

* Controls: sprint end conditions; action floor value; ArcheAge-style bar mode; W+V and other extra combinations.  
* Targeting: build the Targeting Lab; dwell times, radius, fallback and cycle order.  
* Delivery: fill time of damaging areas.  
* Resolve: PvP uptime budget for skill-granted Resolve.  
* Skill structure: number of tiers, X, total skill points, whether tiers also open by level; which skills are morphable.  
* Focus: amounts from mastery passives; spell requirement scale.  
* Mastery: max level, scope (per loadout, per character or Lineage), passive pool contents, impact measure.  
* XP: parallel or split; conversion rates; mastery curve and endgame XP per hour.  
* Inscriptions: floor at 50 or at 1; cost per level.  
* Resources: stamina and mana numbers; basic attacks costing stamina on casters; shield stacking rules; armor weight lean.  
* Stats: crit chance cap; recovery cap after the recovery table exists.  
* Items: slot weights, exchange rates, negative rules, concentrated power on weapons, armor sets, cloak stats, family names, total power ceiling with mastery.  
* Basic kit: Bow Guard and alt; Dual Axes alt.  
* Exploration shop: keep for adventurer abilities only, or remove.

## Part 5. Gaps noticed while compiling

| Gap | Why it matters |
| :---- | :---- |
| Loadout signatures after moving extra weapon skills | The Vision's Sword + Shield signature is the riposte. If Riposte is a Discipline skill, the signature could become a base-kit Guard behavior ("a perfect Guard opens a counter") or something else |
| Shift+RMB movement rule | "Almost always a movement component", but several alts are bashes (shields, Staff, Instrument) or a barrier (Focus). Decide whether bashes get a step-in or stay as exceptions |
| Other resources | War's Fury and Occultism's life-paid skills need a place next to the new stamina/mana split |
| Mana for martial classes | Innate skills cost mana and appear on every loadout of a Discipline, so martial builds need a mana pool sized for them |
| Casters and stamina | If basic attacks cost stamina everywhere, casters manage two bars all the time; confirm that is wanted |
| Context kits | Mount, glider and wing skills have their own trees; how they map onto the board and keys isn't covered |
| Role kit placement | Taunt, Challenge, Unbreakable Guard and resurrection come from the role, outside the Discipline tree; they need cells on the board |
| Healing base for low-damage weapons | Heals start from the weapon damage, so loadouts with low base damage need healing coefficients tuned to match |
| Total power ceiling | Item level, grade, item budget, mastery stat passives and Inscription morphs all add power; the 10–20% BiS ceiling and the single number scale need one combined budget |
| Charged attacks without holds | The Bow's charged shots and the Greatsword's charged strikes were defined as holds; with press only they need a new form (fixed charge time, or a separate skill) |
