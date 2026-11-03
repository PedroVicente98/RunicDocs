---
title: "RunicGame — Appendix: Ping Resolution"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Ping Resolution"
source_url: "https://docs.google.com/document/d/1iYe10T523upQnBfv91Pk3dL1FC6TuyF7hmdGg6ZG5Ys/edit"
created: "2026-10-21"
modified: "2026-10-21"
---

Design appendix from the conversation of 21 October 2026, to be merged later into [[Vision|the game vision]] and the technical architecture. Part 1 is locked: the latency techniques, each tested in the Latency Feel Lab. Part 2 compiles the combat discussion of the same day, for the owner to decide what moves on. Items are labeled Decision, Proposal or Open. Numbers are examples for tuning.

**Latency Feel Lab:** [open the lab](https://claude.ai/artifact/PfdrhpR4XQ3KhEypGybMdq). It runs in any browser (desktop recommended, Space is the action key) and is private until shared from its Share menu. Labs 1–9 match the techniques below.

## Contents

- [[Part 1 Locked ping resolution|Part 1. Locked: ping resolution]]
  - [[Part 1 Locked ping resolution#The common timeline|The common timeline]]
  - [[Part 1 Locked ping resolution#Locked techniques|Locked techniques]]
  - [[Part 1 Locked ping resolution#1. Prediction for own actions|1. Prediction for own actions]]
  - [[Part 1 Locked ping resolution#2. Telegraph fast-forward|2. Telegraph fast-forward]]
  - [[Part 1 Locked ping resolution#3. Defender grace (all defense)|3. Defender grace (all defense)]]
  - [[Part 1 Locked ping resolution#4. Predicted impact effects|4. Predicted impact effects]]
  - [[Part 1 Locked ping resolution#5. Capped rewind|5. Capped rewind]]
  - [[Part 1 Locked ping resolution#6. Remote projectiles at their real position|6. Remote projectiles at their real position]]
  - [[Part 1 Locked ping resolution#7. Adaptive interpolation delay|7. Adaptive interpolation delay]]
  - [[Part 1 Locked ping resolution#8. Input redundancy|8. Input redundancy]]
  - [[Part 1 Locked ping resolution#9. Combat facts first|9. Combat facts first]]
  - [[Part 1 Locked ping resolution#10. Relay routing|10. Relay routing]]
  - [[Part 1 Locked ping resolution#Dependencies and resolution order|Dependencies and resolution order]]
  - [[Part 1 Locked ping resolution#Reaction window by ping|Reaction window by ping]]
  - [[Part 1 Locked ping resolution#Gameplay consequences to keep in mind|Gameplay consequences to keep in mind]]
  - [[Part 1 Locked ping resolution#Ownership|Ownership]]
- [[Part 2 Combat discussion of 21 October for decision|Part 2. Combat discussion of 21 October, for decision]]
  - [[Part 2 Combat discussion of 21 October for decision#Lessons from Vindictus and TERA|Lessons from Vindictus and TERA]]
  - [[Part 2 Combat discussion of 21 October for decision#Animation lock and canceling|Animation lock and canceling]]
  - [[Part 2 Combat discussion of 21 October for decision#What the numbers feel like|What the numbers feel like]]
  - [[Part 2 Combat discussion of 21 October for decision#Design rules for latency (proposal)|Design rules for latency (proposal)]]
  - [[Part 2 Combat discussion of 21 October for decision#Hit detection with Jolt|Hit detection with Jolt]]
  - [[Part 2 Combat discussion of 21 October for decision#Collision between characters|Collision between characters]]
  - [[Part 2 Combat discussion of 21 October for decision#Vindictus-style environment in an open world (proposal)|Vindictus-style environment in an open world (proposal)]]
  - [[Part 2 Combat discussion of 21 October for decision#Cosmetic items and effects|Cosmetic items and effects]]
  - [[Part 2 Combat discussion of 21 October for decision#Open|Open]]
  - [[Part 2 Combat discussion of 21 October for decision#Sources|Sources]]

---

↑ [[index|RunicDocs]]  
Source: [RunicGame — Appendix: Ping Resolution](https://docs.google.com/document/d/1iYe10T523upQnBfv91Pk3dL1FC6TuyF7hmdGg6ZG5Ys/edit) · exported 2026-11-03
