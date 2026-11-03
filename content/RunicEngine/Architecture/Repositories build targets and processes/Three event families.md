---
title: "Three event families"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Repositories, build targets and processes › Three event families"
created: "2026-10-14"
modified: "2026-10-30"
---

| Family | Examples | Delivery |
| :---- | :---- | :---- |
| Application events | Key press, resize, UI focus, connection state | [[Application and LayerStack\|LayerStack]]: top layer first, can be marked handled |
| Simulation facts | HitEvent, DamageEvent, EntityKilled, RegionChanged | Tick-safe buffers; every consumer receives them |
| Distributed messages | Quest facts, inventory operations, world-event directives | Transport, gRPC or NATS, with explicit reliability and idempotency |

---

↑ [[Repositories build targets and processes|Repositories, build targets and processes]] · ← [[Four axes that must stay separate|Four axes that must stay separate]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Repositories, build targets and processes › Three event families · exported 2026-11-03
