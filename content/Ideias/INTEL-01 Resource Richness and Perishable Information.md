---
title: "INTEL-01 · Resource Richness and Perishable Information"
aliases:
  - "INTEL-01"
tags:
  - "ideias"
  - "idea"
  - "status/open"
id: "INTEL-01"
status: "Open"
source: "RunicGame — Ideias"
source_url: "https://docs.google.com/document/d/17LDd3TGBar3XuFIUUvtsdGn95Op5B6Lsv7XYVe7Meow/edit"
created: "2026-10-17"
modified: "2026-11-03"
---

**ID:** INTEL-01 · **Status:** Open

Map discovery is account-wide ([[FAM-01 Account and Alts and The Family|FAM-01]]), so permanent knowledge has finite demand: with 200 nodes and 5 layers, an account needs at most 1,000 charts, ever. Cartography keeps working by selling information that goes stale. The permanent layers are bought once per account: the base layer, species and dens, spawn areas, event locations and Altars.

**Resource richness.** Each cycle, every resource spawn area rolls a richness: poor, normal, rich or abundant (ex.: 0.6×, 1×, 1.4× and 2× yield; rich spots also raise quality and the double-yield chance). Cycles are staggered by resource family, so there is no single reset day (ex.: ore weekly, wood every 5 days, herbs every 3 days, fish schools moving with the currents within hours). Richness is deterministic from the node, the family and the cycle number, and the node's prosperity tilts the odds. Without a report, you only learn that a spot is rich after gathering there; with one, you see the richness overlay for the whole node. Cost: about 40 spawn areas × 1 byte per family per node, sent only to chart owners.

**Perishable information:**

* **Richness report** (resources): until the cycle ends; an overlay and highlights; for gatherers.  
* **Rare veins and blooms** (resources): during their window; a marker while active; for gatherers and crafters.  
* **Fish schools** (environment): hours to days; school markers at sea; for sport fishers.  
* **Patrol timetables** (fauna): fade with the drift; patrol timing and aggro radius; for everyone.  
* **Rare spawns and lair state** (fauna): until killed; the den marker and whether the alpha is there; for hunters and bestiary studies.  
* **Migrations** (fauna): a season; herd routes; for hunters, leatherworkers and husbandry.  
* **Event timetables** (events): fade with the drift; timers and exact locations; for everyone.  
* **NPC convoy and ship schedules** (events): fade with the drift; routes and timing; for pirates and escorts.  
* **Storm forecasts** (environment): days; storm, rogue wave and whirlpool warnings; for sailors.  
* **Current event predictions** (environment): until the event; predicted changes to the currents; for sailors and gliders.  
* **Route charts** (environment and danger): a week; a route plotted with the currents and recorded danger; for trade-pack runners.

**Shelf life.** Every perishable chart stores when it was surveyed. Snapshots, like richness, end with the cycle; timetables fade with the drift ([[LIVE-01 Living World|LIVE-01]]), shown as a reliability bar. Proficiency extends shelf life because masters predict the drift (ex.: a novice's timetable drifts about 2 minutes a day and lasts about a week; a master's drifts about 0.5 minutes a day and lasts about 4 weeks). Reading a chart unlocks it for the Lineage and consumes it. All of this is efficiency, never a requirement (pillar 8).

**Open:** tides, which would add an environment layer and content at low tide.
