---
title: "Conventions (Proposal)"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Database Layout"
source_url: "https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit"
section: "Conventions (Proposal)"
created: "2026-10-26"
modified: "2026-10-30"
---

| Value | Type | Rule |
| :---- | :---- | :---- |
| IDs | bigint (int64) | Matches the Engine's 64-bit IDs. Proposal: persistent entities (characters, ships, [[Trade packs and routes\|trade packs]], crops, survey tools) use their database ID as their GlobalEntityId, with the kind in the top bits. |
| Operation IDs | uuid (128-bit) | SimulationId plus sequence for operations the simulation starts (stable event IDs, [[EVT-1\|EVT-1]]); services make their own for theirs. |
| World positions | double precision × 3 | WorldPosition is 64-bit (decided); stored as pos\_x, pos\_y, pos\_z with the real Y. |
| Local offsets | real | Furniture inside a house is a local 32-bit offset, never a world position. |
| Money | bigint | Smallest currency unit; no floating point anywhere near money. |
| Real time | timestamptz | Cooldowns, expiries, schedules. |
| World time | bigint milliseconds | Since the map's world epoch (coordinator.maps), so every simulation agrees. |
| Content references | text | Namespaced ContentIds such as game:item/iron\_sword, validated by services at boot against the cooked data. |
| Game-defined blobs | jsonb | Only where the shape belongs to the Game and is read whole: item payload, quest branches, appearance sliders. |
| Concurrency | version int | Optimistic concurrency on rows several writers touch. |

---

↑ [[Database Layout|Database Layout]] · ← [[Physical layout Proposal|Physical layout (Proposal)]] · [[Where each thing lives|Where each thing lives]] →  
Source: [RunicEngine — Appendix: Database Layout](https://docs.google.com/document/d/1ex3n2TbxelB7QQnSZYIyQJxl0-Wj1WjmkRuolwk8tY8/edit) › Conventions (Proposal) · exported 2026-11-03
