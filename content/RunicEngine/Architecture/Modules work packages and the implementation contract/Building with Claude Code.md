---
title: "Building with Claude Code"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Building with Claude Code"
created: "2026-10-14"
modified: "2026-10-30"
---

Every package goes through the same short cycle. It keeps design decisions with you and gives each coding session a closed, testable problem.

1. **Contract session.** Claude Code writes or updates the module’s ARCHITECTURE.md, the public headers the package adds and the acceptance tests, which fail at first. Nothing in Source/ yet.

2. **Contract review.** You approve the interface and the tests or ask for changes. This is the cheapest moment to change a design.

3. **Implementation session.** A fresh session implements Source/ until the tests pass, inside the write scope only. When it needs something from another module, it stops and reports the interface change.

4. **Checks.** CI runs the module tests, the headless server build and the dependency checks.

5. **Code review and merge.** The pull request carries the code, the tests, the updated ARCHITECTURE.md and the package status.

Small packages, with a few hundred lines and no new public types, may combine steps 1 and 3 in one session.

Each repository’s docs folder is written from this document: the shared rules once, one ARCHITECTURE.md per module and the package tables. Claude Code reads those files, so the repositories and this document never disagree.

```text
TASK
  Implement CMB-3 (Stage A): statuses and effects, cooldowns, resource costs.

WRITE SCOPE
  Engine/GameplayAPI/Combat/**   (Public, Source, Tests, ARCHITECTURE.md)
  the Runic::Combat target in CMake

READ-ONLY
  Public headers of Runic::Core, Events, Simulation, Gameplay
  Docs: Engine gameplay APIs, Simulation core, Modules and work packages

APPROVED INTERFACE
  [public headers from the contract session]

DONE WHEN
  [acceptance tests from the package table and ARCHITECTURE.md]

RULES
  - Edit nothing outside the write scope; report needed interface changes.
  - No library types in Public/; the server build stays headless.
  - No game rules, names or numbers; tests use engine: test IDs.
  - Never block a tick on I/O; never mutate Flecs from an I/O callback.
  - Build only what the tests need; no placeholders in other modules.
```

---

↑ [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · ← [[Work packages|Work packages]] · [[Maturity stages|Maturity stages]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Building with Claude Code · exported 2026-11-03
