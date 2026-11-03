---
title: "Role of Godot (decided)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › Role of Godot (decided)"
created: "2026-10-14"
modified: "2026-10-30"
---

| \# | Decision | What it means |
| :---- | :---- | :---- |
| 1 | Godot via LibGodot from slice [[Slice 00 Build skeleton\|0]] | It is in the first build, even idle or headless, and every slice pulls one piece of presentation or tooling into it |
| 2 | Godot is interface and renderer only | Authoring editor, rendering, window, input, audio and UI; it never runs a game rule |
| 3 | The server has no Godot | GameServer stays purely headless, as in v3 |
| 4 | The RenderFrame is the only door | Godot never reads [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]], [[Simulation core Flecs and Jolt#Jolt rules\|Jolt]] or domain modules; only [[How the Engine uses Godot\|GodotBridge]] talks to it |
| 5 | Prediction runs in the Runic simulation | The client predicts with Flecs, Jolt in double precision and RunicGame::Shared, the same code as the server |
| 6 | No gameplay nodes; GDScript out of the game | Nodes exist only for authoring (marker nodes) and player UI; no game entity is a node; GDScript is an editor tool language only |
| 7 | Godot built from source with modules removed | No fork; small documented patches only if something requires one |
| 8 | The Engine is not a plugin | Runic code talks to Godot through the GDExtension API (godot-cpp) compiled into Runic executables; only the game’s own editor code is a loaded library |
| 9 | The Engine is game-agnostic | The [[Tools#RunicEditor\|RunicEditor]] opens with no project and offers New project (from a template) and Open |
| 10 | Runic nodes are representation only | Spawn areas, volumes, interactables, water and colliders exist in the editor; [[Cooker\|the Cooker]] writes placements and the Engine creates everything by its own rules |
| 11 | One source, two outputs | The Cooker writes server and client packages from the same scenes; the client’s visual assets come from Godot’s importer and export |
| 12 | Player UI in Godot | Godot UI scenes (Control), including diegetic panels; nameplates and damage numbers on the batched path |
| 13 | Code in an external IDE, assistants in the editor | No embedded code editor; New Flecs system, New Go service and similar assistants generate the files |
| 14 | One Run button | It compiles what changed, cooks, keeps the local stack running and connects a development client |

![[arch-godot-in-the-editor-and-the-client-the-server-neve.png]]
*Godot in the editor and the client — the server never sees it*

*Godot in the editor and the client — the server never sees it*

The editor cooks one source into two outputs: the server runs without Godot, and on the client Godot only receives the [[RenderData in Core|RenderFrame]] the Runic runtime produces.

---

↑ [[Godot integration|Godot integration (Engine)]] · [[Executables and Godot targets|Executables and Godot targets]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › Role of Godot (decided) · exported 2026-11-03
