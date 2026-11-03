---
title: "Platform modules (Platform)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/platform"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Repositories, build targets and processes › Platform modules (Platform)"
created: "2026-10-14"
modified: "2026-10-30"
---

| Module | Contains | Depends on | Packages |
| :---- | :---- | :---- | :---- |
| Transport (C++) | [[Networking stack sessions and responsiveness#Stack (decided)\|GameNetworkingSockets]] implementation of the Engine transport interface; connect-ticket checks; authoritative and candidate connections; simulation-to-simulation links chosen by locality (in-memory queue, local socket or shared memory, GameNetworkingSockets) | Runic::NetworkTransport (the Engine transport interface), Contracts | [[PTR-1\|PTR-1]] to [[PTR-4\|PTR-4]] |
| Contracts | Protobuf service APIs, published facts and the connect-ticket format, generated for C++ and Go; games add their own messages. Realtime messages are encoded by Runic::Network, not Protobuf | — | [[PCT-1\|PCT-1]] |
| Server bindings (C++) | ServicesBridgeLayer (implements the Engine service port with asynchronous gRPC and NATS; completions queued for safe ticks), LifecycleLayer ([[Platform and operations#Simulation placement\|Agones]] SDK), Prometheus exporter for the Core metrics registry; they implement the Engine’s Layer interface | Engine interface targets only: Runic::Application (Layer), Runic::SimulationPort (service port), Runic::Core (metrics registry); Contracts | [[PBND-1\|PBND-1]] to [[PBND-4\|PBND-4]] |
| Go SDK | Service skeleton, configuration, gRPC and NATS wiring, persistence ([[Physical layout Proposal\|PostgreSQL]]), transactions, migrations, idempotency store, metrics | Contracts | [[PSDK-1\|PSDK-1]] to [[PSDK-3\|PSDK-3]] |
| Core services (Go) | Accounts and entitlements, connect tickets, [[Platform and operations#Simulation placement\|World Coordinator]] (worlds, regions and placement by load and traffic), instance allocation, world directives, chat and party groups, admission | Go SDK | [[PCS-1\|PCS-1]] to [[PCS-7\|PCS-7]] |
| Building blocks (Go) | Item ledger (containers, slots, atomic transfers, operation IDs), currency wallets and transfers that move items and currency in one transaction; mechanisms only, with no game rules | Go SDK | [[PBB-1\|PBB-1]] to [[PBB-3\|PBB-3]] |
| Infrastructure | Local development stack, Agones fleets, Kubernetes manifests, Prometheus and Grafana dashboards | — | [[PINF-1\|PINF-1]], [[PINF-2\|PINF-2]] |

---

↑ [[Repositories build targets and processes|Repositories, build targets and processes]] · ← [[Game modules|Game modules]] · [[Processes|Processes]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Repositories, build targets and processes › Platform modules (Platform) · exported 2026-11-03
