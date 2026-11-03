---
title: "WORLD-3 · Activation"
aliases:
  - "WORLD-3"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "WORLD-3"
module: "WORLD World"
slice: "21"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Activation: per-player asymmetric ellipsoid [[World space coordinates cells and activation#Activation volumes|activation volumes]], their union, prepare, commit and release hysteresis, load and unload requests per cell

**Done when:** Walking back and forth on an edge never thrashes loads; a cell far above or below the player stays unloaded until approached

**Needs:** [[WORLD-2|WORLD-2]]

**Slice:** [[Slice 21 World partitions|Slice 21 · World partitions]]

**Module:** [[WORLD World|WORLD · World]] (Engine)

**Defined in:** [[Engine simulation core|Technical Architecture v4 › Engine: simulation core]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
