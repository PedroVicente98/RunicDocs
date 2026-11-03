---
title: "RunicEngine — Appendix: Security"
tags:
  - "archive"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
created: "2026-10-22"
modified: "2026-10-22"
---

Design appendix from the conversation of 22 October 2026, to be merged later into the technical architecture and the game vision. It covers how the game can be attacked (the client, the protocol, bots, the economy, accounts, services, DDoS and the supply chain) and the defenses adopted for each, with the owning repository. Items are labeled Decision, Proposal or Open. Numbers are examples for tuning. The GitHub issues already carry these requirements under the security label; the section Changes to the GitHub issues lists them.

## Decisions

* **No mod or add-on support (Decision).** Players cannot load UI add-ons, scripts or modified files. A game that needs add-ons has a UI that failed; the answer is a better original UI. Editor plugins for developers (GDT-16) are not affected.
* **The soundtrack is the only player-made content (Decision).** Playlists, presets and radio stations, with the game's context choosing the mood. They are data only, validated on import, and live outside the installed game files. The Architecture's soundtrack security rules already apply.
* **Every measure in this appendix is adopted (Decision)**, on the stage plan below.
* **The client is untrusted (Decision).** Anything sent to it can be read, and anything it sends can be forged. Server authority, already in the architecture, stays the foundation; the measures below cover what authority alone does not.
* **No security through obscurity (Decision).** RunicEngine and RunicPlatform are public, so the wire encoding, the bot runtime and the login flow are public. Every defense must hold with the code known.
* **Consequence of having no mods.** Any change to an installed game file is tampering or damage, so the launcher repairs it and the client does not connect after a failed integrity check (GAME-3).

### Who attacks and why

| Attacker | Goal | Main avenue |
| :---- | :---- | :---- |
| Cheater | Win fights, see hidden information | Client tools and input automation |
| Bot farmer | Currency and items to sell for real money | Headless clients and scripts |
| Account thief | Items and currency to resell | Reused passwords, phishing, fake downloads |
| Duper | Create items or currency from nothing | Race conditions, crashes, region handoffs |
| DDoS attacker (rival, extortionist, banned player) | Take a region or the login down | Floods against server addresses |
| Supply-chain attacker | The developer's tokens and keys, or the players' machines | Contaminated dependencies, CI, the update server |

## The client

**Attacks.**

* Memory scanners and debuggers read or change values in RAM.
* Injected code hooks the renderer to draw hidden information (ESP), or hooks the send function to send its own commands. The hook runs before encryption, so encryption does not stop it.
* Modified files: see-through walls, removed fog. Godot packs are easy to extract, so everything shipped in the client is public and will be datamined.
* Input automation: macros, scripts, and USB devices that act as a keyboard, which software cannot see.
* Screen-reading bots: computer vision on the screen with no memory access, growing quickly with AI models.
* DMA hardware: a card that reads the game's memory from a second PC, mostly invisible to software anti-cheat.

**What it gets them.** Changing values locally does nothing, because the server runs the same shared rules and decides every outcome: speed, teleport, fly, god-mode and infinite-stamina hacks fail. What remains is reading what the server sent and automating a real player's hands.

**Defenses.**

* **Need-to-know (Decision).** Every replicated field declares its audience, server only by default (SIM-6), and entity kinds can have a short send range (NET-4). Hidden players are never sent and hidden casters' effects carry no identity (already in the architecture). Game rules: enemy players' exact values are sent only if the UI shows them (GSH-1); rare resource nodes only nearby (GSRV-7).
* **Occlusion-aware interest (Proposal, deferred).** Send hostile players only when they could become visible soon, as Valorant does. Built only if PvP measurements show wallhacks are a real problem (NET-10).
* **Client anti-cheat (Decision; vendor is a Proposal).** Easy Anti-Cheat is free through Epic Online Services, with a kernel driver on Windows and user mode only on Linux and Steam Deck. It stops cheap public cheats, which is most cheaters, but not DMA cards, hardware input devices or screen-reading bots. The Engine provides an opaque integrity channel (NET-9); the Game integrates the provider (GAME-2).
* **File integrity (Decision).** Signed manifests with a hash for every file (COOK-4, ASSET-2); the launcher verifies and repairs (GAME-3). Unreleased content never ships in a client build (COOK-4).
* **Behavior detection** (see Bots and scripts) for everything the client side cannot see.

## The protocol

**Attacks.**

* Headless clients that play without the game. The encoding, RunicBot and the login flow are public, so this is easier than in a closed game.
* Forged commands: selling a negative quantity, trading an item the player does not own, sending a price, acting from out of range.
* Malformed packets meant to crash a region, which can also duplicate items if saves roll back.
* Command floods and expensive requests that slow the tick, and replays of captured packets.

**Defenses.**

* **Server validation of every command** (already a Game rule): ownership, range, cooldown, quantity within limits, prices only from server data.
* **Bounded decoding.** Every length and count is limited before anything is allocated; a bad message is rejected and counted, never fatal (NET-1, NET-3, NET-5). Every decoder that runs on the server has a fuzz target in CI. Attackers can fuzz the public decoder too, so this comes first.
* **Budgets.** Messages and bytes per tick per connection (NET-1); rate and cost per command type (SIM-2), with values from Game data (GSH-1). Anything over budget is dropped and counted, and repeated abuse closes the connection.
* **Encryption and server identity.** GameNetworkingSockets encrypts every packet (AES-GCM-256 with a Curve25519 key exchange). That protects players from third parties, not the server from the player. The client checks the server's identity, so a man-in-the-middle cannot take over a session (PTR-2).
* **Late inputs are dropped** and lag-switch bursts are counted (NET-3).
* **Development tickets and keys never work in production** (PTR-2); RunicBot uses only development tickets (CLI-9).

### The ping helpers as an attack surface

| Helper | Abuse | What limits it |
| :---- | :---- | :---- |
| Defender grace | Fake a high ping for more time to dodge | 150 ms cap; a stamp earlier than the measured latency allows is clamped |
| Capped rewind | Lag on purpose so hits land on old positions | 100 ms cap against players; ties go to the defender |
| Lag switch | Hold packets, then release a burst | Inputs for ticks already simulated are dropped; bursts are counted |
| Telegraph fast-forward | A bot reads the attack-start fact and dodges at once | Cannot be prevented, since the fact must be sent; reaction-time profiling detects it (CMB-9) |
| Input redundancy | Replaying old inputs | Sequence numbers drop duplicates |
| Predicted impact effects | Fake sparks | Cosmetic only; damage waits for the server |

The view-time stamp built for grace and rewind also tells the server when a player saw something, so real reaction times can be measured with no extra traffic.

## Bots and scripts

Bots farm currency and materials for real-money trading, level accounts to sell, gather nonstop, and auto-dodge or auto-aim in PvP. Farming bots are an attack on the economy: they push prices up and lower the value of players' time.

**Detection is behavior profiling (Decision).** A Go scoring service (GSVC-11) rates how human each player looks from these signals:

* **Reaction time.** Most people react to a cue they are watching for in about 200 to 300 ms, with a wide spread; very fast players get near 150 ms. Bots sit near 0 ms or are too regular. Thousands of samples per player make this reliable.
* **Fatigue.** Human timing and accuracy drift over a long session; a bot's do not.
* **Routes.** The same path, jumps and camera angles, repeated.
* **Session shape.** Twenty hours a day, or back online seconds after a kick.
* **Money flow.** Many young accounts feeding one account (mules).

**Pipeline without tick blocking.** The Simulation keeps small per-player counters (SIM-7), and Combat adds reaction and aim samples (CMB-9). One summary per player per minute, about 128 bytes, goes through the service port to NATS on a lossy stream (PBND-5). At 10,000 players that is about 1.8 GB per day, against about 69 GB per day for raw events, and about 170 summaries per second for the scoring service. Features, thresholds and scores stay secret and server-side. RunicBot sessions are the first test: they must be flagged, and a human session must not.

**Making bots unprofitable.** Labor caps production per account (already decided) and Market Isle blueprints are bound. Young-account transfer limits and new-device holds are added (GSVC-4).

**Enforcement.** Automation only flags; a person reviews before any permanent ban. Ban waves (detect now, ban in batches later) hide what triggered detection. Honeypots, entities that only a bot reading the entity list would touch, are a Proposal.

**Macro policy (Open).** The game itself offers optional key combos (Vision), so built-in combos are allowed, as are key remapping and accessibility tools. Third-party tools that fire timed sequences from one key are not. The wording goes into the terms of service.

## Economy exploits

**Attacks.** Two trades at once, logging out mid-trade, crashing the server right after a trade, crossing a region border while dropping an item.

* Every durable change is an operation with an ID and safe retries (already in the Platform).
* Supply counts per item type, and currency in and out per period (PBB-1, PBB-2), with daily supply alerts (GSVC-2).
* Audit history per account and compensating operations for rollback, never deleted history (PBB-1, GSVC-2).
* Adversarial handoff tests (DSIM-3). The region transfer is the main duplication risk in this design.

## Accounts

Most stolen accounts come from reused passwords (credential stuffing), phishing pages, and fake launchers or cheat downloads that steal passwords.

* **Platform (PCS-1):** login rate limits per address and per account; Argon2id password hashing; a known-breach check on new passwords; 2FA with authenticator apps and passkeys; new-device detection with an email; sign-out everywhere.
* **Game (GSVC-4):** after a login from a new device, trades, mail and auction withdrawals wait (example 24 hours); young accounts have transfer limits (example: their first 7 days).
* **Signed launcher**, so a fake launcher cannot pass as the real one (GAME-3).

## Services and infrastructure

* **Two public doors only:** the login and API gateway, and the simulations (PINF-2). Services, databases, NATS, Prometheus (PBND-3), Grafana and Agones SDK ports stay private.
* **Between services:** mTLS, request limits, an audit log for privileged calls and secrets from a store (PSDK-1); parameterized queries and per-service database users (PSDK-2); network policies that deny by default (PINF-2).
* **Ticket signing keys** in a secret store and rotated (PCS-1).
* **Editor attach** is development-only and authenticated to staging, never on production (NET-7, GDT-13).
* **Simulation links** are authenticated by the Platform, and a client can never open one (PTR-3).

## DDoS

| Type | How it works | Target here |
| :---- | :---- | :---- |
| Volumetric | Fill the bandwidth, often amplified: DNS or CLDAP servers turn a small spoofed request into a large reply aimed at the victim | Simulation addresses |
| Protocol | Use up connection state with fake handshakes | Login, simulations |
| Application | Valid-looking but expensive requests | Login, APIs, ticks |

**Scale.** Cloudflare counted 23.2 million network-layer attacks in the first half of 2026. 90.6% ended in under 10 minutes and 96.6% stayed under 500 Mbps, but 935 exceeded 1 Tbps. Small, short attacks are the main risk here, because 500 Mbps already fills a typical game-server uplink.

**Biggest exposure.** Clients connect directly to simulation addresses, so whoever learns a node's address can flood it and take down every simulation on that node.

* **Upstream filtering (PINF-3).** Only a provider with more capacity than the attacker can absorb a volumetric flood. Options: hosts with game-tuned filtering on their game-server lines (OVHcloud is the usual example); AWS Global Accelerator, which includes Shield Standard (Shield Advanced costs US\$3,000 per month on a one-year commitment); game DDoS proxies such as Path.net or Gcore; own relays.
* **Hidden origins (PINF-3).** Clients reach only the edge. This is the same infrastructure as relay routing (Ping Resolution, technique 10), so latency and DDoS protection are bought together once there is an audience. No Platform code change is needed, because identity comes from the ticket, never from the source address (PTR-2).
* **Cheap early drops.** The GameNetworkingSockets challenge handshake means spoofed packets create no state; handshakes are limited per address (PTR-1); the ticket must come first, within a deadline (PTR-2); a kernel-level filter drops junk at scale (PINF-3).
* **Never amplify.** No unauthenticated reply is larger than its request (PTR-1).
* **HTTP behind a CDN** with rate limits (PINF-3); the login queue absorbs login floods (PCS-6).
* **No player addresses exposed.** Client and server only; voice, if ever added, goes through servers (PCS-5).
* **Fail small.** A flooded node is handled as a lost node, and the rest of the world keeps running (PINF-3).

## Supply chain and releases

**Recent incidents.**

* **Shai-Hulud (npm, September and November 2025).** It started by phishing maintainers. Each infected package stole npm, GitHub, cloud and SSH credentials and published infected versions of the maintainer's other packages. The second wave ran before install and registered infected machines as GitHub Actions runners.
* **BoltDB typosquat (Go).** boltdb-go/bolt stayed in the Go module mirror for over three years. The attacker re-pointed the Git tag to clean code, so a manual review looked fine while the mirror kept serving the backdoor.
* **tj-actions/changed-files (March 2025).** A popular GitHub Action's tags were re-pointed to code that printed CI secrets into the logs.

**Defenses.**

* **CI (BUILD-1):** Actions pinned to commit SHAs; read-only tokens by default; no secrets for pull requests from forks; SHA-256 pins for third-party sources (already the rule); go.sum with the checksum database, plus a check of the exact module path of every new dependency, since a typosquat passes the checksum; govulncheck; an update bot without auto-merge.
* **Owner settings:** branch protection on main, 2FA with a hardware key or passkey, no long-lived cloud keys on the development machine.
* **AI agents (Decision):** issues, pull requests and comments on the public repositories are untrusted text. An agent with push access never follows instructions written in them.
* **Releases (GAME-3):** builds and patch manifests signed with an offline key that never touches CI; the launcher verifies before running anything; Windows code signing. A compromised update server then cannot push code to players.

## Moderation

* **Reports carry evidence:** the last 60 seconds (example) of facts and positions around the reported player, attached automatically (GSRV-9).
* **Reports are weighted** by the reporter's history, so mass false reports do nothing (GSVC-12).
* **Sanction ladder:** warning, mute, trade lock, temporary ban, permanent ban; bots and real-money trading go straight to a ban (GSVC-12). Mutes, trade locks and kicks act in the simulation at once (GSRV-9).
* **Appeals**, and an audit log of every GM action (GSVC-12, PSDK-1).
* **Chat:** rate limits, size limits and spam filtering (PCS-5).

## Ownership

| Measure | Engine | Platform | Game |
| :---- | :---- | :---- | :---- |
| Need-to-know | Field audiences, send ranges (SIM-6, NET-4) |  | Audience per field, rare-node ranges (GSH-1, GSRV-7) |
| Decoding and budgets | Bounded decoding, fuzzing, budgets (NET-1, NET-3, NET-5, SIM-2) |  | Budget values (GSH-1) |
| Transport and tickets |  | Handshake, no amplification, ticket rules, server identity, link authentication (PTR-1, PTR-2, PTR-3) |  |
| Client integrity | Signed manifests, file hashes, release flag (ASSET-2, COOK-4); integrity channel (NET-9) |  | Anti-cheat, launcher, signing (GAME-2, GAME-3) |
| Behavior detection | Counters, combat samples (SIM-7, CMB-9) | Publishing (PBND-5) | Scoring (GSVC-11) |
| Economy | Adversarial handoff tests (DSIM-3) | Supply counts, audit, compensation (PBB-1, PBB-2) | Supply alerts, rollback, holds (GSVC-2, GSVC-4) |
| Accounts |  | Login security (PCS-1) | New-device holds, young-account limits (GSVC-4) |
| Services | Development-only attach (NET-7, GDT-13); development tickets for RunicBot (CLI-9) | mTLS, limits, audit, private services (PSDK-1, PSDK-2, PBND-3, PINF-2) |  |
| DDoS |  | Edge, hidden origins, filters (PINF-3); admission (PCS-6) |  |
| Moderation |  | Chat limits (PCS-5) | Reports, sanctions, moderation (GSRV-9, GSVC-12) |
| Supply chain | CI hardening for all three repositories (BUILD-1) |  |  |

## Stage plan

| Stage | Slices | Measures |
| :---- | :---- | :---- |
| Now | 0, 5, 12 to 14, 21, 22, 25 | CI hardening; bounded decoding, fuzzing and budgets; ticket rules and server identity; field audiences; send ranges; signed manifests; release flag |
| Services and persistence | 26 to 28, 33a | mTLS, limits and audit; login security; ledger and wallet supply counts and compensation; supply alerts |
| Scale and operations | 36, 38, 39 | Adversarial handoff tests; authenticated simulation links; development tickets for RunicBot; the behavior pipeline; development-only attach; private services |
| Launch | 44+ | Edge and DDoS protection with relays; anti-cheat; signed launcher; reports and moderation; new-device holds; chat limits; admission queue |
| After launch | 44+ | Ban waves, honeypots, machine-learning scoring, a bug bounty, and occlusion-aware interest if measurements call for it |

## Changes to the GitHub issues

Each changed issue has a Security requirements section and the security label: 58 issues, 31 in RunicEngine, 17 in RunicPlatform and 10 in RunicGame. Engine and Platform issues state mechanisms only; game values sit in RunicGame issues.

**New packages**

| ID | Package | Slice | Issue |
| :---- | :---- | :---- | :---- |
| SIM-7 | Behavior counters | 39 | [RunicEngine#191](https://github.com/PedroVicente98/RunicEngine/issues/191) |
| CMB-9 | Combat behavior samples | 39 | [RunicEngine#192](https://github.com/PedroVicente98/RunicEngine/issues/192) |
| PBND-5 | Behavior summaries to NATS | 39 | [RunicPlatform#33](https://github.com/PedroVicente98/RunicPlatform/issues/33) |
| GSVC-11 | Behavior scoring service | 39 | [RunicGame#41](https://github.com/PedroVicente98/RunicGame/issues/41) |
| NET-9 | Client-integrity channel | 44+ | [RunicEngine#193](https://github.com/PedroVicente98/RunicEngine/issues/193) |
| NET-10 | Occlusion-aware interest | 44+ | [RunicEngine#194](https://github.com/PedroVicente98/RunicEngine/issues/194) |
| PINF-3 | Edge and DDoS protection | 44+ | [RunicPlatform#34](https://github.com/PedroVicente98/RunicPlatform/issues/34) |
| GSVC-12 | Moderation service | 44+ | [RunicGame#42](https://github.com/PedroVicente98/RunicGame/issues/42) |
| GSRV-9 | Reports with evidence and in-world sanctions | 44+ | [RunicGame#43](https://github.com/PedroVicente98/RunicGame/issues/43) |
| GAME-2 | Client anti-cheat integration | 44+ | [RunicGame#44](https://github.com/PedroVicente98/RunicGame/issues/44) |
| GAME-3 | Signed releases, launcher and file integrity | 44+ | [RunicGame#45](https://github.com/PedroVicente98/RunicGame/issues/45) |

**Updated packages.** RunicEngine: BUILD-1, SIM-2, SIM-6, NET-1, NET-3, NET-4, NET-5, NET-7, DSIM-3, GDT-13, CLI-9, COOK-4, ASSET-2. RunicPlatform: PTR-1, PTR-2, PTR-3, PSDK-1, PSDK-2, PCS-1, PCS-5, PCS-6, PBND-3, PINF-2, PBB-1, PBB-2. RunicGame: GSH-1, GSVC-2, GSVC-4, GSRV-7, GCL-2.

**Updated slices.** 0, 5, 12, 13, 14, 21, 22, 24, 25, 26, 27, 28, 33a, 36, 38, 39 and 44+. Slice 39 is now owned by Engine, Platform and Game.

## Differences from the Vision and the Architecture

* **Vision:** adds that there is no mod or add-on support, and that the soundtrack (albums, presets, radio stations) is the only player-made content. The Vision's optional key combos become the allowed side of the macro policy.
* **Vision:** adds new-device holds and young-account limits on trade and mail, and the sanction ladder.
* **Architecture:** adds 11 packages, 4 in slice 39 and 7 in slice 44+, listed above.
* **Architecture:** replicated fields default to server only (SIM-6); the ticket must be the first message, within a deadline; development keys are a separate key set; the client checks the server's identity (PTR-2).
* **Architecture:** the item ledger and wallets gain supply counts, audit history and compensating operations; services gain mTLS, limits and an audit log.
* **Architecture:** DDoS protection and relay routing become one edge (PINF-3), deferred until there is an audience.
* **Architecture:** needs a Security chapter, which this appendix becomes. The existing soundtrack security rules stay as they are.

## Open

* Anti-cheat vendor: Easy Anti-Cheat is proposed because it is free; confirm when the launch plan is made.
* DDoS provider and edge, shared with the relay provider.
* Macro policy wording and the terms of service.
* How precisely enemy players' health is shown (exact, rounded or in bands), which sets what the server sends.
* Hold and limit values (24 hours, 7 days, a 60-second report window) are examples.
* Honeypot design, and when to add machine-learning scoring and a bug bounty.

## Sources

* [Cloudflare DDoS Threat Report, H1 2026](https://blog.cloudflare.com/ddos-threat-report-2026-h1/)
* [Easy Anti-Cheat, Wikipedia](https://en.wikipedia.org/wiki/Easy_Anti-Cheat)
* [GameNetworkingSockets README](https://github.com/michicc/GameNetworkingSockets)
* [GameNetworkingSockets configuration options (Go binding documentation)](https://pkg.go.dev/github.com/KomiMoe/gns)
* [Unit 42: Shai-Hulud npm supply-chain attack](https://unit42.paloaltonetworks.com/npm-supply-chain-attack.md)
* [The Hacker News: malicious Go package served by the module mirror](https://thehackernews.com/2025/02/malicious-go-package-exploits-module.html)
* [AWS Shield pricing](https://aws.amazon.com/shield/pricing)
* [AWS for Games: defending games against DDoS](https://aws.amazon.com/blogs/gametech/how-to-defend-your-games-against-ddos-attacks)
