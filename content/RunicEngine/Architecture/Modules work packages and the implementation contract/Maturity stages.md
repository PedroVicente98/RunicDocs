---
title: "Maturity stages"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Maturity stages"
created: "2026-10-14"
modified: "2026-10-30"
---

| Stage | Meaning | When |
| :---- | :---- | :---- |
| A — vertical proof | The smallest real implementation that proves the module’s boundaries inside a roadmap slice | Every package starts here |
| B — generalize | Broader interface and data coverage once a second real consumer exists | When a later slice needs more |
| C — harden | Performance, scale, recovery, tooling, compatibility and adversarial tests | Battle scale, operations and pre-launch slices |

A consumer never waits for its dependency to reach Stage C; vertical slices validate the architecture first, then it is generalized and hardened.

---

↑ [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · ← [[Building with Claude Code|Building with Claude Code]] · [[Parallel work|Parallel work]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Maturity stages · exported 2026-11-03
