---
title: "Engine: networking"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/platform"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: networking"
created: "2026-10-14"
modified: "2026-10-30"
---

| ID | Package | Done when | Needs | Slice |
| :---- | :---- | :---- | :---- | :---- |
| [[NET-1\|NET-1]] | Transport interface, tick-safe ingress and egress queues, connect-ticket hook, the Network layer; the interface and hook ship as the header-only Runic::NetworkTransport target (Core types only) | A loopback transport passes ping and echo tests | [[SIM-1\|SIM-1]] | [[Slice 12 Transport\|12]] |
| [[NET-2\|NET-2]] | Snapshots: extraction, quantization, deltas against the last acknowledged state, interpolation buffers | Two clients see each other move smoothly under packet loss | [[NET-1\|NET-1]], [[SIM-6\|SIM-6]] | [[Slice 13 Replication\|13]] |
| [[NET-3\|NET-3]] | Prediction and reconciliation: input history, replay, blend or snap | Movement stays responsive under simulated lag; corrections show in the debug view | [[NET-2\|NET-2]], [[SIM-4\|SIM-4]] | [[Slice 14 Prediction\|14]] |
| [[NET-4\|NET-4]] | Interest: candidates by cell, priority and budgets, visibility tiers applied | Only relevant entities arrive and per-client budgets hold | [[NET-2\|NET-2]], [[WORLD-2\|WORLD-2]], [[PRC-2\|PRC-2]] | [[Slice 25 Interest\|25]] |
| [[NET-5\|NET-5]] | Simulation links: ghost deltas and transfer messages encoded with the snapshot codec over simulation-to-simulation connections | Ghosts stay in sync across a border under packet loss; a message with a stale epoch is dropped | [[NET-2\|NET-2]], [[DSIM-2\|DSIM-2]] | [[Slice 36 Multiple simulations\|36]] |
| [[NET-6\|NET-6]] | Parallel replication and the degradation order | 500 bots in one region fit the per-client budget | [[NET-4\|NET-4]], [[SIM-3\|SIM-3]] | [[Slice 38 Battle scale\|38]] |
| [[NET-7\|NET-7]] | Diagnostics layer: network and replication metrics recorded in the Core metrics registry; [[Tools#RunicEditor\|RunicEditor]] attach channel over a development socket transport inside Network, streaming debug shapes and the traces modules publish in Core’s debug-stream registry (compiled only into development and staging builds) | The RunicEditor attaches to a development server and sees its shapes; a production build has no attach endpoint | [[NET-1\|NET-1]], [[CORE-2\|CORE-2]] | [[Slice 39 Operations\|39]] |
| [[NET-8\|NET-8]] | World transitions: the session leaves one world’s simulation after a checkpoint and joins another world’s simulation with a new connect ticket; no [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] or ghosts across worlds | A character moves between two worlds with its checkpointed state, and the old simulation keeps no copy | [[NET-1\|NET-1]], [[SIM-5\|SIM-5]], [[PCS-1\|PCS-1]] | [[Slice 44 Expansion\|44+]] |
| [[DSIM-1\|DSIM-1]] | Authority state, epochs, GlobalEntityId mapping | Messages with a stale epoch are rejected | [[SIM-2\|SIM-2]] | [[Slice 36 Multiple simulations\|36]] |
| [[DSIM-2\|DSIM-2]] | Ghosts: ghost state near borders as plain data; Network encodes the deltas ([[NET-5\|NET-5]]) | Ghosts follow their owners near the border | [[DSIM-1\|DSIM-1]] | [[Slice 36 Multiple simulations\|36]] |
| [[DSIM-3\|DSIM-3]] | Transfer: prepare, final snapshot, authority commit; a snapshot-contributor registry where modules add their state (sequences, quests, ship groups) | A player walks from A to B with no loading screen; the input sequence continues | [[DSIM-2\|DSIM-2]] | [[Slice 36 Multiple simulations\|36]] |
| [[DSIM-4\|DSIM-4]] | Foreign-interaction contract | A request carries enough context for the owner to resolve it | [[DSIM-1\|DSIM-1]] | [[Slice 37 Cross-border combat\|37]] |
| [[DSIM-5\|DSIM-5]] | Authority partitions inside one region (busy areas such as a city) that never cut an indivisible volume (an island, a castle, a docked ship) | Two simulations share a city, each entity has one owner, and no indivisible volume is split | [[DSIM-3\|DSIM-3]] | [[Slice 44 Expansion\|44+]] |

---

↑ [[Work packages|Work packages]] · ← [[Engine world systems|Engine: world systems]] · [[Engine presentation|Engine: presentation]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Modules, work packages and the implementation contract (Engine, Platform, Game) › Work packages › Engine: networking · exported 2026-11-03
