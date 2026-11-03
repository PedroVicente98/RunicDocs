---
title: "Risks (Godot integration)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › Risks"
created: "2026-10-14"
modified: "2026-10-30"
---

* **LibGodot is new:** one instance per process, desktop platforms only. The editor as a library is the least tested path; the slice [[Slice 00 Build skeleton|0]] spike proves it, and the open fallback decision covers a failure.

* **Build and version:** building Godot from source takes tens of minutes without a cache, and moving from 4.x to 4.y becomes a decision with tests.

* **Editor without GDScript:** the editor target must build and open without the module; the spike confirms it.

* **Module names change between versions:** the module lists are reviewed at every update.

* **Code RmlUi would have given:** the view-model binder is Runic’s own.

* **Arguments:** the project manager relaunches the executable with –path; main must pass every argument to Godot.

---

↑ [[Godot integration|Godot integration (Engine)]] · ← [[Threads precision and input|Threads, precision and input]] · [[Open decisions|Open decisions]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › Risks · exported 2026-11-03
