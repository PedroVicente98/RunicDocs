---
title: "Executables and Godot targets"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › Executables and Godot targets"
created: "2026-10-14"
modified: "2026-10-30"
---

Godot is one source tree compiled as a library in two targets: **editor** (the editor, importers and project manager) and **template** (runtime only: rendering, audio, input and resource loading). Each executable links the target it needs; the server links none.

| Executable | Built by | Godot | Runs |
| :---- | :---- | :---- | :---- |
| GameServer | The project’s CMake | None | Engine (simulation, network, world) \+ RunicGame::Server \+ RunicGame::Shared; the v3 server layers |
| GameClient (shipping) | The project’s CMake | Template target | Engine (network, prediction, extraction) \+ RunicGame::Client \+ RunicGame::Shared; reads the exported .pck |
| GameClient (development) | The project’s CMake | Editor target | The same client reading the project folder directly, without export, as Godot’s own play button does |
| [[Tools#RunicEditor\|RunicEditor]] | The Engine distribution | Editor target | The Godot editor \+ Runic tools (GodotTools) \+ [[Cooker\|the Cooker]]; loads the open project’s editor library |
| Cooker on build machines | — | Editor target, no window | The RunicEditor in headless mode with cook and export arguments |
| [[Tools#Testing at scale\|RunicBot]] | The Engine | None | The client runtime without presentation, many bot sessions per process, for scale tests |

```text
GameServer  = Engine (sim, network, world) + Game::Server + Game::Shared
              → no Godot

GameClient  = Engine (network, prediction, extraction) + Game::Client + Game::Shared
              + libgodot → window, rendering, input, audio, UI
              prediction in double → RenderFrame in float → Godot

RunicEditor = libgodot (editor) + Runic tools + Cooker
              + the open project's editor library
```

The inversion that organizes everything: **Godot does not use the client; the client uses Godot.** Inside the client, Godot does not know an MMO exists. It receives RenderingServer calls from the presenter, the UI scenes and the sounds. The “Godot renderer” is the same RenderingServer in both executables: in the editor it draws the authoring viewport, in the client the game.

---

↑ [[Godot integration|Godot integration (Engine)]] · ← [[Role of Godot decided|Role of Godot (decided)]] · [[How the Engine uses Godot|How the Engine uses Godot]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › Executables and Godot targets · exported 2026-11-03
