---
title: "Slice 44+ · Expansion"
aliases:
  - "Slice 44+"
tags:
  - "development"
  - "slice"
  - "progress/not-started"
slice: "44+"
status: "Not started"
owners: "All"
issue: "https://github.com/PedroVicente98/RunicEngine/issues/190"
created: "2026-11-03"
modified: "2026-11-03"
---

**Slice:** 44+ · **Status:** Not started · **Packages done:** 0 of 29 · **Owners:** All · **Issue:** [RunicEngine#190](https://github.com/PedroVicente98/RunicEngine/issues/190)

← [[Slice 43a · Living world]] · [[RunicGame — Development|All slices]]

**Runnable result:** Housing, economy, instances, shop island, the sky world and world transitions, busy-area partitions, placement by traffic and local links, the production look in Godot, crafting, labor and professions, exploration XP, castles, collections, rankings, flight, aerial combat and climbing, launch phases

**Proves:** The same boundaries, reused

**Godot:** Production look in Godot (materials, terrain, VFX); plugin compatibility

### Packages

- [ ] **DSIM-5** · Authority partitions inside one region · [RunicEngine#137](https://github.com/PedroVicente98/RunicEngine/issues/137) · not started
    - Authority partitions inside one region (busy areas such as a city) that never cut an indivisible volume (an island, a castle, a docked ship)
    - **Done when:** Two simulations share a city, each entity has one owner, and no indivisible volume is split
    - **Needs:** [[Slice 36 · Multiple simulations|DSIM-3]]
- [ ] **NAV-2** · Flight navigation · [RunicEngine#141](https://github.com/PedroVicente98/RunicEngine/issues/141) · not started
    - Flight navigation: 3D paths through free space over the sparse cells for flying actors, respecting volumes and altitude ceilings
    - **Done when:** A flying NPC reaches a target behind an obstacle without entering a forbidden volume
    - **Needs:** [[Slice 31 · Navigation and spawning|NAV-1]], [[Slice 11 · Spatial index|WORLD-2]]
- [ ] **NET-8** · World transitions · [RunicEngine#142](https://github.com/PedroVicente98/RunicEngine/issues/142) · not started
    - World transitions: the session leaves one world’s simulation after a checkpoint and joins another world’s simulation with a new connect ticket; no handoff or ghosts across worlds
    - **Done when:** A character moves between two worlds with its checkpointed state, and the old simulation keeps no copy
    - **Needs:** [[Slice 12 · Transport|NET-1]], [[Slice 27 · Accounts and characters|SIM-5]], [[Slice 27 · Accounts and characters|PCS-1]]
- [ ] **GDB-13** · Production look · [RunicEngine#138](https://github.com/PedroVicente98/RunicEngine/issues/138) · not started
    - Production look: materials, terrain, water shading, VFX and decals as Godot resources fed by RenderData; Game render features as materials and presenter hooks
    - **Done when:** Defined when a substantial game slice justifies it
    - **Needs:** [[Slice 22 · World rendering|GDB-5]]
- [ ] **CORE-7** · RenderData effect kinds · [RunicEngine#136](https://github.com/PedroVicente98/RunicEngine/issues/136) · not started
    - RenderData effect kinds: particles, decals, trails
    - **Done when:** Defined when the production look is planned
    - **Needs:** [[Slice 5 · Moving entities|CORE-3]]
- [ ] **COOK-8** · Incremental cooking at scale · [RunicEngine#135](https://github.com/PedroVicente98/RunicEngine/issues/135) · not started
    - Incremental cooking at scale
    - **Done when:** Only changed inputs cook again across a continent
    - **Needs:** [[Slice 21 · World partitions|COOK-3]]
- [ ] **GPL-7** · Flight and climbing movement modes · [RunicEngine#140](https://github.com/PedroVicente98/RunicEngine/issues/140) · not started
    - Flight and climbing movement modes: flight inside flight-zone volumes with an altitude ceiling above which only gliding works, glide and flight as separate mount capabilities, flying vehicles, climbing mounts; restrictions can forbid flight and gliding
    - **Done when:** Above the ceiling flight stops and gliding takes over; outside a flight zone a flying mount only glides; a restriction blocks both; a mount climbs a marked wall
    - **Needs:** [[Slice 14 · Prediction|GPL-1]], [[Slice 18 · Defense|GPL-3]], [[Slice 11 · Spatial index|WORLD-2]], [[Slice 42 · Ships, wind and currents|ENV-2]]
- [ ] **PTR-4** · Simulation links chosen by locality · [RunicPlatform#29](https://github.com/PedroVicente98/RunicPlatform/issues/29) · not started
    - Simulation links chosen by locality: an in-memory queue in one process, a local socket or shared-memory channel on one machine, GameNetworkingSockets between machines
    - **Done when:** The same transfer test passes on every channel with identical results; the link picks its channel from the peers’ placement
    - **Needs:** [[Slice 36 · Multiple simulations|PTR-3]]
- [ ] **PBB-3** · One-transaction transfers that move ledger items and wallet currency… · [RunicPlatform#24](https://github.com/PedroVicente98/RunicPlatform/issues/24) · not started
    - One-transaction transfers that move ledger items and wallet currency together; mechanisms only
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 28 · Persistence|PBB-1]], [[Slice 33a · Exploration prototype|PBB-2]]
- [ ] **PCS-4** · Instance allocation from Agones fleets · [RunicPlatform#25](https://github.com/PedroVicente98/RunicPlatform/issues/25) · not started
    - Instance allocation from Agones fleets
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 36 · Multiple simulations|PCS-2]], [[Slice 39 · Operations|PINF-2]]
- [ ] **PCS-5** · Chat and party groups · [RunicPlatform#26](https://github.com/PedroVicente98/RunicPlatform/issues/26) · not started
    - Chat and party groups
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 30 · Quests|PSDK-3]]
- [ ] **PCS-6** · Admission · [RunicPlatform#27](https://github.com/PedroVicente98/RunicPlatform/issues/27) · not started
    - Admission: per-world capacity limits, login queue and cohort waves for the launch phases
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 27 · Accounts and characters|PCS-1]]
- [ ] **PCS-7** · Placement by load and traffic over Agones · [RunicPlatform#28](https://github.com/PedroVicente98/RunicPlatform/issues/28) · not started
    - Placement by load and traffic over Agones: scores by load, memory and inter-simulation traffic, with distance from the regions’ global coordinates; moves high-traffic pairs onto one node by move-by-handoff, up to a per-node cap
    - **Done when:** Two simulations with heavy link traffic end on one node with no loading screen; no node passes its cap
    - **Needs:** [[Slice 36 · Multiple simulations|PCS-2]], [[Slice 39 · Operations|PINF-2]], PTR-4
- [ ] **GSH-7** · Context kits · [RunicGame#32](https://github.com/PedroVicente98/RunicGame/issues/32) · not started
    - Context kits: mount and aerial skill trees per named class with their own points; mount, glider and wing kit swaps and modifications
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 20a · Arena prototype|GSH-6]], GPL-7
- [ ] **GSVC-4** · Economy, trade, the global auction house, guild, mail and housing services · [RunicGame#36](https://github.com/PedroVicente98/RunicGame/issues/36) · not started
    - Economy, trade, the global auction house, guild, mail and housing services
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 33a · Exploration prototype|PBB-2]], PBB-3
- [ ] **GSVC-6** · Account-wide collections · [RunicGame#37](https://github.com/PedroVicente98/RunicGame/issues/37) · not started
    - Account-wide collections: transmog wardrobe, mounts, pets
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 27 · Accounts and characters|GSVC-1]]
- [ ] **GSVC-7** · Labor: spending and regeneration · [RunicGame#38](https://github.com/PedroVicente98/RunicGame/issues/38) · not started
    - Labor: spending and regeneration, offline regeneration for subscribers checked through entitlements
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 27 · Accounts and characters|GSVC-1]], [[Slice 27 · Accounts and characters|PCS-1]]
- [ ] **GSVC-8** · Rankings service · [RunicGame#39](https://github.com/PedroVicente98/RunicGame/issues/39) · not started
    - Rankings service: region-boss contribution, PvP honor and ranking
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 30 · Quests|PSDK-3]]
- [ ] **GSVC-10** · Exploration XP, the exploration shop and profession proficiency in the… · [RunicGame#35](https://github.com/PedroVicente98/RunicGame/issues/35) · not started
    - Exploration XP, the exploration shop and profession proficiency in the Character service
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 27 · Accounts and characters|GSVC-1]]
- [ ] **GSRV-7** · Gathering, crafting, farming and trade-pack production · [RunicGame#33](https://github.com/PedroVicente98/RunicGame/issues/33) · not started
    - Gathering, crafting, farming and trade-pack production
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 28 · Persistence|GSVC-2]], GSVC-7
- [ ] **GSRV-8** · Castles (neutral continent only): one per region in a designated zone · [RunicGame#34](https://github.com/PedroVicente98/RunicGame/issues/34) · not started
    - Castles (neutral continent only): one per region in a designated zone, built by the ruling guild, fixed once placed, an indivisible volume
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** GSVC-4, [[Slice 11 · Spatial index|WORLD-2]]
- [ ] **GDT-16** · Plugin compatibility · [RunicEngine#139](https://github.com/PedroVicente98/RunicEngine/issues/139) · not started
    - Plugin compatibility: published extension API per build, install validator, runic.plugin.json, Cooker adapters for plugin formats
    - **Done when:** Defined when the expansion slices are planned
    - **Needs:** [[Slice 21 · World partitions|GDT-14]]
- [ ] **NET-9** · Client-integrity channel for an anti-cheat provider · [RunicEngine#193](https://github.com/PedroVicente98/RunicEngine/issues/193) · not started
    - Client-integrity channel: opaque messages between a client-side and a server-side integrity provider (a commercial anti-cheat), on their own lane with a budget; a server hook lets the provider close a connection. No provider types in public headers.
    - **Done when:** A test provider exchanges messages through the channel and closes a connection it rejects
    - **Needs:** [[Slice 12 · Transport|NET-1]]
- [ ] **NET-10** · Occlusion-aware interest against wallhacks · [RunicEngine#194](https://github.com/PedroVicente98/RunicEngine/issues/194) · not started
    - Occlusion-aware interest: a hostile player is sent only when it could become visible to the client soon (precomputed visibility per cell plus a short margin), so wallhacks have nothing to draw.
    - **Done when:** Defined when PvP measurements show wallhack ESP is a real problem
    - **Needs:** [[Slice 25 · Interest|NET-4]]
- [ ] **PINF-3** · Edge and DDoS protection · [RunicPlatform#34](https://github.com/PedroVicente98/RunicPlatform/issues/34) · not started
    - Edge and DDoS protection: clients reach only an edge (a filtering provider, an anycast accelerator or own relays), never a simulation's own address; login, website and APIs behind a CDN with rate limits; a kernel-level filter (eBPF or XDP) that drops non-handshake packets at scale; the same edge carries relay routing for latency; a flooded node is handled as a lost node.
    - **Done when:** Defined when the launch plan is made; provider to be chosen
    - **Needs:** [[Slice 39 · Operations|PINF-2]]
- [ ] **GSRV-9** · Reports with evidence and in-world sanctions · [RunicGame#43](https://github.com/PedroVicente98/RunicGame/issues/43) · not started
    - Reports and in-world sanctions: a report command that attaches the last 60 seconds (example) of facts and positions around the reported player; mute, trade lock and kick enforced in the simulation from moderation decisions.
    - **Done when:** A report reaches the moderation service with its evidence, and a trade lock stops a trade at once
    - **Needs:** GSVC-12, [[Slice 27 · Accounts and characters|PBND-1]]
- [ ] **GSVC-12** · Moderation service · [RunicGame#42](https://github.com/PedroVicente98/RunicGame/issues/42) · not started
    - Moderation service: a review queue fed by reports and the scoring service; reports weighted by the reporter's history; a sanction ladder (warning, mute, trade lock, temporary ban, permanent ban; bots and real-money trading go straight to a ban); appeals; ban waves; an audit log of every GM action.
    - **Done when:** Defined when the launch plan is made
    - **Needs:** [[Slice 26 · Service foundation|PSDK-2]], [[Slice 39 · Operations|GSVC-11]]
- [ ] **GAME-2** · Client anti-cheat integration · [RunicGame#44](https://github.com/PedroVicente98/RunicGame/issues/44) · not started
    - Client anti-cheat: Easy Anti-Cheat through Epic Online Services in RunicGameClient, with its server counterpart in RunicGameServer over the Engine integrity channel (NET-9). Kernel driver on Windows; user mode only on Linux and Steam Deck. RunicGameServer stays headless.
    - **Done when:** Defined when the launch plan is made; a client that fails the provider's checks is disconnected
    - **Needs:** NET-9
- [ ] **GAME-3** · Signed releases, launcher and file integrity · [RunicGame#45](https://github.com/PedroVicente98/RunicGame/issues/45) · not started
    - Signed releases and the launcher: builds and patch manifests signed with an offline key that never touches CI; the launcher verifies signatures before running anything and repairs changed files; the client does not connect after a failed integrity check (there is no mod support, so any change is tampering or damage); Windows code signing. Player soundtrack files live outside the checked files.
    - **Done when:** A changed byte in an installed file is repaired by the launcher, and an unsigned patch is refused
    - **Needs:** [[Slice 21 · World partitions|ASSET-2]], [[Slice 22 · World rendering|COOK-4]]

*Generated by `tools/sync_development.py` from the [[Vertical-slice roadmap]], the work packages and the GitHub issues. Change those, then run it again.*
