---
title: "Part 1. Locked: ping resolution"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Ping Resolution"
source_url: "https://docs.google.com/document/d/1iYe10T523upQnBfv91Pk3dL1FC6TuyF7hmdGg6ZG5Ys/edit"
section: "Part 1. Locked: ping resolution"
created: "2026-10-21"
modified: "2026-10-21"
---


## The common timeline

* **Clock sync** (already decided as ServerTime): the client keeps an estimate of the server's current tick from ping samples. Techniques 2, 3, 5 and 6 depend on it.
* **Your own character** is predicted slightly ahead of the server, about half a round trip, so inputs reach the server in time for their tick.
* **Remote entities** are drawn slightly behind: the client renders them at the server's time minus an interpolation delay, so it always has two snapshots to blend.
* Without help, a remote action reaches your screen late by half the round trip plus the interpolation delay (about 70 ms), and your reaction needs another half round trip to reach the server.

## Locked techniques

| # | Technique | What it does | Lab | Owner |
| :---- | :---- | :---- | :---- | :---- |
| 1 | Prediction for own actions | Moves and attacks start the instant you press; the server confirms later | 1 | Engine, using the shared RunicGame code |
| 2 | Telegraph fast-forward | The impact you see happens when the server applies it | 2 | Engine; Game sets per-skill limits |
| 3 | Defender grace, all defense, 150 ms cap | Hits on players are judged against what the defender saw: dodge, [[Defense Evasion Guard and armor#Guard\|Guard]] and its facing, and position | 2, 5 | Engine; Game marks defensive states |
| 4 | Predicted impact effects | Spark, sound and visual hitstop play when your blade connects on your screen | 3 | Engine hooks; Game content |
| 5 | Capped rewind | The server checks targets where the attacker saw them: up to 200 ms against mobs, 100 ms against players | 4 | Engine; Game sets caps |
| 6 | Remote projectiles at their real position | Projectiles are drawn where the server has them | 5 | Engine; Game projectile data |
| 7 | Adaptive interpolation delay | Remote entities are drawn only as far behind as each connection's jitter needs | 6 | Engine |
| 8 | Input redundancy, 3 ticks | Each input packet repeats the last 3 ticks, so a lost packet costs nothing | 7 | Engine; Game flags time-critical commands |
| 9 | Combat facts first | Survival-critical facts travel on their own top-priority lane and fill the bandwidth budget first | 8 | Engine, Platform transport lanes, Game priorities |
| 10 | Relay routing | Players enter a provider network nearby and ride its backbone to the datacenter | 9 | Platform (provider to be chosen) |

## 1. Prediction for own actions

* **Problem:** waiting for the server to start or chain an action adds a full round trip to every press. This was TERA's main weakness.
* **Logic:** the client runs the same shared code as the server for its own movement, skill timelines and nearby collision. The server returns authoritative state with the last input it processed, and the client replays the inputs after it. Small errors blend; large ones snap.
* **Gameplay:** own actions are instant at any ping; corrections appear only when the server disagrees.
* **Owner:** Engine, with RunicGame::Shared. Already in the architecture.

## 2. Telegraph fast-forward

* **Problem:** a remote attack that starts at server tick S reaches the client late. Played from frame 0, its impact appears 75 to 145 ms after the real one at 150 ms ping.
* **Network:** the attack-start fact carries S (likely already present for ServerTime hits; otherwise 2 to 3 bytes).
* **Logic:** the client computes how much of the attack has already elapsed and starts the animation that far in. Authored skill movement (lunges) plays from the same point and blends back into interpolation. Two limits per skill: a maximum skip (example 150 ms) and a minimum visible windup (example 200 ms).
* **Gameplay:** a 500 ms telegraph means 500 ms for everyone. High-ping players see the start of the windup shortened; a mob can jump forward slightly when an attack starts.
* **Cost:** a few bytes per attack; trivial client math.

## 3. Defender grace (all defense)

* **Rule:** for hits on players, the server evaluates the defender's state as of the moment that player saw the hit, at most 150 ms after the server's hit time. The state includes invulnerability from dodges, Guard and its facing, and position, so it covers melee, ranged, projectiles and ground areas alike.
* **Logic (deferred commit):** a dodgeable hit on a player is computed at its tick and held for that player's measured one-way latency plus a 20 ms margin, capped at 150 ms. Inputs that arrive in the window and were made before the hit, as seen by the defender, are applied to the defender's state at that moment. Then the hit commits. Rollback is not used: undoing procs, deaths and CC chains would be far worse.
* **Validation:** each input carries the server time the client was displaying. Stamps must increase, cannot be earlier than the player's measured latency allows, and the cap bounds lag-switch abuse.
* **Gameplay:** "If I saw myself dodge or step out in time, I did." Damage on players commits up to 150 ms later on the server; healers see health drop slightly later. Moving into a hit late also counts, so the rule is symmetric. Damage over time and undodgeable effects commit immediately.
* **Cost:** per player, about 5 ticks of defensive state (about 20 bytes) and a short list of pending hits (usually 0 to 3, about 32 bytes each).

## 4. Predicted impact effects

* **Logic:** during the active ticks of your own attack, the client runs the shared hit test against what it displays. On a hit it plays the spark, sound, camera shake, visual hitstop and optionally the mob's flinch. Damage numbers, health bars, CC and kills wait for the server. A rejected hit leaves only a spark that already played.
* **Hitstop is visual only:** the client freezes animation and camera; the gameplay timeline on the server never pauses, so a rejected prediction cannot desync a combo.
* **Gameplay:** hits feel instant; rare ghost sparks. Deaths are never predicted.
* **Cost:** a handful of hit tests per own swing on the client; no bandwidth.

## 5. Capped rewind

* **Problem:** the attacker aims at where the target was 75 to 145 ms ago; tested against its current position, a hit on a moving target misses.
* **Network:** each input carries the server time the client was displaying (2 bytes), the same field used by technique 3.
* **Logic:** the server keeps each character's transforms for the last 200 ms and tests the hurt capsules at the transforms from what the attacker saw, up to the cap: 200 ms against mobs, 100 ms against players. Position comes from the rewound time; defensive state comes from technique 3. Ties go to the defender.
* **Gameplay:** melee on moving targets feels right. In PvP a target can be hit after stepping away by up to about 0.6 m at running speed. Positional checks (back attacks, Tank direction, boss facing) use the rewound facing too. Above the cap, attackers lead their targets.
* **Cost:** about 200 bytes of history per character, about 400 KB for 2,000 characters in one simulation.

## 6. Remote projectiles at their real position

* **Network:** one spawn fact per projectile (origin, direction, speed, inherited ship velocity, start tick), about 25 to 35 bytes once, instead of 600 to 900 bytes of per-tick updates over a 2 s flight. A hit or expired fact closes it.
* **Logic:** projectiles are deterministic paths, so the client evaluates the path at its server-time estimate. Client collision with the world is cosmetic only.
* **Gameplay:** with technique 3, stepping out of a projectile's line works as it looks. The projectile appears slightly ahead of the caster's hand; a short trail hides it.
* **Cost:** saves bandwidth overall.

## 7. Adaptive interpolation delay

* **Logic:** the client measures how irregularly snapshots arrive (rolling 95th percentile) and sets its render delay to one snapshot interval plus that margin, between 40 and 150 ms, changing it gradually by playing back up to 5% faster or slower. Typical result at 30 Hz: 45 to 60 ms on cable, 100 to 130 ms on poor Wi-Fi.
* **Gameplay:** stable connections see the world less in the past; no rule changes.
* **Cost:** none on the server.

## 8. Input redundancy

* **Logic:** each input packet repeats the last 3 ticks, delta-encoded; the server applies each tick exactly once. Time-critical commands ride this stream: dodge, Guard, skill starts. Commands that are not time-critical stay reliable: trade, NPC interactions, menus.
* **Gameplay:** at 1 to 2% loss, inputs are almost never lost; without redundancy a lost dodge is resent a round trip later.
* **Cost:** upstream goes from about 1.56 to 2.04 KB/s per player, mostly packet headers.

## 9. Combat facts first

* **Problem:** in big fights, attack warnings can queue behind positions and cosmetics, and on a single ordered reliable stream a lost packet holds everything behind it until it is resent.
* **Network:** [[Networking stack sessions and responsiveness#Stack (decided)|GameNetworkingSockets]] lanes: lower-priority lanes are processed only when higher ones are empty, lanes of equal priority share bandwidth by weight, and ordering holds only within a lane. Survival-critical facts get the top lane and must stay small so they cannot starve the rest.
* **Logic:** each tick, the per-player budget fills in order: facts about your survival, nearby hostile transforms, other facts, far transforms and cosmetics. Waiting messages age upward.
* **Gameplay:** in the lab, one ordered stream in a big fight or with 2 to 5% loss delays warnings by 100 to 300 ms; lanes bring that close to zero.
* **Cost:** a per-player sort each tick; no extra bandwidth.

## 10. Relay routing

* **Logic:** players connect to a provider network near them and travel its backbone to the datacenter, avoiding congested public routes.
* **Correction:** Valve's relay network works with GameNetworkingSockets but requires Steamworks. Outside Steam, the options are an anycast accelerator or own relay points.
* **Cost example (AWS Global Accelerator):** US\$0.025 per hour per accelerator plus US\$0.007 to 0.105 per GB in the dominant direction. At about 100 MB per player-hour and US\$0.035 per GB, 1,000 concurrent players add about US\$3.50 per hour, roughly US\$2,500 per month.
* **Open:** provider, and whether to enable it everywhere or only for distant regions.

## Dependencies and resolution order

* Clock sync comes first; techniques 2, 3, 5 and 6 depend on it.
* Techniques 4 and 5 ship together: rewind is what makes predicted impacts agree with the server.
* Technique 7 makes the corrections of 2, 3 and 5 smaller.
* Player against player: positions from the attacker's rewound view (at most 100 ms), defensive state from the defender's grace (at most 150 ms); ties go to the defender.

## Reaction window by ping

Time from first seeing an attack to the latest press that still dodges, with 70 ms interpolation. "With helpers" means fast-forward plus defender grace. Most people need about 200 to 250 ms to react to a cue they are watching for.

| Ping | 300 ms windup | 300 ms, with helpers | 500 ms windup | 500 ms, with helpers |
| :---- | :---- | :---- | :---- | :---- |
| 0 ms | 230 ms | 300 ms | 430 ms | 500 ms |
| 50 ms | 180 ms | 275 ms | 380 ms | 475 ms |
| 100 ms | 130 ms | 250 ms | 330 ms | 450 ms |
| 150 ms | 80 ms | 225 ms | 280 ms | 425 ms |
| 200 ms | 30 ms | 200 ms | 230 ms | 400 ms |
| 250 ms | 0 ms | 175 ms | 180 ms | 375 ms |

## Gameplay consequences to keep in mind

* Rewind and positional mechanics: a victim occasionally feels they had already turned. The 100 ms PvP cap is the dial.
* Defender grace: damage on players commits up to 150 ms late.
* Fast-forward: high-ping players see shortened windups. The minimum visible windup is the dial.
* Hard blocking of enemies: predicted collision against slightly old enemy positions causes small corrections.

## Ownership

| Technique | Engine | Platform | Game |
| :---- | :---- | :---- | :---- |
| Clock sync | Network | — | — |
| 1. Prediction | Prediction and reconciliation | — | Shared rules code |
| 2. Telegraph fast-forward | Start tick in facts, playback offset | — | Max skip, min windup per skill |
| 3. Defender grace | Input stamps and validation, deferred commit, defensive history | — | Defensive states, cap |
| 4. Predicted impact effects | Client hit query, cosmetic events | — | Effect content |
| 5. Capped rewind | Past-transform test | — | Caps per relationship |
| 6. Projectiles at real position | Spawn facts, client presenter | — | Projectile data |
| 7. Adaptive interpolation | Client replication | — | — |
| 8. Input redundancy | Input encoding, deduplication | — | Time-critical command flags |
| 9. Combat facts first | Priorities, budget | Transport lanes | Priority per fact type |
| 10. Relay routing | — | Transport, infrastructure | — |

---

↑ [[Ping Resolution|Ping Resolution]] · [[Part 2 Combat discussion of 21 October for decision|Part 2. Combat discussion of 21 October, for decision]] →  
Source: [RunicGame — Appendix: Ping Resolution](https://docs.google.com/document/d/1iYe10T523upQnBfv91Pk3dL1FC6TuyF7hmdGg6ZG5Ys/edit) › Part 1. Locked: ping resolution · exported 2026-11-03
