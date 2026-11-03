---
title: "PTR-2 · Connect-ticket verification inside the simulation"
aliases:
  - "PTR-2"
tags:
  - "runicengine"
  - "package"
  - "repo/platform"
id: "PTR-2"
module: "PTR Transport"
slice: "12"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** Connect-ticket verification inside the simulation (signature, expiry, key ID) against a configured set of public keys; tickets are test-signed with a local key until [[PCS-1|PCS-1]] issues real ones

**Done when:** Bad or expired tickets are rejected with no service call

**Needs:** [[PTR-1|PTR-1]]

**Slice:** [[Slice 12 Transport|Slice 12 · Transport]]

**Module:** [[PTR Transport|PTR · Transport]] (Platform)

**Defined in:** [[Platform|Technical Architecture v4 › Platform]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
