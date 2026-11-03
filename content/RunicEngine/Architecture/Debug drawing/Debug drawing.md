---
title: "Debug drawing (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Debug drawing (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

Debug drawing is the first thing the client shows through Godot: a debug-draw API that turns shapes into plain DebugGeometry, and GodotBridge layers that draw it with Godot. That alone is enough to debug movement, [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] collision, client reconciliation, attack volumes, projectiles, cells, paths, ships, gliders, water flow and boss telegraphs before any production art exists.

**Core rule:** simulation owns meaning; GodotBridge owns visualization. [[Simulation core Flecs and Jolt#Flecs rules|Flecs]], Jolt, combat, networking and gameplay systems never call Godot.

## Contents

- [[Ownership (Debug drawing)|Ownership]]
- [[Debug-draw API|Debug-draw API]]
- [[Math helpers for wire shapes|Math helpers for wire shapes]]
- [[Shapes|Shapes]]
- [[Drawing DebugGeometry with Godot|Drawing DebugGeometry with Godot]]
- [[Physics debug view Physics extracts GodotBridge draws|Physics debug view (Physics extracts, GodotBridge draws)]]
- [[What to visualize|What to visualize]]
- [[Performance and correctness|Performance and correctness]]
- [[Implementation order and definition of done|Implementation order and definition of done]]

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Tools|Tools (Engine)]] · [[World authoring and cooking|World authoring and cooking (Engine, Game)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Debug drawing (Engine) · exported 2026-11-03
