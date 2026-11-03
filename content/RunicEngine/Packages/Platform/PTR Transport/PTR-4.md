---
title: "PTR-4 · Simulation links chosen by locality"
aliases:
  - "PTR-4"
tags:
  - "runicengine"
  - "package"
  - "repo/platform"
id: "PTR-4"
module: "PTR Transport"
slice: "44+"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Simulation links chosen by locality: an in-memory queue in one process, a local socket or shared-memory channel on one machine, [[Networking stack sessions and responsiveness#Stack (decided)|GameNetworkingSockets]] between machines

**Done when:** The same transfer test passes on every channel with identical results; the link picks its channel from the peers’ placement

**Needs:** [[PTR-3|PTR-3]]

**Slice:** [[Slice 44 Expansion|Slice 44+ · Expansion]]

**Module:** [[PTR Transport|PTR · Transport]] (Platform)

**Defined in:** [[Platform|Technical Architecture v4 › Platform]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
