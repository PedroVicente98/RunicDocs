---
title: "Sizes of work"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Sizes of work"
created: "2026-10-14"
modified: "2026-10-30"
---

| Size | What it is | Example | Who uses it |
| :---- | :---- | :---- | :---- |
| Group | A folder plus an umbrella build target that links related modules under one name; no code of its own | Runic::GameplayAPI \= Gameplay, Combat, [[Scripted sequences GameplayFlow and restrictions\|GameplayFlow]], Quest | The Game links one name; the documents categorize by it |
| Module | A CMake target with its own folder, public headers, tests and ARCHITECTURE.md; the unit of ownership and dependency | Runic::Combat | Other modules link it and include only its public headers |
| Subsystem | A folder inside a module’s Source/; not linkable on its own | Combat/Cooldowns | Only its own module |
| Work package | One Claude Code session and one pull request: a subsystem, or part of one, at a stated maturity stage, with its tests and docs | [[CMB-3\|CMB-3]]: statuses, cooldowns and resource costs | You review and merge it; the roadmap lists it |

---

↑ [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · [[Why the code is segmented this way|Why the code is segmented this way]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Sizes of work · exported 2026-11-03
