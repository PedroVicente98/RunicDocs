---
title: "Automated checks"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Automated checks"
created: "2026-10-14"
modified: "2026-10-30"
---

| Check | Catches |
| :---- | :---- |
| Headless build of GameServer | Godot, UI, audio or editor code reaching the server |
| Dependency check per module | Links outside the allowed list; includes of another module’s Source/ |
| Public-header scan | Library types in Public/, and Godot types outside [[How the Engine uses Godot\|GodotBridge]] and GodotTools |
| Client export check | Scripts, editor-only classes or Tools/ content in the client .pck |
| Module tests | The Done when behavior of every merged package |
| Docs check | A code change without its ARCHITECTURE.md or package-status update |

---

↑ [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · ← [[Parallel work|Parallel work]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Automated checks · exported 2026-11-03
