---
title: "Game"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Game"
created: "2026-10-14"
modified: "2026-10-30"
---

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| [[GAME-0\|GAME-0]] | GameClient and GameServer executables on the Engine entry point, composing their first layers; the client’s GodotLayer on top | Both start and stop cleanly in CI; the server links no Godot | [[APP-1\|APP-1]], [[GDB-1\|GDB-1]] | [[Slice 01 Application and layers\|1]] |
| [[GAME-1\|GAME-1]] | RunicGame as a RunicEngine project: project.godot, runic.project.json, the template’s folder layout, the game’s editor library target | The [[Tools#RunicEditor\|RunicEditor]] opens RunicGame and loads its editor library | [[GDT-2\|GDT-2]] | [[Slice 06 Editor shell\|6]] |
| [[GSH-1\|GSH-1]] | Movement parameters and the prediction set in RunicGame::Shared | Client and server move identically for the same inputs | [[SIM-4\|SIM-4]], [[GPL-1\|GPL-1]] | [[Slice 14 Prediction\|14]] |
| [[GSH-2\|GSH-2]] | First skills on the ability toolkit: one melee, one projectile | Both hit a dummy with Game timings | [[CMB-2\|CMB-2]] | [[Slice 16 Ability toolkit\|16]] |
| [[GSH-3\|GSH-3]] | Damage types, resolver order, Bleed, Stagger and one interaction | A Stagger on an already staggered target becomes Trip | [[CMB-4\|CMB-4]] | [[Slice 17 Statuses and rules\|17]] |
| [[GSH-4\|GSH-4]] | Defense rules: Evasion charges, Guard modes, [[Combat#Resolve hard and light CC\|Resolve]] T1 and T2, [[Combat#Conditions, build-up and Tolerance\|Tolerance]] | A dodge spends a charge; [[Defense Evasion Guard and armor#Guard\|Guard]] blocks from the front | [[CMB-5\|CMB-5]] | [[Slice 18 Defense\|18]] |
| [[GSH-5\|GSH-5]] | Threat, taunt, Challenge and the combat prototype acceptance list | The full prototype list passes | [[CMB-6\|CMB-6]] | [[Slice 19 Combat prototype\|19]] |
| [[GSH-6\|GSH-6]] | Arena class set: three named classes, one per role (from Espada \+ Escudo, Lança 2H and Varinha \+ Foco Arcano), their weapon and [[Weapon Class System#Disciplines\|Discipline]] skill trees and armor weights as Shared data and rules | Each class fills its role in a 3v3 arena test with Game values and equal point totals | [[GSH-5\|GSH-5]], [[GCNT-1\|GCNT-1]] | [[Slice 20a Arena prototype\|20a]] |
| [[GSH-7\|GSH-7]] | Context kits: mount and aerial skill trees per [[Weapon Class System#Named classes\|named class]] with their own points; mount, glider and wing kit swaps and modifications | Defined when the expansion slices are planned | [[GSH-6\|GSH-6]], [[GPL-7\|GPL-7]] | [[Slice 44 Expansion\|44+]] |
| [[GCNT-1\|GCNT-1]] | Skills, items and effects as data; one custom behavior | A skill changes through data with live reload | [[CNT-2\|CNT-2]] | [[Slice 20 Data-driven content\|20]] |
| [[GCL-1\|GCL-1]] | First GameUI scenes in Godot: HUD and skill bar, bound to view models | The skill bar triggers abilities and UI clicks never attack | [[GDB-9\|GDB-9]] | [[Slice 19 Combat prototype\|19]] |
| [[GCL-2\|GCL-2]] | Soundtrack settings screens and audio content | A player assigns an album to a music context | [[AUD-2\|AUD-2]], [[GDB-9\|GDB-9]] | [[Slice 24 Sound and music\|24]] |
| [[GCL-3\|GCL-3]] | First world UI: nameplates and health bars, an interaction prompt, one diegetic notice board | The board accepts clicks in the world; Hidden players show no nameplate | [[GDB-10\|GDB-10]] | [[Slice 23a World UI\|23a]] |
| [[GCL-4\|GCL-4]] | Map screen with fog of war over the character’s map knowledge | The map shows only what this character has discovered | [[GDB-9\|GDB-9]], [[GSRV-6\|GSRV-6]] | [[Slice 33a Exploration prototype\|33a]] |
| [[GSVC-1\|GSVC-1]] | Character service | A character saves and reloads | [[PSDK-2\|PSDK-2]] | [[Slice 27 Accounts and characters\|27]] |
| [[GSVC-2\|GSVC-2]] | Inventory service: stacking, binding and trade rules over the Platform item ledger | A loot grant is applied once across reconnects | [[PBB-1\|PBB-1]] | [[Slice 28 Persistence\|28]] |
| [[GSVC-3\|GSVC-3]] | Quest service: stores progress, deduplicates facts, commits rewards | Replaying a fact changes nothing | [[QST-2\|QST-2]], [[PSDK-3\|PSDK-3]] | [[Slice 30 Quests\|30]] |
| [[GSVC-4\|GSVC-4]] | Economy, trade, the global auction house, guild, mail and housing services | Defined when the expansion slices are planned | [[PBB-2\|PBB-2]], [[PBB-3\|PBB-3]] | [[Slice 44 Expansion\|44+]] |
| [[GSVC-5\|GSVC-5]] | Build persistence in the Character service: [[Weapon Class System#Loadouts\|loadout]], Discipline, skill points and level choices (class and role are derived); [[Real exploration#Altars, death, respawn and teleports\|Altar]] reset that redistributes the points | A build survives relog; an Altar reset rebuilds the loadout and redistributes the points exactly once | [[GSVC-1\|GSVC-1]], [[GSH-6\|GSH-6]], [[PBB-2\|PBB-2]] | [[Slice 33a Exploration prototype\|33a]] |
| [[GSVC-6\|GSVC-6]] | Account-wide collections: transmog wardrobe, mounts, pets | Defined when the expansion slices are planned | [[GSVC-1\|GSVC-1]] | [[Slice 44 Expansion\|44+]] |
| [[GSVC-7\|GSVC-7]] | [[Labor\|Labor]]: spending and regeneration, offline regeneration for subscribers checked through entitlements | Defined when the expansion slices are planned | [[GSVC-1\|GSVC-1]], [[PCS-1\|PCS-1]] | [[Slice 44 Expansion\|44+]] |
| [[GSVC-8\|GSVC-8]] | Rankings service: region-boss contribution, PvP honor and ranking | Defined when the expansion slices are planned | [[PSDK-3\|PSDK-3]] | [[Slice 44 Expansion\|44+]] |
| [[GSVC-9\|GSVC-9]] | World routines service: stores player-caused exceptions to routines and how they fade back | A delayed escort stays delayed across a simulation restart and rejoins its routine on schedule | [[PSDK-2\|PSDK-2]] | [[Slice 43a Living world\|43a]] |
| [[GSVC-10\|GSVC-10]] | [[Real exploration#Exploration XP\|Exploration XP]], the exploration shop and profession proficiency in the Character service | Defined when the expansion slices are planned | [[GSVC-1\|GSVC-1]] | [[Slice 44 Expansion\|44+]] |
| [[GSRV-1\|GSRV-1]] | Loot rules and durable grant requests | Kill, loot, log out and keep the item | [[GPL-4\|GPL-4]], [[PBND-1\|PBND-1]] | [[Slice 28 Persistence\|28]] |
| [[GSRV-2\|GSRV-2]] | First encounter: a boss phase and a cutscene on [[Scripted sequences GameplayFlow and restrictions\|GameplayFlow]] | Every exit path releases the player’s restrictions | [[FLOW-2\|FLOW-2]] | [[Slice 29 Scripted sequences\|29]] |
| [[GSRV-5\|GSRV-5]] | Death and respawn at the nearest discovered Altar in the same world, Altar discovery, durability loss, Altars as interactables | A character dies to a mob, respawns at an Altar and its gear loses durability | [[GPL-5\|GPL-5]], [[GSVC-1\|GSVC-1]] | [[Slice 33a Exploration prototype\|33a]] |
| [[GSRV-6\|GSRV-6]] | Map knowledge: discovered cells per Lineage, charts per node and layer, and cartography | Explored cells persist per Lineage; a chart unlocks its node layer for the Lineage | [[WORLD-2\|WORLD-2]], [[GSVC-1\|GSVC-1]] | [[Slice 33a Exploration prototype\|33a]] |
| [[GSRV-7\|GSRV-7]] | Gathering, crafting, farming and trade-pack production | Defined when the expansion slices are planned | [[GSVC-2\|GSVC-2]], [[GSVC-7\|GSVC-7]] | [[Slice 44 Expansion\|44+]] |
| [[GSRV-8\|GSRV-8]] | Castles (neutral continent only): one per region in a designated zone, built by the ruling guild, fixed once placed, an indivisible volume | Defined when the expansion slices are planned | [[GSVC-4\|GSVC-4]], [[WORLD-2\|WORLD-2]] | [[Slice 44 Expansion\|44+]] |
| [[GSRV-3\|GSRV-3]] | First quests built with the Quest API | A kill-and-interact quest completes and persists | [[QST-1\|QST-1]] | [[Slice 30 Quests\|30]] |
| [[GSRV-4\|GSRV-4]] | Mob profiles, light values, [[Behavior-tree runtime\|behavior trees]] and custom nodes | Mobs warn, detect and leash at night with Game values | [[AI-3\|AI-3]], [[PRC-3\|PRC-3]] | [[Slice 33 Perception at night\|33]] |
| [[GNAV-1\|GNAV-1]] | Ship classes, sails and naval rules | A ship class sails with its Game stats | [[WATER-6\|WATER-6]] | [[Slice 42 Ships wind and currents\|42]] |
| [[GWTH-1\|GWTH-1]] | Weather patterns, tide gameplay and the wind and current routines; the world-events service that decides storms and schedules operator events | A Game weather pattern runs on schedule; an operator event changes a current for its duration and the routine resumes | [[ENV-5\|ENV-5]], [[PCS-3\|PCS-3]] | [[Slice 43 Tides waves and weather\|43]] |

---

↑ [[Work packages|Work packages]] · ← [[Platform|Platform]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Game · exported 2026-11-03
