---
title: "Animation"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Animation"
created: "2026-10-26"
modified: "2026-10-30"
---

* **Decision.** The vertical slice uses free animations and rigs from the web.
* **Proposal.** Quaternius' Universal Animation Library 1 and 2 as the main source: 120+ and 130+ animations on a humanoid rig ready for Godot, under CC0. The second volume adds melee and armed combos, parkour, farming and fishing. The free Standard version of the first has 45 animations; the full set comes in the paid Pro and Source versions.
* **Proposal.** Mixamo only for internal use. It is free for commercial games, but its FAQ excludes templates and asset packages that redistribute its raw character or animation files, and forbids using its content to train machine-learning models. The Engine will be distributed, so its templates and samples ship only with CC0 or own animations. Check Adobe's current terms before use.
* **Proposal.** Later: motion capture packs for sword and spear combat, or markerless capture from phone video, polished in Blender for weight, anticipation and the hit frame.
* **Proposal.** Retargeting in Godot with SkeletonProfileHumanoid, which maps bones automatically and works best with common English bone names. Twist and corrective bones are not part of that profile; they are computed in code from the limb rotation, so they work with any retargeted clip.
* **Proposal.** Swings are built in the phases of [[Vision|the Vision]]'s timing profiles (startup, active, recovery), each with a clean blend point, so cancelling into a dodge does not make the character jump. Example: a sword light attack has 6 ticks of startup (about 200 ms) and 8 ticks of recovery (about 267 ms).
* **Proposal.** The pipeline exports each clip's hit marker, and the validation script fails a clip whose marker differs from its weapon's timing profile by more than one tick (33 ms).
* **Proposal.** One skeleton per creature family: humanoid, quadruped, bird and so on. Mixamo and Quaternius cover humanoids only, so wolves need their own quadruped rig and animations, reused by every four-legged creature.

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Characters|Characters]] · [[Weapons|Weapons]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Animation · exported 2026-11-03
