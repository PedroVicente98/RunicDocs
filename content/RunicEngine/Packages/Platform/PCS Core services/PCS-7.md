---
title: "PCS-7 · Placement by load and traffic over Agones"
aliases:
  - "PCS-7"
tags:
  - "runicengine"
  - "package"
  - "repo/platform"
id: "PCS-7"
module: "PCS Core services"
slice: "44+"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Placement by load and traffic over [[Platform and operations#Simulation placement|Agones]]: scores by load, memory and inter-simulation traffic, with distance from the regions’ global coordinates; moves high-traffic pairs onto one node by move-by-[[Networking replication interest and handoff#Simulations, handoff and ghosts|handoff]], up to a per-node cap

**Done when:** Two simulations with heavy link traffic end on one node with no loading screen; no node passes its cap

**Needs:** [[PCS-2|PCS-2]], [[PINF-2|PINF-2]], [[PTR-4|PTR-4]]

**Slice:** [[Slice 44 Expansion|Slice 44+ · Expansion]]

**Module:** [[PCS Core services|PCS · Core services]] (Platform)

**Defined in:** [[Platform|Technical Architecture v4 › Platform]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
