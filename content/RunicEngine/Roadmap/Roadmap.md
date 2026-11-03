---
title: "Vertical-slice roadmap"
aliases:
  - "Slices"
tags:
  - "runicengine"
  - "slice"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-11-03"
modified: "2026-11-03"
---

The vertical slices of the [[Vertical-slice roadmap|roadmap]], one note per slice. Each slice is small, ends in something runnable and testable, and adds one piece of the architecture.

| Slice | Runnable result | Owner |
| :---- | :---- | :---- |
| [[Slice 00 Build skeleton\|0. Build skeleton]] | Engine library plus empty GameClient, GameServer and [[Tools#RunicEditor\|RunicEditor]] build in CI in all three repositories; libgodot builds in the editor and template targets; the… | Engine, Platform, Game |
| [[Slice 01 Application and layers\|1. Application and layers]] | A Godot window opens from the client; layers push, pop and replace at safe points; events stop when handled | Engine, Game |
| [[Slice 02 Debug drawing\|2. Debug drawing]] | Grid, camera, colored shapes with opacity and text drawn by Godot | Engine |
| [[Slice 03 Fixed-step clock\|3. Fixed-step clock]] | The scheduler runs 60/30/20/10 Hz on the server loop with metrics | Engine |
| [[Slice 04 ECS and world coordinates\|4. ECS and world coordinates]] | Entities with 64-bit positions are created and queried; one fact reaches two consumers | Engine |
| [[Slice 05 Moving entities\|5. Moving entities]] | Entities move on a plane through commands and are drawn | Engine |
| [[Slice 06 Editor shell\|6. Editor shell]] | The RunicEditor opens the RunicGame project and a dock inspects entities of a local world | Engine |
| [[Slice 07 Physics\|7. Physics]] | A capsule walks on static terrain far from the origin under keyboard control | Engine |
| [[Slice 08 Physics view\|8. Physics view]] | Collision shapes are drawn and can be inspected | Engine |
| [[Slice 09 First cooker proof\|9. First cooker proof]] | A mesh made in Blender is imported by Godot, its collision cooked by the [[Cooker\|Runic Cooker]], drawn and walked on | Engine |
| [[Slice 10 Worker pool\|10. Worker pool]] | The same scene with several workers gives identical results | Engine |
| [[Slice 11 Spatial index\|11. Spatial index]] | 3D cells, volumes and membership drawn; queries visualized | Engine |
| [[Slice 12 Transport\|12. Transport]] | A client connects to a local server with a test-signed ticket; ping and echo | Engine, Platform |
| [[Slice 13 Replication\|13. Replication]] | Two clients see each other move; the Run button starts the server and both clients | Engine |
| [[Slice 14 Prediction\|14. Prediction]] | Responsive movement with correction under simulated lag | Engine, Game |
| [[Slice 15 Character state\|15. Character state]] | A dummy has health, tags and modifiers; casts and overlaps are drawn | Engine |
| [[Slice 16 Ability toolkit\|16. Ability toolkit]] | One melee swing and one projectile hit a dummy | Engine, Game |
| [[Slice 17 Statuses and rules\|17. Statuses and rules]] | Bleed, Stagger and one interaction (a Stagger on an already staggered target becomes Trip) | Engine, Game |
| [[Slice 18 Defense\|18. Defense]] | Dodge with charges, shield Guard, a [[Combat#Resolve hard and light CC\|Resolve]] chain | Engine, Game |
| [[Slice 19 Combat prototype\|19. Combat prototype]] | The full acceptance list below | Engine, Game |
| [[Slice 20 Data-driven content\|20. Data-driven content]] | Skills, items and effects as data with live reload; one custom behavior | Engine, Game |
| [[Slice 20a Arena prototype\|20a. Arena prototype]] | Three [[Weapon Class System#Named classes\|named classes]], one per role, fight 3v3 in an arena with their skill trees and armor | Game |
| [[Slice 21 World partitions\|21. World partitions]] | Walk across regions authored as scenes, down into a cave volume and up a cliff with activation-volume streaming | Engine |
| [[Slice 22 World rendering\|22. World rendering]] | Cooked meshes and terrain draw through Godot far from the origin | Engine |
| [[Slice 23 Animated characters\|23. Animated characters]] | A skinned character animates with blended clips | Engine |
| [[Slice 23a World UI\|23a. World UI]] | Nameplates and health bars follow entities; a notice board in the world accepts clicks | Engine, Game |
| [[Slice 24 Sound and music\|24. Sound and music]] | Sound events play through buses; a music context switches albums | Engine, Game |
| [[Slice 25 Interest\|25. Interest]] | Only relevant entities arrive; visibility tiers at night | Engine |
| [[Slice 25a Night on screen\|25a. Night on screen]] | Torches light the night; darkness zones and fog draw, matching what the server treats as dark | Engine |
| [[Slice 26 Service foundation\|26. Service foundation]] | A Go service writes to [[Physical layout Proposal\|PostgreSQL]] idempotently on the local stack | Platform |
| [[Slice 27 Accounts and characters\|27. Accounts and characters]] | Log in, receive a real ticket, load and save a character | Platform, Game |
| [[Slice 28 Persistence\|28. Persistence]] | Kill, loot, log out, keep the item | Engine, Platform, Game |
| [[Slice 29 Scripted sequences\|29. Scripted sequences]] | A boss phase locks the arena; a cutscene protects the player; a disconnect releases everything | Engine, Game |
| [[Slice 30 Quests\|30. Quests]] | A persistent quest driven by gameplay facts | Engine, Platform, Game |
| [[Slice 31 Navigation and spawning\|31. Navigation and spawning]] | Spawned NPCs walk navmesh paths across cells | Engine |
| [[Slice 32 AI brains\|32. AI brains]] | An NPC patrols and chases through behavior-tree intents | Engine |
| [[Slice 33 Perception at night\|33. Perception at night]] | Mobs warn, detect, fight and leash at night | Engine, Game |
| [[Slice 33a Exploration prototype\|33a. Exploration prototype]] | Explore at night with a torch, die to a mob, respawn at an [[Real exploration#Altars, death, respawn and teleports\|Altar]], and keep both the map you uncovered and your build | Platform, Game |
| [[Slice 34 Reactive combat\|34. Reactive combat]] | A mob answers a telegraphed skill with a defensive action; its trace explains why | Engine |
| [[Slice 35 AI editor\|35. AI editor]] | A [[Behavior-tree runtime\|behavior tree]] is edited, saved and reloaded; a live NPC is inspected | Engine |
| [[Slice 36 Multiple simulations\|36. Multiple simulations]] | Walk from simulation A into B | Engine, Platform |
| [[Slice 37 Cross-border combat\|37. Cross-border combat]] | An attack across the border damages its target once; a sequence and a quest survive [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] | Engine |
| [[Slice 38 Battle scale\|38. Battle scale]] | 200, then 500 bots fighting in one region; nameplates fall back to the batched path | Engine |
| [[Slice 39 Operations\|39. Operations]] | Fleets on [[Platform and operations#Simulation placement\|Agones]], the Grafana panel, RunicEditor live attach | Engine, Platform |
| [[Slice 40 Water bodies\|40. Water bodies]] | A descending river crosses two cells without a seam | Engine |
| [[Slice 41 Floating and swimming\|41. Floating and swimming]] | A platform floats, a crate drifts, a character swims | Engine |
| [[Slice 42 Ships wind and currents\|42. Ships, wind and currents]] | A sailing ship is faster downstream and with a favorable wind; a crosswind pushes it sideways | Engine, Game |
| [[Slice 42a Water and currents on screen\|42a. Water and currents on screen]] | River and ocean surfaces draw; currents and wind show as arrows and heatmaps | Engine |
| [[Slice 42b Ships across borders\|42b. Ships across borders]] | A ship with passengers and cargo sails from simulation A into B with nothing lost | Engine |
| [[Slice 43 Tides waves and weather\|43. Tides, waves and weather]] | A tide opens a path; a storm reaches two simulations at the same world time | Engine, Game, Platform |
| [[Slice 43a Living world\|43a. Living world]] | A caravan follows its route by world time and is where it should be when a player arrives; a player delays it and the delay fades back into the routine | Engine, Game |
| [[Slice 44 Expansion\|44+. Expansion]] | Housing, economy, instances, shop island, the sky world and world transitions, busy-area partitions, placement by traffic and local links, the production look… | All |

---

↑ [[index|RunicDocs]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
