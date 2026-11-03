---
title: "WORLD-2 · Sparse 3D spatial index"
aliases:
  - "WORLD-2"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "WORLD-2"
module: "WORLD World"
slice: "11"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Sparse 3D spatial index (XZ columns holding only occupied Y cells), exact XYZ candidate queries (radius, box, ellipsoid), membership updates; authored volumes (caves, rule areas, indivisible volumes) with point-in-volume queries

**Done when:** Query results match brute force in 3D and draw in the debug view; a point inside a cave volume is reported inside it

**Needs:** [[WORLD-1|WORLD-1]]

**Slice:** [[Slice 11 Spatial index|Slice 11 · Spatial index]]

**Module:** [[WORLD World|WORLD · World]] (Engine)

**Defined in:** [[Engine simulation core|Technical Architecture v4 › Engine: simulation core]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
