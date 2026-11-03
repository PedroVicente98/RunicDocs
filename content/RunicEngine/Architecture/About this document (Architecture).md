---
title: "About this document (Architecture)"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "About this document"
created: "2026-10-14"
modified: "2026-10-30"
---

This is the single technical architecture for RunicEngine, RunicGame and RunicPlatform: what each one owns, how they connect, and the decisions behind them.

* **Ownership labels.** Every section and table names its owner: **Engine** (RunicEngine — generic mechanisms any MMORPG can use), **Game** (RunicGame — this game’s rules, content and executables) or **Platform** (RunicPlatform — services, SDK and infrastructure any MMORPG can use).

* **Goal.** The most performant architecture that does not sacrifice [[Vision|the game vision]], generic enough that another team could build a different MMORPG on Engine and Platform, including a much larger world.

* **Numbers** (rates, sizes, budgets) are planning targets unless the decisions log marks them as decided; final values come from profiling and playtests.

* **Code** appears only as contract sketches. Names are illustrative, not a frozen API.

* **Self-contained.** Everything needed is written here; the documents this one consolidates are listed by name in the footer.

* **What changed in v4.** Godot is integrated as a library from the first build: it renders, plays audio and owns the window, input and player UI in the client, and it is the editor (the [[Tools#RunicEditor|RunicEditor]]). The simulation, networking, world, Platform and services of v3 are unchanged, and the server never links Godot. New section: Godot integration. Rewritten: Client runtime, Render data and world UI, Tools, Debug drawing (formerly Debug renderer), World authoring and cooking, the presentation and tool work packages, and the roadmap, which now names the Godot step of every slice from slice [[Slice 00 Build skeleton|0]]\.

---

↑ [[Architecture|Technical Architecture v4]] · [[Architecture overview|Architecture overview]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › About this document · exported 2026-11-03
