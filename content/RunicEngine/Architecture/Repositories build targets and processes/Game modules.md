---
title: "Game modules"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Repositories, build targets and processes › Game modules"
created: "2026-10-14"
modified: "2026-10-30"
---

| Target | Contains | Depends on |
| :---- | :---- | :---- |
| RunicGame::Shared | Rules compiled into both executables. GameCombat: skills mapped to the ability toolkit, damage types and formula, resolver order, defense, threat, custom behaviors. GameBuilds: ten fixed loadouts, named classes (loadout \+ [[Weapon Class System#Disciplines\|Discipline]], one role each), weapon skills unlocked by level and one merged tree per class with points in the Discipline skills, context kits (mount and aerial trees), armor rules. Movement parameters, item rules, client-safe content definitions | Runic::GameplayAPI, Perception |
| RunicGame::Server | Server-only rules. GameCore registers Game systems, hooks and actions. GameWorld: continents, regions, volumes (caves, flight zones, castle zones), world rules, castles, world routines. GameAI: mob profiles, trees, custom nodes. GameQuests: quests built with the Quest API. GameEncounters: boss phases, dungeon scripts and cutscenes on GameplayFlow. GameNaval, GameInstances. GameExploration: death and respawn, durability, [[Real exploration#Altars, death, respawn and teleports\|Altars]], map knowledge, cartography and exploration XP. GameProduction (expansion): gathering, crafting, farming, professions, trade packs, [[Labor\|labor]]. Spawns, loot, world events, service clients, persistence bridge | Shared, Runic::Simulation, Network, AI, Water, Environment; Platform server bindings and contracts |
| RunicGame::Client | GameClientPresentation: camera rules, animation, VFX and audio binding, cutscene presentation. GameUI: Godot UI scenes bound to view models, including the map with fog of war. Audio content, input bindings | Shared, Runic::Client, [[How the Engine uses Godot\|GodotBridge]], Animation, Audio |
| RunicGame::Editor | The game’s marker nodes, docks and inspectors, built as the project’s editor library and loaded by the [[Tools#RunicEditor\|RunicEditor]] | Runic::GodotTools |
| GameServer (executable) | Composes the server layers: the Engine’s Network, Simulation and Diagnostics layers and the Platform’s services-bridge and lifecycle layers | RunicGame::Server, Runic::Application, Platform transport and server bindings |
| GameClient (executable) | Composes the client layers, the GodotLayer on top; links libgodot (template build) | RunicGame::Client, Runic::Application, Platform transport |
| Game services (Go) | Character (characters, builds — [[Weapon Class System#Loadouts\|loadout]], Discipline, skill points and level choices, with class and role derived — exploration XP and professions, faction and crime state, map knowledge (per Lineage), discovered Altars (per character), labor (per Lineage), account-wide collections); Inventory (rules over the Platform item ledger); Quest (stores progress, commits rewards); Economy and upgrades with a global auction house, the auction tax and the land fund; Trade; Guild; Mail; Housing and land; World events; Rankings; World routines (player-caused exceptions to routines) | Platform Go SDK, item ledger, wallets |
| Game content | Scenes, assets and data authored in the RunicEditor (Content/, Data/), split into Shared, Client and Server, cooked by [[Cooker\|the Cooker]] and exported as the client .pck | — |

---

↑ [[Repositories build targets and processes|Repositories, build targets and processes]] · ← [[Engine modules|Engine modules]] · [[Platform modules|Platform modules (Platform)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Repositories, build targets and processes › Game modules · exported 2026-11-03
