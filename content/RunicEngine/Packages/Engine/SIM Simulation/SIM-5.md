---
title: "SIM-5 · Service port"
aliases:
  - "SIM-5"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "SIM-5"
module: "SIM Simulation"
slice: "27"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Service port: an outbox of durable operations with stable operation IDs and an inbox of accepted results drained at safe ticks; the Engine interface the Platform services bridge implements, shipped as the header-only Runic::SimulationPort target (Core types only)

**Done when:** A fake port that delivers a result twice is applied once; no I/O callback touches [[Simulation core Flecs and Jolt#Flecs rules|Flecs]]

**Needs:** [[SIM-2|SIM-2]], [[EVT-1|EVT-1]]

**Slice:** [[Slice 27 Accounts and characters|Slice 27 · Accounts and characters]]

**Module:** [[SIM Simulation|SIM · Simulation]] (Engine)

**Defined in:** [[Engine simulation core|Technical Architecture v4 › Engine: simulation core]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
