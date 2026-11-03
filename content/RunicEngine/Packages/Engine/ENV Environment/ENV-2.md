---
title: "ENV-2 · Deterministic wind field with a cyclic baseline routine"
aliases:
  - "ENV-2"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "ENV-2"
module: "ENV Environment"
slice: "42"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Deterministic wind field with a cyclic baseline routine: per-region direction at any angle and a signed speed (0 has no effect; a negative speed reverses the push without changing the angle)

**Done when:** The same position and time give the same wind on two simulations; a negative speed reverses the push without changing its angle

**Needs:** [[ENV-1|ENV-1]]

**Slice:** [[Slice 42 Ships wind and currents|Slice 42 · Ships, wind and currents]]

**Module:** [[ENV Environment|ENV · Environment]] (Engine)

**Defined in:** [[Engine world systems|Technical Architecture v4 › Engine: world systems]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
