---
title: "BUILD-1 · Build skeleton in all three repositories"
aliases:
  - "BUILD-1"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "BUILD-1"
module: "BUILD Build skeleton"
slice: "0"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Build skeleton in all three repositories: runic\_add\_module helper, presets, CI, the chosen test framework, automated headless and forbidden-dependency checks, submodule pins (Game pins Engine and Platform; Platform pins Engine; Engine pins Godot and godot-cpp at a release tag) with a local option for sibling checkouts, an AVX2 (x86-64-v3) CPU baseline; libgodot built from source in the editor and template targets with the module lists and the SCons cache; libgodot, godot-cpp, [[How the Engine uses Godot|GodotBridge]] and GodotTools catalogued as presentation

**Done when:** Every repository configures and builds; libgodot builds in both targets; the server target links no graphics library and no Godot; a forbidden link fails CI

**Needs:** —

**Slice:** [[Slice 00 Build skeleton|Slice 0 · Build skeleton]]

**Module:** [[BUILD Build skeleton|BUILD · Build skeleton]] (Engine)

**Defined in:** [[Engine foundation|Technical Architecture v4 › Engine: foundation]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
