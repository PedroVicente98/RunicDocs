---
title: "APP-1 · Entry point, Application, ApplicationHost, Layer, LayerStack…"
aliases:
  - "APP-1"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "APP-1"
module: "APP Application"
slice: "1"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Entry point, Application, ApplicationHost, Layer, [[Application and LayerStack|LayerStack]] with queued changes at safe points, application events, loop policies, RunFrame so a host can drive one frame at a time

**Done when:** Layer order, events top-down until handled, updates bottom-up, safe-point push and pop, no allocation per event

**Needs:** [[CORE-1|CORE-1]]

**Slice:** [[Slice 01 Application and layers|Slice 1 · Application and layers]]

**Module:** [[APP Application|APP · Application]] (Engine)

**Defined in:** [[Engine foundation|Technical Architecture v4 › Engine: foundation]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
