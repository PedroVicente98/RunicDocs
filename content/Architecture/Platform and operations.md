---
title: "Platform and operations"
tags:
  - "architecture"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-10-30"
---

The Platform supplies the services every MMORPG needs, an SDK for building more, and the infrastructure that places one multi-core simulation per region; game-specific services live in RunicGame on that SDK.

### Services

| Service | Owner | Owns |
| :---- | :---- | :---- |
| Auth and accounts | Platform | Login, entitlements (early access, subscription, free), connect tickets |
| World Coordinator | Platform | Region-to-simulation map per world, neighbor topology, handoff candidates, drains, placement by load, memory and inter-simulation traffic, placement requests to Agones |
| Instance allocation | Platform | Dungeons, raids, naval raids and the shop island from Agones fleets |
| Chat and party groups | Platform | Social transport and party membership; group rules come from game data |
| World directives | Platform | Weather, wind and current events and other world-wide directives with an effective world time and a duration |
| Admission | Platform | Per-world capacity limits, login queue and cohort waves for the launch phases (PCS-6) |
| Item ledger | Platform | Item instances, containers, slots, atomic transfers, operation IDs; mechanisms only, with no game rules |
| Currency wallets | Platform | Balances, atomic transfers, and one-transaction transfers together with the item ledger; mechanisms only |
| Character | Game | Characters, build (loadout, Discipline, skill points and level choices; class and role are derived), exploration XP and professions, faction and crime state, map knowledge (per Lineage), discovered Altars (per character), labor (per Lineage); account-wide collections (wardrobe, mounts, pets) |
| Inventory | Game | Stacking, binding, equip and trade limits, loot grants, duplication checks; applied through the item ledger |
| Economy | Game | Upgrades (item level, grades, RNG and guarantees), a global auction house, the auction tax, land fund |
| Trade | Game | Two-party trade rules and confirmations; atomic item and currency transfers through the ledger and wallets |
| Guild | Game | Guild membership, roles, progression and rules |
| Mail | Game | Mail delivery and claim rules; item and currency attachments through the ledger and wallets |
| Housing and land | Game | Grid slots, deeds (Escrituras), freezing and relocation |
| Quest | Game | Stores quest progress, deduplicates quest facts and commits rewards; quest logic runs inside the simulation on the Quest runtime |
| Rankings | Game | Region-boss contribution, PvP honor and rankings |
| World events | Game | Decides storms and other world-wide overrides, including wind and current events scheduled from an operator panel; delivers them as Platform world directives with a duration |
| World routines | Game | Player-caused exceptions to world routines (a delayed escort, a sunk caravan) and how they fade back into the routine |

Every service is built on the Platform Go SDK. Persistence is PostgreSQL. Every durable change is an operation with an ID, so retries are safe. The simulation never waits for the database; durable writes happen at explicit boundaries (logout, trade, upgrade, periodic checkpoint).

### Simulation placement

* **One region per simulation pod by default** (decided); quiet neighboring regions may share a pod, and several simulations may share one process, to save cost.

* Pods request whole vCPUs, and the simulation sizes its worker pool from them.

* **Growing in place:** Kubernetes in-place pod resize (stable since Kubernetes 1.35) raises a running pod’s CPU without a restart; the simulation picks up the new worker count at a safe point.

* **Pinned cores:** exclusive cores (the static CPU manager) give the steadiest tick, but Kubernetes does not allow in-place resize with them. Use them only for hot fleets after profiling; those pods grow by moving.

* **Moving to a bigger machine:** Kubernetes never moves a running process. The World Coordinator starts a new pod on a bigger node, transfers the region’s entities with the handoff protocol and retires the old pod, with no loading screen for players.

* **Busy areas:** a busy area such as a city can get its own simulation through an AuthorityPartition, using the same border handoff; a partition never cuts an indivisible volume.

* A new open-world simulation is never allocated inside a handoff’s critical path; neighbors already exist.

* **Placement by load and traffic (decided).** The World Coordinator, a Platform Go service on top of Agones, places simulations by load, memory and traffic. The distance between simulations comes from their regions’ global coordinates; pairs that exchange much traffic move onto the same node by move-by-handoff, up to a per-node cap (PCS-7).

* **Links by locality (decided).** Simulation links use the cheapest channel for where the peers run: an in-memory queue in one process, a local socket or shared memory on one machine, GameNetworkingSockets between machines (PTR-4). DistributedSimulation semantics do not change with the channel.

### Instances and geography

* Instances are Agones-allocated game servers from fleets; the client preloads while the player approaches the entrance.

* Worlds are hosted in datacenters near their players (for example South America, North America, Europe), each with its own Kubernetes cluster and Agones. Accounts are global.

### Launch phases

| Phase | Mechanism |
| :---- | :---- |
| Early access for subscribers | Entitlement check at login |
| Pay-to-play launch (a month or more) | Entitlements plus per-world capacity limits |
| Gradual free access (open: depends on the base business model, still undecided) | Admission waves by account cohort and a login queue per world, paced by server metrics |

### Monitoring: one panel (decided)

* **Grafana is the single operations panel.** Agones exports its metrics (fleets, allocations, game server states) to Prometheus and ships Grafana dashboards for them.

* Each GameServer records its metrics in the Core metrics registry (the Diagnostics layer adds network metrics), and the Platform’s exporter (PBND-3) publishes the registry to the same Prometheus: time per clock domain and system, tick backlog, players, entities, bandwidth per client, handoffs, ghosts. Go services export theirs through the SDK. Logs join the same panel.

* **Live inspection is the RunicEditor’s job, not the server’s.** In development and staging, the RunicEditor attaches to a running GameServer through a privileged debug channel: entity inspector, live behavior trees, resolver traces, and a stream of debug shapes the RunicEditor draws. Production builds compile the attach channel out, and servers never link Godot.

### Local development

Gameplay work never needs Kubernetes: run GameServer directly, without a lifecycle layer or with the LifecycleLayer’s local stub (PBND-2) and, only when a feature needs them, local NATS and Go services. The RunicEditor’s Run button starts and keeps this local stack (see [[Godot integration (Engine)|Godot integration]]).
