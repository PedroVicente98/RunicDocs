---
title: "RunicGame systems (Game)"
tags:
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-04"
---

RunicGame turns the Engine APIs into this game’s rules. Shared rules compile into both executables, so client prediction runs the same code as the server.

### Skills mapped to Engine APIs

| Skill component | Holds | Engine API used |
| :---- | :---- | :---- |
| Identity | ID, weapon, skill tree and slot, tags | Tags |
| Activation | Cost, cooldown, cast time, requirements | Ability toolkit |
| Timeline | Startup, active, recovery, cancel windows | Ability toolkit |
| Shape | Cone, circle, line, projectile; origin; range | Ability toolkit |
| Damage | Parts with domain, delivery and optional subtype or element | Attributes, rule pipeline |
| Effect | Conditions with build-up (Burn, Chill, Shock, Poison, Bleed, Curse, Madness, Acid) through Tolerance, Armor Break, buffs | Status container |
| Control | Stagger, Trip, Knockdown, Stun, Root through Resolve (T1 and T2); slows capped by the light-CC Resolve | Status container, rule pipeline |
| Movement | Dash, leap, root while casting | Movement |
| Defense | Guard or iframe granted by the skill | Damage interception |
| Threat and protection | Threat multiplier, Challenge | Threat table, damage interception |
| World utility | Light emitter, reveal | Light and perception |
| Hit timing | ServerTime or CappedRewind | Hit timing |
| Custom | Behavior ID and parameters | Behavior registries |
| Interactions | Condition → modifier rules | Rule pipeline |

* A damage type only selects defenses; effects and CC are always declared components.

* Weapon timing profiles (one per weapon; there are no versatile weapons) scale recovery.

* Role efficiency and per-component coefficients (PvE and PvP) are data tables reloadable at runtime. Every value has a base, and a skill, item or effect may declare its own PvE and/or PvP values (e.g., base 100, PvP 85, PvE 105); the rule pipeline’s per-hit context picks the variant. Proposal: the context is decided by the target of each hit.

$${D}_{final}={D}_{base}\times \prod\limits_{c\in C}^{}{k}_{c}\times {E}_{role}\times \left({1-min\left({{R}_{max},\,\sum\limits_{c\in C}^{}{r}_{c}}\right)}\right)$$

### Resolver

The resolver is RunicGame’s configuration of the Engine rule pipeline: two stages and a fixed order.

| Stage | Reads | May change |
| :---- | :---- | :---- |
| Activation | Caster state, previous skill and its window, resources, position | Cost, cast time, variant |
| Hit | Target state and position | Control swap, added effects, values |

* Order inside each stage: component swaps, then additions, then value changes (summed per category, capped), then defenses. Identical effects from the role passive and the Discipline do not stack: the stronger applies (provisional; confirm with the skill trees).

* Rules come from five sources — the skill and the choices in its tree, the role passive of the named class, item effects (including extracted ones), the mount, glider or wing modifications of the context kit, and the class signature. They compile into one resolved loadout per character, rebuilt only when equipment, class, tree choices or the context (on foot, mounted, gliding, winged) change, so no hit searches for rules.

* Hit timing is chosen per skill: ServerTime by default, CappedRewind (e.g., ≤ 100 ms) only on skills flagged after playtests. Full rewind is not offered.

### Custom behaviors

```cpp
// Illustrative contract, not a frozen API.
struct BleedJumpParams { float jump_radius_m; uint8_t max_jumps; };

class BleedJump final : public SkillBehavior<BleedJumpParams> {
public:
    HookMask Hooks() const override { return Hook::OnKill; }

    void OnKill(const KillContext& ctx, const BleedJumpParams& p,
                BehaviorOutput& out) const override {
        auto next = ctx.Spatial().NearestEnemies(ctx.VictimPosition(),
                                                 p.jump_radius_m, p.max_jumps);
        for (EntityRef target : next)
            out.ApplyStatus(target, "game:bleed", ctx.SourceStatus());
    }
};

void RegisterGameBehaviors(BehaviorRegistry& registry) {
    registry.RegisterSkill<BleedJump>("game:bleed_jump");
}
```

```yaml
custom:
  id: game:bleed_jump
  params: { jump_radius_m: 8, max_jumps: 2 }
effects:
  - bleed: { buildup_pct: 40 }   # the standard component stays
```

A custom behavior never replaces standard components, so defenses, coefficients, caps and item effects keep working on it.

### Defense and threat

| Game system | Holds | Built on |
| :---- | :---- | :---- |
| Evasion | Charges by the class’s role, dodge form by Discipline, iframe length by armor, minimum recovery | Resource pools, invulnerability windows |
| Guard | One resource; modes Free (shield arc), Timed (the Quarterstaff), DuringMovement (greatsword dash, spear run), Filtered (mage, by damage domain and delivery) | Damage interception |
| Resolve | CC immunity buff: full CC, then Resolve T1 (about 2 s; a CC during it drops one level), then Resolve T2 (about 2 s, immune to every CC); slows last at most about 10 s, then about 5 s of slow immunity. Tolerance, per condition: after about 10 s active, or at once on a peak, about 5 s with no added time or build-up | Status container |
| Threat and taunt | Threat values per action; spatial taunt | Threat table |
| Challenge | PvP protection: a share of damage redirected to the Tank, non-stacking | Damage interception |

### Items, progression and inventory

* ItemDefinition (type, slot, base stats, weapon kit) and ItemInstance (item level, grade, secondary stats, unique effects, durability) are game data on the Engine item runtime; the Platform item ledger is their durable owner. Unique effects can add or swap tags on a skill, change its element, add an effect or add a skill; they come from PvE and may also come from PvP. An effect can be extracted, destroying the source item, into a tradeable item that fits one socket per weapon (Proposal: called a Rune); extraction is one ledger operation in the economy service.

* Grades are a data table (bonus, chance, guarantee, visual); adding or removing a grade needs no code.

* Upgrades, rerolls and grade attempts run in the Go economy game service with operation IDs; RNG and guarantee counters live there, never on the client. The simulation receives the new item and rebuilds the resolved loadout.

* Inventory is slots only, no weight. Expansions raise container capacity through a ledger operation paid in game currency.

* Trade packs are world entities carried on the back or in vehicles (CarriedBy, CargoOf), not inventory items. Vehicles hold them in dedicated cargo slots. They drop where the carrier dies or where the vehicle is destroyed or unsummoned, and can then be stolen. They forbid flying and gliding (a movement restriction) and allow only slow walking; carrying them needs vehicles or specialized mounts, one pack per mount.

### Quests, dialogue and world interactions

* Quests are made with the Engine’s quest-creation API: definitions are data (states, objectives, triggers, conditions, actions), and Game-only triggers, conditions and actions are C++ registered under game:. The quest runtime runs inside the simulation, so a kill or an interaction advances a quest in the same tick.

* The Go Quest service stores progress, deduplicates quest facts by their stable IDs and commits rewards; the simulation never waits for it.

* Dialogue graphs are data whose conditions read quest and character state. Scripted scenes (escorts, boss phases, cutscenes) run on GameplayFlow.

* Physical interactions (levers, escorts, gathering, rituals, the cartography table) are C++ behaviors registered on the Engine interaction framework.

* Flow: client intent, then the simulation checks reach, state and permissions, executes and emits a fact; the quest runtime advances the quest in the same tick; the fact travels with its stable ID to the Quest service, which stores progress idempotently and commits rewards; the accepted result returns at a later safe tick.

### Map knowledge, altars, factions and progression

* **Map knowledge:** one bit per explored cell per Lineage, shared by its characters — about 150,000 surface cells (≈ 18 KB before compression) per 600 km² map at 64 m cells; underground and floating-island cells add their own bits, so the map can show them separately. The simulation marks cells on the cell changes it already detects and sends batched updates to the character service; reading a chart unlocks its node layer for the Lineage and consumes it ([[RunicGame — Appendix Nodes, Economy and Exploration|RunicGame — Appendix: Nodes, Economy and Exploration]]).

* **Altars:** world entities in the spatial index; the Altars a character has discovered are durable character state. Death respawns the character at the nearest Altar that character has discovered, in the world where it died, and choosing or resetting the loadout and the Discipline, which redistributes the skill points, is an altar interaction that rebuilds the resolved loadout. The Lineage sees on the map every Altar its characters found, but respawn and teleports use only the character's own discovered Altars, so each character rediscovers them. Settlement Altars are teleport destinations once the character has visited them, for a fixed fee plus distance, much more between continents, and no cargo fee; from the field a teleport also uses a consumable and has a long cooldown, and from one Altar to another it costs only the fee (RunicGame — Appendix: Nodes, Economy and Exploration).

* **Factions:** faction, crime and pirate status are durable state mirrored in the simulation; PvP eligibility and group rules (pirates may group with both factions) are game data.

* **Named classes:** one of ten fixed loadouts plus one of five Disciplines is a named class with exactly one role (Damage, Tank or Support); class and role are derived, never chosen. Weapon skills are the basic kit, unlocked by level with no point cost, with some level choices; skill points go only into the Discipline skills, in one merged tree per class. Combat skill points come only from levels, every max-level character has the same total, and a character has at most 28 combat skills, weapon and Discipline together; emotes, the context kit and other auxiliary skills are separate categories ([[Weapon Class System#Skills, trees and points]]). There are no versatile weapons and no weapon-type swap: changing the loadout or the Discipline is an Altar reset that redistributes the points and the level choices.

* **Context kits:** mounted, gliding or winged characters use only their context kit, from per-class mount and aerial trees with their own points (in definition). The mount, glider or wing can modify the kit, and a mount’s kit is the same on the ground and in the air.

* **Mounts, gliders and wings:** the glider only glides; the wing is equipment that glides and flies in flight zones; mounts carry glide and flight as separate capabilities; other vehicles are summoned by scroll.

* **Exploration XP:** a separate durable counter in the Character service, earned from discoveries the simulation reports and spent in an exploration shop on adventurer abilities (for example moving objects, traversal) or resources, never on combat skills or cosmetics.

* **Professions:** 23 professions based on ArcheAge's list level with practice; Cartography includes nautical charts and exploration, and Larceny includes opening coin purses (RunicGame — Appendix: Nodes, Economy and Exploration). Language proficiency gates communication with the other faction; Proposal: it is required to change faction.

* **Castles:** only on the neutral continent, one per region, built by the ruling guild in one of the region’s designated zones (authored volumes), fixed once placed; a castle is an indivisible volume. On the faction continents the ruling guild uses the city and an exclusive guild building (RunicGame — Appendix: Nodes, Economy and Exploration).

### Land hazards

* Land hazards follow the same rule: the simplest server model and a client spectacle ([[RunicGame — Ideias]], [[HAZARD-01 Environmental Hazards|HAZARD-01]]), with effects that go through Resolve and Tolerance unless flagged.

* Verticality is terrain from the elevation layer. Mounts have a slope limit in their movement profile, falls use fall damage, and some places are reached only by gliding down or with climbing gear.

* Inland weather reuses the WeatherState: blizzards and sandstorms lower visibility and apply build-up (Chill) or damage to exposed characters; lightning on high ground uses the same highest-point query as at sea.

* Snow is a level per snowfield region (none, light, heavy or deep) in the replicated WeatherState: it rises while it snows, and a timer drops it one level at a time while it isn't snowing. Each level maps to a movement modifier through the region's hazard volumes: light is only visual, heavy slows, and deep slows more, blocks sprinting and keeps some mounts out. Drift-zone volumes at the bottom of slopes count one level deeper. Snow cover and footprints are client-only. Cost: about one byte per snowfield region, sent only when its level changes.

* Avalanches are weather events on the slide paths from terrain hydrology (below), possible only while the slope's snow is heavy or deep, and never something players set off easily. Each path has a start, an end and the area where the snow lands, and hand-placed markers only add, remove or adjust paths ([[RunicGame — Appendix Content Pipeline and Art Direction|RunicGame — Appendix: Content Pipeline and Art Direction]], Map authoring markers). The server moves one hazard volume from the start to the end, which knocks characters down through Resolve and damages them, then makes the landing area deep snow for a while; the falling snow is a client effect. Cost: one hazard entity for a few seconds.

* Rain and ground levels: the WeatherState's precipitation maps to a rain level (none, drizzle, heavy, monsoon). Each region also has a ground level (dry, damp, mud, soaked) that rises one level after a set time under rain at least that strong and drops one level per timer while the rain is lighter, with a drying rate per biome. Both are one byte per region in the replicated weather state, sent only when they change (RunicGame — Ideias, [[HAZARD-01 Environmental Hazards|HAZARD-01]]).

* Mud and wet ground need no new data: the terrain type under a character, the ground normal its CharacterVirtual already has and the region's ground level pick a movement modifier (mud slows; soaked slows more and blocks sprinting). Rock, sand and paved road cells never turn to mud, and traversal gear scales the modifier.

* Sliding is a movement mode. On wet ground or ice, the slip chance per second is a smooth curve of the slope angle between a start angle and a full angle, both set by the surface, the ground level and the gear, and scaled by movement speed. The roll is a hash of the character ID and the tick: a number that looks random but is the same on every machine, so the owning client predicts the same slip as the server with nothing sent. A second hash (same inputs, another salt) picks the outcome, weighted by the angle so the tiers fade into each other: a stumble (a short speed loss), prone with no slide, or prone and sliding. A slide accelerates down the slope at g·(sin θ − μ·cos θ), with μ from the surface, the ground level and the gear, so it only starts where the slope beats the grip, and the character enters climbing mode, where holding on grips with the same curve. A slip is a movement state, not a CC, so it ignores Resolve and Tolerance. Mounts use the same tiers with their own angles: a stumble slows the mount, prone keeps the rider on, and a slide throws the rider off; the mount then slides prone to the end of the slide path and stays there, keeping its health and its trade pack, until it is unsummoned and summoned again (RunicGame — Ideias, [[HAZARD-01 Environmental Hazards|HAZARD-01]]). Climbing on wet rock rolls the same way. Cost: a few nanoseconds per character per tick, only on slippery ground.

* Terrain hydrology is a Cooker step on the elevation layer: flow direction per terrain cell (toward its lowest neighbor); flow accumulation, whose high cells are the channels (authored rivers plus dry gullies, canyons and dry beds); for each cell, its height above the channel it drains into (HAND, Height Above Nearest Drainage) and that channel stretch; low spots with no outlet and the height where each overflows; and slide paths, cells within a release-angle range (about 30–45° for snow) followed downhill to where the slope flattens, each with a start, a path and a landing area. The RunicEditor shows the flood at monsoon and the slide paths; a painted exclusion mask and hand-placed markers remove, add or adjust results.

* Floods: each channel stretch (a few hundred meters) has a stage, the water height above its bed. The stage is a pure function of the ground levels of the regions that drain into it, with weights from the cook, so clients compute it themselves and nothing per stretch is replicated. A cell is under water when its height above the channel is below the stage, and its depth is the difference: authored rivers rise with the stage and spill onto low bank cells, canyons flood deep and narrow, flat valleys wide and shallow, and dry channels and low spots fill too, low spots up to their overflow height. The current runs along the channel, strong in the channel and weak on the flooded plain, and grows with the stage.

* The WaterSystem gets a flood layer: when no water body answers TrySample, it compares the cell's height above the channel with the stage, so swimming, breath, buoyancy and drifting work unchanged on flooded ground.

* Flash floods are events on one drainage path, dry beds included: an Environment override (route, start time, peak height, front speed, rise, hold, fall and flow multiplier; about 32 bytes, sent once) adds a front that travels down the path, offset(s, t) \= H · f(t − start − s / v), where s is the distance along the path and f rises from 0 to 1, holds and falls. The client plays a rumble and dust a few seconds before the front reaches a point.

* Slides: each generated path rolls about once a minute, with a hidden seed, while its region's snow is heavy or deep (avalanche) or its ground is soaked (mudslide); a slide is the moving hazard volume described above, and its landing area becomes deep snow or mud for a while.

* Roads: paved road cells never turn to mud and are less slippery; the Cooker raises roads over cells that flood or bridges the channels, and its validation warns when a road would flood in a monsoon.

* Client: a flood water mesh over the visible floodable tiles, whose vertex shader reads the cooked height-above-channel texture and a buffer of stages and hides dry spots; mud is a terrain shader blend driven by the ground level.

* Flood and slide cost (estimates): cooking takes seconds to about a minute for the map and can be redone per region; the height above the channel and the stretch ID are stored only for cells that can flood, about 8 to 16 MB for the 600 km² map, streamed by cell; slide paths take about 100 bytes each (2,000 paths, about 200 KB); the network carries one byte per region level change and about 32 bytes per event; stages are recomputed only when a ground level changes; flood checks run only on floodable cells during a flood, so 500 characters at 30 Hz are about 15,000 checks per second, about 1.5 ms of CPU per second (around 0.15% of a core); slide rolls are about 30 per second.

* Earthquakes never change terrain. A cave entrance is a placed object with a closed and an open model; an earthquake flips its world-state flag for a while and spawns rockfall hazard areas. Screen shake and dust are client effects.

* Volcanoes: an eruption is client effects plus hazard zones that hit random spots with fire damage and leave damaging ground for a while; ash clouds are fog volumes and lava flows follow authored channels. When it ends, the Game sets the nearby ore richness and spawn script to their maximum.

* Swamps are hazard volumes that slow, with gas pockets that apply Poison build-up; magnetic anomalies are volumes whose tag the client compass reads to spin.

* New islands and new terrain come only with patches; nothing is generated at runtime.

* Cost: the same as at sea. Cooked terrain and volumes cost nothing at rest, and an event is one override fact, a flag flip or a few hazard entities.

* Acceptance: an earthquake opens a cave entrance for a while and closes it again, at the same world time in two simulations. In a monsoon, the same cells flood in two simulations and their clients with no flood marker placed, and a flash flood front reaches a given point at the same world time; on wet ground, a character slips more often as the slope gets steeper, with no step at any single angle, and its client predicts the same slip as the server.
