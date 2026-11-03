---
title: "ENV-5 · Weather state and time-boxed overrides"
aliases:
  - "ENV-5"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "ENV-5"
module: "ENV Environment"
slice: "43"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Weather state and time-boxed overrides (effective time and duration) for weather, wind and currents; the baseline routine returns when they end

**Done when:** A storm and a wind event reach two simulations at the same world time and end on schedule, after which the routine resumes

**Needs:** [[ENV-1|ENV-1]]

**Slice:** [[Slice 43 Tides waves and weather|Slice 43 · Tides, waves and weather]]

**Module:** [[ENV Environment|ENV · Environment]] (Engine)

**Defined in:** [[Engine world systems|Technical Architecture v4 › Engine: world systems]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
