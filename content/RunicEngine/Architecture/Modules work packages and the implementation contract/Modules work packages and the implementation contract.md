---
title: "Modules, work packages and the implementation contract (Engine, Platform, Game)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game)"
created: "2026-10-14"
modified: "2026-10-30"
---

The code is organized at two working sizes. A **module** is a build target with one owner, a public interface and its own tests; the dependency rules are written between modules. A **work package** is what one Claude Code session implements and one pull request delivers: one subsystem of one module, with its tests. Modules keep the architecture honest; packages keep each piece of work small enough to be built well.

## Contents

- [[Sizes of work|Sizes of work]]
- [[Why the code is segmented this way|Why the code is segmented this way]]
- [[Module contract|Module contract]]
- [[Dependency rules|Dependency rules]]
- [[Work packages|Work packages]]
- [[Building with Claude Code|Building with Claude Code]]
- [[Maturity stages|Maturity stages]]
- [[Parallel work|Parallel work]]
- [[Automated checks|Automated checks]]

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Repositories build targets and processes|Repositories, build targets and processes]] · [[Application and LayerStack|Application and LayerStack (Engine)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) · exported 2026-11-03
