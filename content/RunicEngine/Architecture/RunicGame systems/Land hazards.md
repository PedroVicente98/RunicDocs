---
title: "Land hazards"
tags:
  - "runicengine"
  - "architecture"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "RunicGame systems (Game) › Land hazards"
created: "2026-10-14"
modified: "2026-10-30"
---

* Land hazards follow the same rule: the simplest server model and a client spectacle ([[Ideias|RunicGame — Ideias]], [[HAZARD-01 Environmental Hazards|HAZARD-01]]), with effects that go through [[Combat#Resolve hard and light CC|Resolve]] and [[Combat#Conditions, build-up and Tolerance|Tolerance]] unless flagged.

* Verticality is terrain from the elevation layer. Mounts have a slope limit in their movement profile, falls use fall damage, and some places are reached only by gliding down or with climbing gear.

* Inland weather reuses the WeatherState: blizzards and sandstorms lower visibility and apply build-up (Chill) or damage to exposed characters; lightning on high ground uses the same highest-point query as at sea.

* Snow is a level per snowfield region (none, light, heavy or deep) in the replicated WeatherState: it rises while it snows, and a timer drops it one level at a time while it isn't snowing. Each level maps to a movement modifier through the region's hazard volumes: light is only visual, heavy slows, and deep slows more, blocks sprinting and keeps some mounts out. Drift-zone volumes at the bottom of slopes count one level deeper. Snow cover and footprints are client-only. Cost: about one byte per snowfield region, sent only when its level changes.

* Avalanches are weather events on the slide paths from terrain hydrology (below), possible only while the slope's snow is heavy or deep, and never something players set off easily. Each path has a start, an end and the area where the snow lands, and hand-placed markers only add, remove or adjust paths ([[Content Pipeline and Art Direction|RunicGame — Appendix: Content Pipeline and Art Direction]], Map authoring markers). The server moves one hazard volume from the start to the end, which knocks characters down through Resolve and damages them, then makes the landing area deep snow for a while; the falling snow is a client effect. Cost: one hazard entity for a few seconds.

* Rain and ground levels: the WeatherState's precipitation maps to a rain level (none, drizzle, heavy, monsoon). Each region also has a ground level (dry, damp, mud, soaked) that rises one level after a set time under rain at least that strong and drops one level per timer while the rain is lighter, with a drying rate per biome. Both are one byte per region in the replicated weather state, sent only when they change (RunicGame — Ideias, [[HAZARD-01 Environmental Hazards|HAZARD-01]]).

* Mud and wet ground need no new data: the terrain type under a character, the ground normal its CharacterVirtual already has and the region's ground level pick a movement modifier (mud slows; soaked slows more and blocks sprinting). Rock, sand and paved road cells never turn to mud, and traversal gear scales the modifier.

* Sliding is a movement mode. On wet ground or ice, the slip chance per second is a smooth curve of the slope angle between a start angle and a full angle, both set by the surface, the ground level and the gear, and scaled by movement speed. The roll is a hash of the character ID and the tick: a number that looks random but is the same on every machine, so the owning client predicts the same slip as the server with nothing sent. A second hash (same inputs, another salt) picks the outcome, weighted by the angle so the tiers fade into each other: a stumble (a short speed loss), prone with no slide, or prone and sliding. A slide accelerates down the slope at g·(sin θ − μ·cos θ), with μ from the surface, the ground level and the gear, so it only starts where the slope beats the grip, and the character enters climbing mode, where holding on grips with the same curve. A slip is a movement state, not a CC, so it ignores Resolve and Tolerance. Mounts use the same tiers with their own angles: a stumble slows the mount, prone keeps the rider on, and a slide throws the rider off; the mount then slides prone to the end of the slide path and stays there, keeping its health and its [[Trade packs and routes|trade pack]], until it is unsummoned and summoned again (RunicGame — Ideias, [[HAZARD-01 Environmental Hazards|HAZARD-01]]). Climbing on wet rock rolls the same way. Cost: a few nanoseconds per character per tick, only on slippery ground.

* Terrain hydrology is a Cooker step on the elevation layer: flow direction per terrain cell (toward its lowest neighbor); flow accumulation, whose high cells are the channels (authored rivers plus dry gullies, canyons and dry beds); for each cell, its height above the channel it drains into (HAND, Height Above Nearest Drainage) and that channel stretch; low spots with no outlet and the height where each overflows; and slide paths, cells within a release-angle range (about 30–45° for snow) followed downhill to where the slope flattens, each with a start, a path and a landing area. The [[Tools#RunicEditor|RunicEditor]] shows the flood at monsoon and the slide paths; a painted exclusion mask and hand-placed markers remove, add or adjust results.

* Floods: each channel stretch (a few hundred meters) has a stage, the water height above its bed. The stage is a pure function of the ground levels of the regions that drain into it, with weights from the cook, so clients compute it themselves and nothing per stretch is replicated. A cell is under water when its height above the channel is below the stage, and its depth is the difference: authored rivers rise with the stage and spill onto low bank cells, canyons flood deep and narrow, flat valleys wide and shallow, and dry channels and low spots fill too, low spots up to their overflow height. The current runs along the channel, strong in the channel and weak on the flooded plain, and grows with the stage.

* The [[Core model water reports facts|WaterSystem]] gets a flood layer: when no water body answers TrySample, it compares the cell's height above the channel with the stage, so swimming, breath, buoyancy and drifting work unchanged on flooded ground.

* Flash floods are events on one drainage path, dry beds included: an Environment override (route, start time, peak height, front speed, rise, hold, fall and flow multiplier; about 32 bytes, sent once) adds a front that travels down the path, offset(s, t) \= H · f(t − start − s / v), where s is the distance along the path and f rises from 0 to 1, holds and falls. The client plays a rumble and dust a few seconds before the front reaches a point.

* Slides: each generated path rolls about once a minute, with a hidden seed, while its region's snow is heavy or deep (avalanche) or its ground is soaked (mudslide); a slide is the moving hazard volume described above, and its landing area becomes deep snow or mud for a while.

* Roads: paved road cells never turn to mud and are less slippery; [[Cooker|the Cooker]] raises roads over cells that flood or bridges the channels, and its validation warns when a road would flood in a monsoon.

* Client: a flood water mesh over the visible floodable tiles, whose vertex shader reads the cooked height-above-channel texture and a buffer of stages and hides dry spots; mud is a terrain shader blend driven by the ground level.

* Flood and slide cost (estimates): cooking takes seconds to about a minute for the map and can be redone per region; the height above the channel and the stretch ID are stored only for cells that can flood, about 8 to 16 MB for the 600 km² map, streamed by cell; slide paths take about 100 bytes each (2,000 paths, about 200 KB); the network carries one byte per region level change and about 32 bytes per event; stages are recomputed only when a ground level changes; flood checks run only on floodable cells during a flood, so 500 characters at 30 Hz are about 15,000 checks per second, about 1.5 ms of CPU per second (around 0.15% of a core); slide rolls are about 30 per second.

* Earthquakes never change terrain. A cave entrance is a placed object with a closed and an open model; an earthquake flips its world-state flag for a while and spawns rockfall hazard areas. Screen shake and dust are client effects.

* Volcanoes: an eruption is client effects plus hazard zones that hit random spots with fire damage and leave damaging ground for a while; ash clouds are fog volumes and lava flows follow authored channels. When it ends, the Game sets the nearby ore richness and spawn script to their maximum.

* Swamps are hazard volumes that slow, with gas pockets that apply Poison build-up; magnetic anomalies are volumes whose tag the client compass reads to spin.

* New islands and new terrain come only with patches; nothing is generated at runtime.

* Cost: the same as at sea. Cooked terrain and volumes cost nothing at rest, and an event is one override fact, a flag flip or a few hazard entities.

* Acceptance: an earthquake opens a cave entrance for a while and closes it again, at the same world time in two simulations. In a monsoon, the same cells flood in two simulations and their clients with no flood marker placed, and a flash flood front reaches a given point at the same world time; on wet ground, a character slips more often as the slope gets steeper, with no step at any single angle, and its client predicts the same slip as the server.

---

↑ [[RunicGame systems|RunicGame systems (Game)]] · ← [[Map knowledge altars factions and progression|Map knowledge, altars, factions and progression]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › RunicGame systems (Game) › Land hazards · exported 2026-11-03
