---
title: "Open questions"
tags:
  - "architecture"
source: "RunicEngine — Technical Architecture"
created: "2026-11-13"
modified: "2026-11-13"
---

Questions the architecture leaves open, in one place. Each one names where it gets decided: a work package’s contract session, or the owner. When a question is decided, write the answer into the note it belongs to (and the [[Decisions log]] when it is a decision of its own), then delete it here. Questions about the game’s design itself stay in the [[RunicGame — Complete MMORPG Vision|Vision]], which marks its proposals.

These questions were collected on 13 November 2026 from the repositories' former copies of the architecture (the Engine’s open questions, the Game’s module and service notes and its current state), when RunicDocs became the only source.

### Engine

| Question | Decided in |
| :---- | :---- |
| Who performs the loads that World’s activation volumes request for streamed cells (the Client or the server runtime), and why ASSET-2 needs WORLD-3. Proposal: no World → Assets edge; WORLD-3 emits what to load and a consumer above both performs the load | ASSET-2 contract session (slice 21), with NAV-1 for nav tiles |
| GPL-1 uses CharacterVirtual (Physics), GPL-2 uses ContentId (Content) and GPL-5 emits facts (Events), while Gameplay’s catalog row allows only Simulation and Environment: confirm that they arrive through Simulation’s public headers, or widen the row | GPL-1, GPL-2 and GPL-5 contract sessions |
| The MoveTo and MoveGoal contract between Navigation and AI | NAV-1 contract session, with AI-2 |
| How development builds turn on Jolt’s debug renderer, which the build configures off | PHYS-3 contract session (slice 8) |
| The shape of the override operation ENV-5 receives through the service port’s inbox | PBND-4 (slice 30) and PCS-3 (slice 43) |

### Platform

| Question | Decided in |
| :---- | :---- |
| The canonical Go module path: the placeholder runic.local/platform or the hosted github.com/PedroVicente98/RunicPlatform | Owner, before the first Go code (PCT-1, slice 12) |

### Game: areas the architecture does not name yet

RunicGame::Shared and RunicGame::Server list some contents without an area (see [[Repositories, build targets and processes#Game modules|Game modules]]); until the owner names one, each is hosted where the table says.

| Content | Hosted with, until named |
| :---- | :---- |
| Movement parameters and the prediction set (GSH-1) | GameCombat |
| Item rules (Shared) | GameContent |
| Spawns, loot (GSRV-1) and world events | GameWorld |
| Service clients and the persistence bridge | GameCore |
| Faction, crime and PvP rules | GameWorld |
| Dialogue | GameQuests |
| The boss region and its contribution counting | GameEncounters (proposal) |
| The in-world side of housing (houses on grid slots, furniture placement); vehicle movement values other than ships | GameProduction and the Shared movement parameters (proposal; confirm when the expansion is planned) |
| Reports and in-world sanctions (GSRV-9) | No area yet |

### Game: registration and targets

| Question | Decided in |
| :---- | :---- |
| How the client registers the Shared prediction set, since GameCore is server-only. Proposal: Shared exports one registration function that GameCore and the client both call | GAME-0 or GSH-1 contract session |
| How a feature package adds its registration call while writing inside one area. Proposal: each area exports one Register function, and the package adds its one-line call in GameCore as an approved exception | GAME-0 contract session |
| Which package creates the three library targets: GAME-0, or the first package that writes into each one | GAME-0 contract session |

### Game: combat, builds and content

| Question | Decided in |
| :---- | :---- |
| Which balance tables (per-component coefficients, role efficiency, resistance cap) are client-safe for tooltips and which stay server-only | GSH-3 and GCNT-1 contract sessions |
| Identical effects from the role passive and the Discipline do not stack and the stronger applies (provisional, to confirm with the skill trees): how the resolver recognizes two effects as identical | GSH-3 or GSH-6 contract session |
| The CappedRewind cap and which skills use it | After playtests |
| Which two Disciplines GSH-6 pairs with its three weapon sets, and so which three named classes the arena builds (the Vision proposes Sword + Shield, Spear and Wand + Focus, one class per role) | Owner, GSH-6 contract session |
| The level curve and the point total at the maximum level | Development and playtests (data) |
| Final AI balance values (reaction times, radii, utility weights, leash distances) | Playtests |

### Game: exploration, production and economy

| Question | Decided in |
| :---- | :---- |
| The "nearest" Altar: straight-line or travel distance | GSRV-5 contract session |
| Whether durability writes on ledger item instances (GSRV-5) go through the Inventory service (GSVC-2) | GSRV-5 contract session |
| Whether copies of a Carta (paper, ink, labor) are in scope before labor (GSVC-7) and one-transaction item and currency transfers (PBB-3) exist | GSRV-6 contract session |
| Which service commits trade-pack delivery payments (gold and special resources): Economy or Inventory | When the expansion is planned |
| GSRV-7 writes four subsystems and is split into smaller packages | When the expansion is planned |
| The Market Isle’s purchases other than inventory expansions: their currency and service | Owner |
| Item upgrades: the item progression needs them before slice 44+, and no earlier package exists | Owner (roadmap) |

### Game: quests, encounters and naval play

| Question | Decided in |
| :---- | :---- |
| The split between quest scenes (GameQuests) and encounter sequences (GameEncounters) | GSRV-3 contract session |
| Story content (the main story, race chains, the sky-world chapter) has no package | Owner |
| Bosses with reactive combat (AI-4) and sea creatures have no Game package | Later encounter and naval work |
| Only GNAV-1 is defined: naval combat, breath, sea threats, charts and ship ownership need packages | When the naval slices are planned |
| Whether ship class stats and SwimProfiles are Shared (client prediction of steering and swimming) or server-only | GNAV-1 contract session |
| Whether armor changes SwimProfiles | Owner, with the armor design |

### Game: client and UI

| Question | Decided in |
| :---- | :---- |
| How the client reaches Game services for screens such as auction search, trade or mail: through the simulation as commands, or a Platform gateway | Owner, before the first such screen |
| The dialogue screen’s design, which waits for the dialogue data format | GSRV-3, then the Game UI package that draws it |
| Camera rules, animation binding, Game extractors and VFX have no package; nor do the optional key-sequence combos and the chain key | The Game slices that first need them |

### Game: services

| Question | Decided in |
| :---- | :---- |
| Where the character’s level and combat point total are stored (proposal: the Character service, with the build) | GSVC-1 and GSVC-5 contract sessions |
| Whether the service-side writes of GSRV-5 and GSRV-6 are separate GSVC packages | GSRV-5 and GSRV-6 contract sessions |
| Where regional renown is stored (proposal: the Character service) | Owner |
| The storage format of map knowledge (compressed bitsets per map, with underground and floating-island cells apart; about 18 KB of surface cells per 600 km² map before compression) | GSRV-6 contract session |
| Whether a housing deed is a ledger item, and the account limits per region | Owner |
| Whether quest rewards and mail claims call the Inventory service or the ledger directly (a quest reward commits in one transaction with its progress) | GSVC-3 contract session |
| Which service stores durable water state (dams, locks, water levels); it reaches the simulation through the service port when the owning region loads | Owner |
| Trade limits beyond binding (cooldowns, regional or faction restrictions) | Owner |
| Which simulation facts count as region-boss contribution, the share a PvP kill steals, and ranked PvP formats | With the boss-region encounter |
| Which routine kinds exist at launch (escorts, trade routes, ships, mob routines) and their fade-back rules | GSVC-9 contract session |
| Whether routine exceptions are read per cell on activation or pushed per region when a simulation takes ownership | GSVC-9 contract session, with GPL-8 |
| Guild progression, sizes and guild-owned land; mail limits (attachment count, expiry, cost) | With the expansion slices |
