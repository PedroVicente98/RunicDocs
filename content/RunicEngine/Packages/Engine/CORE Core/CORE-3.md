---
title: "CORE-3 · RenderData foundation"
aliases:
  - "CORE-3"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "CORE-3"
module: "CORE Core"
slice: "5"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** RenderData foundation: the double-buffered [[RenderData in Core|RenderFrame]] and DebugGeometry (lines, triangles, text, cached debug meshes)

**Done when:** A frame is written on one thread and read on another with no lock; debug vertices need no conversion before upload

**Needs:** [[CORE-1|CORE-1]]

**Slice:** [[Slice 05 Moving entities|Slice 5 · Moving entities]]

**Module:** [[CORE Core|CORE · Core]] (Engine)

**Defined in:** [[Engine foundation|Technical Architecture v4 › Engine: foundation]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
