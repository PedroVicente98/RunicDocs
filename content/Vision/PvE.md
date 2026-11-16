---
title: "PvE"
tags:
  - "vision"
  - "appendix/design-compile"
source: "RunicGame — Complete MMORPG Vision"
source_url: "https://docs.google.com/document/d/1BgyjnLHmloU-AswLXJO2lkD7R-jxIFSedYrKTsCNnqk/edit"
created: "2026-10-13"
modified: "2026-11-16"
---

PvE is a pillar, not an add-on: each dungeon and raid has exclusive materials that, together with drops, become the endgame weapons used in PvP. When content doesn't give power, it gives exclusive cosmetics.

| Content | Size *(proposal)* | Where it happens | Main reward |
| :---- | :---- | :---- | :---- |
| Dungeon | Group of 5 | Instance | Exclusive materials and weapons with unique effects |
| Raid | 10 to 20 players | Instance | Raid materials and exclusive cosmetics |
| Naval raid | 2 or more ships | An instance at sea, in the Underground or an instanced stretch of the world | Raid materials and naval cosmetics |
| World boss (PvPvE) | Open | World | Materials and cosmetics |
| Boss region (PvPvE) | A whole region, every faction | World | Rewards by contribution |
| Rare mobs | Solo or group | World | Rare materials and mounts |

World bosses and the boss region are PvPvE: only PvP mode characters take part, and the world boss targets only PvP players (see [[Factions, PvP and crime]]).

**Naval raid rules**

* The number of ships in the instance is limited, and the raid lends a ship to each player.  
* A player uses the raid's ship or their own, never both.  
* The raid ship expires when the raid ends.

**Region mechanics and monsters** (decided on 5 November)

* Every region mechanic is built from meters, conditions, effects and counter-measures; more piece types can be added later.  
* **PvP fairness:** a region mechanic only adds noise. It never hides real information and never changes combat numbers.  
* **Sanity in the dark** exists only in its region, in four tiers: whispers; false steps and shadows; hallucinations only you see, which do no damage; and at zero, a real shadow, only yours, until you reach light. The other examples (cold, toxic swamp, altitude, sandstorm, magnetic region, rift distortion) stay as examples in [[RunicGame — Ideias|Ideias]].  
* Monsters get behavior modules with parameters and conditions (night, day, rain, light); the lurker and pack specs are defined during implementation.  
* Undiscovered stealth, a player's or a mob's, is never sent to clients. *Proposal: clients get only sound cues with a fuzzed position.*  
* The light query returns the overall luminosity at a point: the environment plus every light source.

**Encounters made for tactical combat.** Bosses attack in space: cleaves hit whoever is in the area, the boss's facing matters, and the Tank has to position, turn and block. That rewards the choice of loadout: a Phalanx (Spear) holds a line well, and a Bow works between ships.
