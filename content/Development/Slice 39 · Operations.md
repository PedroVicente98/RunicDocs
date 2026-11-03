---
title: "Slice 39 · Operations"
aliases:
  - "Slice 39"
tags:
  - "development"
  - "slice"
  - "progress/not-started"
slice: "39"
status: "Not started"
owners: "Engine, Platform, Game"
issue: "https://github.com/PedroVicente98/RunicEngine/issues/182"
created: "2026-11-03"
modified: "2026-11-03"
---

**Slice:** 39 · **Status:** Not started · **Packages done:** 0 of 9 · **Owners:** Engine, Platform, Game · **Issue:** [RunicEngine#182](https://github.com/PedroVicente98/RunicEngine/issues/182)

← [[Slice 38 · Battle scale]] · [[RunicGame — Development|All slices]] · [[Slice 40 · Water bodies]] →

**Runnable result:** Fleets on Agones, the Grafana panel, RunicEditor live attach

**Proves:** Diagnostics layer, lifecycle layer, metrics export, infrastructure

**Godot:** Live attach docks

### Packages

- [ ] **NET-7** · Diagnostics layer · [RunicEngine#116](https://github.com/PedroVicente98/RunicEngine/issues/116) · not started
    - Diagnostics layer: network and replication metrics recorded in the Core metrics registry; RunicEditor attach channel over a development socket transport inside Network, streaming debug shapes and the traces modules publish in Core’s debug-stream registry (compiled only into development and staging builds)
    - **Done when:** The RunicEditor attaches to a development server and sees its shapes; a production build has no attach endpoint
    - **Needs:** [[Slice 12 · Transport|NET-1]], [[Slice 3 · Fixed-step clock|CORE-2]]
- [ ] **PBND-2** · LifecycleLayer · [RunicPlatform#20](https://github.com/PedroVicente98/RunicPlatform/issues/20) · not started
    - LifecycleLayer: Agones SDK ready, health and shutdown, plus a local stub mode for development without Agones
    - **Done when:** Against the Agones local SDK server the layer reports Ready, sends health pings and drains on shutdown; the stub mode runs with no Agones
    - **Needs:** [[Slice 1 · Application and layers|APP-1]]
- [ ] **PBND-3** · Prometheus exporter that publishes the Core metrics registry · [RunicPlatform#21](https://github.com/PedroVicente98/RunicPlatform/issues/21) · not started
    - Prometheus exporter that publishes the Core metrics registry (tick-domain timings, and the network metrics the Diagnostics layer records)
    - **Done when:** A scrape returns time per tick domain in Prometheus format
    - **Needs:** [[Slice 3 · Fixed-step clock|CORE-2]], [[Slice 3 · Fixed-step clock|SIM-1]]
- [ ] **PINF-2** · Agones fleets, Kubernetes manifests, Prometheus and Grafana dashboards · [RunicPlatform#22](https://github.com/PedroVicente98/RunicPlatform/issues/22) · not started
    - Agones fleets, Kubernetes manifests, Prometheus and Grafana dashboards
    - **Done when:** A fleet runs in a development cluster, servers report Ready, and Grafana shows time per tick domain
    - **Needs:** PBND-2, PBND-3
- [ ] **GDT-13** · Live attach docks to development and staging servers · [RunicEngine#115](https://github.com/PedroVicente98/RunicEngine/issues/115) · not started
    - Live attach docks to development and staging servers
    - **Done when:** Entity inspector and debug shapes come from a remote server
    - **Needs:** [[Slice 6 · Editor shell|GDT-2]], NET-7
- [ ] **SIM-7** · Behavior counters flushed through the service port · [RunicEngine#191](https://github.com/PedroVicente98/RunicEngine/issues/191) · not started
    - Behavior counters: modules and the project register small per-player counters (histograms, counts, route fingerprints). The Simulation keeps them in fixed memory and flushes one compact summary per player per interval through the service port. Enqueue only; when the queue is full the oldest summaries are dropped and counted.
    - **Done when:** Summaries flush on the interval with no measurable tick cost, and a RunicBot session shows in them
    - **Needs:** [[Slice 27 · Accounts and characters|SIM-5]], [[Slice 38 · Battle scale|CLI-9]]
- [ ] **CMB-9** · Combat behavior samples for the behavior counters · [RunicEngine#192](https://github.com/PedroVicente98/RunicEngine/issues/192) · not started
    - Combat behavior samples: reaction time from a telegraph cue to the defense input's view-time stamp (the server estimates when the cue could first be shown to that client from the fact's send tick and the client's latency), and aim error against player targets, recorded into the behavior counters. No extra traffic.
    - **Done when:** A scripted defender that reacts instantly produces a reaction histogram at zero; a delayed one shows its delay
    - **Needs:** SIM-7, [[Slice 18 · Defense|CMB-5]]
- [ ] **PBND-5** · Behavior summaries published to NATS · [RunicPlatform#33](https://github.com/PedroVicente98/RunicPlatform/issues/33) · not started
    - Behavior summaries from the service port published to NATS on a lossy stream; never blocks a tick; drops under backpressure and counts the drops.
    - **Done when:** Summaries from a simulation reach a test subscriber, and a stalled subscriber never slows the simulation
    - **Needs:** [[Slice 30 · Quests|PBND-4]], SIM-7
- [ ] **GSVC-11** · Behavior scoring service · [RunicGame#41](https://github.com/PedroVicente98/RunicGame/issues/41) · not started
    - Behavior scoring service (Go): consumes behavior summaries and scores how human each player looks: reaction-time distributions, consistency over a session, route repetition, session shape, and currency or items flowing from many accounts to one. Flags players for human review; never bans by itself. Thresholds, features and scores are secret and server-side.
    - **Done when:** RunicBot sessions are flagged for review and a human test session is not
    - **Needs:** PBND-5, [[Slice 30 · Quests|PSDK-3]]

*Generated by `tools/sync_development.py` from the [[Vertical-slice roadmap]], the work packages and the GitHub issues. Change those, then run it again.*
