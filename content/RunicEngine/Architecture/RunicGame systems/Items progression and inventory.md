---
title: "Items, progression and inventory"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "RunicGame systems (Game) › Items, progression and inventory"
created: "2026-10-14"
modified: "2026-10-30"
---

* ItemDefinition (type, slot, base stats, weapon kit) and ItemInstance (item level, grade, secondary stats, unique effects, durability) are game data on the Engine item runtime; the Platform item ledger is their durable owner. Unique effects can add or swap tags on a skill, change its element, add an effect or add a skill; they come from PvE and may also come from PvP. An effect can be extracted, destroying the source item, into a tradeable item that fits one socket per weapon (Proposal: called a Rune); extraction is one ledger operation in the economy service.

* Grades are a data table (bonus, chance, guarantee, visual); adding or removing a grade needs no code.

* Upgrades, rerolls and grade attempts run in the Go economy game service with operation IDs; RNG and guarantee counters live there, never on the client. The simulation receives the new item and rebuilds the resolved [[Weapon Class System#Loadouts|loadout]].

* Inventory is slots only, no weight. Expansions raise container capacity through a ledger operation paid in game currency.

* Trade packs are world entities carried on the back or in vehicles (CarriedBy, CargoOf), not inventory items. Vehicles hold them in dedicated cargo slots. They drop where the carrier dies or where the vehicle is destroyed or unsummoned, and can then be stolen. They forbid flying and gliding (a movement restriction) and allow only slow walking; carrying them needs vehicles or specialized mounts, one pack per mount.

---

↑ [[RunicGame systems|RunicGame systems (Game)]] · ← [[Defense and threat|Defense and threat]] · [[Quests dialogue and world interactions|Quests, dialogue and world interactions]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › RunicGame systems (Game) › Items, progression and inventory · exported 2026-11-03
