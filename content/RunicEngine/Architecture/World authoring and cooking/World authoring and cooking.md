---
title: "World authoring and cooking (Engine, Game)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "World authoring and cooking (Engine, Game)"
created: "2026-10-14"
modified: "2026-10-30"
---

The world is assembled in the [[Tools#RunicEditor|RunicEditor]] (Godot) as one low-detail world scene plus detailed region scenes, Blender makes the assets, and [[Cooker|the Cooker]] turns those scenes into Runic-native server and client packages; the shipping client and server never read an editor scene or a Blender file.

## Contents

- [[Ownership (World authoring and cooking)|Ownership]]
- [[Godot and Blender|Godot and Blender]]
- [[World scene and region scenes|World scene and region scenes]]
- [[Large worlds in the editor|Large worlds in the editor]]
- [[Seamless terrain and borders|Seamless terrain and borders]]
- [[Marker nodes and what they cook into|Marker nodes and what they cook into]]
- [[Resources by spawn area decided|Resources by spawn area (decided)]]
- [[Interchange glTF and terrain sources|Interchange: glTF and terrain sources]]
- [[Cooker|Cooker]]
- [[Cooked world files and packages|Cooked world files and packages]]
- [[Authoring work per roadmap slice|Authoring work per roadmap slice]]
- [[Project layout and schemas|Project layout and schemas]]

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Debug drawing|Debug drawing (Engine)]] · [[Vertical-slice roadmap|Vertical-slice roadmap]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › World authoring and cooking (Engine, Game) · exported 2026-11-03
