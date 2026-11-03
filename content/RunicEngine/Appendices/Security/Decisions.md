---
title: "Decisions"
tags:
  - "runicengine"
  - "appendix"
source: "RunicEngine — Appendix: Security"
source_url: "https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit"
section: "Decisions"
created: "2026-10-22"
modified: "2026-10-22"
---

* **No mod or add-on support (Decision).** Players cannot load UI add-ons, scripts or modified files. A game that needs add-ons has a UI that failed; the answer is a better original UI. Editor plugins for developers ([[GDT-16|GDT-16]]) are not affected.
* **The soundtrack is the only player-made content (Decision).** Playlists, presets and radio stations, with the game's context choosing the mood. They are data only, validated on import, and live outside the installed game files. The Architecture's soundtrack security rules already apply.
* **Every measure in this appendix is adopted (Decision)**, on the stage plan below.
* **The client is untrusted (Decision).** Anything sent to it can be read, and anything it sends can be forged. Server authority, already in the architecture, stays the foundation; the measures below cover what authority alone does not.
* **No security through obscurity (Decision).** RunicEngine and RunicPlatform are public, so the wire encoding, the bot runtime and the login flow are public. Every defense must hold with the code known.
* **Consequence of having no mods.** Any change to an installed game file is tampering or damage, so the launcher repairs it and the client does not connect after a failed integrity check ([[GAME-3|GAME-3]]).

## Who attacks and why

| Attacker | Goal | Main avenue |
| :---- | :---- | :---- |
| Cheater | Win fights, see hidden information | Client tools and input automation |
| Bot farmer | Currency and items to sell for real money | Headless clients and scripts |
| Account thief | Items and currency to resell | Reused passwords, phishing, fake downloads |
| Duper | Create items or currency from nothing | Race conditions, crashes, region handoffs |
| [[DDoS\|DDoS]] attacker (rival, extortionist, banned player) | Take a region or the login down | Floods against server addresses |
| Supply-chain attacker | The developer's tokens and keys, or the players' machines | Contaminated dependencies, CI, the update server |

---

↑ [[Security|Security]] · [[The client|The client]] →  
Source: [RunicEngine — Appendix: Security](https://docs.google.com/document/d/1W9S-5tPLsfXRzNXKb9vazkhnFiolq1QhV1C1i_o2PbQ/edit) › Decisions · exported 2026-11-03
