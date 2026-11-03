---
title: "Bots and scripts"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
section: "Bots and scripts"
created: "2026-10-22"
modified: "2026-10-22"
---

Bots farm currency and materials for real-money trading, level accounts to sell, gather nonstop, and auto-dodge or auto-aim in PvP. Farming bots are an attack on the economy: they push prices up and lower the value of players' time.

**Detection is behavior profiling (Decision).** A Go scoring service ([[GSVC-11|GSVC-11]]) rates how human each player looks from these signals:

* **Reaction time.** Most people react to a cue they are watching for in about 200 to 300 ms, with a wide spread; very fast players get near 150 ms. Bots sit near 0 ms or are too regular. Thousands of samples per player make this reliable.
* **Fatigue.** Human timing and accuracy drift over a long session; a bot's do not.
* **Routes.** The same path, jumps and camera angles, repeated.
* **Session shape.** Twenty hours a day, or back online seconds after a kick.
* **Money flow.** Many young accounts feeding one account (mules).

**Pipeline without tick blocking.** The Simulation keeps small per-player counters ([[SIM-7|SIM-7]]), and Combat adds reaction and aim samples ([[CMB-9|CMB-9]]). One summary per player per minute, about 128 bytes, goes through the service port to NATS on a lossy stream ([[PBND-5|PBND-5]]). At 10,000 players that is about 1.8 GB per day, against about 69 GB per day for raw events, and about 170 summaries per second for the scoring service. Features, thresholds and scores stay secret and server-side. [[Tools#Testing at scale|RunicBot]] sessions are the first test: they must be flagged, and a human session must not.

**Making bots unprofitable.** Labor caps production per account (already decided) and [[Inventory equipment and the Market Isle#Market Isle (working name)|Market Isle]] blueprints are bound. Young-account transfer limits and new-device holds are added ([[GSVC-4|GSVC-4]]).

**Enforcement.** Automation only flags; a person reviews before any permanent ban. Ban waves (detect now, ban in batches later) hide what triggered detection. Honeypots, entities that only a bot reading the entity list would touch, are a Proposal.

**Macro policy (Open).** The game itself offers optional key combos (Vision), so built-in combos are allowed, as are key remapping and accessibility tools. Third-party tools that fire timed sequences from one key are not. The wording goes into the terms of service.

---

↑ [[Security|Security]] · ← [[The protocol|The protocol]] · [[Economy exploits|Economy exploits]] →  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) › Bots and scripts · exported 2026-11-03
