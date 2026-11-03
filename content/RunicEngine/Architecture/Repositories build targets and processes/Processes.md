---
title: "Processes"
tags:
  - "runicengine"
  - "architecture"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Repositories, build targets and processes › Processes"
created: "2026-10-14"
modified: "2026-10-30"
---

| Process | Owner | Runs | Shipped |
| :---- | :---- | :---- | :---- |
| GameClient | Game | Client layers on the Engine; Godot renders, plays audio and owns the window | Yes; shipping builds use Godot’s template build and no development overlay |
| GameServer | Game | Server layers on the Engine, one region per pod | Yes, to the server fleet |
| [[Tools#RunicEditor\|RunicEditor]] | Engine | The Godot editor with the Runic tools and the project’s editor library; attaches to development and staging servers | Never |
| [[Cooker\|Cooker]] | Engine | Inside the RunicEditor, or the RunicEditor headless on build machines | Never |
| [[Tools#Testing at scale\|RunicBot]] | Engine | The client runtime without presentation, many bot sessions per process, for scale tests | Never |
| Game services | Game | Go services built on the Platform SDK | Yes, to the server fleet |
| Platform services | Platform | Core services and building blocks | Yes, to the server fleet |

---

↑ [[Repositories build targets and processes|Repositories, build targets and processes]] · ← [[Platform modules|Platform modules (Platform)]] · [[Four axes that must stay separate|Four axes that must stay separate]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Repositories, build targets and processes › Processes · exported 2026-11-03
