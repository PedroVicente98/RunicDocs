---
title: "NET-8 · World transitions"
aliases:
  - "NET-8"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "NET-8"
module: "NET Network"
slice: "44+"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** World transitions: the session leaves one world’s simulation after a checkpoint and joins another world’s simulation with a new connect ticket; no [[Networking replication interest and handoff#Simulations, handoff and ghosts|handoff]] or ghosts across worlds

**Done when:** A character moves between two worlds with its checkpointed state, and the old simulation keeps no copy

**Needs:** [[NET-1|NET-1]], [[SIM-5|SIM-5]], [[PCS-1|PCS-1]]

**Slice:** [[Slice 44 Expansion|Slice 44+ · Expansion]]

**Module:** [[NET Network|NET · Network]] (Engine)

**Defined in:** [[Engine networking|Technical Architecture v4 › Engine: networking]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
