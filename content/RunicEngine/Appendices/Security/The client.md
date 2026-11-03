---
title: "The client"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
section: "The client"
created: "2026-10-22"
modified: "2026-10-22"
---

**Attacks.**

* Memory scanners and debuggers read or change values in RAM.
* Injected code hooks the renderer to draw hidden information (ESP), or hooks the send function to send its own commands. The hook runs before encryption, so encryption does not stop it.
* Modified files: see-through walls, removed fog. Godot packs are easy to extract, so everything shipped in the client is public and will be datamined.
* Input automation: macros, scripts, and USB devices that act as a keyboard, which software cannot see.
* Screen-reading bots: computer vision on the screen with no memory access, growing quickly with AI models.
* DMA hardware: a card that reads the game's memory from a second PC, mostly invisible to software anti-cheat.

**What it gets them.** Changing values locally does nothing, because the server runs the same shared rules and decides every outcome: speed, teleport, fly, god-mode and infinite-[[Stamina and climbing#Stamina|stamina]] hacks fail. What remains is reading what the server sent and automating a real player's hands.

**Defenses.**

* **Need-to-know (Decision).** Every replicated field declares its audience, server only by default ([[SIM-6|SIM-6]]), and entity kinds can have a short send range ([[NET-4|NET-4]]). Hidden players are never sent and hidden casters' effects carry no identity (already in the architecture). Game rules: enemy players' exact values are sent only if the UI shows them ([[GSH-1|GSH-1]]); rare resource nodes only nearby ([[GSRV-7|GSRV-7]]).
* **Occlusion-aware interest (Proposal, deferred).** Send hostile players only when they could become visible soon, as Valorant does. Built only if PvP measurements show wallhacks are a real problem ([[NET-10|NET-10]]).
* **Client anti-cheat (Decision; vendor is a Proposal).** Easy Anti-Cheat is free through Epic Online Services, with a kernel driver on Windows and user mode only on Linux and Steam Deck. It stops cheap public cheats, which is most cheaters, but not DMA cards, hardware input devices or screen-reading bots. The Engine provides an opaque integrity channel ([[NET-9|NET-9]]); the Game integrates the provider ([[GAME-2|GAME-2]]).
* **File integrity (Decision).** Signed manifests with a hash for every file ([[COOK-4|COOK-4]], [[ASSET-2|ASSET-2]]); the launcher verifies and repairs ([[GAME-3|GAME-3]]). Unreleased content never ships in a client build ([[COOK-4|COOK-4]]).
* **Behavior detection** (see Bots and scripts) for everything the client side cannot see.

---

↑ [[Security|Security]] · ← [[Decisions|Decisions]] · [[The protocol|The protocol]] →  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) › The client · exported 2026-11-03
