---
title: "PBND-4 · NATS in the services bridge"
aliases:
  - "PBND-4"
tags:
  - "runicengine"
  - "package"
  - "repo/platform"
id: "PBND-4"
module: "PBND Server bindings"
slice: "30"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

**Package:** NATS in the services bridge: durable facts published from the outbox; world directives and other subscriptions delivered to the inbox at safe ticks

**Done when:** A fact published from a tick reaches a test subscriber once; a slow broker never delays a tick

**Needs:** [[PBND-1|PBND-1]], [[PSDK-3|PSDK-3]]

**Slice:** [[Slice 30 Quests|Slice 30 · Quests]]

**Module:** [[PBND Server bindings|PBND · Server bindings]] (Platform)

**Defined in:** [[Platform|Technical Architecture v4 › Platform]]

---

Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) · exported 2026-11-03
