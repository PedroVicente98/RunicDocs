---
title: "NET-7 · Diagnostics layer"
aliases:
  - "NET-7"
tags:
  - "runicengine"
  - "package"
  - "repo/engine"
id: "NET-7"
module: "NET Network"
slice: "39"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Diagnostics layer: network and replication metrics recorded in the Core metrics registry; [[Tools#RunicEditor|RunicEditor]] attach channel over a development socket transport inside Network, streaming debug shapes and the traces modules publish in Core’s debug-stream registry (compiled only into development and staging builds)

**Done when:** The RunicEditor attaches to a development server and sees its shapes; a production build has no attach endpoint

**Needs:** [[NET-1|NET-1]], [[CORE-2|CORE-2]]

**Slice:** [[Slice 39 Operations|Slice 39 · Operations]]

**Module:** [[NET Network|NET · Network]] (Engine)

**Defined in:** [[Engine networking|Technical Architecture v4 › Engine: networking]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
