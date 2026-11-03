---
title: "Budgets"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Budgets"
created: "2026-10-26"
modified: "2026-10-30"
---


## Character triangles

**Proposal.** Triangle budgets at full detail:

| **Part** | **Triangles** | **Notes** |
| :---- | :---- | :---- |
| Body and head | 12k to 16k | About 5k in the face, for Black Desert-style creation and expressions |
| Hair | 5k to 10k | Often the hidden cost |
| Armor (5 pieces) | +8k to 12k net | The body under each piece is hidden, so triangles are not paid twice |
| Weapon | 2k to 4k |  |
| Player total | 25k to 35k | Between the Black Desert NPC (24k) and AAA single-player characters |
| Lower-detail versions (LODs) | 50%, 20% and 8% of full detail | The farthest at about 2k to 3k, for sieges |
| Common mob | 8k to 20k |  |
| World boss | 50k to 150k | Only one on screen |

Detailed swings do not need more triangles: the Black Desert NPC above has 24k. What changes is where the triangles go (see Characters).

## Crowds

* 200 players (100 vs 100) at 30k with no LODs: 6M triangles. Shadows draw most of them one or two more times, so 12M to 18M per frame, with about 4M vertices skinned.
* 200 players with LODs (10 near at 30k, 40 mid at 12k, 150 far at 3k): about 1.2M triangles, 5× cheaper, with no visible difference at distance.
* 500 players with the same split (10, 40 and 450): about 2.1M triangles.
* Draw calls: 8 meshes per character (5 armor pieces, head, hair and weapon) × 200 players is 1,600 per pass, about 4,800 with two shadow passes. Merging distant players into one or two meshes with a shared texture brings it to about 550 to 700 per pass.
* Bones: 200 players × 140 bones × 60 updates per second is about 1.7M bone updates per second. With animation LODs (10 at the full rig and 60 Hz, 40 at about 70 bones and 30 Hz, 150 at about 25 bones and 15 Hz), it is about 224k per second, about 7× less. This matches the [[Simulation core clock and threads#Multi-rate fixed-step scheduler|multi-rate scheduler]].

## Texture memory

| **Size** | **Memory per map with mipmaps, block-compressed (approx.)** |
| :---- | :---- |
| 2K (2048 × 2048) | 5.3 MB |
| 1K | 1.3 MB |
| 512 | 0.35 MB |
| One fully unique character: 8 pieces at 2K with 3 maps each | About 130 MB |

Distant characters need small texture versions: a 256-pixel texture uses 1/64 of the memory of a 2K one.

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Art direction|Art direction]] · [[Characters|Characters]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Budgets · exported 2026-11-03
