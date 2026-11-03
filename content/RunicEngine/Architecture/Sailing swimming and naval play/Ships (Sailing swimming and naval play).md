---
title: "Ships (Sailing swimming and naval play)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Sailing, swimming and naval play (Game) › Ships"
created: "2026-10-14"
modified: "2026-10-30"
---

* **A ship is an entity** with Transform, a [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] dynamic body, BuoyantBody, WatercraftMovement and ShipTag, plus Game components: hull points, compartments with breach limits, cargo capacity, crew stations and cannon slots. Ship classes, from small boats to large warships, are data. Each class lists the part slots it allows (hull, bow, masts, sails, helm, cannons and more), and part upgrades are data that change the ship's stats (ex.: an ice bow takes less ice damage, a ram bow deals more collision damage).

* **Controls are intents:** the helm steers, sail trim scales sail force, the anchor adds heavy drag, oars or other propulsion move small boats without wind. The helmsman applies acceleration and rotation, and currents push the ship off its heading, so holding a course needs constant correction. With nobody at the helm both intents are zero, while the ship keeps its momentum, its sail force as trimmed and the current: it drifts. Ship classes set lateral\_current\_influence, so a clipper holds its course in a side current far better than a galleon, and their hull depth is their draft ([[Ideias|RunicGame — Ideias]], [[SEA-01 Ship Handling and Sea Balance|SEA-01]]).

* **Passengers** stand on deck as CharacterVirtuals carried by the moving body. Boarding is walking or jumping onto the deck; falling overboard switches the character to swimming.

* **Cargo:** [[Trade packs and routes|trade packs]] aboard are CargoOf entities. When a ship sinks they become floating objects (BuoyantBody and ObjectWaterMovement) that drift with the current and can be looted, which feeds piracy and PvP.

* **Range bonus at sea:** a rule-pipeline condition (caster is a passenger of a ship) adds the small range bonus [[Vision|the game vision]] gives eligible skills.

* **Handoff:** hull, passengers and cargo transfer to the next simulation together, in one authority epoch.

* **Ownership and persistence:** owned ships are items in the Platform ledger; the ship spawns at a dock, and damage and repairs are economy operations. Proposal: a sunk ship returns damaged to its home port and its cargo stays at sea.

---

↑ [[Sailing swimming and naval play|Sailing, swimming and naval play (Game)]] · ← [[Ownership (Sailing swimming and naval play)|Ownership (Sailing swimming and naval play)]] · [[Naval combat|Naval combat]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Sailing, swimming and naval play (Game) › Ships · exported 2026-11-03
