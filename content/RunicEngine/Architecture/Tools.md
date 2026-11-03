---
title: "Tools (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Tools (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

The RunicEditor is the Godot editor run through LibGodot with the Runic tools inside; [[Cooker|the Cooker]] runs in it, or in the same binary headless on build machines. Neither is ever distributed to players.

## RunicEditor

* **Godot’s editor, unchanged at its core:** scenes, viewport, inspector, importers, undo and redo, the project manager with New and Open.

* **Runic tools (GodotTools):** marker nodes (volumes, spawn areas, interactables, routes, colliders, water bodies, regions), inspectors generated from schemas for Runic data files, region tools, the “see what the server sees” layer, assistants that generate code, the Run button.

* **Docks:** world, ECS and physics inspectors; the behavior-tree editor on GraphEdit with a live NPC debugger; a resolver debugger that shows which rules applied to a hit and why it landed or missed.

* **Live attach** to development and staging servers through the GameServer’s Diagnostics layer, drawing the server’s debug shapes in the viewport.

* **The project’s editor library** adds the game’s own marker nodes and docks and reloads with the editor open.

## Cooker

Turns the project’s scenes, imported assets and data into runtime formats: server packages (collision, nav tiles, cells, volumes, spawn areas, water fragments, rules) and client packages (cell visual lists, client-safe data, nearby collision), next to the .pck that Godot’s export writes. It runs inside the RunicEditor from an export plugin, in the background with progress so a long cook never freezes the editor, and on build machines as the RunicEditor without a window. See World authoring and cooking.

## Debug drawing

Debug drawing is the eyes of the RunicEditor and of development clients; its design is in the Debug drawing section below.

## Testing at scale

Because the client runtime is separated from Godot by the [[RenderData in Core|RenderFrame]], a bot is the client without the drawing part. Scale is tested in three layers.

| Layer | What it is | What it measures | Realistic scale |
| :---- | :---- | :---- | :---- |
| 1\. Agents inside the server | Fake players created directly in the simulation, no network | Simulation CPU: combat, AI, physics, snapshot building | 500 in one region, on one machine |
| 2\. Network bots without rendering | RunicBot: the client runtime with a simple brain (walk, fight, follow a quest), many bots per process | Transport, replication, interest, [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]], services | Hundreds per process; thousands need several machines |
| 3\. Real clients | The development client joining in | Rendering, UI and game feel | One or a few |

A real client receives only what interest sends: by the v3 budget, the roughly 100 most relevant at 20 Hz, the rest at 5 Hz, and Hidden players never. A crowd rendering test is therefore up to about 500 visible in a battle, never 10,000 on screen. At about 50 KB/s per player in battle, 1,000 bots in one fight make the bot machine receive 50 MB/s, about 400 Mbit/s; outside battle each bot drops to a few KB/s. Ten thousand players is a distributed test with several simulations (the v3 target is 5,000 per world) and bots spread over a few cloud machines; locally, layer 1 plus a few hundred layer 2 bots cover almost everything.

## Metrics every process exports

* **Per simulation tick:** time per clock domain and per major system (p50, p95, p99), backlog, [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] counts, queries, events, worker utilization, time per layer.

* **Per client:** replication bytes, entities per visibility tier, snapshot age, presenter time and instance count.

* **Per simulation:** CPU, players, bandwidth, handoffs, ghosts.

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Audio|Audio (Engine, Game)]] · [[Debug drawing|Debug drawing (Engine)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Tools (Engine) · exported 2026-11-03
