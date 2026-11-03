---
title: "Characters"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Characters"
created: "2026-10-26"
modified: "2026-10-30"
---

* **Decision.** Two body types, female and male, each with variation in height, width and similar.
* **Decision.** One armor model per weight class (cloth, leather, plate), fitted to the body types and then modified and morphed into variants.
* **Proposal.** One skeleton for every playable race and body type. Races already share one hurtbox ([[RACE-02 Race Archetypes and Size|RACE-02]]), so every animation works on every race.
* **Proposal.** Bodies start from MPFB2 (MakeHuman Plugin for Blender, Blender 4.2 or later): parametric age, build and gender, automatic rigging with Rigify support, and characters with realistic proportions. Its code is GPLv3 and its bundled assets are CC0. The MakeHuman project's position is that output, including output generated through scripts, contains no program code, so it can be used without restriction. Check its triangle count against the 12k to 16k body budget.
* **Proposal.** Height and limb length come from bone scaling, which armor follows automatically. Body mass comes from 2 or 3 shape keys that the pipeline copies onto every armor piece with Blender's Data Transfer or Surface Deform. The hurtbox stays the same for everyone.
* **Proposal.** The body is split into the five armor regions (head, chest, hands, legs, feet). Each armor piece hides its region, which avoids clipping and spends no triangles twice.
* **Proposal.** Armor is built from the body surface: select the region, offset it outward and add details. It fits the body and inherits the skinning weights.
* **Proposal.** Nothing in any armor stops the arm from going above the head. Pauldrons are segmented and follow the collarbone and the upper arm.
* **Proposal.** At least three edge loops at elbows and knees, and extra density at the shoulder, armpit and hips.
* **Proposal.** Textures carry dye masks from the start, so one armor mesh gives many looks.

## Rig

**Proposal.** Bones per part:

| **Part** | **Bones** | **Why** |
| :---- | :---- | :---- |
| Standard humanoid with fingers | About 55 | Weapon grips, drawing a bow, playing instruments |
| Twist bones (upper arm, forearm, thigh, calf) | 8 to 16 | Stops the forearm from collapsing when the wrist rotates mid-swing |
| Corrective bones (shoulder, elbow, knee, hip) | 6 to 10 | Keeps the shape in extreme poses |
| Weapon bones | 3 to 5 | Both hands, back or hip, two-handed grips |
| Hair, cloak and cloth chains | 10 to 30 | Follow-through motion and physics; the cloak slot |
| Face | 30 to 60, or shape keys | Black Desert-style character creation and expressions |
| Total at full detail | About 110 to 170 |  |

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Budgets|Budgets]] · [[Animation|Animation]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Characters · exported 2026-11-03
