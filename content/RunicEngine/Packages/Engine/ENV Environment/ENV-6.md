---
title: "ENV-6 · World routines"
aliases:
  - "ENV-6"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "ENV-6"
module: "ENV Environment"
slice: "43a"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** World routines: cooked routes and schedules evaluated as position \= f(route, world time, seed), with slow deterministic drift (a cycle that does not match the clock plus a small seeded variation)

**Done when:** Two simulations compute the same routine position at the same world time, drift included

**Needs:** [[ENV-1|ENV-1]]

**Slice:** [[Slice 43a Living world|Slice 43a · Living world]]

**Module:** [[ENV Environment|ENV · Environment]] (Engine)

**Defined in:** [[Engine world systems|Technical Architecture v4 › Engine: world systems]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
