---
title: "Ships (Content Pipeline)"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
section: "Ships"
created: "2026-10-26"
modified: "2026-10-30"
---

* **Decision.** Ships are modular. Stations (helm, cannons, anchor, mage, archer, repair and others) are models attached to the ship, each ship has its own hull, and mast types (such as the fore-and-aft sail at the stern) are reused and resized across ships.
* **Proposal.** Stations are prefabs that snap onto named attachment points on the hull (socket_cannon_01), each with its own collision and interaction volume.
* **Proposal.** Masts are scaled in length only, never uniformly, so thickness and texture density stay the same.
* **Proposal.** Sails move in a vertex shader driven by the ship's wind value from the wind system, with no bones.

---

↑ [[Content Pipeline and Art Direction|Content Pipeline and Art Direction]] · ← [[Environment|Environment]] · [[Textures and materials|Textures and materials]] →  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) › Ships · exported 2026-11-03
