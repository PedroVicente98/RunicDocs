---
title: "GFX-02 · Far Entity Tier"
aliases:
  - "GFX-02"
tags:
  - "ideias"
  - "idea"
  - "status/open"
  - "appendix/rendering-lighting-visibility"
id: "GFX-02"
status: "Open"
created: "2026-11-09"
modified: "2026-11-16"
---

**ID:** GFX-02 · **Status:** Open (future idea, after the vertical slice; very low priority) · **Related:** [[Rendering, lighting and visibility (Engine, Game)#Entity visibility|Entity visibility]], [[Real exploration#Night and lighting|Night and lighting]], [[GFX-01 Visual Style and Character Creation|GFX-01]], [[LIVE-01 Living World|LIVE-01]], [[SHIP-01 Naval Combat Flooding, Repair and Sea Events|SHIP-01]]

From the conversation of 9 November 2026 ([[RunicGame — Appendix Rendering, Lighting and Visibility|RunicGame — Appendix: Rendering, Lighting and Visibility]]). Today entities are sent up to 1 km at most. A far entity tier would show anonymous proxies beyond that, so ships on the horizon, war beacons and smoke columns can be seen from far away without giving away identity.

* Anonymous proxies beyond 1 km: class, position (about 1 m), heading and flags, about 8 to 10 bytes each at 1 Hz; about 1 KB/s per player for 100 proxies. Never an ID, name or gear.  
* Ranges per class from screen size (1080p, 60° vertical field of view): a player is 1.7 px at 1 km; a ship with a 30 m mast is 5.6 px at 5 km, 2.8 px at 10 km and 1.4 px at 20 km; a 200 m smoke column or beam is 37 px at 5 km and 3.7 px at 50 km. So players up to about 2 km, ships up to about 20 to 30 km.  
* Occlusion from baked horizon profiles: 256 m cells (40,000 for the map), 64 directions, 6 distance rings, 30 to 50 MB, about a minute to bake; a test is 20 to 50 ns. Biased toward visible, because the client's renderer hides what is behind a hill anyway.  
* Recomputed only when something changes cell (256 m), not every second: about 1 to 2 ms of CPU per second (0.1% to 0.2% of a core) instead of about half a core with per-pair ray marching.  
* One far-view service per world (Platform): input about 40 KB/s for 5,000 far-visible entities, output 0.5 to 1 KB/s per player.  
* Extras: a channel for landmark event visuals; far proxies for scheduled NPC traffic from the routine service; a spyglass that raises class ranges; an optional horizon check inside 1 km.  
* **Sound cues in the dark:** the same anonymous-event channel that draws silhouettes could carry sound cues (footsteps, casting).  
* References: Valorant's fog of war, DayZ's network bubble, WoW's server visibility by size class, PlanetSide 2 and Sea of Thieves as the warning (ships replicated far, so ESP tools show every ship).  
* Effort: about 3 to 5 weeks.
