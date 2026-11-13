---
title: "Tools (Engine)"
tags:
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-13"
---

The RunicEditor is the Godot editor run through LibGodot with the Runic tools inside; the Cooker runs in it, or in the same binary headless on build machines. Neither is ever distributed to players.

### RunicEditor

* **Godot’s editor, unchanged at its core:** scenes, viewport, inspector, importers, undo and redo, the project manager with New and Open.

* **Runic tools (GodotTools):** marker nodes (volumes, spawn areas, interactables, routes, colliders, water bodies, regions), inspectors generated from schemas for Runic data files, region tools, the “see what the server sees” layer, assistants that generate code, the Run button.

* **Docks:** world, ECS and physics inspectors; the behavior-tree editor on GraphEdit with a live NPC debugger; a resolver debugger that shows which rules applied to a hit and why it landed or missed.

* **Live attach** to development and staging servers through the GameServer’s Diagnostics layer, drawing the server’s debug shapes in the viewport.

* **The project’s editor library** adds the game’s own marker nodes and docks and reloads with the editor open.

* **Editor UI that fits the editor.** Runic tools add UI only through the editor’s own extension points (docks, the bottom panel, a main-screen tab, inspector plugins, Project › Tools and context menus) and take their colors, fonts, icons and sizes from the editor theme and the editor scale, so they look like the rest of the editor. They never insert controls into a container whose layout they do not own: the slice 0 spike’s toolbar button sat at the far right of the top bar and broke it. Player UI follows the same rule with the project’s own Theme resources.

### Authoring path for every system

Every system ships with the tools to create its content, and creating content for it must be easy. The path has two levels, both on the same Runic API (see [[Simulation core Flecs and Jolt (Engine)#The Runic API over Flecs and Jolt|The Runic API over Flecs and Jolt]]):

* **Base, in the slice that adds the system:** its items registered with their metadata, a data format for its content and validation in the Cooker. Content is written as data files from day one, and the Cooker reports unknown IDs, a trigger on a state that is not observable and a write to a state the content does not own.

* **Visual, later:** a dock in the RunicEditor (a quest editor with a palette of triggers, conditions and actions, for example) that writes the same data files through the same API. It comes when the amount of content justifies it.

* **One registration, many consumers.** The registry that the runtime uses also fills the editor’s palettes and the Cooker’s checks. (Proposal: the same registry generates a reference page of the vocabulary for RunicDocs.)

* **Assistants** create new vocabulary items (a state, a condition, a trigger, a volume kind): the C++ registration, a test and the entry in the reference.

* **Obsidian notes are for the creative process only.** Quest and other content definitions live in the project’s data format (the versioned schemas of CNT-2), not in the notes.

### Cooker

Turns the project’s scenes, imported assets and data into runtime formats: server packages (collision, nav tiles, cells, volumes, spawn areas, water fragments, rules) and client packages (cell visual lists, client-safe data, nearby collision), next to the .pck that Godot’s export writes. It runs inside the RunicEditor from an export plugin, in the background with progress so a long cook never freezes the editor, and on build machines as the RunicEditor without a window. See World authoring and cooking.

### Debug drawing

Debug drawing is the eyes of the RunicEditor and of development clients; its design is in the Debug drawing section below.

### Testing at scale

Because the client runtime is separated from Godot by the RenderFrame, a bot is the client without the drawing part. Scale is tested in three layers.

| Layer | What it is | What it measures | Realistic scale |
| :---- | :---- | :---- | :---- |
| 1\. Agents inside the server | Fake players created directly in the simulation, no network | Simulation CPU: combat, AI, physics, snapshot building | 500 in one region, on one machine |
| 2\. Network bots without rendering | RunicBot: the client runtime with a simple brain (walk, fight, follow a quest), many bots per process | Transport, replication, interest, handoff, services | Hundreds per process; thousands need several machines |
| 3\. Real clients | The development client joining in | Rendering, UI and game feel | One or a few |

A real client receives only what interest sends: by the v3 budget, the roughly 100 most relevant at 20 Hz, the rest at 5 Hz, and Hidden players never. A crowd rendering test is therefore up to about 500 visible in a battle, never 10,000 on screen. At about 50 KB/s per player in battle, 1,000 bots in one fight make the bot machine receive 50 MB/s, about 400 Mbit/s; outside battle each bot drops to a few KB/s. Ten thousand players is a distributed test with several simulations (the v3 target is 5,000 per world) and bots spread over a few cloud machines; locally, layer 1 plus a few hundred layer 2 bots cover almost everything.

### Metrics every process exports

* **Per simulation tick:** time per clock domain and per major system (p50, p95, p99), backlog, Jolt counts, queries, events, worker utilization, time per layer.

* **Per client:** replication bytes, entities per visibility tier, snapshot age, presenter time and instance count.

* **Per simulation:** CPU, players, bandwidth, handoffs, ghosts.
