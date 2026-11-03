---
title: "Ownership (Sailing swimming and naval play)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Sailing, swimming and naval play (Game) › Ownership"
created: "2026-10-14"
modified: "2026-10-30"
---

| Game system | Built on (Engine) | Durable state (Platform) |
| :---- | :---- | :---- |
| Ship classes: hull, sails, oars, cargo capacity, crew stations, cannon slots | [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] dynamic body, BuoyantBody, WatercraftMovement | Ship ownership in the item ledger |
| Sailing controls: helm, sail trim, anchor, oars | WatercraftMovement intents, wind | — |
| Cargo and [[Trade packs and routes\|trade packs]] on board | CargoOf relationships, group [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] | — (trade packs are world entities) |
| Passengers, boarding, falling overboard | PassengerOf, CharacterVirtual on moving bodies, CharacterWaterMovement | — |
| Naval combat: cannons, ramming, hull damage, breaches and flooding, sinking | Ability toolkit with the ship as source, damage interception, BuoyancyProfile scale and righting strength, water samples at breach points | Repairs through the economy game service |
| Swimming, diving and breath | CharacterWaterMovement, WaterInteractionState | — |
| Sea threats and water bosses | AI framework, CharacterWaterMovement, perception, SwimMovementModifiers | — |
| Nautical charts | Map knowledge, cooked current and wind fields | Learned charts in the character service |
| Naval raids | Instances, lent ships | Raid rewards |
| Tides, storms and sea gimmicks | Tides, weather overrides | Event schedule in the world-events game service |

---

↑ [[Sailing swimming and naval play|Sailing, swimming and naval play (Game)]] · [[Ships (Sailing swimming and naval play)|Ships (Sailing swimming and naval play)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Sailing, swimming and naval play (Game) › Ownership · exported 2026-11-03
