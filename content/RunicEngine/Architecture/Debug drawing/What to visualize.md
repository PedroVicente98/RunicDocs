---
title: "What to visualize"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine) › What to visualize"
created: "2026-10-14"
modified: "2026-10-30"
---

| System | Visualization | Why |
| :---- | :---- | :---- |
| Movement prediction | Predicted capsule, server sphere, correction arrow | Makes reconciliation error obvious |
| Melee combat | Arc sector or arc volume plus victim capsules | Shows exact spatial coverage and timing |
| Projectiles | Sphere or capsule, direction arrow, past path | Debugs speed, collision and latency |
| Ground AoE | Circle or cylinder at the server-validated point | Separates cursor preview from authoritative placement |
| Boss telegraphs | Cone, ring, line or cylinder | Verifies encounter geometry before VFX |
| Aim assist | Crosshair ray, candidate rays, assist cone | Shows why one entity was picked |
| Cells and interest | AABBs, grid cells, colored boundaries, visibility tiers | Makes spatial ownership and visibility visible |
| Navigation and AI | Path lines, waypoint spheres, query rays, warn, detect and leash radii | Debugs navigation and perception without art |
| Ships and gliders | OBBs, hull bounds, buoyancy points, velocity, current and wind arrows | Exposes water and movement math |

| Meaning | Color |
| :---- | :---- |
| Predicted or local state | Green |
| Authoritative server state | Yellow or orange |
| Damage or harmful volume | Red |
| Healing or beneficial volume | Cyan or green |
| Physics bounds and broadphase | Blue |
| Queries and rays | Magenta or white |
| Inactive or past geometry | Dim gray |

---

↑ [[Debug drawing|Debug drawing (Engine)]] · ← [[Physics debug view Physics extracts GodotBridge draws|Physics debug view (Physics extracts, GodotBridge draws)]] · [[Performance and correctness|Performance and correctness]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) › What to visualize · exported 2026-11-03
