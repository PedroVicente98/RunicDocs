---
title: "The protocol"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
section: "The protocol"
created: "2026-10-22"
modified: "2026-10-22"
---

**Attacks.**

* Headless clients that play without the game. The encoding, [[Tools#Testing at scale|RunicBot]] and the login flow are public, so this is easier than in a closed game.
* Forged commands: selling a negative quantity, trading an item the player does not own, sending a price, acting from out of range.
* Malformed packets meant to crash a region, which can also duplicate items if saves roll back.
* Command floods and expensive requests that slow the tick, and replays of captured packets.

**Defenses.**

* **Server validation of every command** (already a Game rule): ownership, range, cooldown, quantity within limits, prices only from server data.
* **Bounded decoding.** Every length and count is limited before anything is allocated; a bad message is rejected and counted, never fatal ([[NET-1|NET-1]], [[NET-3|NET-3]], [[NET-5|NET-5]]). Every decoder that runs on the server has a fuzz target in CI. Attackers can fuzz the public decoder too, so this comes first.
* **Budgets.** Messages and bytes per tick per connection ([[NET-1|NET-1]]); rate and cost per command type ([[SIM-2|SIM-2]]), with values from Game data ([[GSH-1|GSH-1]]). Anything over budget is dropped and counted, and repeated abuse closes the connection.
* **Encryption and server identity.** [[Networking stack sessions and responsiveness#Stack (decided)|GameNetworkingSockets]] encrypts every packet (AES-GCM-256 with a Curve25519 key exchange). That protects players from third parties, not the server from the player. The client checks the server's identity, so a man-in-the-middle cannot take over a session ([[PTR-2|PTR-2]]).
* **Late inputs are dropped** and lag-switch bursts are counted ([[NET-3|NET-3]]).
* **Development tickets and keys never work in production** ([[PTR-2|PTR-2]]); RunicBot uses only development tickets ([[CLI-9|CLI-9]]).

## The ping helpers as an attack surface

| Helper | Abuse | What limits it |
| :---- | :---- | :---- |
| [[Part 1 Locked ping resolution#3. Defender grace (all defense)\|Defender grace]] | Fake a high ping for more time to dodge | 150 ms cap; a stamp earlier than the measured latency allows is clamped |
| [[Part 1 Locked ping resolution#5. Capped rewind\|Capped rewind]] | Lag on purpose so hits land on old positions | 100 ms cap against players; ties go to the defender |
| Lag switch | Hold packets, then release a burst | Inputs for ticks already simulated are dropped; bursts are counted |
| [[Part 1 Locked ping resolution#2. Telegraph fast-forward\|Telegraph fast-forward]] | A bot reads the attack-start fact and dodges at once | Cannot be prevented, since the fact must be sent; reaction-time profiling detects it ([[CMB-9\|CMB-9]]) |
| Input redundancy | Replaying old inputs | Sequence numbers drop duplicates |
| Predicted impact effects | Fake sparks | Cosmetic only; damage waits for the server |

The view-time stamp built for grace and rewind also tells the server when a player saw something, so real reaction times can be measured with no extra traffic.

---

↑ [[Security|Security]] · ← [[The client|The client]] · [[Bots and scripts|Bots and scripts]] →  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) › The protocol · exported 2026-11-03
