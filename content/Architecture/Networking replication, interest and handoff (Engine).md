---
title: "Networking: replication, interest and handoff (Engine)"
tags:
  - "architecture"
  - "repo/engine"
  - "appendix/rendering-lighting-visibility"
  - "appendix/ping-resolution"
source: "RunicEngine — Technical Architecture"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
created: "2026-10-14"
modified: "2026-11-16"
---

Each client receives a priority-ordered, bandwidth-capped delta of only what it may perceive, which keeps a 500-player battle near 50 KB/s per player.

### Replication

* Per client, the simulation builds a delta against the last state that client acknowledged; unchanged fields cost nothing.

* Values are quantized: positions relative to the cell origin, angles in 16 bits, health in steps where acceptable.

* Snapshot building runs in parallel, one client per task.

### Priority and bandwidth budget

Each client has a byte budget per update. Entities are ranked by distance, combat involvement, targeting, party membership and importance; the highest go first and the rest accumulate priority until they are sent. Rough planning at about 12 bytes per entity update:

| Battle size | Plan per client | Download per client | Upload per simulation |
| :---- | :---- | :---- | :---- |
| 200 (100 vs 100\) | Everyone nearby at 20 Hz | ≈ 48 KB/s | ≈ 9.6 MB/s |
| 500 | The \~100 most relevant at 20 Hz, the rest at 5 Hz | ≈ 48 KB/s | ≈ 24 MB/s |

Beyond the budget, degradation follows a fixed order: lower update rates for distant entities, then less cosmetic detail (gear and animation flags), then a cap on visible effects. Combat correctness never degrades.

### Interest and visibility tiers (decided)

Candidates come from the 3D cells around the client inside its interest volume (plus a preload margin), filtered by category. Each candidate pair then gets a visibility tier — server-side fog of war. The tiers and what each one sends are data, and a function the Game registers picks the tier from distance, light, concealment and its own rules. RunicGame uses two (GSRV-10):

| Tier | Condition | Data sent |
| :---- | :---- | :---- |
| Full | Within the visibility range: class range × ambient light × target emission × weather, clamped between about 1 m and 1 km; an entity enters at range R and leaves only beyond R + 10% (hysteresis) | Everything |
| Hidden | Otherwise | Nothing |

* The client knows only what the player knows (decided on 9 November): the server never sends an entity the player can't see, and height has no effect on the range. Ambient light comes from the time of day, weather, node, the Underground and the server darkness grid; lanterns, torches and fires lengthen the range; complete darkness and blindness bring it to about 1 m.

* Contact events (RunicGame): every interaction with a hidden entity (it hits you, or you hit it) sends an anonymous event with position, facing and size class (about 12 bytes) and a handle scoped to the viewer, never the real ID. The client draws a generic silhouette, frozen where the attack came from and colored by relation. Damage over time and auras send at most one per direct hit, or one per attacker every few seconds.

* Projectiles and effects are judged by their own position and light, never the caster’s, and are sent without the caster’s identity when the caster is hidden.

* Cost: the range per observer is about 50 ns and membership about 3 ns per candidate pair. *Proposal: recheck membership at 5 to 10 Hz instead of every tick.* Details: [[Rendering, lighting and visibility (Engine, Game)#Entity visibility|Entity visibility]].

* Cost: one multiplication per candidate pair inside an interest pass that already runs.

* Combat never uses tiers; the server resolves every hit regardless of visibility. Telegraph fast-forward, defender grace and predicted impacts apply only to entities the client knows (see [[Ping resolution (Engine, Game)]]).

### Detail levels and focus

* A replicated component can declare detail levels; the Game says which fields each level carries and who receives which level.

* The client tells the server which entities it is focusing (in RunicGame, the action target and the Ward). The hint only raises priority and detail; it never grants authority and never lifts a visibility tier.

* RunicGame, as planning numbers: everyone in view gets health and a status bitmask (about 8 bytes per change); the focused entities and the party get every status with its time, build-up, Resolve and shields (about 50–100 bytes per change).

### Simulations, handoff and ghosts

* Exactly one simulation is authoritative for an entity at any moment; authority epochs reject stale messages. Handoff between simulations is required, not optional: ships cross borders with their passengers and cargo. Worlds never share a border, so there is no handoff or ghost between worlds; a world transition is a checkpoint plus a new ticket.

* Near a border, neighbor simulations receive ghost state and the client preconnects to up to three candidates; crossing promotes one and drops the others, with no loading screen.

* Connection roles: Primary (authoritative), WarmCandidate (connected and prepared for promotion), Dormant (kept with minimal traffic) and Retiring (the old authority during a grace window). The player’s WorldSession stays the same while the Platform tells the client to prepare, promote, sleep, retire or drop connections; gameplay code never reasons about addresses.

* Cross-boundary combat: the target’s owner resolves the hit (ForeignCombatVolume, then RemoteHitResult).

* World partition is not simulation ownership. Regions, Sectors and Cells stay fixed, while an AuthorityPartition (an operational area with an owner and an epoch) can give a busy area such as a city its own simulation; a partition never cuts an indivisible volume (an island, a castle, a docked ship). Every participating simulation loads the same static geometry; each dynamic entity keeps exactly one owner and appears as a ghost elsewhere. Players are never spread round-robin across simulations, which would turn most local interactions into remote ones.

* A world boss keeps its health, phase, AI and cooldowns on one simulation. Attacks from players owned elsewhere arrive as foreign combat, and the boss’s area effects reach other simulations as foreign effect volumes that each applies only to its own entities.

* Simulation-to-simulation traffic uses a direct link chosen by locality — an in-memory queue in one process, a local socket or shared memory on one machine, GameNetworkingSockets between machines — never NATS or gRPC in the hot path. DistributedSimulation semantics are the same on every channel; shared memory is only a message channel, never a central memory shared between simulations.

* The code lives in two Engine modules: Runic::DistributedSimulation (authority, ghost state, transfer and its snapshot-contributor registry, foreign interactions, authority partitions) and Runic::Network (all encoding, including snapshots, ghost deltas and transfer messages; interest; prediction); the Platform transport carries the bytes. GameplayFlow, Quest and Water register their state as snapshot contributors, so a sequence, a quest or a whole ship group moves with its owner.
