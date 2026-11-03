---
title: "Work packages"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages"
created: "2026-10-14"
modified: "2026-10-30"
---

A package ID is the module prefix plus its build order inside the module: [[CMB-3|CMB-3]] is the third Combat package. Every package is defined by five things:

* **Write scope:** one module folder, its CMake target and its docs. Nothing else is edited.

* **Interface change:** the public headers it adds or changes, approved before the implementation.

* **Done when:** the acceptance behavior, written as automated tests.

* **Needs:** the packages that must be merged first. A package starts only when all of them are merged.

* **Slice:** the roadmap slice that first needs it. Packages are Stage A unless the table says otherwise (see Maturity stages).

Big modules carry several packages; small ones one or two. The tables cover every package through the current roadmap; expansion packages (slice [[Slice 44 Expansion|44]] onward) get their full definition when those slices are planned.

**Prefixes.** Engine: BUILD build skeleton, CORE Core, APP Application, EVT Events, CNT Content, ASSET Assets, ECS, WORLD World, PHYS Physics, SIM Simulation, GPL Gameplay, CMB Combat, FLOW GameplayFlow, QST Quest, PRC Perception, NAV Navigation, AI, ENV Environment, WATER Water, NET Network, DSIM DistributedSimulation, CLI Client, GDB GodotBridge, ANIM Animation, AUD Audio, GDT GodotTools, COOK [[Cooker|Cooker]]. Platform: PCT Contracts, PTR Transport, PSDK Go SDK, PBND Server bindings, PCS Core services, PBB Building blocks, PINF Infrastructure. Game: GAME executables, GSH Shared rules, GSRV Server module, GCL Client module, GCNT content, GSVC Go game services, GNAV naval rules, GWTH weather rules.

## Contents

- [[Engine foundation|Engine: foundation]]
- [[Engine simulation core|Engine: simulation core]]
- [[Engine GameplayAPI group|Engine: GameplayAPI group]]
- [[Engine world systems|Engine: world systems]]
- [[Engine networking|Engine: networking]]
- [[Engine presentation|Engine: presentation]]
- [[Engine tools|Engine: tools]]
- [[Platform|Platform]]
- [[Game|Game]]

---

↑ [[Modules work packages and the implementation contract|Modules, work packages and the implementation contract (Engine, Platform, Game)]] · ← [[Dependency rules|Dependency rules]] · [[Building with Claude Code|Building with Claude Code]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages · exported 2026-11-03
