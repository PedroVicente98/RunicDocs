---
title: "Sea hazards"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Sailing, swimming and naval play (Game) › Sea hazards"
created: "2026-10-14"
modified: "2026-10-30"
---

* Hazards follow one rule: the server simulates the simplest model that decides gameplay, and the client sells the spectacle (fog walls, spray, debris, lightning, sound). The game design is in [[Ideias|RunicGame — Ideias]], [[HAZARD-01 Environmental Hazards|HAZARD-01]]. Hazard effects go through [[Combat#Resolve hard and light CC|Resolve]] and [[Combat#Conditions, build-up and Tolerance|Tolerance]] like attacks, unless a hazard is flagged in its data to ignore them (ex.: slips).

* Static hazards (the ocean floor, reefs, sandbanks, glaciers) are terrain and collision cooked from the map's hazard layer, plus tagged hazard volumes in the spatial index: reef, shallow, freezing water, vent, kelp, fog bank and calm zone. Reef, sandbank and iceberg hits are [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] contacts that the Game turns into damage, and reef and iceberg hits also open breaches.

* Freezing water and vents are volume or water-body tags: while a character's WaterInteractionState says it is swimming inside one, the Game applies condition build-up through the status container (Chill or Burn) at the status tick rate, with the build-up rate set per water body or volume.

* Fog banks are volumes whose density scales the perception radius and visibility tiers of everyone inside. They drift by the wind function, so their position is a pure function of world time, like any routine. Calm zones are areas where the wind routine's speed is zero.

* Drifting icebergs are BuoyantBody objects with ObjectWaterMovement; the mostly underwater ones simply have most of their collision below the surface.

* Events (giant waves, waterspouts, maelstroms) are Environment overrides. A waterspout or a maelstrom center is one entity with a position routine and a radius: at about 10 Hz it queries the ships inside its radius, pushes them with a swirling current override, and the Game applies the damage. Inside a maelstrom the Game deals chip damage to ships sailing against its current and heavy damage at its center, enough to sink most ships in seconds; an entrance maelstrom moves a ship that reaches its center, with its whole group, into a rift or raid instance. Lightning uses the highest-point query from Weather.

* False lights and sirens are NPCs with perception and [[Behavior-tree runtime|behavior trees]]; a siren's pull is an offset added to the helm's WatercraftMovement intent while its song lasts.

* Ships can anchor anywhere, deep ocean included: the anchor adds heavy drag and doesn't need the seafloor.

* Cost: static hazards do no work until something touches them, through contacts and volume membership the engine already computes; a cyclic hazard is a pure function with nothing replicated per tick; an event is one override fact plus one entity; a vortex's 10 Hz radius query touches only the ships near it.

---

↑ [[Sailing swimming and naval play|Sailing, swimming and naval play (Game)]] · ← [[Tides storms and sea gimmicks|Tides, storms and sea gimmicks]] · [[Ship attachments|Ship attachments]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Sailing, swimming and naval play (Game) › Sea hazards · exported 2026-11-03
