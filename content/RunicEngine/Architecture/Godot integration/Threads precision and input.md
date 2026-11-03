---
title: "Threads, precision and input"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › Threads, precision and input"
created: "2026-10-14"
modified: "2026-10-30"
---

* **Threads:** Godot’s scene tree is not thread-safe. Prediction and extraction run on Runic workers; the presenter applies everything on Godot’s main thread, and the [[RenderData in Core|RenderFrame]] stays double-buffered as in v3.

* **Precision:** Godot stays in single precision (no double-precision Godot build). The RenderFrame is camera-relative, and the presenter keeps its own origin, rebased about every 4 km (see Client runtime).

* **Input:** Godot owns the window, so input is born there. Godot’s UI consumes first, and what is left becomes an AppEvent that goes down the [[Application and LayerStack|LayerStack]]: the v3 rule “the top handles first” unchanged.

---

↑ [[Godot integration|Godot integration (Engine)]] · ← [[Godot plugins|Godot plugins]] · [[Risks (Godot integration)|Risks (Godot integration)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › Threads, precision and input · exported 2026-11-03
