---
title: "Part 2. Combat discussion of 21 October, for decision"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Ping Resolution"
source_url: "https://docs.google.com/document/d/1iYe10T523upQnBfv91Pk3dL1FC6TuyF7hmdGg6ZG5Ys/edit"
section: "Part 2. Combat discussion of 21 October, for decision"
created: "2026-10-21"
modified: "2026-10-21"
---


## Lessons from Vindictus and TERA

* **Vindictus combat:** light attacks (normals) chain into heavy finishers (smashes); [[Stamina and climbing#Stamina|stamina]] pays for offense and defense; hitboxes closely follow the attack animations; targeted attacks break boss parts, which can change behavior and drops.
* **Vindictus environment:** built on Source physics. Columns topple and become clubs, debris can be thrown, spears pin enemies to walls, enemies can be grabbed and dragged, and burning debris gathered into a campfire heals the party. Physics was optional: always usable, not always the best choice.
* **Vindictus network:** never documented by the developer. Players describe dungeons as peer-to-peer with one player hosting: the host plays with no lag, everyone else depends on the host's upload, and non-hosts must dodge earlier at low connection bars. It felt good mostly because players were geographically close.
* **TERA:** server-authoritative, but the client waited on the server for too much, including chaining skills and boss attack timing; the community built proxy mods to align boss attacks with the server.
* **Lesson:** never make a player wait a round trip to start or chain an action, and never judge a dodge against a picture the player did not see. Both are covered by the locked techniques.

## Animation lock and canceling

* **Decision:** no animation lock. Players can cancel their own attacks; the cooldown still applies.
* **Proposal:** cancel at any time during the windup, at least into dodge or [[Defense Evasion Guard and armor#Guard|Guard]]. A canceled skill goes on cooldown. A canceled basic attack costs a short recovery (100 to 150 ms) unless canceled into dodge or Guard.
* **Consequence:** PvP feints exist (start a heavy, bait a dodge, cancel); the cost keeps them from being free. Observers see a canceled windup continue for their one-way delay, then stop.
* Long windups apply only to attacks meant to be reacted to (boss attacks, heavy hits, hard CC). Light attacks stay fast (Sword light 200 ms, Dagger 133 ms), and own attacks start instantly through prediction, so combat is not sluggish for the attacker.

## What the numbers feel like

* **300 ms** is 9 ticks or 18 frames at 60 fps, close to human reaction time for a cue you are watching for. Fighting-game players generally treat about 20 frames (330 ms) as reactable and under about 15 frames (250 ms) as guessing.
* **150 ms** of delay on your own actions is clearly mushy (Lab 1 with prediction off). The same delay on other players' actions is subtle and shows up as "I dodged too late", which the locked techniques remove.

| Moment | 100 ms ping | 200 ms ping |
| :---- | :---- | :---- |
| Own moves and attacks | Instant | Instant |
| Dodge window, 300 ms windup, with helpers | About 250 ms, hard but fair | About 200 ms, hard |
| Dodge window, 500 ms windup, with helpers | About 450 ms | About 400 ms |
| Hitting a moving player (100 ms rewind cap) | Fully compensated | Lead the target by about 70 ms (0.4 m) |
| Being knocked back or CC'd | Small correction after about 50 ms | Noticeable snap after about 100 ms |
| Spark and sound on own hits | Instant | Instant |
| Damage numbers | +100 ms | +200 ms |

## Design rules for latency (proposal)

* Attacks meant to be reacted to have windups of at least 350 to 400 ms.
* Parry and perfect-Guard windows are at least 150 to 200 ms and favor the defender.
* No instant hard CC in PvP; no "react to the reaction" exchanges under about 200 ms.
* Telegraph decals fill up exactly at the server's impact tick.
* Knockbacks in PvP stay modest, since being knocked back always corrects the predicted position.
* Optional: a [[Cooker|Cooker]] validator that warns when a skill tagged as reactable has too short a windup.

## Hit detection with Jolt

**Decision:** CharacterVirtual is the only character object, and hurt shapes are generous capsules.

| Role | [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] object | Notes |
| :---- | :---- | :---- |
| Movement and collision | CharacterVirtual with a tight movement capsule (example 0.30 m radius) | No inner rigid body, so characters never enter Jolt's broadphase |
| Hurt shape, players and normal mobs | A separate generous capsule shape (example 0.42 m), tested at the character's transform | Shared from the shape registry, one capsule per size class |
| Hurt shapes, large mobs and bosses | Several capsule or sphere shapes placed from tracks baked from the animations at cook time | The server never runs a skeleton (proposal) |
| Melee attack volume | A shape in CollideShape, swept along the weapon path during the active ticks | Already in the architecture |
| Projectile | A shape in CastShape, one cast per tick segment | Already in the architecture |
| Rewind | The character's transforms from the last 200 ms | About 180 to 200 bytes per character |

* Candidates still come from the Runic cell grid; Jolt only answers whether two shapes touch.
* Two capsules on purpose: the tight one keeps blocking from feeling sticky, the generous one keeps hits forgiving.
* Cost: capsule against capsule about 0.1 to 0.5 µs; capsule against a swept convex shape about 1 to 3 µs.
* **Vocabulary:** "hard" and "soft" hitboxes mean either precision (shapes that follow bones and the weapon path, versus simple generous shapes) or collision (bodies that block, versus bodies that push or pass through). A hitbox deals damage; a hurtbox receives it.
* **Open:** boss part breaks and weak points, enabled by baked part tracks, are not yet in [[Vision|the Vision]].

## Collision between characters

| Pair | Movement | Hostile hits |
| :---- | :---- | :---- |
| Hostile (enemy faction, pirate, active [[Factions PvP and crime#Outlaw and Infamy\|Outlaw]], hostile mob) | Hard: solid contact | Yes |
| Ally (same faction, party, mob with mob) | Soft push | No |
| PvE player with anyone | Soft push, treated as an ally | No |

* **Decision:** enemies hard-block, allies soft-push, and PvE players are treated as allies: no hard block between players and no hits.
* **Implementation:** a custom character-against-character interface returns only hostile characters to Jolt's movement solver. Soft push is a small Runic system: allies overlapping within about 1 m get a separation velocity of up to 1 to 1.5 m/s (proposal). The rule follows the live relationship, so Outlaw changes it at once.
* **Lock (proposal):** soft push never moves anyone off a walkable edge or off a ship's deck.
* **Latency:** hard blocking against a remote enemy is predicted against a slightly old position; the tight movement capsule keeps corrections small. If playtests show sticking, extrapolate the enemy's position for the collision test only.

## Vindictus-style environment in an open world (proposal)

* **Breakables:** the server sends one event; flying debris is client-only cosmetics, and the server keeps only gameplay chunks.
* **Carried props:** chunks and spears are world entities you carry, like [[Trade packs and routes|trade packs]]; throwing uses the projectile path, not free physics.
* **Grab:** a CC status that attaches the target to the grabber; in PvP it goes through [[Combat#Resolve hard and light CC|Resolve]], on mobs it depends on size class.
* **Big moments** (falling pillar, rolling log, battering ram): authored kinematic motion.
* **Persistence:** broken props regrow on a timer.
* **War budget:** cap gameplay physics bodies per cell and degrade them first. One freely moving body costs about 300 to 500 bytes/s per viewer, so 50 in view would cost 15 to 25 KB/s per player.

## Cosmetic items and effects

* **Decision:** when an entity enters a player's interest set, its spawn message carries its equipped appearance IDs (about 20 to 60 bytes). Changes go out as appearance-changed events to everyone who has that entity in interest. The interest set is the [[Business model launch visuals and audio#Subscription|subscription]].
* **Decision:** effects are never sent. The server sends facts such as "skill started at tick S" and "hit landed"; each client picks the visual and sound effects from the skill ID and the caster's equipped cosmetics.

## Open

* Basic-attack cancel recovery value, and exactly which actions cancel into what.
* Adoption of the design rules for latency.
* Soft push numbers.
* Boss part breaks and weak points.
* Relay provider and where to enable it.

## Sources

* [Vindictus, Wikipedia](https://en.wikipedia.org/wiki/Vindictus)
* [Curb-stomping baddies in Vindictus, PC Gamer](https://pcgamer.com/curb-stomping-baddies-in-vindictus)
* [Vindictus review, MMOs.com](https://mmos.com/review/Vindictus)
* [Vindictus connection thread, GameFAQs](https://gamefaqs.gamespot.com/boards/991388-vindictus/62998037)
* [Raid lag thread, Vindictus forums](https://forums.vindictus.nexon.net/discussion/13438/if-they-ever-make-the-raids-more-lag-friendly)
* [Connection bars thread, Vindictus forums](https://forums.vindictus.nexon.net/discussion/14182/connection-bars-lag)
* [TERA proxy modules by Kasea, GitHub](https://github.com/Kasea)
* [Networking sockets lanes, GodotSteam docs](https://godotsteam.com/classes/networking_sockets/)
* [AWS Global Accelerator pricing](https://aws.amazon.com/global-accelerator/pricing)

---

↑ [[Ping Resolution|Ping Resolution]] · ← [[Part 1 Locked ping resolution|Part 1. Locked: ping resolution]]  
Source: [RunicGame — Appendix: Ping Resolution](https://docs.google.com/document/d/1iYe10T523upQnBfv91Pk3dL1FC6TuyF7hmdGg6ZG5Ys/edit) › Part 2. Combat discussion of 21 October, for decision · exported 2026-11-03
