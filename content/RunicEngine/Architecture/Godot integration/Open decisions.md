---
title: "Open decisions"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine) › Open decisions"
created: "2026-10-14"
modified: "2026-10-30"
---

| \# | Decision | Options | Recommendation |
| :---- | :---- | :---- | :---- |
| 1 | Data file format (skills, items, AI, quests) | Runic text files opened in Godot through a loader, or Godot .tres | Runic files: the server reads them without Godot and the v3 versioned schemas keep working |
| 2 | New project from the project manager | A small patch in Godot’s project manager, or a plugin that initializes an empty project | The plugin first; the patch only if the experience asks for it |
| 3 | Client animation | (A) the Runic evaluator with poses sent to RenderingServer skeletons, no nodes; (B) Godot’s AnimationTree driven by the animation intent | A keeps “no nodes” and controls crowd cost; B brings a visual blend editor |
| 4 | MusicDirector | Runic logic with a Godot backend, or code on the Godot side | Runic logic: generic, testable and independent of rendering |
| 5 | Fallback if the editor cannot run as a library | The [[Tools#RunicEditor\|RunicEditor]] becomes a Godot editor built by Runic that loads the Runic tools as a GDExtension | Approve now as plan B: the same code, only the owner of the process changes |

---

↑ [[Godot integration|Godot integration (Engine)]] · ← [[Risks (Godot integration)|Risks (Godot integration)]]  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) › Open decisions · exported 2026-11-03
