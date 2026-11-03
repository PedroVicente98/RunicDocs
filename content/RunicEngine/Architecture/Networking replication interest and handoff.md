---
title: "Networking: replication, interest and handoff (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Networking: replication, interest and handoff (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

Each client receives a priority-ordered, bandwidth-capped delta of only what it may perceive, which keeps a 500-player battle near 50 KB/s per player.

## Replication

* Per client, the simulation builds a delta against the last state that client acknowledged; unchanged fields cost nothing.

* Values are quantized: positions relative to the cell origin, angles in 16 bits, health in steps where acceptable.

* Snapshot building runs in parallel, one client per task.

## Priority and bandwidth budget

Each client has a byte budget per update. Entities are ranked by distance, combat involvement, targeting, party membership and importance; the highest go first and the rest accumulate priority until they are sent. Rough planning at about 12 bytes per entity update:

| Battle size | Plan per client | Download per client | Upload per simulation |
| :---- | :---- | :---- | :---- |
| 200 (100 vs 100\) | Everyone nearby at 20 Hz | ≈ 48 KB/s | ≈ 9.6 MB/s |
| 500 | The \~100 most relevant at 20 Hz, the rest at 5 Hz | ≈ 48 KB/s | ≈ 24 MB/s |

Beyond the budget, degradation follows a fixed order: lower update rates for distant entities, then less cosmetic detail (gear and animation flags), then a cap on visible effects. Combat correctness never degrades.

## Interest and visibility tiers (decided)

Candidates come from the 3D cells around the client inside its interest volume (plus a preload margin), filtered by category. Each candidate pair then gets a tier — server-side fog of war:

| Tier | Condition | Data sent |
| :---- | :---- | :---- |
| Full | Within visibility range, set by the target’s luminosity and concealment | Everything |
| Silhouette | Within the minimum silhouette range in any light, or revealed by contact in the last few seconds | Coarse position and pose at a low rate; no name, gear or identity |
| Hidden | Otherwise | Nothing |

* Contact reveals: hitting or being hit, a heal nearby, AoE contact.

* Projectiles and effects from hidden players are sent without the caster’s identity.

* Cost: one multiplication per candidate pair inside an interest pass that already runs.

* Combat never uses tiers; the server resolves every hit regardless of visibility.

## Simulations, handoff and ghosts

* Exactly one simulation is authoritative for an entity at any moment; authority epochs reject stale messages. Handoff between simulations is required, not optional: ships cross borders with their passengers and cargo. Worlds never share a border, so there is no handoff or ghost between worlds; a world transition is a checkpoint plus a new ticket.

* Near a border, neighbor simulations receive ghost state and the client preconnects to up to three candidates; crossing promotes one and drops the others, with no loading screen.

* Connection roles: Primary (authoritative), WarmCandidate (connected and prepared for promotion), Dormant (kept with minimal traffic) and Retiring (the old authority during a grace window). The player’s WorldSession stays the same while the Platform tells the client to prepare, promote, sleep, retire or drop connections; gameplay code never reasons about addresses.

* Cross-boundary combat: the target’s owner resolves the hit (ForeignCombatVolume, then RemoteHitResult).

* World partition is not simulation ownership. Regions, Sectors and Cells stay fixed, while an AuthorityPartition (an operational area with an owner and an epoch) can give a busy area such as a city its own simulation; a partition never cuts an indivisible volume (an island, a castle, a docked ship). Every participating simulation loads the same static geometry; each dynamic entity keeps exactly one owner and appears as a ghost elsewhere. Players are never spread round-robin across simulations, which would turn most local interactions into remote ones.

* A world boss keeps its health, phase, AI and cooldowns on one simulation. Attacks from players owned elsewhere arrive as foreign combat, and the boss’s area effects reach other simulations as foreign effect volumes that each applies only to its own entities.

* Simulation-to-simulation traffic uses a direct link chosen by locality — an in-memory queue in one process, a local socket or shared memory on one machine, [[Networking stack sessions and responsiveness#Stack (decided)|GameNetworkingSockets]] between machines — never NATS or gRPC in the hot path. DistributedSimulation semantics are the same on every channel; shared memory is only a message channel, never a central memory shared between simulations.

* The code lives in two Engine modules: Runic::DistributedSimulation (authority, ghost state, transfer and its snapshot-contributor registry, foreign interactions, authority partitions) and Runic::Network (all encoding, including snapshots, ghost deltas and transfer messages; interest; prediction); the Platform transport carries the bytes. [[Scripted sequences GameplayFlow and restrictions|GameplayFlow]], Quest and Water register their state as snapshot contributors, so a sequence, a quest or a whole ship group moves with its owner.

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Networking stack sessions and responsiveness|Networking: stack, sessions and responsiveness]] · [[Platform and operations|Platform and operations]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Networking: replication, interest and handoff (Engine) · exported 2026-11-03
