---
title: "PHYS-4 · Jolt job system on the Core worker pool"
aliases:
  - "PHYS-4"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "PHYS-4"
module: "PHYS Physics"
slice: "10"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] job system on the Core worker pool: a JobSystem adapter inside Physics, so Jolt never owns threads

**Done when:** A physics step on the pool matches a single-thread step; no thread is created outside the pool

**Needs:** [[PHYS-1|PHYS-1]], [[CORE-2|CORE-2]]

**Slice:** [[Slice 10 Worker pool|Slice 10 · Worker pool]]

**Module:** [[PHYS Physics|PHYS · Physics]] (Engine)

**Defined in:** [[Engine simulation core|Technical Architecture v4 › Engine: simulation core]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
