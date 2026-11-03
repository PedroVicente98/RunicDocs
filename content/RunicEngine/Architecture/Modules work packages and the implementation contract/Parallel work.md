---
title: "Parallel work"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Parallel work"
created: "2026-10-14"
modified: "2026-10-30"
---

* Packages whose Needs are all merged can run at the same time, each in its own Claude Code session and git worktree. Examples: [[GDB-2|GDB-2]] alongside [[SIM-1|SIM-1]]; [[PCT-1|PCT-1]] alongside [[NET-1|NET-1]]; [[GDT-2|GDT-2]] alongside [[PHYS-1|PHYS-1]].

* Two or three sessions at once is the practical limit, because every contract and pull request still needs your review.

* Two packages that write the same module never run at the same time.

---

↑ [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · ← [[Maturity stages|Maturity stages]] · [[Automated checks|Automated checks]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Parallel work · exported 2026-11-03
