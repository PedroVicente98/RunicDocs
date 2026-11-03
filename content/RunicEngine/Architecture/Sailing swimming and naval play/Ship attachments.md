---
title: "Ship attachments"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Sailing, swimming and naval play (Game) › Ship attachments"
created: "2026-10-14"
modified: "2026-10-30"
---

* An attachment is an entity linked to a ship by an AttachedTo relationship to a hull socket, like passengers (PassengerOf) and cargo (CargoOf). It has no physics body: its transform is the socket's transform on the ship, so it costs no movement simulation.

* Engine needs: hull sockets authored per ship class in the editor (a point and a normal in ship space, flagged as reachable from the deck or only over the side), the AttachedTo relationship, and attachments in the ship's transfer-snapshot group, so they cross simulation borders with the ship ([[WATER-7|WATER-7]]).

* Each attachment is a light Character: health, a status container and one small behavior that ticks every 0.5 to 1 s. It drains hull points, adds weight (a step in the BuoyancyProfile scale), tags the ship for an AI's or a faction's perception (tracking), spawns boarders or applies build-up to the characters on deck. Each sea region has its own attachment types, from basic to dangerous, so no region is fully safe.

* Removal uses normal combat: hit volumes reach sockets near the rail; sockets low on the hull need a character leaning over the side, an interaction that exposes them and can make them fall; fire and cleanses act through the status system.

* Cost: about 64 bytes of server state per attachment. With a limit of 1 to 8 per ship, by ship type, and 100 ships at sea carrying them, that is at most 800 attachments, about 50 KB, and 800 to 1,600 behavior ticks per second, well under 1% of one core. Network: one spawn and one death event (about 16 bytes each) and a health value sent only when it changes; attachments add no movement traffic, because they follow the ship's transform.

* Visuals sell it: the client grows tentacles, chains or coral on the hull from the socket and the attachment type. The game design is in [[Ideias|RunicGame — Ideias]], [[ATTACH-01 Ship Attachments|ATTACH-01]].

---

↑ [[Sailing swimming and naval play|Sailing, swimming and naval play (Game)]] · ← [[Sea hazards|Sea hazards]] · [[Sea acceptance list|Sea acceptance list]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Sailing, swimming and naval play (Game) › Ship attachments · exported 2026-11-03
