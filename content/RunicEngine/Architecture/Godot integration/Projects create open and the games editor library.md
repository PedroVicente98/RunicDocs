---
title: "Projects: create, open and the game’s editor library"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › Projects: create, open and the game’s editor library"
created: "2026-10-14"
modified: "2026-10-30"
---

The Engine is distributed ready to use and knows no game: the [[Tools#RunicEditor|RunicEditor]] opens with no project, creates a new one from a template or opens an existing one. RunicGame is one such project.

```text
RunicEngine/ (distribution)
  bin/        RunicEditor, libgodot (editor and template targets), Cooker tools
  sdk/        Engine headers and libraries (Core, Simulation, Network, Client, GodotBridge…) + godot-cpp
  templates/  runic-mmo/  (the new-project template)
  platform/   Go SDK and Platform core services

MyGame/
  project.godot             ← what Godot opens
  runic.project.json        ← Runic manifest: Engine version, paths, executables, cook settings
  game_editor.gdextension   ← loads the game's editor library
  Content/                  ← assets, world and region scenes, UI scenes (Godot imports these)
  Data/                     ← schema-backed definitions: skills, items, AI, quests, spawn rules
  Tools/                    ← editor tools in GDScript (never reach the client)
  Source/    (.gdignore)
    Shared/ Server/ Client/ ← the game's C++: Flecs systems, rules, behaviors
    Editor/                 ← the game's marker nodes and docks
  Services/  (.gdignore)    ← Go: the game's services on the Platform SDK
  Build/     (.gdignore)    ← binaries and cooked packages
  CMakeLists.txt  go.work
```

An empty .gdignore file keeps a folder out of Godot’s importer, so code and binaries never clutter the asset panel.

```json
{
  "runic": 1,
  "engine": "0.4.0",
  "game": { "name": "RunicGame" },
  "paths": { "content": "Content", "data": "Data", "source": "Source",
             "services": "Services", "cooked": "Build/Cooked" },
  "executables": { "server": "RunicGameServer", "client": "RunicGameClient" },
  "cook": { "world": "Content/World.tscn", "cellSizeM": 64, "clientPck": "Build/Client/game.pck" }
}
```

1. The RunicEditor opens in Godot’s project manager, with **New** and **Open**.

2. **New** copies templates/runic-mmo/ and creates the whole layout above. How the project manager offers it is an open decision: a small patch in the project manager, or a Runic plugin that offers to initialize an empty project.

3. **Open** loads an existing project. The project manager opens a project by relaunching its own executable with –path; with LibGodot that executable is the RunicEditor, so its main passes the arguments to Godot unchanged.

**The game’s editor library.** A distributed RunicEditor cannot have a game’s C++ compiled in. The game’s marker nodes and docks (Source/Editor) become a library of the project, loaded by the editor through Godot’s GDExtension mechanism, which reloads it with the editor open. The Engine lives inside the RunicEditor; the game enters through this library, the same model as Unreal’s generic editor plus project module.

; game\_editor.gdextension, at the project root  
\[configuration\]  
entry\_symbol \= "game\_editor\_init"  
compatibility\_minimum \= "4.6"  
reloadable \= true

\[libraries\]  
windows.editor.x86\_64 \= "res://Build/bin/game\_editor.dll"  
linux.editor.x86\_64   \= "res://Build/bin/libgame\_editor.so"

The game’s server and client do not load libraries this way: the project’s CMake builds them against the Engine sdk/, like the v3 executables.

---

↑ [[Godot integration|Godot integration (Engine)]] · ← [[How the Engine uses Godot|How the Engine uses Godot]] · [[Game code and the Run button|Game code and the Run button]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › Projects: create, open and the game’s editor library · exported 2026-11-03
