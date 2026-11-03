---
title: "Stamina and climbing"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Nodes, Economy and Exploration"
source_url: "https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit"
section: "Stamina and climbing"
created: "2026-10-19"
modified: "2026-10-30"
---


## Stamina

* **Decision.** Stamina is its own resource, separate from [[Labor|labor]]: labor is the economic budget in hours, stamina is physical effort in seconds and minutes.  
* **Decision.** Maximum stamina is raised in the exploration shop, which keeps it centralized. Items found on summits are one source of the shop's currency, among many others from exploration.  
* **Decision.** Uses: climbing, sprinting, fast swimming, open-sea fishing (stamina drains every second the fish is not caught) and other non-combat activities, such as moving heavy objects. [[Defense Evasion Guard and armor#Guard|Guard]] and evasion use their own charges, and combat skills never cost stamina.  
* **Decision.** In combat, costs are a fixed percentage of the maximum, so they last the same time for everyone. Out of combat, costs are a flat value per tick, so more stamina goes further.  
* **Decision.** Regeneration is always a percentage of the maximum, in and out of combat. Otherwise a larger maximum would take longer to refill and become a combat disadvantage.  
* **Decision.** The in-combat cost mode follows the combat state: it starts on the first hostile action and ends 30 s after the last. A chase before the first hit still uses flat costs; this is accepted.

## Climbing

* **Decision.** Climbing in the style of Crimson Desert, with stamina, for large vertical mountains and cliffs.  
* **Decision.** Getting hit while climbing deals the full normal damage and removes a fixed percentage of maximum stamina, regardless of the damage (e.g. 20%).  
* **Decision.** The terrain sets the stamina drain by difficulty. With gear, the gear sets the drain on the surfaces it covers, never making it worse. Surfaces that can only be climbed with gear have a drain that empties stamina in one tick.  
* **Decision.** The one-tick drain is a special value that empties the whole pool, so it works with any maximum; the character grabs and slips, which teaches that gear is needed. In combat the drain is divided by a fresh character's base stamina, so everyone climbs as if unupgraded.  
* **Decision.** Some surfaces can never be climbed, with any gear: castle and fort walls, barriers, zone boundaries, instance walls and house walls.  
* **Decision.** The default comes from the asset type: terrain and rock are climbable; every structure is not, and an artist opts a structure in on purpose (e.g. a ruined tower).  
* **Decision.** Spiked shoes (ice) and climbing gear (special surfaces) exist and also help on ordinary terrain. They sit in the profession gear slots, which are always active.  
* **Decision.** Consumables: the piton is a rest point that restores stamina, stays in the world for a while (about 2 h) and anyone can use it, with up to about 5 active per player; rope reduces the drain for a few minutes. A rope fixed between two pitons makes that stretch cheaper for everyone.  
* **Open.** Whether climbing mounts, already in [[Vision|the Vision]], use stamina.

## Ships

* **Decision.** A ship's hull can be climbed only in three ways: with boarding hooks, which can be cut; with the crew ropes every ship has, which cannot be cut; or with movement skills to jump aboard.  
* **Decision.** Climbing gear has no effect on climbing ships.  
* **Decision.** The boarding hook is a consumable used from the hotbar. It is thrown as a projectile at a hull up to about 15 m away; the rope anchors to the ship and moves with it for about 30 s; anyone who can attack that ship can climb it; defenders cut it by attacking it or by interacting. Hooks only grab hulls, never walls or cliffs.

## Engine notes

* Climbing is a third movement component next to gliding and flying. A short cast finds the wall and reads the material, stored per triangle in the collision data.  
* Estimated cost: 2 to 4 casts per climber per tick, about 5 to 40 µs each. A hundred people climbing at once in one simulation use 0.5 to 4 ms of a 33 ms tick.  
* Heightfields are 2.5D and cannot make vertical walls or overhangs; large cliffs need meshes, with collision within 10 to 20 cm of the visuals. A 1 km by 500 m face at about 4 m² per triangle has about 125,000 triangles, loaded with the region.  
* Ship crew ropes and hook ropes are climbable line segments attached to the ship in ship-local coordinates, so they move with it and migrate with it in a [[Networking replication interest and handoff#Simulations, handoff and ghosts|handoff]].  
* Hand and foot animation is visual only on the client; the server sees only the capsule and owns stamina.

---

↑ [[Nodes Economy and Exploration|Nodes, Economy and Exploration]] · ← [[Maps and cartography|Maps and cartography]] · [[Profession gear and actions|Profession gear and actions]] →  
Source: [RunicGame — Appendix: Nodes, Economy and Exploration](https://docs.google.com/document/d/1HW3MV5eSJhU-cTdsMnc-3lC6XhBCCcP07pZzexqmjCA/edit) › Stamina and climbing · exported 2026-11-03
