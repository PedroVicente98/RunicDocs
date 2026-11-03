---
title: "GDB-1 · GodotLayer"
aliases:
  - "GDB-1"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "GDB-1"
module: "GDB GodotBridge"
slice: "1"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** GodotLayer: the LibGodot instance (create, start, iteration, stop) at the top of the client [[Application and LayerStack|LayerStack]]; window from the DisplayServer; input forwarded as AppEvents after Godot’s UI; headless mode

**Done when:** The client starts Godot windowed and headless and exits cleanly; UI clicks never reach the stack

**Needs:** [[APP-1|APP-1]], [[BUILD-1|BUILD-1]]

**Slice:** [[Slice 01 Application and layers|Slice 1 · Application and layers]]

**Module:** [[GDB GodotBridge|GDB · GodotBridge]] (Engine)

**Defined in:** [[Engine presentation|Technical Architecture v4 › Engine: presentation]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
