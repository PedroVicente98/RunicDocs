---
title: "Principles and performance targets"
tags:
  - "architecture"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

The C++ simulation is the single authority for the world, and every other choice in this document serves two goals: hold a 500-player battle in one region, and never block the 30 Hz tick.

### Non-negotiable principles

1. The C++ simulation is authoritative for everything happening in the world. Clients send intentions; they never decide position, hits, damage, loot or quest completion.

2. The simulation runs headless and never depends on rendering, UI or tools.

3. The engine provides mechanisms; the game provides data and rules. Anything game-specific lives in RunicGame as data or as registered C++ behaviors.

4. Data first: skills, items, effects, AI, light values and balance are data with stable namespaced IDs and versioned schemas, reloadable without recompiling.

5. Nothing blocks the tick: network, service and database work is queued and applied at defined points.

6. Spatial partitions are indexes, not servers. Which process owns what is a separate, explicit assignment.

7. Every feature is built as a vertical slice first, generalized second, hardened third.

8. Performance is measured, not assumed: every clock domain and major system reports its cost per tick.

9. Godot is presentation and tooling only: it renders, plays audio, owns the window, input and player UI, and hosts the editor; it never runs a game rule, and the server never links it.

### Targets

| Target | Value |
| :---- | :---- |
| Players per world | Up to 5,000 concurrent |
| Battle that must feel perfect | 100 vs 100 in one region |
| Largest battle that must still work | 500 players in one region, with graceful degradation |
| Combat and physics rate | 30 Hz |
| Scheduler master clock | 60 Hz |
| World coordinates | 64-bit doubles with a real Y axis; 1 cm minimum unit |
| First world size | About 600 km² per map, land and sea included; underground spaces and floating islands live inside the main world, and the Game’s sky world matches its size |
| Expansion | New continents and regions added to a live world by patch and streamed in seamlessly |
| Engine ceiling | Continent-scale worlds for other teams without architectural change |

### Planning budgets

| Budget | Planning value | Why |
| :---- | :---- | :---- |
| Simulation work per 30 Hz tick | ≤ 25 ms of the 33 ms window at p99 | Headroom for spikes and I/O |
| Download per player in a 500-player battle | ≈ 50 KB/s | Fits any broadband connection |
| Upload per simulation in a 500-player battle | ≈ 25 MB/s | Fits a standard server network card |
| Input to visible action | Immediate on the client; server confirmation within one round trip | Combat feels responsive at any ping |
