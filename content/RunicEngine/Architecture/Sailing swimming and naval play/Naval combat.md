---
title: "Naval combat"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Sailing, swimming and naval play (Game) › Naval combat"
created: "2026-10-14"
modified: "2026-10-30"
---

* **Cannons** are abilities whose source is a crewed ship station, using projectile shapes that hit hulls and characters on deck. Wind affects them only if the skill sets the wind flag.

* **Hull damage** goes through damage interception on the ship entity, with Game defense values per ship class. A ship has one pool of hull points: cannons, ramming and sea creatures deal fixed damage; environment events (big waves, lightning, waterspouts, maelstroms) deal a percentage of the ship's maximum hull points, small per hit for events that hit many times and large for a single hit, so every ship class takes them the same way; and water counts as hull points drained.

* **Ramming** reads [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] contacts; the Game turns contact speed and mass into damage.

* **Sinking:** at zero hull points the Game lowers the BuoyancyProfile scale over a few seconds, so the ship physically sinks while passengers swim away. Ships never capsize: the righting strength keeps them upright, so the worst a ship takes is damage and water.

* Breaches belong to a hull compartment, and each compartment has a breach limit; the main body takes the most. About 5 times a second the Game tests each open breach with [[Core model water reports facts|WaterSystem]]::TrySample; a breach under water drains hull points at a fixed rate, so a single breach left open can sink a ship.

* Repair heals in three ways: closing breaches, removing water (which restores what the water drained) and repairing the hull and stations (which restores fixed damage). Each ship part has its own repair kit with durability, and using a kit needs no profession level. Removing water uses bailing, described next.

* A bucket is an inventory item used for bailing. Each ship class authors its compartments as volumes in ship space, so bigger ships have more; when a character stands in a compartment with water, the interaction prompt appears. Filling stows the weapon, which stays equipped, and sets a carrying-water state built on the GameplayAPI character state, movement modifiers and interactions: no sprint (normal movement speed is unchanged), kept through damage and CC (a stun only stops movement), and ended only by the player. Emptying sends the aim direction with the action; the server casts one short ray along the aim against the ship's own collision only, and the throw counts as out when the ray hits nothing of the ship within the throw distance, its end point lies outside the ship's footprint and the pitch stays below a limit (window and opening shapes sit on a pass-through collision layer the ray ignores); it then removes that water and restores the hull points it drained; otherwise the water goes back into the ship. The splash is a client-only cosmetic projectile, so nothing is simulated on the server; each throw costs one ray against one body and one point-in-box test.

* A big wave that hits a ship from the side deals damage and opens a breach; whirlpools pull ships toward their center. Both are Environment events (see Waves).

* Storm lightning strikes the highest point, usually a mast, and damages it; in the water it stuns and damages characters within a radius. Lightning comes only from storms, never from player abilities.

* Replication per ship: hull points, the water per compartment and about 3 bytes per breach, sent only when they change.

* **Naval raids:** the instance limits the number of ships, lends each player a raid ship, allows the raid ship or the player’s own but not both, and expires lent ships when the raid ends.

---

↑ [[Sailing swimming and naval play|Sailing, swimming and naval play (Game)]] · ← [[Ships (Sailing swimming and naval play)|Ships (Sailing swimming and naval play)]] · [[Swimming diving and breath|Swimming, diving and breath]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Sailing, swimming and naval play (Game) › Naval combat · exported 2026-11-03
