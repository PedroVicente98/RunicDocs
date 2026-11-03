---
title: "RunicGame — Appendix: Content Pipeline and Art Direction"
tags:
  - "runicgame"
  - "appendix"
source: "RunicGame — Appendix: Content Pipeline and Art Direction"
source_url: "https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit"
created: "2026-10-26"
modified: "2026-10-30"
---

Design appendix from the conversation of 26 October 2026 about [[Art direction|art direction]] and the content pipeline, to be merged later into [[Vision|the game vision]] and the technical architecture. It was compared with the Drive versions of [[Vision|RunicGame — Visão Completa do MMORPG]] (13 Oct), [[Ideias|RunicGame — Ideias]] (25 Oct) and [[Architecture|RunicEngine — Technical Architecture v4]] (14 Oct).

In short: RunicGame keeps World of Warcraft's identity (color, readable shapes, armor design) on bodies with near-real proportions like Black Desert's, so weapon swings can be animated in detail, at a fidelity between World of Warcraft and ArcheAge. Crimson Desert's fidelity is out of scope, because it is a single-player budget. Content comes from a small set of human-made base models that scripts and recipes turn into many variants, so one or two developers can produce a vertical slice.

The first sections list the differences from those documents. The rest describes each part, and the requirements at the end are split by repository: Engine, Game and Platform. Every item is labeled Decision (stated in the conversation), Proposal (recommended, not yet accepted), Open or Dropped. Numbers are planning estimates; budgets are confirmed by measuring in Godot.

## Contents

- [[Differences from the Vision (Content Pipeline)|Differences from the Vision]]
- [[Differences from Technical Architecture v4 (Content Pipeline)|Differences from Technical Architecture v4]]
- [[Related entries in Ideias|Related entries in Ideias]]
- [[Art direction|Art direction]]
  - [[Art direction#Target|Target]]
  - [[Art direction#Reference games|Reference games]]
  - [[Art direction#Texture approach|Texture approach]]
  - [[Art direction#Reference sources|Reference sources]]
- [[Budgets|Budgets]]
  - [[Budgets#Character triangles|Character triangles]]
  - [[Budgets#Crowds|Crowds]]
  - [[Budgets#Texture memory|Texture memory]]
- [[Characters|Characters]]
  - [[Characters#Rig|Rig]]
- [[Animation|Animation]]
- [[Weapons|Weapons]]
- [[Mobs|Mobs]]
- [[Environment|Environment]]
- [[Ships (Content Pipeline)|Ships]]
- [[Textures and materials|Textures and materials]]
- [[Pipeline|Pipeline]]
  - [[Pipeline#Sources and scripts|Sources and scripts]]
  - [[Pipeline#Build flow|Build flow]]
  - [[Pipeline#Naming and attachment points|Naming and attachment points]]
  - [[Pipeline#Validation script|Validation script]]
  - [[Pipeline#Version control and licenses|Version control and licenses]]
- [[Map authoring markers|Map authoring markers]]
  - [[Map authoring markers#Painted layers (GIMP)|Painted layers (GIMP)]]
  - [[Map authoring markers#Points|Points]]
  - [[Map authoring markers#Areas|Areas]]
  - [[Map authoring markers#Paths|Paths]]
  - [[Map authoring markers#Ship assets (Blender)|Ship assets (Blender)]]
- [[Vertical slice order|Vertical slice order]]
- [[Requirements by repository (Content Pipeline)|Requirements by repository]]
  - [[Requirements by repository (Content Pipeline)#Engine|Engine]]
  - [[Requirements by repository (Content Pipeline)#Game|Game]]
  - [[Requirements by repository (Content Pipeline)#Platform|Platform]]
- [[Open (Content Pipeline)|Open]]
- [[Dropped (Content Pipeline)|Dropped]]
- [[Sources (Content Pipeline)|Sources]]

---

↑ [[index|RunicDocs]]  
Source: [RunicGame — Appendix: Content Pipeline and Art Direction](https://docs.google.com/document/d/1SQ4d0oVU_sqVEO6JtGF4nym9JUYtIM7-3-52tHIbcYQ/edit) · exported 2026-11-03
