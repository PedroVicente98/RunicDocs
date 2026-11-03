---
title: "Platform"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Platform"
created: "2026-10-14"
modified: "2026-10-30"
---

The server bindings implement the Engine’s Layer interface and the Simulation’s service port, and depend only on Engine interface targets: Runic::Core, Runic::Application and Runic::SimulationPort (the service port), while the Transport links Runic::NetworkTransport (the transport interface); the Engine never includes them. Those headers include only Core types, so a Platform build configures Core and Application and never [[Simulation core Flecs and Jolt#Flecs rules|Flecs]], [[Simulation core Flecs and Jolt#Jolt rules|Jolt]] or the gameplay modules. Platform CI builds them against the Engine commit pinned as a submodule, so the Platform builds and tests on its own.

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| [[PCT-1\|PCT-1]] | Protobuf service APIs, fact messages and the connect-ticket format; C++ and Go code generation | Both languages round-trip the same message | [[BUILD-1\|BUILD-1]] | [[Slice 12 Transport\|12]] |
| [[PTR-1\|PTR-1]] | [[Networking stack sessions and responsiveness#Stack (decided)\|GameNetworkingSockets]] transport implementing the Engine transport interface | A client and a local server exchange reliable and unreliable messages | [[NET-1\|NET-1]], [[PCT-1\|PCT-1]] | [[Slice 12 Transport\|12]] |
| [[PTR-2\|PTR-2]] | Connect-ticket verification inside the simulation (signature, expiry, key ID) against a configured set of public keys; tickets are test-signed with a local key until [[PCS-1\|PCS-1]] issues real ones | Bad or expired tickets are rejected with no service call | [[PTR-1\|PTR-1]] | [[Slice 12 Transport\|12]] |
| [[PTR-3\|PTR-3]] | Candidate connections (up to three), promotion, simulation-to-simulation links | Promotion happens with no loading screen | [[PTR-2\|PTR-2]], [[DSIM-3\|DSIM-3]] | [[Slice 36 Multiple simulations\|36]] |
| [[PTR-4\|PTR-4]] | Simulation links chosen by locality: an in-memory queue in one process, a local socket or shared-memory channel on one machine, GameNetworkingSockets between machines | The same transfer test passes on every channel with identical results; the link picks its channel from the peers’ placement | [[PTR-3\|PTR-3]] | [[Slice 44 Expansion\|44+]] |
| [[PSDK-1\|PSDK-1]] | Go service skeleton: configuration, gRPC wiring, metrics | A sample service answers a gRPC call and reports metrics | [[PCT-1\|PCT-1]] | [[Slice 26 Service foundation\|26]] |
| [[PSDK-2\|PSDK-2]] | Persistence: [[Physical layout Proposal\|PostgreSQL]], transactions, migrations, idempotency store | A retried operation commits once | [[PSDK-1\|PSDK-1]] | [[Slice 26 Service foundation\|26]] |
| [[PSDK-3\|PSDK-3]] | NATS wiring: publish, subscribe, JetStream where replay is needed | A fact published once is consumed once per subscriber | [[PSDK-1\|PSDK-1]] | [[Slice 30 Quests\|30]] |
| [[PBND-1\|PBND-1]] | ServicesBridgeLayer: implements the Engine service port with asynchronous gRPC calls; completions queued for safe ticks | A slow service never delays a tick | [[PCT-1\|PCT-1]], [[APP-1\|APP-1]], [[SIM-5\|SIM-5]] | [[Slice 27 Accounts and characters\|27]] |
| [[PBND-2\|PBND-2]] | LifecycleLayer: [[Platform and operations#Simulation placement\|Agones]] SDK ready, health and shutdown, plus a local stub mode for development without Agones | Against the Agones local SDK server the layer reports Ready, sends health pings and drains on shutdown; the stub mode runs with no Agones | [[APP-1\|APP-1]] | [[Slice 39 Operations\|39]] |
| [[PBND-3\|PBND-3]] | Prometheus exporter that publishes the Core metrics registry (tick-domain timings, and the network metrics the Diagnostics layer records) | A scrape returns time per tick domain in Prometheus format | [[CORE-2\|CORE-2]], [[SIM-1\|SIM-1]] | [[Slice 39 Operations\|39]] |
| [[PBND-4\|PBND-4]] | NATS in the services bridge: durable facts published from the outbox; world directives and other subscriptions delivered to the inbox at safe ticks | A fact published from a tick reaches a test subscriber once; a slow broker never delays a tick | [[PBND-1\|PBND-1]], [[PSDK-3\|PSDK-3]] | [[Slice 30 Quests\|30]] |
| [[PCS-1\|PCS-1]] | Accounts and entitlements, GlobalPlayerId issue, login, connect tickets signed with rotating keys whose public halves the simulations load | Login returns a signed ticket the simulation accepts | [[PSDK-2\|PSDK-2]], [[PTR-2\|PTR-2]] | [[Slice 27 Accounts and characters\|27]] |
| [[PCS-2\|PCS-2]] | [[Platform and operations#Simulation placement\|World Coordinator]]: worlds and region map, neighbor topology, [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] candidates, the world epoch | The Coordinator names the candidates for a border | [[PSDK-1\|PSDK-1]] | [[Slice 36 Multiple simulations\|36]] |
| [[PCS-3\|PCS-3]] | World directives with an effective time and a duration (weather, wind and current events) | A directive applies and expires at the same world time everywhere | [[PSDK-3\|PSDK-3]], [[PBND-4\|PBND-4]] | [[Slice 43 Tides waves and weather\|43]] |
| [[PCS-4\|PCS-4]] | Instance allocation from Agones fleets | Defined when the expansion slices are planned | [[PCS-2\|PCS-2]], [[PINF-2\|PINF-2]] | [[Slice 44 Expansion\|44+]] |
| [[PCS-5\|PCS-5]] | Chat and party groups | Defined when the expansion slices are planned | [[PSDK-3\|PSDK-3]] | [[Slice 44 Expansion\|44+]] |
| [[PCS-6\|PCS-6]] | Admission: per-world capacity limits, login queue and cohort waves for the launch phases | Defined when the expansion slices are planned | [[PCS-1\|PCS-1]] | [[Slice 44 Expansion\|44+]] |
| [[PCS-7\|PCS-7]] | Placement by load and traffic over Agones: scores by load, memory and inter-simulation traffic, with distance from the regions’ global coordinates; moves high-traffic pairs onto one node by move-by-handoff, up to a per-node cap | Two simulations with heavy link traffic end on one node with no loading screen; no node passes its cap | [[PCS-2\|PCS-2]], [[PINF-2\|PINF-2]], [[PTR-4\|PTR-4]] | [[Slice 44 Expansion\|44+]] |
| [[PBB-1\|PBB-1]] | Item ledger: containers, slots, atomic transfers, operation IDs; mechanisms only | Concurrent transfers never duplicate or lose an item | [[PSDK-2\|PSDK-2]] | [[Slice 28 Persistence\|28]] |
| [[PBB-2\|PBB-2]] | Currency wallets: balances and atomic transfers with operation IDs; mechanisms only | A balance changes once per operation ID under concurrent requests | [[PSDK-2\|PSDK-2]] | [[Slice 33a Exploration prototype\|33a]] |
| [[PBB-3\|PBB-3]] | One-transaction transfers that move ledger items and wallet currency together; mechanisms only | Defined when the expansion slices are planned | [[PBB-1\|PBB-1]], [[PBB-2\|PBB-2]] | [[Slice 44 Expansion\|44+]] |
| [[PINF-1\|PINF-1]] | Local development stack (PostgreSQL, NATS) started by one command | The stack starts and the service tests pass against it | — | [[Slice 26 Service foundation\|26]] |
| [[PINF-2\|PINF-2]] | Agones fleets, Kubernetes manifests, Prometheus and Grafana dashboards | A fleet runs in a development cluster, servers report Ready, and Grafana shows time per tick domain | [[PBND-2\|PBND-2]], [[PBND-3\|PBND-3]] | [[Slice 39 Operations\|39]] |

---

↑ [[Work packages|Work packages]] · ← [[Engine tools|Engine: tools]] · [[Game|Game]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Platform · exported 2026-11-03
