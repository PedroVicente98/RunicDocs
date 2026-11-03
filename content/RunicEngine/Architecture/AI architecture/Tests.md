---
title: "Tests"
tags:
  - "runicengine"
  - "architecture"
  - "repo/engine"
  - "repo/game"
source: "RunicEngine — Technical Architecture v4"
source_url: "https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit"
section: "AI architecture (Engine, Game) › Tests"
created: "2026-10-14"
modified: "2026-10-30"
---

| Area | Representative tests |
| :---- | :---- |
| Perception | A hostile entering detect radius wakes the NPC engaged; entering only warn radius wakes it alerted; high concealment shrinks the radii; the minimum radius still detects in total darkness; damage wakes from outside both radii |
| Target validity | Death, concealment beyond detect range or leash break invalidates or changes behavior according to policy |
| Reaction timing | A threat before reactAt fails HasReactableThreat; the same threat after reactAt succeeds |
| Utility | Unavailable actions score invalid; personality biases change ordering; a fixed seed reproduces a choice |
| Intent boundary | A tree action emits the expected intent and never changes CombatState directly |
| Command rejection | Choosing a defensive action while committed is rejected; AI never bypasses combat rules |
| Wake and sleep | A BrainHandle is created on wake and recycled on sleep; dormant entities never tick a tree |
| Editor validation | Unknown nodes, ports or content IDs are reported; valid assets round-trip without loss |

**Integration tests**

1. An NPC detects a player, approaches, attacks, reacts to a telegraphed attack and returns home after a leash break.

2. At night an unlit player passes outside the reduced detect radius unnoticed, while a player carrying a torch is detected from farther away.

3. A player raises concealment while engaged; the target is dropped according to Game policy, and lowering it makes the player detectable again.

4. An NPC chooses a defense after its action became non-cancellable and correctly fails to execute it.

5. A SkillStarted fact produced in the realtime phase reaches AI memory only in the post-realtime phase and is acted on in a later pre-realtime tick.

6. Runic::AI builds and runs headless with no Godot or editor dependency.

7. Selecting a live NPC in the [[Tools#RunicEditor|RunicEditor]] shows the same BrainHandle, tree, memory and intents the runtime instrumentation records.

---

↑ [[AI architecture|AI architecture (Engine, Game)]] · ← [[Performance and scaling|Performance and scaling]] · [[Implementation order|Implementation order]] →  
Source: [RunicEngine — Technical Architecture v4](https://docs.google.com/document/d/1GOCAfCfUjXrdDzDlcPFirDjGKZ6h20uFtqAEfqHy-dA/edit) › AI architecture (Engine, Game) › Tests · exported 2026-11-03
