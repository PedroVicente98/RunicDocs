---
title: "Networking: stack, sessions and responsiveness"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Networking: stack, sessions and responsiveness"
created: "2026-10-14"
modified: "2026-10-30"
---

Clients talk directly to their simulation through the Engine’s transport interface, implemented by the Platform on GameNetworkingSockets; the player’s own actions feel instant through prediction that runs the game’s shared code, plus an input queue.

## Stack (decided)

| Piece | Owner | Used for |
| :---- | :---- | :---- |
| Transport interface | Engine | The only door between a process and the network; tick-safe ingress and egress queues |
| GameNetworkingSockets transport | Platform | Real-time UDP, client ↔ simulation and simulation ↔ simulation: reliable and unreliable messages, encryption, congestion control |
| Replication, interest, prediction, [[Networking replication interest and handoff#Simulations, handoff and ghosts\|handoff]] roles | Engine | What to send, to whom, and how clients correct themselves |
| Realtime message encoding | Engine | Every message on the realtime connection, envelope included: inputs, snapshots, deltas, simulation-link messages |
| Protobuf contracts | Platform (games add messages) | Service APIs, published facts and the connect-ticket format; never per-tick traffic |
| gRPC | Platform SDK | Calls that need an answer: load character, consume item, commit trade, allocate instance |
| NATS | Platform SDK | Publish and subscribe without an answer; JetStream only where replay is required |
| Go services | Platform and Game | Core services and game services |
| [[Platform and operations#Simulation placement\|Agones]] and Kubernetes | Platform | Simulation lifecycle, placement, fleets, configuration |

Runic::Network encodes every message on the realtime connection, envelope included; high-frequency payloads are bit-packed and quantized. Protobuf (Platform Contracts) defines service APIs, published facts and the connect-ticket format, never per-tick traffic.

## Sessions

1. The client logs in through the Platform auth service and receives a signed, short-lived connect ticket for its simulation.

2. The client opens a transport connection directly to the simulation and presents the ticket first.

3. The simulation checks the ticket locally (signature, expiry and key ID against the configured public keys), with no service call in the hot path.

4. The WorldSession survives handoffs: one authoritative connection plus up to three candidate connections near borders.

| Traffic | Delivery |
| :---- | :---- |
| Movement input and transform state | Unreliable, sequenced; the latest wins |
| Skill and interaction commands | Reliable or acknowledged per command type |
| Facts (damage, death, skill result) | Reliable |
| Snapshots | Unreliable deltas against the last acknowledged state |
| Handoff and authority control | Reliable, ordered, with authority epochs |

## Client prediction and reconciliation (decided)

* Prediction runs RunicGame::Shared, the same code the server runs, with only a subset of systems enabled: the local player’s movement, its own skill timelines and nearby collision. There is no separate copy to keep in sync.

* The client applies its own input immediately and keeps a short history of numbered inputs; the server returns authoritative state with the last input it processed, and the client replays the inputs after it.

* Any disagreement — collision with another player, knockback, CC, a failed speed check — is corrected: small errors blend, large ones snap.

* Skill starts are predicted cosmetically and cancelled in the rare case the server refuses.

* Speed and teleport hacks are stopped by server validation of every movement, independent of prediction.

## Input queue (decided)

* The queue lives in Runic::Combat, which knows each skill’s recovery and cancel windows; Network only carries the inputs. The client may send the next action before the current one ends, inside a queue window the game sets (e.g., 200–400 ms).

* The server keeps at most one queued action per character and starts it on the first tick after recovery ends, so at most 33 ms late.

* A queued action is validated when it starts, not when it arrives; a stun in between cancels it.

* Priority inputs the game names (in RunicGame, Dodge and [[Defense Evasion Guard and armor#Guard|Guard]]) skip the queue when the current skill’s cancel window allows.

* Regional datacenters keep typical latency low, which is what makes ServerTime hit timing comfortable.

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Sailing swimming and naval play|Sailing, swimming and naval play (Game)]] · [[Networking replication interest and handoff|Networking: replication, interest and handoff (Engine)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Networking: stack, sessions and responsiveness · exported 2026-11-03
