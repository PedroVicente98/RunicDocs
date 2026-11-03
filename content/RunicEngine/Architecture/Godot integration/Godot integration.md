---
title: "Godot integration (Engine)"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "Godot integration (Engine)"
created: "2026-10-14"
modified: "2026-10-30"
---

Godot enters the Engine as a library (LibGodot) in two roles: renderer, window, input, audio and player UI inside the client, and the authoring editor inside the [[Tools#RunicEditor|RunicEditor]]. The simulation, networking, world, Platform and services of v3 do not change, the server never links Godot, and the [[RenderData in Core|RenderFrame]] is the only door from the Runic client into Godot.

## Contents

- [[Role of Godot decided|Role of Godot (decided)]]
- [[Executables and Godot targets|Executables and Godot targets]]
- [[How the Engine uses Godot|How the Engine uses Godot]]
- [[Projects create open and the games editor library|Projects: create, open and the game’s editor library]]
- [[Game code and the Run button|Game code and the Run button]]
- [[Building Godot|Building Godot]]
- [[GDScript editor tools only|GDScript: editor tools only]]
- [[Godot plugins|Godot plugins]]
- [[Threads precision and input|Threads, precision and input]]
- [[Risks (Godot integration)|Risks]]
- [[Open decisions|Open decisions]]

---

↑ [[Architecture|Technical Architecture v4]] · ← [[Application and LayerStack|Application and LayerStack (Engine)]] · [[Simulation core clock and threads|Simulation core: clock and threads (Engine)]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › Godot integration (Engine) · exported 2026-11-03
