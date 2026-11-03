---
title: "CMB-7 · Input queue"
aliases:
  - "CMB-7"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "CMB-7"
module: "CMB Combat"
slice: "19"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Input queue: one queued action per character inside the game-set window, started on the first legal tick; game-named priority inputs skip it when the cancel window allows

**Done when:** An early input fires on the first legal tick; a stun in between cancels it

**Needs:** [[CMB-1|CMB-1]], [[SIM-4|SIM-4]]

**Slice:** [[Slice 19 Combat prototype|Slice 19 · Combat prototype]]

**Module:** [[CMB Combat|CMB · Combat]] (Engine)

**Defined in:** [[Engine GameplayAPI group|Technical Architecture v4 › Engine: GameplayAPI group]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
