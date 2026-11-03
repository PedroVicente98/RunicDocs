---
title: "Game code and the Run button"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › Game code and the Run button"
created: "2026-10-14"
modified: "2026-10-30"
---

Game code is always compiled before it runs, and Godot never executes it. The Run button compiles what changed, cooks what changed and starts the processes; most iteration is data and never compiles.

| Written in | Becomes | Runs in |
| :---- | :---- | :---- |
| Source/Shared (rules and shared [[Simulation core Flecs and Jolt#Flecs rules\|Flecs]] systems) | C++ compiled into both executables | The server with authority, the client for prediction |
| Source/Server (AI, quests, loot, server rules) | Part of the server executable | Server only |
| Source/Client (view models, game presentation) | Part of the client executable | Client only |
| Source/Editor (game marker nodes and docks) | The editor library, loaded and reloaded by the editor | Editor only |
| Services/ (Go) | Service binaries | Next to the server |
| Data/ and Content/ | Nothing to compile: cooked, or reloaded live | Read by server and client |

**External IDE and assistants.** C++ and Go are written in an external IDE. The editor generates what the IDE needs (compile\_commands.json for clangd, go.work, VS Code tasks and launch configurations), and a build error in the editor opens the file at its line. Assistants generate template files, register them in CMake or the right registry and open the result in the IDE: **New Flecs system**, **New behavior**, **New quest condition or action**, **New AI node**, **New data type** (a schema), **New marker node** and **New Go service**. Each costs days, the same flow as Unreal’s “New C++ class”.

**What Run does:**

1. Saves and cooks only the changed cells and definitions.

2. Compiles if code changed, with the same CMake the IDE uses, incrementally.

3. Keeps the local stack up: Platform services and the game’s Go services keep running between runs; only a service whose code changed restarts.

4. Starts the local server with the freshly cooked packages.

5. Starts the development client, already connected as one of your characters (or several clients).

RunicGameClient \--project . \--connect 127.0.0.1:7777 \--dev-ticket Build/dev.ticket \--character dev1

| Change | What happens | Typical time (estimate) |
| :---- | :---- | :---- |
| Data (skill, quest, [[Behavior-tree runtime\|behavior tree]]) | Reloads in the running server | Under 1 s |
| Map or asset | Cooks the affected cells and reloads them | A few seconds |
| One game .cpp | Recompiles, relinks and restarts the local server | 10 to 40 s, mostly linking |
| One Go service | go build and a restart of that service only | 2 to 10 s |
| The editor library | Recompiles and reloads inside the open editor | 10 to 30 s |

A server restart loses simulation state, but durable state stays in the services. A development checkpoint on stop returns you exactly where you were, with quests and inventory.

**Login and scenes.** Godot scenes are the UI of the v3 client states: Boot → Login → Server and character select → Loading → World. The Runic client owns the transitions (each state replaces its presentation layer, which shows its Godot UI scene). Login runs inside the client: the screen is Godot’s, the call to the accounts service is Runic code; a separate patching launcher is optional. The world is not a Godot scene: the World state shows the HUD scene while the presenter draws the cells and entities the server sends. Character creation uses a small 3D scene for the model; the data goes to the character service. In development, Run skips the screens with a ticket signed by the local key; to test login itself, run from the login screen.

---

↑ [[Godot integration|Godot integration (Engine)]] · ← [[Projects create open and the games editor library|Projects: create, open and the game’s editor library]] · [[Building Godot|Building Godot]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › Game code and the Run button · exported 2026-11-03
